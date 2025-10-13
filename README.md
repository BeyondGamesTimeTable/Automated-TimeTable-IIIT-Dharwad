#  Automated Timetable Generator for IIIT Dharwad

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Success](https://img.shields.io/badge/Success-96.9%25-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Comprehensive academic scheduling system with daily timetables, exam schedules, and intelligent seating arrangements**

> Built by **Team BeyondGames** | Complete end-to-end solution for CSE, DSAI, and ECE departments

---

##  Quick Start

### **Just open `index.html` in your browser!**

No installation needed - everything runs directly in your browser with a modern, responsive interface.

**What You Get:**
-  **18 Daily Timetables** - Zero conflicts, 96.9% automated
-  **Exam Schedules** - 58 courses across 9 days
-  **324 Seating Charts** - Anti-adjacency algorithm for 1,800 students
-  **Modern UI** - Gradients, animations, and responsive design

---

##  System Overview

### Dual-System Architecture

#### 1.  Daily Timetable System
- **18 Timetables**: 3 departments  3 semesters  2 sections
- **96.9% Success**: 563/582 sessions automated (only 17 manual adjustments)
- **Zero Conflicts**: No room or faculty double-bookings
- **Smart Scheduling**: Lab blocks, tutorial placement, elective rotation

#### 2.  Exam Timetable & Seating System
- **58 Courses**: Intelligently scheduled across 9 exam days (18 sessions)
- **1,800 Students**: 600 per department with auto roll number generation
- **324 Seating Charts**: One for each classroom  session combination
- **Zero Adjacency**: Anti-adjacency algorithm ensures no same-exam students sit together
- **8,880 Seats**: Optimal allocation across 18 classrooms

###  Key Achievements

| Metric | Value |
|--------|-------|
| Timetables Generated | 18 conflict-free schedules |
| Success Rate | 96.9% (563/582 sessions) |
| Perfect Timetables | 14 out of 18 (78%) |
| Students Covered | 1,800 across 3 departments |
| Seating Charts | 324 with zero same-exam adjacency |
| Generation Speed | < 30 seconds for all timetables |
| Constraint Satisfaction | 100% (12/12 requirements) |

---

##  Installation & Usage

### For Generation (Optional)

```bash
# Clone repository
git clone https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad.git
cd Automated-TimeTable-IIIT-Dharwad

# Install dependencies
pip install pandas

# Generate daily timetables
cd timetable_generator
python main.py

# Generate exam timetables
cd ../exam_timetable
python main.py
```

### For Viewing (No Installation)

Simply open `index.html` in any modern browser. All HTML files are pre-generated and ready to use!

---

##  Project Structure

```
Automated-Time-Table-IIIT-DHARWAD/

  index.html                          # Main menu - Entry point
  README.md                           # This file
  .git/                               # Git repository

  timetable_generator/                # Daily Timetable System
     main.py                         # Generate 18 timetables
     timetable_to_html.py            # Convert CSV to HTML
     input_files/                    # Input CSV files (Even/Odd CSE/DSAI/ECE)
     timetable_outputs/              # Generated CSV timetables (18 files)
     timetable_html/                 # Interactive HTML viewers (19 files)
        index.html                     # Timetable selector
        *_Timetable.html               # Individual timetables

  exam_timetable/                     # Exam Timetable System
     main.py                         # Generate exam schedules
     generate_seating_viewer.py      # Generate seating viewer
     inputs/                         # Exam input data
     src/                            # Source modules
     outputs/                        # Generated files (329 files)
        exam_timetable.html            # Exam schedule viewer
        seating_charts_viewer.html     # Browse 324 charts
        exam_schedule.csv              # Raw schedule data
        seating_summary.csv            # Seating data
        seating_charts/                # 324 individual HTML charts

  screenshots/                        # UI screenshots

Total Files: 382 output files (53 daily + 329 exam system)
```

---

##  Key Features

### Daily Timetable Features
-  **Zero Conflicts** - No room/faculty double-bookings across 18 timetables
-  **Smart Allocation** - Lectures (60min), Tutorials (60min), Labs (120min)
-  **Elective Rotation** - "After Midsems" courses reduce load by 30-65%
-  **Evening Slot** - 18:30-20:00 overflow for high-demand courses
-  **Saturday Support** - Optional Saturday classes (ECE Sem 4)
-  **Multiple Outputs** - CSV (18), TXT (16), HTML (19)

### Exam & Seating Features
-  **Intelligent Scheduling** - 58 courses optimally distributed across 9 days
-  **Anti-Adjacency Algorithm** - Zero same-exam students sit adjacent
-  **Round-Robin Interleaving** - Mixed-course seating for maximum separation
-  **Student Management** - 1,800 students with auto roll numbers
-  **Classroom Optimization** - 25-35 students per room based on capacity
-  **324 Seating Charts** - One for each session  classroom combination

### Modern UI/UX
-  **Beautiful Design** - Gradient backgrounds, animated particles, responsive cards
-  **Enhanced Buttons** - Ripple effects, 3D transforms, color-coded navigation
-  **Responsive** - Works on desktop, tablet, and mobile
-  **Fast & Offline** - No server required, works from local files
-  **Intuitive Navigation** - Clear flow from main menu to detailed views

---

##  Performance Metrics

### Success Rate by Department

| Department | Timetables | Success Rate | Unscheduled | Perfect |
|------------|------------|--------------|-------------|---------|
| **CSE**    | 6          | **100%**     | 0/192       | 6/6     |
| **DSAI**   | 6          | **98.0%**    | 6/192       | 4/6     |
| **ECE**    | 6          | **95.4%**    | 11/198      | 4/6     |
| **Overall**| 18         | **96.9%**    | 17/582      | 14/18   |

### Evolution
- **v1.0**: 79% success (105 unscheduled)
- **v2.0**: 95% success (30 unscheduled)
- **v3.1**: 96.9% success (17 unscheduled)  **Current**

**Result**: 84% reduction in unscheduled sessions!

---

##  Input File Format

Place CSV files in `timetable_generator/input_files/sdtt_inputs/`:

```csv
Course,Faculty,Session Type,Hours per Week,After Midsems
DSA,Prof. Kumar,Lecture,3,No
DSA,Prof. Kumar,Tutorial,1,No
DSA Lab,Prof. Kumar,Lab,2,No
ML Elective,Prof. Sharma,Lecture,3,Yes
```

**Required Columns:**
- `Course` - Course name
- `Faculty` - Faculty name (for conflict checking)
- `Session Type` - Lecture/Tutorial/Lab
- `Hours per Week` - Weekly hours
- `After Midsems` - Yes/No (for elective rotation)

---

##  Customization

### Modify Time Slots
Edit time slots in the generator code:
```python
TIME_SLOTS = [
    '09:00-10:00', '10:00-11:00', '11:00-12:00',
    '12:00-13:00',  # Lunch
    '14:00-15:00', '15:00-16:00', '16:00-17:00',
    '17:00-18:00', '18:30-20:00'  # Evening
]
```

### Enable Saturday for More Departments
Modify department configuration to include Saturday scheduling for high-load semesters.

### Adjust Classroom Capacities
Update classroom list in configuration for exam seating optimization.

---

##  Known Limitations

**Unscheduled Sessions**: 17 out of 582 (2.9%) require manual scheduling due to:
- High concurrent load in some semesters
- Faculty availability conflicts
- Limited classroom capacity during peak hours

**Solution**: Use evening slots (18:30-20:00) or Saturday for overflow sessions.

---

##  Troubleshooting

### HTML Navigation Errors
**Issue**: Back buttons not working  
**Fix**: Ensure proper file structure - open `index.html` from project root

### Buttons Not Displaying
**Issue**: Styling not applied  
**Fix**: Clear browser cache (Ctrl+Shift+R) and reload

### Generation Errors
**Issue**: `pandas not found`  
**Fix**: `pip install pandas`

### Performance Issues
**Issue**: Slow browser with 324 charts  
**Fix**: Open charts one session at a time, use Chrome/Firefox/Edge 120+

---

##  Future Enhancements

- [ ] PDF Export for printable timetables
- [ ] iCalendar format for Google Calendar/Outlook sync
- [ ] Mobile app (iOS/Android)
- [ ] Web dashboard for live editing
- [ ] Extended Saturday support for more departments
- [ ] AI-powered conflict resolution
- [ ] Real-time timetable updates

---

##  About Team BeyondGames

**Mission**: Create an intelligent, automated timetable system that simplifies academic scheduling while maintaining 100% constraint satisfaction.

**Development Timeline**:
- v1.0: 79% success  v2.0: 95% success  v3.1: 96.9% success  **Production Ready**

**Institution**: IIIT Dharwad  
**Course**: Software Design Tools and Techniques (Third Semester, 2024-2025)

---

##  Contact & Repository

**GitHub**: [BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad)

**Team**: BeyondGames  
**Academic Year**: 2024-2025

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  Acknowledgments

- IIIT Dharwad faculty for requirements and specifications
- Academic planning committee for constraint definitions
- Student community for testing and valuable feedback
- Open-source Python community for excellent libraries

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

**Built with ❤️ by Team BeyondGames**

*Automated Academic Scheduling Made Simple*

</div>
