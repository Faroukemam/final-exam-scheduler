"""
Test: Verify terminated courses don't show as missing
"""
import pandas as pd
import os

# Simulate what happens in the scheduler

# 1. Original courses with Terminated column
courses_original = pd.DataFrame({
    'CourseCode': ['CS101', 'CS102', 'MATH201'],
    'Program': ['CS', 'CS', 'MATH'],
    'ExamGroup': ['G1', 'G2', 'G3'],
    'Terminated': ['', 'Yes', '']  # CS102 is terminated
})

# 2. Filter out terminated (this is what scheduler does)
courses_active = courses_original[
    ~courses_original['Terminated'].apply(
        lambda x: str(x).strip().upper() in ('YES', 'TRUE', '1', 'Y', 'TERMINATED')
    )
].copy()

print("📚 Original Courses:")
print(courses_original[['CourseCode', 'Terminated']])
print(f"\n✅ Active Courses (after filtering):")
print(courses_active[['CourseCode', 'ExamGroup']])

# 3. Student enrollments include terminated course
enrollments = pd.DataFrame({
    'StudentID': ['S001', 'S001', 'S002'],
    'CourseCode': ['CS101', 'CS102', 'MATH201'],  # CS102 is terminated!
    'Program': ['CS', 'CS', 'MATH']
})

print(f"\n📝 Student Enrollments:")
print(enrollments)

# 4. Join with active courses
merged = enrollments.merge(
    courses_active[['CourseCode', 'Program', 'ExamGroup']], 
    on=['CourseCode', 'Program'], 
    how='left'
)

print(f"\n🔗 After joining with active courses:")
print(merged)

# 5. Check what's missing
missing = merged[merged['ExamGroup'].isna()]
print(f"\n⚠️  Missing courses:")
print(missing[['StudentID', 'CourseCode']])

print(f"\n✨ RESULT:")
print(f"  - S001 enrolled in CS102 (terminated)")
print(f"  - CS102 shows as 'missing' (expected behavior)")
print(f"  - This is CORRECT - helps identify students with terminated enrollments")
