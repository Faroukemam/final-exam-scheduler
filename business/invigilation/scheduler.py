# optimizer.py
import os
import sys
import ctypes
import pandas as pd
from ortools.sat.python import cp_model


# ===================== OR-Tools DLL Fix =====================

def _ensure_ortools_dll_loaded():
    """
    لو شغال من PyInstaller EXE:
    - ندور على ortools.dll جوه الباندل (_MEIPASS) أو جنب الـ exe
    - نعمله ctypes.CDLL عشان cp_model_helper يلاقيه
    """
    if not getattr(sys, "frozen", False):
        # شغال بايثون عادي مش EXE -> مفيش مشكلة
        return

    base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))

    candidates = [
        os.path.join(base, "ortools", "ortools.dll"),
        os.path.join(base, ".libs", "ortools.dll"),
        os.path.join(base, "ortools.dll"),
    ]

    for p in candidates:
        if os.path.exists(p):
            try:
                ctypes.CDLL(p)
                return
            except OSError:
                # نجرب اللي بعدها
                pass


_ensure_ortools_dll_loaded()


# ===================== Helpers =====================

def _normalize_date(val):
    """
    نخلي التاريخ key من الشهر واليوم بس
    أمثلة:
    5/1           -> 05-01
    05/01/2025    -> 05-01
    2025-01-05    -> 01-05 (لو مكتوبة سنة-شهر-يوم)
    """
    s = str(val).strip()
    if not s or s.lower() in ("nan", "nat"):
        return s

    for sep in ["/", "-", "."]:
        if sep in s:
            parts = s.split(sep)
            if len(parts) == 3:
                # نفترض فورمات يوم/شهر/سنة أو سنة-شهر-يوم
                if len(parts[0]) == 4:  # سنة
                    m, d = parts[1], parts[2]
                else:
                    d, m = parts[0], parts[1]
                return f"{str(m).zfill(2)}-{str(d).zfill(2)}"
            elif len(parts) >= 2:
                d, m = parts[0], parts[1]
                return f"{str(m).zfill(2)}-{str(d).zfill(2)}"
    return s


def _parse_time_to_min(val):
    """
    يحوّل 930 أو '09:30' أو 930.0 إلى دقائق من بداية اليوم.
    """
    s = str(val).strip()

    if ":" in s:
        parts = s.split(":")
        if len(parts) >= 2:
            h = int(parts[0])
            m = int(parts[1])
            return h * 60 + m

    # شكل HHMM
    v = int(float(s))
    h = v // 100
    m = v % 100
    return h * 60 + m


def _intervals_overlap(a_start, a_end, b_start, b_end):
    """
    هل المقطعين [a_start, a_end) و [b_start, b_end) متداخلين؟
    """
    return (a_start < b_end) and (b_start < a_end)


# ===================== Main Optimization Function =====================

