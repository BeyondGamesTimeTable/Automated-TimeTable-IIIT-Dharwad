# Sankalp - Automated Timetable Generator

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Intelligent academic scheduling system with web-based interface for IIIT Dharwad. Supports automated timetable generation, minor courses, and conflict-free scheduling for CSE, DSAI, and ECE departments.

---

## Quick Start

### Web Interface

```bash
# Start the Flask server
python upload_server.py

# Open browser
http://localhost:5000
```

Upload CSV files through the web interface and generate timetables instantly.

### Command Line

```bash
cd timetable_generator
python main.py
```

---

## Features

- Web upload interface with drag & drop support
- 18 daily timetables (3 departments × 3 semesters × 2 sections)
- Minor courses support with evening slots (18:30-20:00 Tue/Thu)
- Excel and image export for individual timetables
- Zero faculty/room conflicts
- Version control for all uploads
- Smart scheduling for lectures, tutorials, and labs
- Elective rotation and cross-department courses

---

## Installation

### Requirements

```bash
Python 3.12+
Flask 3.0+
Pandas 2.0+
openpyxl
```

### Setup

```bash
git clone https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad.git
cd Automated-TimeTable-IIIT-Dharwad
pip install -r requirements-backend.txt
python upload_server.py
```

---

## Usage

### Web Interface

1. Navigate to `http://localhost:5000`
2. Upload CSV files (CSE, DSAI, ECE, electives, minors)
3. Click "Generate Timetables"
4. View, download Excel, or export as images

### Input Files

Sample files are available in `timetable_generator/input_files/sdtt_inputs/`:
- `CSE.csv` - CSE department courses
- `DSAI.csv` - DSAI department courses
- `ECE.csv` - ECE department courses
- `electives.csv` - Elective courses
- `minors.csv` - Minor courses (Semester 3+)

---

## CSV File Format

### Department Files (CSE.csv, DSAI.csv, ECE.csv)

```csv
Course Code,Course Title,Lectures,Tutorials,Practicals,Self-Study,Credits,Faculty,Semester,Section,Lab
MA163,Linear Algebra,3,1,0,0,2,Dr. Sibasankar Padhy,2,2A,
CS163,Data Structures & Algorithms,3,0,2,0,4,Dr. C. B. Akki,2,2A,S
CS206,Theory of Computation,3,1,0,0,4,Dr. Pavan,4,4A,
```

**Required Columns:**
- Course Code, Course Title, Lectures, Tutorials, Practicals, Self-Study, Credits, Faculty, Semester
- Optional: Section (e.g., 2A, 4B), Lab (S for separate lab, H for hardware lab)

### Electives File (electives.csv)

```csv
Course Code,Course Title,Lectures,Tutorials,Practicals,Self-Study,Credits,Faculty,Semester,Branch,HSS
HS153,Innovation and Entrepreneurship,3,1,0,0,3,Dr. Deepak K T,2,Cse,Y
CS471,Deep Computer Vision,3,1,0,0,4,Chinmayanand,6,,
```

**Required Columns:**
- Course Code, Course Title, Lectures, Tutorials, Practicals, Self-Study, Credits, Faculty, Semester
- Optional: Branch (Cse/DSAI/ECE), HSS (Y for humanities electives)

### Minors File (minors.csv)

```csv
Course Code,Course Title,Lectures,Tutorials,Practicals,Self-Study,Credits,Faculty,Semester
DS358,Deep Speech Processing,3,0,0,0,4,Prof. SRM Prasanna,"4,6"
QU505,Quantum Computing,3,0,0,0,4,Dr. Aswath B,4
```

**Required Columns:**
- Course Code, Course Title, Lectures, Tutorials, Practicals, Self-Study, Credits, Faculty, Semester
- **Note:** Semester field can be comma-separated for multi-semester courses (e.g., "4,6")

---

## Configuration

Edit `timetable_generator/time_config.py` to customize time slots:

```python
# Standard time slots
TIME_SLOTS = [
    ('09:00', '10:00'),
    ('10:00', '11:00'),
    ('11:00', '12:00'),
    ('12:00', '13:00'),  # Lunch
    ('14:00', '15:00'),
    ('15:00', '16:00'),
    ('16:00', '17:00'),
    ('17:00', '18:00')
]

# Minor slot (evening) for Semester 3+
MINOR_SLOT_ENABLED = True
MINOR_SLOT_TIME = ('18:30', '20:00')
MINOR_SLOT_DAYS = ['Tuesday', 'Thursday']
```

---

## Troubleshooting

### Server Won't Start

Check if port 5000 is in use:
```bash
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### CSV Upload Issues

- Ensure CSV files are UTF-8 encoded
- Check column names match required format exactly
- Verify semester numbers are integers
- Use correct file names: CSE.csv, DSAI.csv, ECE.csv, electives.csv, minors.csv

---

## Technology Stack

- Python 3.12+, Flask 3.0+
- Pandas 2.0+, openpyxl
- HTML5, CSS3, JavaScript

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Team

Team BeyondGames  
IIIT Dharwad

---

**Last Updated**: February 6, 2026
