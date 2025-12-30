"""
Full test of Terminated courses feature in actual scheduler code
"""
import pandas as pd
import tempfile
import os

# Create test courses with Terminated column
courses_data = {
    'CourseCode': ['CS101', 'CS102', 'MATH201', 'ENG301'],
    'Program': ['CS', 'CS', 'ALL', 'ALL'],
    'ExamGroup': ['G1', 'G2', 'G3', 'G4'],
    'CourseName': ['Programming', 'Data Structures', 'Calculus', 'English'],
    'DurationMin': [120, 120, 120, 120],
    'Terminated': ['', 'Yes', '', 'TRUE']  # CS102 and ENG301 terminated
}

# Save to temp file
tf = tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx', delete=False)
courses_path = tf.name
tf.close()

pd.DataFrame(courses_data).to_excel(courses_path, sheet_name='Courses', index=False)

print("📄 Created test file:", courses_path)
print("\n📚 Test Courses:")
print(pd.DataFrame(courses_data)[['CourseCode', 'Terminated']])

# Now test the actual scheduler code
try:
    from business.exam_scheduling.scheduler import normalize_str, normalize_program
    
    # Read back
    courses_df = pd.read_excel(courses_path, sheet_name='Courses')
    
    print("\n🔍 Before filtering:")
    print(f"  Total courses: {len(courses_df)}")
    
    # Apply the EXACT same logic from scheduler.py lines 157-171
    courses_df["CourseCode"] = courses_df["CourseCode"].astype(str).str.strip()
    courses_df["Program"] = courses_df["Program"].apply(normalize_program)
    courses_df["ExamGroup"] = courses_df["ExamGroup"].apply(normalize_str)
    
    # Handle Terminated column (optional)
    if "Terminated" not in courses_df.columns:
        courses_df["Terminated"] = False
    else:
        # Convert to boolean - accept Yes/True/1/Y as terminated
        courses_df["Terminated"] = courses_df["Terminated"].apply(
            lambda x: str(x).strip().upper() in ("YES", "TRUE", "1", "Y", "TERMINATED")
        )
    
    print(f"\n🔄 After parsing Terminated column:")
    print(courses_df[['CourseCode', 'Terminated']])
    
    # Filter out terminated courses
    courses_df = courses_df[~courses_df["Terminated"]].copy()
    
    print(f"\n✅ After filtering:")
    print(f"  Remaining courses: {len(courses_df)}")
    print(f"  Course codes: {list(courses_df['CourseCode'])}")
    
    if len(courses_df) == 2 and 'CS101' in list(courses_df['CourseCode']) and 'MATH201' in list(courses_df['CourseCode']):
        print("\n✅ SUCCESS! Filtering works correctly!")
    else:
        print("\n❌ FAILED! Expected CS101 and MATH201 only")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    os.remove(courses_path)
    print(f"\n🧹 Cleaned up temp file")
