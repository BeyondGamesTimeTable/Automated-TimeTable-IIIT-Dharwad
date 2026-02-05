# Automated Timetable Generator for IIIT Dharwad

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Intelligent academic scheduling system with web-based upload interface, automated timetable generation, minor courses support, and conflict-free scheduling**

> Built by **Team BeyondGames** | Complete solution for CSE, DSAI, and ECE departments

---

## Quick Start

### Web Interface (Recommended)

```bash
# Start the Flask server
python upload_server.py

# Open in browser
http://localhost:5000
```

Upload your CSV files through the web interface and generate timetables instantly!

### Direct Generation

```bash
cd timetable_generator
python main.py
```

**What You Get:**
- ✨ **Web Upload Interface** - Drag & drop CSV files with live validation
- 📅 **18 Daily Timetables** - Zero conflicts across all departments
- 🎓 **Minor Courses** - Evening slot (6:30-8:00 PM) for cross-department minors
- 📊 **Excel Export** - Download individual timetables as Excel files
- 🖼️ **Image Export** - Convert timetables to PNG images
- 🕒 **Version Control** - All uploads timestamped and preserved
- 🎨 **Modern UI** - Responsive design with smooth navigation

---

## Features

### Core Capabilities
- ✅ **Zero Conflicts** - No faculty/room double-bookings
- 🕐 **Smart Scheduling** - Lectures (60min), Tutorials (60min), Labs (120-180min)
- 🎓 **Minor Courses** - Evening slot (18:30-20:00) on Tue/Thu for Semester 3+
- 📚 **Elective Support** - Section rotation and cross-department courses
- 🏫 **Multi-Department** - CSE, DSAI, ECE with 2 sections each
- 📅 **Saturday Classes** - Optional 6-day scheduling
- 💾 **Version Control** - All uploads timestamped and preserved

### Web Interface Features
- 📤 **Drag & Drop Upload** - Easy CSV file upload with validation
- 📊 **Excel Downloads** - Export individual timetables to Excel
- 🖼️ **Image Export** - Convert timetables to PNG images
- 🔄 **Live Updates** - Real-time generation status and progress
- 📁 **Version History** - Browse previous timetable generations
- 🎨 **Responsive Design** - Works on desktop, tablet, and mobile

### Minor Courses System
- ⏰ **Evening Slot** - 6:30-8:00 PM (90 minutes) on Tuesday & Thursday
- 🎓 **Cross-Department** - Shared across CSE, DSAI, ECE
- 📝 **Multi-Semester** - Single course can span multiple semesters
- 👨‍🏫 **Faculty Tracking** - Faculty assignments displayed for each minor
- 🏛️ **Classroom Assignment** - Automatic classroom allocation
- 📋 **Separate CSV** - `minors.csv` with dedicated minor courses data

---

## Installation

### Requirements
```bash
Python 3.12+
Flask 3.0+
Pandas 2.0+
openpyxl (for Excel export)
```

### Setup
```bash
# Clone repository
git clone https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad.git
cd Automated-TimeTable-IIIT-Dharwad

# Install dependencies
pip install -r requirements-backend.txt

# Start web server
python upload_server.py

# Open browser to http://localhost:5000
```

---

## Usage

### 1. Web Interface (Recommended)

**Upload CSV files:**
1. Navigate to `http://localhost:5000`
2. Upload department CSV files (CSE, DSAI, ECE)
3. Upload electives CSV (optional)
4. Upload minors CSV (optional)
5. Click "Generate Timetables"
6. View, download Excel, or export as images

**Input Files:**
- `cse_sample.csv` - CSE courses
- `dsai_sample.csv` - DSAI courses  
- `ece_sample.csv` - ECE courses
- `electives_sample.csv` - Elective courses
- `minors.csv` - Minor courses (Semester 3+)

### 2. Command Line

```bash
cd timetable_generator
python main.py
```

Generated files in:
- `timetable_outputs/` - CSV timetables
- `timetable_html/` - Interactive HTML viewers

---

## CSV File Format

### Department Files (CSE/DSAI/ECE)

```csv
Course Code,Course Title,Lectures,Tutorials,Practicals,Self-Study,Credits,Faculty,Semester
CS201,Data Structures,3,1,2,6,4,Prof. Kumar,2
```

### Electives File

```csv
Course Code,Course Title,Lectures,Tutorials,Practicals,Self-Study,Credits,Faculty,Semester,Section
CS301,Machine Learning,3,0,0,9,3,Prof. Sharma,6,A
```

### Minors File

```csv
Course Code,Course Title,Lectures,Tutorials,Practicals,Self-Study,Credits,Faculty,Semester
DS358,Deep Speech Processing,1,0,0,2,1,Prof. SRM Prasanna,"4,6"
QU505,Quantum Computing,1,0,0,2,1,Prof. Aswath,4
```

