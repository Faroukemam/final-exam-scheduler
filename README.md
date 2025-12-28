# Final Exam Scheduler

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CP-SAT Solver](https://img.shields.io/badge/OR--Tools-CP--SAT-green.svg)](https://developers.google.com/optimization)

A professional Windows desktop application for scheduling university final exams and invigilation using **constraint programming (CP-SAT)** optimization.

![Logo](assets/logo.png)

## ✨ Features

### 📝 Exam Scheduling
- **Smart Scheduling**: CP-SAT optimization ensures conflict-free exam schedules
- **Capacity Management**: Respects room/slot capacity constraints
- **Rest Days**: Configurable rest periods between exams for students
- **Fixed Assignments**: Support for pre-scheduled exams
- **Load Balancing**: Distributes exams evenly across available slots

### 🔍 Diagnostics & Validation
- **Data Validation**: Comprehensive checks for input file integrity
- **Conflict Detection**: Identifies student exam conflicts before scheduling
- **Capacity Analysis**: Validates slot capacity vs. enrollment
- **Detailed Reports**: Excel output with diagnostic information

### 📊 Courses Report
- **Enrollment Analysis**: Generate detailed course enrollment reports
- **Program-wise Breakdown**: Analyze by academic program
- **Issue Detection**: Identify data inconsistencies

### 👥 Invigilation Scheduling
- **Fair Assignment**: Balanced workload distribution among staff
- **Availability Handling**: Respects staff engagement/unavailability
- **Load Types**: Supports full-time and part-time staff
- **CP-SAT Optimization**: Optimal staff-to-session assignments

### 📄 Template Generation
- **Excel Templates**: Auto-generate sample input files
- **README Sheets**: Built-in documentation in each template
- **Sample Data**: Realistic examples to understand format

## 🏗️ Architecture

The application follows a professional **5-layer architecture**:

```
├── models/              # Data structures (Student, Course, Session, etc.)
├── utils/               # Date/time utilities, async helpers
├── data/                # File I/O, template generation
├── business/            # CP-SAT optimization logic
└── presentation/        # Tkinter GUI, widgets, styles
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Windows OS (for pre-built EXE)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Faroukemam/final-exam-scheduler.git
cd final-exam-scheduler
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

### Using Pre-built EXE (Windows)
Download `FinalExamScheduler.exe` from the [Releases](https://github.com/Faroukemam/final-exam-scheduler/releases) page and run directly.

## 📖 Usage

### 1. Generate Templates
- Click on any tool (e.g., "Exam Scheduler")
- Click "📄 Generate Template Files"
- Select output folder
- Templates will be created with README sheets explaining each column

### 2. Prepare Your Data
- Fill in the generated templates with your data
- Each template has a "📖 README" sheet with column descriptions
- Examples provided in each template

### 3. Run Scheduling
- Select input files using "Browse" buttons
- Configure settings (e.g., Rest Days)
- Click "Run Scheduler"
- Results saved to specified output path

## 📁 Project Structure

```
ExamScha_1/
├── assets/                     # Logo and static files
├── models/                     # Data models
│   ├── exam_models.py
│   └── invigilation_models.py
├── utils/                      # Utilities
│   ├── date_utils.py
│   ├── time_utils.py
│   └── async_utils.py
├── data/                       # Data layer
│   └── templates/
│       └── template_generator.py
├── business/                   # Business logic
│   ├── exam_scheduling/
│   │   └── scheduler.py
│   └── invigilation/
│       └── scheduler.py
├── presentation/               # GUI
│   ├── styles.py
│   └── gui/
│       └── widgets/
├── main.py                     # Entry point
├── gui.py                      # Main GUI
├── requirements.txt
├── README.md
└── LICENSE
```

## 🛠️ Building from Source

### Create Standalone EXE

```bash
pyinstaller --onefile --noconsole \
  --name "FinalExamScheduler" \
  --icon=assets/logo.ico \
  --add-data "assets/logo.png;assets" \
  --collect-all ortools \
  --collect-binaries ortools \
  main.py --clean
```

Output: `dist/FinalExamScheduler.exe`

## 🔧 Dependencies

- **pandas** >= 2.0.0 - Data manipulation
- **openpyxl** >= 3.1.0 - Excel file handling
- **ortools** >= 9.7.0 - CP-SAT constraint solver

See `requirements.txt` for complete list.

## 📝 Input File Formats

### Exam Scheduler Inputs
1. **Regs** (Registrations): Student ID, Name, Program, Courses
2. **Courses Master**: Course Code, Name, Program, Exam Group, Duration
3. **Calendar**: Available exam dates and time slots
4. **Slot Capacity**: Maximum students per slot
5. **Constraints** (Optional): Fixed assignments, optimization weights

### Invigilation Inputs
1. **Sessions**: Session ID, Room, Date, Time, Invigilators Needed
2. **Staff**: Staff ID, Name, Load Type, Max Hours
3. **Engagement** (Optional): Staff unavailability periods

All formats documented in generated template README sheets.

## 🎨 Features Walkthrough

- Modern dark-themed GUI
- Template generation with documentation
- Real-time status updates
- Excel output with formatted results
- Professional About dialog
- Threading for responsive UI

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Eng. Farouk Emam Waked**
- Email: farouk.waked@must.edu.eg
- Phone/WhatsApp: +201092527272

## 🙏 Acknowledgments

- Built with [OR-Tools](https://developers.google.com/optimization) CP-SAT solver
- Icons and modern UI inspired by contemporary design principles
- Layered architecture following industry best practices

## 🐛 Issues & Contributions

Found a bug or want to contribute? Please open an issue or submit a pull request on [GitHub](https://github.com/Faroukemam/final-exam-scheduler).

## 📊 Version

**v1.1** - Layered Architecture Edition
- Complete refactoring to 5-layer architecture
- Template generation with documentation
- Professional branding and copyright
- Enhanced GUI with modern design

---

**© 2025 Eng. Farouk Emam Waked. All rights reserved.**