def run_optimization(
    sessions_path,
    staff_path,
    engagement_path,
    output_path="invigilation_schedule.xlsx",
):
    print("=== Loading data ===")
    print("sessions:", sessions_path)
    print("staff:", staff_path)
    print("engagement:", engagement_path)

    # ---- Load data ----
    sessions_df = pd.read_excel(sessions_path)
    staff_df = pd.read_excel(staff_path)
    engage_df = pd.read_excel(engagement_path)

    # Required columns
    req_sessions = {"Room", "Date", "Start", "End", "Duration", "InvigilatorsNeeded"}
    req_staff = {"StaffID", "Name"}
    req_engage_base = {"StaffID", "Date", "Start", "Engagement"}

    if not req_sessions.issubset(sessions_df.columns):
        raise ValueError(f"sessions.xlsx must contain columns: {req_sessions}")
    if not req_staff.issubset(staff_df.columns):
        raise ValueError(f"staff.xlsx must contain columns: {req_staff}")
    if not req_engage_base.issubset(engage_df.columns):
        raise ValueError(
            f"engagement.xlsx must contain at least columns: {req_engage_base}"
        )

    # هل فيه End في الـ engagement؟
    has_eng_end = "End" in engage_df.columns

    sessions_df = sessions_df.copy()
    staff_df = staff_df.copy()
    engage_df = engage_df.copy()

    # StaffID كـ string
    staff_df["StaffID"] = staff_df["StaffID"].astype(str)
    engage_df["StaffID"] = engage_df["StaffID"].astype(str)

    # Default LoadType + optional MaxHours
    if "LoadType" not in staff_df.columns:
        staff_df["LoadType"] = "full"

    has_max_hours = "MaxHours" in staff_df.columns
    if has_max_hours:
        staff_df["MaxHours"] = pd.to_numeric(staff_df["MaxHours"], errors="coerce")

    # LoadType → weight
    load_weight = {}
    for _, row in staff_df.iterrows():
        sid = row["StaffID"]
        lt = str(row["LoadType"]).strip().lower()
        load_weight[sid] = 2 if lt == "half" else 1

    # ---- Sessions preprocessing ----
    sessions_df["SessionID"] = ["S" + str(i + 1) for i in range(len(sessions_df))]

    # DateKey من الشهر/اليوم فقط
    sessions_df["DateKey"] = sessions_df["Date"].map(_normalize_date)

    # Start/End as minutes
    sessions_df["Start_min"] = sessions_df["Start"].apply(_parse_time_to_min)
    sessions_df["End_min"] = sessions_df["End"].apply(_parse_time_to_min)

    # DurationMinutes من الفرق بين Start/End
    sessions_df["DurationMinutes"] = (
        sessions_df["End_min"] - sessions_df["Start_min"]
    ).astype(int)

    # Check على مدة الجلسات
    if (sessions_df["DurationMinutes"] <= 0).any():
        bad = sessions_df[sessions_df["DurationMinutes"] <= 0]
        raise ValueError(
            "في جلسات مدتهم <= 0 دقيقة، راجع أعمدة Start و End في sessions.xlsx\n"
            f"Rows:\n{bad[['Room','Date','Start','End']].to_string(index=False)}"
        )

    # Maps
    session_ids = sessions_df["SessionID"].tolist()
    staff_ids = staff_df["StaffID"].tolist()

    duration_map = dict(
        zip(sessions_df["SessionID"], sessions_df["DurationMinutes"])
    )
    inv_needed = dict(zip(sessions_df["SessionID"], sessions_df["InvigilatorsNeeded"]))
    date_key_map = dict(zip(sessions_df["SessionID"], sessions_df["DateKey"]))
    start_min_map = dict(zip(sessions_df["SessionID"], sessions_df["Start_min"]))
    end_min_map = dict(zip(sessions_df["SessionID"], sessions_df["End_min"]))

    id_to_name = dict(zip(staff_df["StaffID"], staff_df["Name"]))

    # ---- Engagement preprocessing ----
    # نحول Engagement لـ 0/1 أرقام عشان المقارنة تبقى مظبوطة
    engage_df["Engagement"] = pd.to_numeric(
        engage_df["Engagement"], errors="coerce"
    ).fillna(0).astype(int)

    engage_df["DateKey"] = engage_df["Date"].map(_normalize_date)
    engage_df["Start_min"] = engage_df["Start"].apply(_parse_time_to_min)
    if has_eng_end:
        engage_df["End_min"] = engage_df["End"].apply(_parse_time_to_min)
    else:
        # لو مفيش End هنفترض ساعه واحدة
        engage_df["End_min"] = engage_df["Start_min"] + 60

    # نشتغل على صفوف Engagement = 1 بس
    engage_busy = engage_df[engage_df["Engagement"] == 1].copy()

    # حوّل لـ list عشان التعامل يبقى أسهل
    busy_intervals = []
    for _, r in engage_busy.iterrows():
        busy_intervals.append(
            dict(
                staff_id=str(r["StaffID"]),
                date_key=r["DateKey"],
                start_min=int(r["Start_min"]),
                end_min=int(r["End_min"]),
            )
        )

    # ---- MaxHours (in minutes) ----
    max_hours_map = {}
    if has_max_hours:
        for _, row in staff_df.iterrows():
            sid = row["StaffID"]
            mh = row["MaxHours"]
            if pd.notna(mh):
                max_hours_map[sid] = int(float(mh) * 60)

    # ============== Diagnostics ==============
    print("=== Diagnostics ===")
    print(f"Number of sessions: {len(sessions_df)}")
    print(f"Number of staff   : {len(staff_df)}")
    total_demand = sessions_df["InvigilatorsNeeded"].sum()
    print(f"Total invigilator slots (sessions): {total_demand}")

    # ============== OR-Tools model ==============
    model = cp_model.CpModel()

    # Decision vars
    x = {}
    for d in staff_ids:
        for s in session_ids:
            x[(d, s)] = model.NewBoolVar(f"x_{d}_{s}")

    # 1) exact invigilators per session
    for s in session_ids:
        model.Add(sum(x[(d, s)] for d in staff_ids) == int(inv_needed[s]))

    # جهز info عن الجلسات عشان التداخلات
    sessions_info = []
    for s in session_ids:
        sessions_info.append(
            dict(
                id=s,
                date_key=date_key_map[s],
                start_min=start_min_map[s],
                end_min=end_min_map[s],
            )
        )

    # 2) ممنوع نفس الشخص في لجان متداخلة في نفس اليوم
    for i in range(len(sessions_info)):
        si = sessions_info[i]
        for j in range(i + 1, len(sessions_info)):
            sj = sessions_info[j]
            if si["date_key"] != sj["date_key"]:
                continue
            if not _intervals_overlap(
                si["start_min"], si["end_min"], sj["start_min"], sj["end_min"]
            ):
                continue
            # متداخلين في نفس اليوم → نفس الشخص ما ينفعش ياخد الاتنين
            for d in staff_ids:
                model.Add(x[(d, si["id"])] + x[(d, sj["id"])] <= 1)

    # 3) ممنوع يوضع في لجنة وهو عنده Engagement متداخل معها
    for s in sessions_info:
        sid = s["id"]
        s_date = s["date_key"]
        s_start = s["start_min"]
        s_end = s["end_min"]

        for bi in busy_intervals:
            if bi["date_key"] != s_date:
                continue
            if not _intervals_overlap(
                s_start, s_end, bi["start_min"], bi["end_min"]
            ):
                continue
            d = bi["staff_id"]
            if d in staff_ids:
                model.Add(x[(d, sid)] == 0)

    # 4) load minutes + MaxHours
    max_total = sum(sessions_df["DurationMinutes"])
    load_minutes = {}
    for d in staff_ids:
        load_minutes[d] = model.NewIntVar(0, max_total, f"load_{d}")
        model.Add(
            load_minutes[d]
            == sum(duration_map[s] * x[(d, s)] for s in session_ids)
        )
        if d in max_hours_map:
            model.Add(load_minutes[d] <= max_hours_map[d])

    # 5) normalized load (حسب LoadType) + fairness
    max_norm = model.NewIntVar(0, max_total * 2, "max_norm")
    min_norm = model.NewIntVar(0, max_total * 2, "min_norm")
    norm_load = {}
    for d in staff_ids:
        w = load_weight[d]
        norm_load[d] = model.NewIntVar(0, max_total * 2, f"norm_{d}")
        model.Add(norm_load[d] == load_minutes[d] * w)
        model.Add(norm_load[d] <= max_norm)
        model.Add(norm_load[d] >= min_norm)

    spread = model.NewIntVar(0, max_total * 2, "spread")
    model.Add(spread == max_norm - min_norm)
    model.Minimize(spread)

    # ============== Solve ==============
    print("=== Solving model ===")
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 25
    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)
    print("Solver status:", solver.StatusName(status))

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(
            f"No feasible solution. OR-Tools status = {solver.StatusName(status)}.\n"
            "Check:\n"
            "- InvigilatorsNeeded too high for overlapped sessions.\n"
            "- Too many Engagement=1 intervals.\n"
            "- MaxHours too small for all staff combined."
        )

    # ============== Build outputs ==============
    rows = []
    for s in session_ids:
        ids = []
        names = []
        for d in staff_ids:
            if solver.Value(x[(d, s)]) == 1:
                ids.append(d)
                names.append(id_to_name[d])
        rows.append(
            {
                "SessionID": s,
                "Invigilators_IDs": ", ".join(ids),
                "Invigilators_Names": ", ".join(names),
            }
        )
    out_df = pd.DataFrame(rows)

    merged = sessions_df.merge(out_df, on="SessionID", how="left")

    # Summary
    summary_rows = []
    for d in staff_ids:
        hours = round(solver.Value(load_minutes[d]) / 60.0, 2)
        staff_row = staff_df.loc[staff_df["StaffID"] == d].iloc[0]
        summary_rows.append(
            {
                "StaffID": d,
                "Name": staff_row["Name"],
                "LoadType": staff_row["LoadType"],
                "MaxHours": staff_row["MaxHours"] if has_max_hours else None,
                "TotalHours": hours,
            }
        )
    summary_df = pd.DataFrame(summary_rows)

    print("=== Saving Excel ===")
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        merged.to_excel(writer, index=False, sheet_name="SessionsWithInvigilators")
        summary_df.to_excel(writer, index=False, sheet_name="StaffLoadSummary")

    print("Done, saved to:", output_path)
    return merged, summary_df
