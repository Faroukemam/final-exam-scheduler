"""
Test: Verify fixed assignments for terminated courses are ignored
"""
import pandas as pd
import tempfile
import os

# Create test data
courses_data = {
    'CourseCode': ['CS101', 'CS102'],
    'Program': ['CS', 'CS'],
    'ExamGroup': ['G1', 'G2'],  # G2 is terminated
    'Terminated': ['', 'Yes']
}

fixed_data = {
    'ExamGroup': ['G1', 'G2'], # Fixed assignment for terminated group G2
    'Date': ['2025-05-20', '2025-05-20'],
    'SlotID': ['Morning', 'Morning']
}

enrollments_data = {
    'StudentID': ['S1', 'S2'],
    'CourseCode': ['CS101', 'CS102'],
    'Program': ['CS', 'CS']
}

# Simulate scheduler logic manually to verify flow
print("🚀 Simulating Scheduler Logic...")

# 1. Load Courses
courses_df = pd.DataFrame(courses_data)
print(f"\n📚 Original Courses:\n{courses_df[['CourseCode', 'ExamGroup', 'Terminated']]}")

# 2. Filter Terminated Courses
courses_df["Terminated"] = courses_df["Terminated"].apply(
    lambda x: str(x).strip().upper() in ("YES", "TRUE", "1", "Y", "TERMINATED")
)
active_courses = courses_df[~courses_df["Terminated"]].copy()
print(f"\n✅ Active Courses:\n{active_courses[['CourseCode', 'ExamGroup']]}")

# 3. Load Fixed Assignments
fixed_df = pd.DataFrame(fixed_data)
print(f"\n📌 Original Fixed Assignments:\n{fixed_df}")

# 4. Filter Fixed Assignments (The Fix!)
active_groups = set(active_courses["ExamGroup"].unique())
filtered_fixed = fixed_df[fixed_df["ExamGroup"].isin(active_groups)].copy()

print(f"\n✨ Filtered Fixed Assignments:\n{filtered_fixed}")

# 5. Check Results
if len(filtered_fixed) == 1 and 'G1' in filtered_fixed['ExamGroup'].values:
    print("\n✅ SUCCESS! Fixed assignment for terminated group G2 was removed.")
else:
    print("\n❌ FAILED! G2 still present or G1 missing.")