**Note:** Semester field in minors can be comma-separated for multi-semester courses.

---

## Project Structure

```
Automated-Time-Table-IIIT-DHARWAD/
├── upload_server.py              # Flask web server
├── index.html                    # Main landing page
├── upload.html                   # Upload interface
├── timetable_versions.html       # Version history viewer
├── requirements-backend.txt      # Python dependencies
│
├── timetable_generator/
│   ├── main.py                   # Core generation logic
│   ├── timetable_to_html.py      # HTML converter
│   ├── time_config.py            # Time slot configuration
│   ├── validate_timetable.py     # Conflict checker
│   │
│   ├── input_files/
│   │   ├── sdtt_inputs/          # Sample CSV files
│   │   │   ├── cse_sample.csv
│   │   │   ├── dsai_sample.csv
│   │   │   ├── ece_sample.csv
│   │   │   ├── electives_sample.csv
│   │   │   └── minors.csv
│   │   └── versions/             # Timestamped uploads
│   │
│   ├── timetable_outputs/        # Generated CSV files
│   ├── timetable_html/           # HTML timetables
│   └── __pycache__/
│
├── exam_timetable/               # Exam scheduling system
└── test_cases/                   # Test suite
```

---

## Configuration

### Time Slots

Edit [time_config.py](timetable_generator/time_config.py) to customize scheduling:

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

### Classroom Configuration

Modify classroom lists in [main.py](timetable_generator/main.py):
- `self.large_classrooms` - For lectures (capacity 80-100)
- `self.lab_rooms` - For practical sessions (capacity 30-40)

---

## Key Algorithms

### 1. Conflict Detection
- **Faculty Availability**: Prevents faculty double-booking across departments
- **Room Allocation**: Ensures no room conflicts across sections
- **Time Validation**: Checks for overlapping sessions

### 2. Lab Scheduling
- **Block Allocation**: 2-3 hour continuous blocks for labs
- **Room Rotation**: Distributes lab sessions across available rooms
- **Daily Limit**: Maximum labs per day to prevent overcrowding

### 3. Elective Rotation
- **Section Split**: Different electives for Section A and B
- **Mid-Semester Switch**: Rotates electives after midsems
- **Load Balancing**: Distributes electives across week

### 4. Minor Course Assignment
- **Cross-Department**: Same minor options for all departments in a semester
- **Evening Slot**: Dedicated 18:30-20:00 time on Tue/Thu
- **Classroom Allocation**: Automatic room assignment from large classrooms
- **Multi-Semester Support**: Single minor can span multiple semesters

---

## Troubleshooting

### Server Won't Start
```bash
# Check if port 5000 is available
netstat -ano | findstr :5000

# Kill process if needed (Windows)
taskkill /PID <process_id> /F

# Try different port
set FLASK_RUN_PORT=5001
python upload_server.py
```

### CSV Upload Fails
- ✅ Ensure CSV files are UTF-8 encoded
- ✅ Check column names match required format exactly
- ✅ Remove any special characters from file names
- ✅ Verify semester numbers are integers

### Timetables Not Generating
- ✅ Check server console for error messages
- ✅ Verify all required CSV files are uploaded
- ✅ Ensure `timetable_generator` folder exists
- ✅ Check write permissions on output folders

### Minor Courses Not Showing
- ✅ Upload `minors.csv` file (plural, not singular)
- ✅ Verify semester field contains valid semester numbers
- ✅ Ensure courses are for Semester 3 or higher
- ✅ Check CSV format matches template

---

## API Endpoints

The Flask server provides these endpoints:

```
GET  /                          - Main landing page
GET  /upload.html               - Upload interface
GET  /timetable_versions.html   - Version history
POST /api/upload_csvs           - Upload CSV files
POST /api/generate_timetables   - Generate timetables
GET  /api/versions              - List all versions
GET  /api/download_single_excel - Download Excel file
```

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Departments | 3 (CSE, DSAI, ECE) |
| Timetables per Generation | 18 (3 depts × 3 sems × 2 sections) |
| Generation Time | < 30 seconds |
| Conflict Rate | 0% (zero conflicts) |
| Automation Rate | ~97% |
| Upload File Size Limit | 16 MB per file |

---

## Technology Stack

- **Backend**: Python 3.12+, Flask 3.0+
- **Data Processing**: Pandas 2.0+
- **Excel Export**: openpyxl
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Deployment**: Local server (localhost:5000)

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Team

**Team BeyondGames**  
IIIT Dharwad | Software Design Tools and Techniques

---

## Acknowledgments

- IIIT Dharwad faculty for requirements and specifications
- Academic planning committee for constraint definitions
- Student community for testing and feedback

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

### Built with ❤️ by Team BeyondGames

**[GitHub Repository](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad)** | **[Report Issue](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad/issues)**

---

**Last Updated**: February 6, 2026  
**Status**: ✅ Active & Maintained

</div>
