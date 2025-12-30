"""
Quick Test Script for Terminated Courses Feature
"""
import pandas as pd
import os

# Create test data directory
test_dir = "test_terminated"
os.makedirs(test_dir, exist_ok=True)

# Create sample Courses Master with Terminated column
courses_data = {
    'CourseCode': ['CS101', 'CS102', 'MATH201', 'ENG301', 'PHY401'],
    'Program': ['CS', 'CS', 'MATH', 'ENG', 'PHY'],
    'ExamGroup': ['GROUP_A', 'GROUP_B', 'GROUP_C', 'GROUP_D', 'GROUP_E'],
    'CourseName': ['Intro to CS', 'Data Structures', 'Calculus', 'Literature', 'Quantum Physics'],
    'DurationMin': [120, 120, 180, 120, 180],
    'Terminated': ['', 'Yes', '', 'TRUE', '']  # CS102 and ENG301 are terminated
}

courses_df = pd.DataFrame(courses_data)
courses_path = os.path.join(test_dir, 'courses_master_test.xlsx')
courses_df.to_excel(courses_path, sheet_name='Courses', index=False)

# Create sample Regs file
regs_data = {
    'ID': ['S001', 'S002', 'S003'],
    'Program': ['CS', 'MATH', 'ENG'],
    'COURSES': ['CS101,CS102', 'MATH201', 'ENG301,CS101']  # Note: includes terminated courses
}

regs_df = pd.DataFrame(regs_data)
regs_path = os.path.join(test_dir, 'regs_test.xlsx')
regs_df.to_excel(regs_path, sheet_name='Regs', index=False)

print("✅ Test files created!")
print(f"\n📁 Created in: {os.path.abspath(test_dir)}")
print(f"\n📄 Files:")
print(f"  - {courses_path}")
print(f"  - {regs_path}")

print(f"\n📊 Courses Master Summary:")
print(f"  Total courses: {len(courses_df)}")
print(f"  Terminated: {courses_df['Terminated'].apply(lambda x: str(x).strip().upper() in ('YES', 'TRUE', '1', 'Y', 'TERMINATED')).sum()}")
print(f"\n  Terminated Courses:")
for _, row in courses_df[courses_df['Terminated'].apply(lambda x: str(x).strip().upper() in ('YES', 'TRUE', '1', 'Y', 'TERMINATED'))].iterrows():
    print(f"    - {row['CourseCode']}: {row['CourseName']}")

print(f"\n🎯 Now run Diagnostics or Courses Report with these files to see terminated courses excluded!")
print(f"\n⚠️  Expected behavior:")
print(f"  - CS102 (Data Structures) → Should NOT appear in exam groups")
print(f"  - ENG301 (Literature) → Should NOT appear in exam groups")
print(f"  - Students enrolled in these → Will show as 'missing course codes'")
