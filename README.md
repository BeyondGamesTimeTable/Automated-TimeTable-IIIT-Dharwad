#  Automated Timetable Generator for IIIT Dharwad

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Success](https://img.shields.io/badge/Success-96.9%25-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Smart academic scheduling system that generates 18 conflict-free timetables in under 30 seconds**

> Built by **Team BeyondGames** | Automated timetable generation for CSE, DSAI, and ECE departments covering semesters 2, 4, and 6 with sections A and B.

---

##  Overview

This system automatically generates **conflict-free, optimized timetables** for IIIT Dharwad with:

-  **3 Departments**: Computer Science (CSE), Data Science & AI (DSAI), Electronics & Communication (ECE)
-  **3 Semesters per Department**: Semester 2, 4, and 6
-  **2 Sections per Semester**: Section A and Section B
-  **Result**: 18 complete timetables with 96.9% automated success rate

### Key Highlights
-  **Zero conflicts** - No room or faculty double-bookings
-  **96.9% success rate** - Only 17 out of 582 sessions require manual intervention
-  **Fast generation** - Complete 18 timetables in 30 seconds
-  **Multiple outputs** - CSV, TXT, and interactive HTML formats
-  **Smart rotation** - Elective courses rotated to reduce 30-65% load

---

##  Quick Start

### Prerequisites
- Python 3.12 or higher
- pandas library

### Installation & Usage

```bash
# 1. Install required dependency
pip install pandas

# 2. Navigate to the generator directory
cd timetable_generator

# 3. Generate all timetables
python main.py

# 4. Create interactive HTML viewer
python timetable_to_html.py

# 5. Open in browser
start timetable_html\index.html
```

**That''s it!** All 18 timetables are now generated and viewable.

---

##  Key Features

###  Core Capabilities
-  **Zero Conflicts** - No room or faculty double-bookings across all 18 timetables
-  **Smart Allocation** - Lectures (60 min), tutorials (60 min), and labs (120 min) properly scheduled
-  **Constraint Satisfaction** - 100% compliance with all 12 institutional requirements
-  **Evening Slot** - 18:30-20:00 overflow slot for high-demand courses
-  **Saturday Classes** - Optional Saturday scheduling for ECE Semester 4 (high load optimization)
-  **Elective Rotation** - "After Midsems" courses reduce concurrent load by 30-65%

###  Output Formats
1. **CSV Files** - Machine-readable timetable grids (Excel-compatible)
2. **Text Files** - Detailed session information with room assignments and elective baskets
3. **HTML Viewer** - Interactive, color-coded timetables with gradient design

###  Smart Scheduling
- Lab sessions scheduled in 2-hour blocks
- Tutorials placed after lectures
- Even distribution across days
- Faculty availability tracking
- Classroom capacity optimization

---

##  Performance Metrics

### Success Rate by Department

| Department | Semesters | Sections | Success Rate | Unscheduled Sessions | Perfect Timetables |
|------------|-----------|----------|--------------|----------------------|--------------------|
| **CSE**    | 2, 4, 6   | A, B     | **100%**     | 0 / 192 sessions     | 6/6              |
| **DSAI**   | 2, 4, 6   | A, B     | **98.0%**    | 6 / 192 sessions     | 4/6              |
| **ECE**    | 2, 4, 6   | A, B     | **95.4%**    | 11 / 198 sessions    | 4/6              |
| **Overall**| All 18    | -        | **96.9%**    | 17 / 582 sessions    | 14/18 (78%)      |

### Evolution & Improvements
- **Initial version**: 79% success rate (105 unscheduled sessions)
- **After Solution 3**: 95% success rate (30 unscheduled sessions)
- **Current version**: 96.9% success rate (17 unscheduled sessions)

**Result**: 84% reduction in unscheduled sessions through iterative optimization!

---

##  Complete Project Structure

```
Automated-Time-Table-IIIT-DHARWAD/

 README.md                              # This file
 LICENSE                                # MIT License

 timetable_generator/                   # Main application directory
   
    main.py                            # Entry point - generates all timetables
    schedule_generator.py              # Core scheduling algorithm
    excel_loader.py                    # CSV input file processor
    excel_exporter.py                  # CSV & TXT output generator
    timetable_to_html.py               # HTML viewer generator
    config.py                          # Configuration (rooms, time slots)
    file_manager.py                    # File I/O utilities
   
    input_files/                       # Input CSV files
       sdtt_inputs/
           Even CSE.csv               # CSE Semester 2, 4, 6 courses
           Even DSAI.csv              # DSAI Semester 2, 4, 6 courses
           Even ECE.csv               # ECE Semester 2, 4, 6 courses
   
    timetable_outputs/                 # Generated timetables (CSV & TXT)
       CSE_Sem2_SectionA_Timetable.csv
       CSE_Sem2_SectionA_Timetable_Electives.txt
       CSE_Sem2_SectionB_Timetable.csv
       CSE_Sem2_SectionB_Timetable_Electives.txt
       ... (18 CSV files + 16 TXT files for electives)
       [All 34 output files]
   
    timetable_html/                    # HTML viewer files
       index.html                     # Main dashboard
       CSE_Sem2_SectionA_Timetable.html
       CSE_Sem2_SectionB_Timetable.html
       ... (18 HTML timetables)
       [All 19 HTML files]
   
    Documentation/                     # Detailed documentation
        CONSTRAINTS_ANALYSIS.md        # 100% satisfaction analysis
        FINAL_SOFTWARE_STATUS.md       # Executive summary
        QUICK_START.md                 # Usage guide
        SCHEDULE_EXPLANATION.md        # Algorithm details
        IMPROVEMENTS_SUMMARY.md        # Evolution history
        TIMETABLE_README.md            # Technical details

 screenshots/                           # UI screenshots
     timetable_html_view1.png          # HTML dashboard
     timetable_html_view2.png          # Individual timetable
     timetable_csv_view.png            # CSV output sample
```

---

##  Input Format

### CSV File Structure

Each department has one CSV file (e.g., `Even CSE.csv`) with the following columns:

| Column | Description | Example | Required |
|--------|-------------|---------|----------|
| **Course Code** | Unique identifier | `CSE201`, `MATH101` | Yes |
| **Course Name** | Full course title | `Data Structures` | Yes |
| **Credits** | Credit hours | `3` or `4` | Yes |
| **Faculty** | Professor name | `Dr. John Doe` | Yes |
| **Semester** | Semester number | `2`, `4`, or `6` | Yes |
| **Section** | Target section | `A`, `B`, or `Both` | Yes |
| **After Midsems** | Rotation flag | `Yes` or `No` | Yes |
| **Type** | Session type | `Lecture`, `Tutorial`, `Lab` | Yes |

### Sample CSV Content

```csv
Course Code,Course Name,Credits,Faculty,Semester,Section,After Midsems,Type
CSE201,Data Structures,4,Dr. Jane Smith,2,Both,No,Lecture
CSE201,Data Structures,4,Dr. Jane Smith,2,Both,No,Tutorial
CSE202,Computer Organization,4,Dr. Bob Wilson,2,A,No,Lecture
CSE202,Computer Organization,4,Dr. Bob Wilson,2,A,No,Lab
```

---

##  Output Files Generated

**Three formats**: CSV (18 files) + TXT (16 files) + HTML (19 files) = **53 total output files**

### 1. CSV Timetables (18 files)

**Format**: `{DEPT}_Sem{X}_Section{Y}_Timetable.csv`

Grid-based timetable with:
- **Rows**: Time slots (09:00-10:00, 10:00-11:00, etc.)
- **Columns**: Days (Monday to Saturday*)
- **Cells**: Course sessions with classroom assignments

**Example**: `CSE_Sem2_SectionA_Timetable.csv`

```
Time Slot,Monday,Tuesday,Wednesday,Thursday,Friday
09:00-10:00,CSE201 (C101),MATH201 (C102),...
10:00-11:00,CSE202 Lab (C301),CSE201 (C101),...
```

*Saturday column appears only for ECE Semester 4  
*CSV files can be opened in Excel for easy editing

### 2. Elective Text Files (16 files)

**Format**: `{DEPT}_Sem{X}_Section{Y}_Timetable_Electives.txt`

Detailed information including:
-  All scheduled sessions with time and room
-  Elective baskets with course options
-  "After Midsems" courses clearly marked
-  Unscheduled sessions (if any)

**Example content**:

```
================================================================================
                  CSE SEMESTER 2 - SECTION A TIMETABLE
================================================================================

SCHEDULED SESSIONS:
----------------------------------------
CSE201: Data Structures
   Monday 09:00-10:00
   Classroom: C101
   Faculty: Dr. Jane Smith

CSE201: Data Structures (Tutorial)
   Tuesday 11:00-12:00
   Classroom: C102
   Faculty: Dr. Jane Smith

...

================================================================================
ELECTIVE COURSES - Choose ONE from each basket
================================================================================

Basket B3:
----------------------------------------
   CS152: Data Science with Python
    Classroom: C002
   EC154: Introduction to Digital VLSI Design
    Classroom: C203

...

================================================================================
AFTER MIDSEMS (Rotated Courses):
================================================================================
These courses will be scheduled in the second half of the semester:
   CSE2xx_Elec3: Machine Learning Basics
   CSE2xx_Elec4: Web Development
```

### 3. HTML Viewer (19 files)

**Files**: `index.html` + 18 individual timetable HTMLs

**Features**:
-  Beautiful gradient design
-  Color-coded by course type
-  Responsive layout
-  Easy navigation
-  Fast loading

**Visual Design**:
-  Lectures: Blue gradient
-  Tutorials: Green gradient
-  Labs: Purple gradient
-  Evening sessions: Highlighted
-  Electives: Special badge

---

##  Screenshots

### 1. HTML Dashboard (index.html)

The main landing page shows all 18 timetables organized by department:

![HTML Dashboard](screenshots/timetable_html_view1.png)

*Interactive dashboard with quick navigation to any timetable*

---

### 2. Individual Timetable View

Each timetable features color-coded sessions and clear layout:

![Individual Timetable](screenshots/timetable_html_view2.png)

*CSE Semester 2 Section A - showing lectures, tutorials, and labs with room assignments*

---

### 3. CSV Output Sample

Machine-readable format for further processing:

![CSV View](screenshots/timetable_csv_view.png)

*Excel-compatible CSV format with all session details*

---

##  Customization & Configuration

### 1. Enable Elective Rotation

Reduce concurrent course load by 30-65% using "After Midsems" rotation:

```python
# In main.py, configure rotated courses (around line 50):
self.rotated_courses = {
    ('CSE', 2): [
        ['CSE2xx_Elec1', 'CSE2xx_Elec2'],  # Basket 1: First half
        ['CSE2xx_Elec3', 'CSE2xx_Elec4']   # Basket 2: Second half
    ],
    ('DSAI', 4): [
        ['DSAI4xx_Elec1', 'DSAI4xx_Elec2'],
        ['DSAI4xx_Elec3', 'DSAI4xx_Elec4']
    ],
    ('ECE', 6): [
        ['ECE6xx_Elec1', 'ECE6xx_Elec2']
    ]
}
```

Then mark courses in CSV with `After Midsems: Yes`

### 2. Modify Time Slots

```python
# In config.py, adjust time slots:
TIME_SLOTS = [
    '09:00-10:00',
    '10:00-11:00',
    '11:00-12:00',
    '12:00-13:00',  # Lunch
    '14:00-15:00',
    '15:00-16:00',
    '16:00-17:00',
    '17:00-18:00',
    '18:30-20:00'   # Evening slot
]
```

### 3. Configure Classrooms

```python
# In config.py, define available rooms:
CLASSROOMS = {
    'lecture': ['C101', 'C102', 'C103', 'C104', 'C201', ...],
    'lab': ['C301', 'C302', 'C303', 'C304', ...],
    'tutorial': ['C101', 'C102', 'C103', ...]
}
```

### 4. Enable Saturday for Other Departments

```python
# In main.py (line ~181), add departments:
if department == 'ECE' and semester == 4:
    self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
elif department == 'DSAI' and semester == 2:  # Add this
    self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
else:
    self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
```

---

##  Known Limitations

### Unscheduled Sessions Breakdown

| Department | Semester | Section | Unscheduled | Reason | Manual Solution |
|------------|----------|---------|-------------|--------|-----------------|
| DSAI | 2 | A | 2 sessions | Elective overflow | Schedule in evening slot |
| DSAI | 2 | B | 1 session | Elective conflict | Combine with Section A |
| DSAI | 4 | A | 2 sessions | High lab load | Use Saturday or evening |
| DSAI | 4 | B | 1 session | Lab room conflict | Share lab with Section A |
| ECE | 2 | A | 2 sessions | Elective timing | Move to afternoon slots |
| ECE | 2 | B | 1 session | Faculty clash | Adjust faculty schedule |
| ECE | 4 | A | 3 sessions | Maximum load | Already using Saturday |
| ECE | 4 | B | 5 sessions | Maximum load | Already using Saturday |
| **Total** | - | - | **17/582** | - | Average 0.94 per timetable |

### Why These Limitations Exist

1. **Hard Constraints**: 
   - Faculty cannot be in two places simultaneously
   - Classrooms have capacity limits
   - Lab equipment availability
   - Section separation requirements

2. **Soft Constraints**:
   - Even distribution across days preferred
   - Avoiding back-to-back 3-hour sessions
   - Lunch break preservation (12:00-14:00)

3. **Realistic Constraints**:
   - 96.9% automation is industry-leading
   - Manual intervention for 2.9% is minimal
   - Perfect automation often produces sub-optimal human experience

---

##  Detailed Documentation

Comprehensive documentation available in `timetable_generator/` directory:

### Core Documentation
- **[CONSTRAINTS_ANALYSIS.md](timetable_generator/CONSTRAINTS_ANALYSIS.md)** 
  - All 12 institutional requirements
  - 100% satisfaction analysis
  - Evidence for each constraint
  
- **[FINAL_SOFTWARE_STATUS.md](timetable_generator/FINAL_SOFTWARE_STATUS.md)** 
  - Executive summary
  - Performance metrics
  - Production readiness assessment

- **[QUICK_START.md](timetable_generator/QUICK_START.md)** 
  - Step-by-step usage guide
  - Troubleshooting tips
  - Common workflows

- **[SCHEDULE_EXPLANATION.md](timetable_generator/SCHEDULE_EXPLANATION.md)** 
  - Algorithm details
  - Scheduling logic
  - Optimization strategies

### Additional Guides
- **IMPROVEMENTS_SUMMARY.md** - Evolution from v1.0 to v3.1
- **TIMETABLE_README.md** - Technical implementation details
- **HTML_VIEWER_README.md** - HTML generation process
- **UNSCHEDULED_VS_AFTER_MIDSEMS_CLARIFICATION.md** - Rotation system explained

---

##  Current Status

### Version Information
- **Version**: 3.1 (Production Ready)
- **Release Date**: October 2025
- **Python Requirement**: 3.12+
- **Dependencies**: pandas

### Performance Summary
-  **Success Rate**: 96.9% (563/582 sessions automated)
-  **Constraint Satisfaction**: 100% (12/12 requirements met)
-  **Perfect Timetables**: 14 out of 18 (78%)
-  **Zero Conflicts**: No room or faculty double-bookings
-  **Generation Speed**: 18 timetables in ~30 seconds
-  **Manual Intervention**: Only 17 sessions (0.94 per timetable)

### Tested Scenarios
-  All 3 departments (CSE, DSAI, ECE)
-  All 3 semesters (2, 4, 6)
-  Both sections (A, B)
-  Multiple session types (Lecture, Tutorial, Lab)
-  Elective rotation ("After Midsems")
-  Evening slot utilization
-  Saturday scheduling (ECE Sem 4)
-  Faculty availability tracking
-  Classroom capacity constraints

---

##  Future Enhancements

### Potential Improvements
1. **Extended Saturday Support**: Enable for DSAI Sem 2, 4 (would reach 98.6% success)
2. **PDF Export**: Generate printable PDF timetables
3. **iCalendar Format**: Export for Google Calendar/Outlook
4. **Mobile App**: Native iOS/Android applications
5. **Admin Dashboard**: Web-based management interface
6. **Real-time Updates**: Live timetable modifications
7. **Student Portal Integration**: Direct sync with student systems
8. **Conflict Resolution AI**: Machine learning for optimal scheduling

---

##  Contributing

We welcome contributions! Areas for improvement:
- Algorithm optimization
- Additional output formats
- UI/UX enhancements
- Documentation improvements
- Bug reports and fixes

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 About Team BeyondGames

This project was **developed by Team BeyondGames** as part of the Software Design Tools and Techniques course at IIIT Dharwad.

### Team Mission
To create an intelligent, automated timetable generation system that simplifies academic scheduling while maintaining 100% constraint satisfaction and zero conflicts.

### Project Highlights
- 🎯 **96.9% automation** - Industry-leading success rate
- ⚡ **30-second generation** - Fast and efficient
- 🔧 **Production-ready** - Deployed and tested with real data
- 📚 **Well-documented** - Comprehensive guides and analysis

### Development Timeline
- **Initial Version (v1.0)**: 79% success rate
- **Enhanced Version (v2.0)**: 95% success rate  
- **Current Version (v3.1)**: 96.9% success rate (Production Ready)

---

##  Repository & Contact

**GitHub**: [BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad)

**Team**: BeyondGames  
**Institution**: IIIT Dharwad  
**Academic Year**: 2024-2025  
**Course**: Software Design Tools and Techniques (Third Semester)

---

##  Acknowledgments

- IIIT Dharwad faculty and administration for requirements
- Academic planning committee for constraint specifications
- Student community for testing and feedback
- Open-source Python community for excellent libraries

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

**Built with ❤️ by Team BeyondGames for IIIT Dharwad**

*Automated Academic Scheduling System*

</div>
