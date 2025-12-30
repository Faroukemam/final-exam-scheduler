"""
Test: Verify Program-Based Termination
"""
import pandas as pd
import tempfile
import os

# Scenario:
# CS101 is offered to CS and SE programs.
# We terminate CS101 for CS program only. 
# CS101 for SE program should remain active.

# 1. Courses
courses_data = {
    'CourseCode': ['CS101', 'CS101'],
    'Program': ['CS', 'SE'],
    'ExamGroup': ['G_CS', 'G_SE'],
    'Terminated': ['Yes', 'No']  # Terminate CS101 for CS only
}
courses_df = pd.DataFrame(courses_data)

# 2. Logic simulation (from scheduler.py)
print("🚀 Simulating Program-Based Termination...")

# Filter Terminated
courses_df["Terminated"] = courses_df["Terminated"].apply(
    lambda x: str(x).strip().upper() in ("YES", "TRUE", "1", "Y", "TERMINATED")
)

# Store keys
terminated_keys = set(
    zip(courses_df[courses_df["Terminated"]]["CourseCode"], 
        courses_df[courses_df["Terminated"]]["Program"])
)
print(f"\n🗑️  Terminated Keys: {terminated_keys}")

# Active courses
active_courses = courses_df[~courses_df["Terminated"]].copy()
print(f"\n✅ Active Courses:\n{active_courses[['CourseCode', 'Program']]}")

# 3. Enrollments
enrollments = [
    {'StudentID': 'S1', 'Program': 'CS', 'CourseCode': 'CS101'}, # Should be excluded (CS101 is term for CS)
    {'StudentID': 'S2', 'Program': 'SE', 'CourseCode': 'CS101'}  # Should be KEPT (CS101 is active for SE)
]

print(f"\n📝 Enrollments to Process: {enrollments}")

final_enrollments = []
for r in enrollments:
    cc = r['CourseCode']
    prog = r['Program']
    
    # Logic check
    if (cc, prog) in terminated_keys:
        print(f"❌ Skipping {cc} for {prog} (Terminated)")
        continue
    if (cc, 'ALL') in terminated_keys:
        print(f"❌ Skipping {cc} for {prog} (Terminated by ALL)")
        continue
        
    final_enrollments.append(r)
    print(f"✅ Keeping {cc} for {prog}")

print(f"\n✨ Final Enrollments: {final_enrollments}")

if len(final_enrollments) == 1 and final_enrollments[0]['Program'] == 'SE':
    print("\n✅ SUCCESS! Program-specific termination working correctly.")
else:
    print("\n❌ FAILED! Incorrect filtering.")
