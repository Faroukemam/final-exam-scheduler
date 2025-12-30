# template_generator.py
"""
Template Generator for Final Exam Scheduler
Generates Excel templates with sample data AND documentation (README sheets)
"""
import pandas as pd
from datetime import datetime, timedelta

def generate_exam_scheduler_templates(output_dir="."):
    """Generate all template files for the Exam Scheduler with README sheets."""
    
    # 1. Regs Template
    regs_data = {
        'ID': ['STU001', 'STU002', 'STU003', 'STU004', 'STU005'],
        'NAME': ['Ahmed Mohamed', 'Sara Hassan', 'Omar Ali', 'Fatma Khaled', 'Mohamed Youssef'],
        'Program': ['CS', 'CS', 'IS', 'IS', 'AI'],
        'COURSES': [
            'CS101,CS102,MATH101',
            'CS101,CS103,PHYS101',
            'IS101,IS102,MATH101',
            'IS101,CS101,STAT101',
            'AI101,AI102,MATH101'
        ]
    }
    regs_df = pd.DataFrame(regs_data)
    
    regs_readme = pd.DataFrame({
        'Column': ['ID', 'NAME', 'Program', 'COURSES'],
        'Description': [
            'Unique student identifier',
            'Student full name',
            'Program code (e.g., CS, IS, AI)',
            'Comma-separated course codes (e.g., CS101,CS102)'
        ],
        'Format': ['Text', 'Text', 'Text (2-4 chars)', 'Text (comma-separated)'],
        'Example': ['STU001', 'Ahmed Mohamed', 'CS', 'CS101,MATH101,PHYS101']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_regs.xlsx", engine='openpyxl') as writer:
        regs_readme.to_excel(writer, sheet_name='📖 README', index=False)
        regs_df.to_excel(writer, sheet_name='Regs', index=False)
    
    # 2. Courses Master Template
    courses_data = {
        'CourseCode': ['CS101', 'CS102', 'CS103', 'IS101', 'IS102', 'AI101', 'AI102', 'MATH101', 'PHYS101', 'STAT101'],
        'CourseName': ['Intro to Programming', 'Data Structures', 'Algorithms', 'Information Systems', 
                      'Database Systems', 'Machine Learning', 'Deep Learning', 'Calculus I', 
                      'Physics I', 'Statistics'],
        'Program': ['CS', 'CS', 'CS', 'IS', 'IS', 'AI', 'AI', 'ALL', 'ALL', 'ALL'],
        'ExamGroup': ['GRP_CS1', 'GRP_CS2', 'GRP_CS3', 'GRP_IS1', 'GRP_IS2', 'GRP_AI1', 'GRP_AI2', 
                     'GRP_MATH', 'GRP_PHYS', 'GRP_STAT'],
        'DurationMin': [120, 120, 150, 120, 150, 180, 180, 120, 120, 120],
        'Terminated': ['', '', '', '', '', '', '', '', '', '']  # Use Yes/True/1 to exclude course
    }
    courses_df = pd.DataFrame(courses_data)
    
    courses_readme = pd.DataFrame({
        'Column': ['CourseCode', 'CourseName', 'Program', 'ExamGroup', 'DurationMin', 'Terminated'],
        'Description': [
            'Unique course code (must match Regs file)',
            'Full course name for reports',
            'Program code. Use "ALL" for shared courses',
            'Grouping for scheduling (same group = scheduled together)',
            'Exam duration in minutes',
            'OPTIONAL: Yes/True/1 to exclude from scheduling'
        ],
        'Format': ['Text', 'Text', 'Text', 'Text', 'Number', 'Text'],
        'Example': ['CS101', 'Intro to Programming', 'CS', 'GRP_CS1', '120', '']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_courses_master.xlsx", engine='openpyxl') as writer:
        courses_readme.to_excel(writer, sheet_name='📖 README', index=False)
        courses_df.to_excel(writer, sheet_name='Courses', index=False)
    
    # 3. Exam Calendar Template
    base_date = datetime(2025, 5, 20)
    calendar_data = {
        'Date': [base_date + timedelta(days=i) for i in range(5) for _ in range(2)],
        'SlotID': ['Morning', 'Afternoon'] * 5,
        'Start': ['09:00', '14:00'] * 5,
        'End': ['12:00', '17:00'] * 5
    }
    calendar_df = pd.DataFrame(calendar_data)
    
    calendar_readme =pd.DataFrame({
        'Column': ['Date', 'SlotID', 'Start', 'End'],
        'Description': [
            'Exam date (any date format Excel accepts)',
            'Slot identifier (e.g., Morning, Afternoon)',
            'Start time (HH:MM format)',
            'End time (HH:MM format)'
        ],
        'Format': ['Date', 'Text', 'Time (HH:MM)', 'Time (HH:MM)'],
        'Example': ['2025-05-20', 'Morning', '09:00', '12:00']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_exam_calendar.xlsx", engine='openpyxl') as writer:
        calendar_readme.to_excel(writer, sheet_name='📖 README', index=False)
        calendar_df.to_excel(writer, sheet_name='Calendar', index=False)
    
    # 4. Slot Capacity Template
    capacity_data = {
        'Date': [base_date + timedelta(days=i) for i in range(5) for _ in range(2)],
        'SlotID': ['Morning', 'Afternoon'] * 5,
        'CapacityStudents': [100, 80, 100, 80, 100, 80, 100, 80, 100, 80]
    }
    capacity_df = pd.DataFrame(capacity_data)
    
    capacity_readme = pd.DataFrame({
        'Column': ['Date', 'SlotID', 'CapacityStudents'],
        'Description': [
            'Exam date (must match Calendar)',
            'Slot identifier (must match Calendar)',
            'Maximum number of students for this slot'
        ],
        'Format': ['Date', 'Text', 'Number'],
        'Example': ['2025-05-20', 'Morning', '100']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_slot_capacity.xlsx", engine='openpyxl') as writer:
        capacity_readme.to_excel(writer, sheet_name='📖 README', index=False)
        capacity_df.to_excel(writer, sheet_name='SlotCapacity', index=False)
    
    # 5. Constraints Template
    fixed_data = {
        'ExamGroup': ['GRP_CS1', 'GRP_AI1'],
        'Date': [base_date, base_date + timedelta(days=1)],
        'SlotID': ['Morning', 'Afternoon']
    }
    fixed_df = pd.DataFrame(fixed_data)
    
    balance_data = {
        'WeightCapacity': [5],
        'WeightRestViolation': [1],
        'WeightSpread': [3]
    }
    balance_df = pd.DataFrame(balance_data)
    
    constraints_readme = pd.DataFrame({
        'Sheet': ['FixedAssignments', 'FixedAssignments', 'FixedAssignments', 
                 'BalanceSettings', 'BalanceSettings', 'BalanceSettings'],
        'Column': ['ExamGroup', 'Date', 'SlotID', 
                  'WeightCapacity', 'WeightRestViolation', 'WeightSpread'],
        'Description': [
            'Exam group to fix (from courses_master)',
            'Fixed date for this exam group',
            'Fixed slot for this exam group',
            'Weight for capacity violations (higher = stricter)',
            'Weight for rest day violations (higher = stricter)',
            'Weight for load balancing (higher = more balanced days)'
        ],
        'Example': ['GRP_CS1', '2025-05-20', 'Morning', '5', '1', '3']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_constraints.xlsx", engine='openpyxl') as writer:
        constraints_readme.to_excel(writer, sheet_name='📖 README', index=False)
        fixed_df.to_excel(writer, sheet_name='FixedAssignments', index=False)
        balance_df.to_excel(writer, sheet_name='BalanceSettings', index=False)
    
    return [
        'template_regs.xlsx',
        'template_courses_master.xlsx', 
        'template_exam_calendar.xlsx',
        'template_slot_capacity.xlsx',
        'template_constraints.xlsx'
    ]

def generate_invigilation_templates(output_dir="."):
    """Generate all template files for the Invigilation Scheduler with README sheets."""
    
    base_date = datetime(2025, 5, 20)
    
    # 1. Sessions Template
    sessions_data = {
        'SessionID': [f'SES{i:03d}' for i in range(1, 11)],
        'Room': [f'Room {chr(65+i%5)}' for i in range(10)],
        'Date': [base_date + timedelta(days=i//2) for i in range(10)],
        'Start': ['09:00', '11:00', '14:00', '09:00', '11:00', '14:00', '09:00', '11:00', '14:00', '09:00'],
        'End': ['11:00', '13:00', '17:00', '11:00', '13:00', '17:00', '11:00', '13:00', '17:00', '11:00'],
        'Duration': [120, 120, 180, 120, 120, 180, 120, 120, 180, 120],
        'InvigilatorsNeeded': [2, 2, 3, 2, 2, 3, 2, 2, 3, 2]
    }
    sessions_df = pd.DataFrame(sessions_data)
    
    sessions_readme = pd.DataFrame({
        'Column': ['SessionID', 'Room', 'Date', 'Start', 'End', 'Duration', 'InvigilatorsNeeded'],
        'Description': [
            'Unique session identifier',
            'Room/location name',
            'Session date',
            'Start time (HH:MM)',
            'End time (HH:MM)',
            'Duration in minutes',
            'Number of invigilators required'
        ],
        'Example': ['SES001', 'Room A', '2025-05-20', '09:00', '11:00', '120', '2']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_sessions.xlsx", engine='openpyxl') as writer:
        sessions_readme.to_excel(writer, sheet_name='📖 README', index=False)
        sessions_df.to_excel(writer, sheet_name='Sessions', index=False)
    
    # 2. Staff Template
    staff_data = {
        'StaffID': [f'STAFF{i:03d}' for i in range(1, 11)],
        'Name': ['Dr. Ahmed Mohamed', 'Dr. Sara Hassan', 'Prof. Omar Ali', 'Dr. Fatma Khaled',
                'Dr. Mohamed Youssef', 'Dr. Laila Ibrahim', 'Prof. Karim Mansour', 
                'Dr. Noha Salem', 'Dr. Tarek Farouk', 'Dr. Heba Nabil'],
        'LoadType': ['full', 'full', 'half', 'full', 'full', 'half', 'full', 'full', 'half', 'full'],
        'MaxHours': [20, 20, 10, 20, 20, 10, 20, 20, 10, 20]
    }
    staff_df = pd.DataFrame(staff_data)
    
    staff_readme = pd.DataFrame({
        'Column': ['StaffID', 'Name', 'LoadType', 'MaxHours'],
        'Description': [
            'Unique staff identifier',
            'Staff member full name',
            'Load type: "full" or "half" (affects fairness calculation)',
            'Maximum total hours this staff can invigilate'
        ],
        'Example': ['STAFF001', 'Dr. Ahmed Mohamed', 'full', '20']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_staff.xlsx", engine='openpyxl') as writer:
        staff_readme.to_excel(writer, sheet_name='📖 README', index=False)
        staff_df.to_excel(writer, sheet_name='Staff', index=False)
    
    # 3. Engagement Template
    engagement_data = {
        'StaffID': ['STAFF001', 'STAFF002', 'STAFF003', 'STAFF001', 'STAFF004'],
        'Date': [base_date, base_date, base_date + timedelta(days=1), 
                base_date + timedelta(days=2), base_date + timedelta(days=1)],
        'Start': ['09:00', '14:00', '09:00', '11:00', '14:00'],
        'End': ['10:00', '15:00', '10:00', '12:00', '16:00'],
        'Engagement': [1, 1, 1, 1, 1]
    }
    engagement_df = pd.DataFrame(engagement_data)
    
    engagement_readme = pd.DataFrame({
        'Column': ['StaffID', 'Date', 'Start', 'End', 'Engagement'],
        'Description': [
            'Staff ID (must match Staff file)',
            'Date of engagement/unavailability',
            'Start time of engagement (HH:MM)',
            'End time of engagement (HH:MM)',
            'Engagement type: 1 = busy (cannot invigilate), 0 = available'
        ],
        'Example': ['STAFF001', '2025-05-20', '09:00', '10:00', '1']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_engagement.xlsx", engine='openpyxl') as writer:
        engagement_readme.to_excel(writer, sheet_name='📖 README', index=False)
        engagement_df.to_excel(writer, sheet_name='Engagement', index=False)
    
    return [
        'template_sessions.xlsx',
        'template_staff.xlsx',
        'template_engagement.xlsx'
    ]

def generate_courses_report_templates(output_dir="."):
    """Generate template files for Courses Report with README sheets."""
    
    regs_data = {
        'ID': ['STU001', 'STU002', 'STU003', 'STU004', 'STU005'],
        'NAME': ['Ahmed Mohamed', 'Sara Hassan', 'Omar Ali', 'Fatma Khaled', 'Mohamed Youssef'],
        'Program': ['CS', 'CS', 'IS', 'IS', 'AI'],
        'COURSES': [
            'CS101,CS102,MATH101',
            'CS101,CS103,PHYS101',
            'IS101,IS102,MATH101',
            'IS101,CS101,STAT101',
            'AI101,AI102,MATH101'
        ]
    }
    regs_df = pd.DataFrame(regs_data)
    
    regs_readme = pd.DataFrame({
        'Column': ['ID', 'NAME', 'Program', 'COURSES'],
        'Description': [
            'Student unique identifier',
            'Student name',
            'Program enrolled in',
            'Comma-separated course codes'
        ],
        'Example': ['STU001', 'Ahmed Mohamed', 'CS', 'CS101,MATH101']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_regs_for_report.xlsx", engine='openpyxl') as writer:
        regs_readme.to_excel(writer, sheet_name='📖 README', index=False)
        regs_df.to_excel(writer, sheet_name='Regs', index=False)
    
    courses_data = {
        'CourseCode': ['CS101', 'CS102', 'CS103', 'IS101', 'IS102', 'AI101', 'AI102', 'MATH101', 'PHYS101', 'STAT101'],
        'CourseName': ['Intro to Programming', 'Data Structures', 'Algorithms', 'Information Systems', 
                      'Database Systems', 'Machine Learning', 'Deep Learning', 'Calculus I', 
                      'Physics I', 'Statistics'],
        'Program': ['CS', 'CS', 'CS', 'IS', 'IS', 'AI', 'AI', 'ALL', 'ALL', 'ALL'],
        'ExamGroup': ['GRP_CS1', 'GRP_CS2', 'GRP_CS3', 'GRP_IS1', 'GRP_IS2', 'GRP_AI1', 'GRP_AI2', 
                     'GRP_MATH', 'GRP_PHYS', 'GRP_STAT'],
        'DurationMin': [120, 120, 150, 120, 150, 180, 180, 120, 120, 120],
        'Terminated': ['', '', '', '', '', '', '', '', '', '']  # OPTIONAL column
    }
    courses_df = pd.DataFrame(courses_data)
    
    courses_readme = pd.DataFrame({
        'Column': ['CourseCode', 'CourseName', 'Program', 'ExamGroup', 'DurationMin', 'Terminated'],
        'Description': [
            'Course unique code',
            'Course full name',
            'Owning program ("ALL" for shared)',
            'Exam grouping identifier',
            'Exam duration in minutes',
            'OPTIONAL: Yes/True/1 to exclude'
        ],
        'Example': ['CS101', 'Programming', 'CS', 'GRP_CS1', '120', '']
    })
    
    with pd.ExcelWriter(f"{output_dir}/template_courses_for_report.xlsx", engine='openpyxl') as writer:
        courses_readme.to_excel(writer, sheet_name='📖 README', index=False)
        courses_df.to_excel(writer, sheet_name='Courses', index=False)
    
    return [
        'template_regs_for_report.xlsx',
        'template_courses_for_report.xlsx'
    ]
