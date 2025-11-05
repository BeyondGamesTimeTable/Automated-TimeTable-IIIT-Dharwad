# 📚 Automated Timetable Generator - User Manual

## IIIT Dharwad Timetable Management System

**Version:** 2.0.0  
**Date:** November 2025  
**Developed by:** BeyondGames Team  
**Institution:** Indian Institute of Information Technology, Dharwad

---

## 📋 Table of Contents

1. [Cover Page](#cover-page)
2. [Overview](#overview)
3. [System Architecture](#system-architecture)
4. [Installation Guide](#installation-guide)
5. [Usage Scenarios](#usage-scenarios)
6. [Sample Inputs & Configuration](#sample-inputs--configuration)
7. [Web Application Guide](#web-application-guide)
8. [Troubleshooting](#troubleshooting)
9. [FAQ's](#faqs)
10. [Technical Specifications](#technical-specifications)
11. [Support & Contact](#support--contact)

---

## 1. Cover Page

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║           AUTOMATED TIMETABLE GENERATOR                    ║
║                                                            ║
║                   User Manual v2.0                         ║
║                                                            ║
║     Indian Institute of Information Technology, Dharwad    ║
║                                                            ║
║                  BeyondGames Team                          ║
║                                                            ║
║                   November 2025                            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

**Document Purpose:** This manual provides comprehensive guidance for using the Automated Timetable Generator system, including installation, configuration, usage scenarios, and troubleshooting.

**Target Audience:** 
- Academic administrators
- Timetable coordinators
- IT support staff
- Faculty members

**System Access:**
- **Web Application:** https://beyondgamesclasssync.netlify.app/
- **Backend API:** https://automated-timetable-iiit-dharwad.onrender.com/
- **GitHub Repository:** https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad

---

## 2. Overview

### 2.1 What is the Automated Timetable Generator?

The Automated Timetable Generator is an intelligent scheduling system designed to create conflict-free weekly timetables for IIIT Dharwad. It handles multiple departments, semesters, sections, and course types while ensuring optimal classroom utilization and instructor scheduling.

### 2.2 Key Features

✅ **Automated Scheduling**
- Generates timetables for 3 departments (CSE, DSAI, ECE)
- Handles 3 semesters (2, 4, 6) with 2 sections each
- Creates 12 complete weekly timetables automatically

✅ **Smart Conflict Resolution**
- Prevents instructor double-booking
- Ensures classroom availability
- Manages common courses across sections
- Handles cross-department shared courses

✅ **LTPSC Conversion**
- Lecture hours: L ÷ 1.5 = number of 90-minute lectures
- Tutorial hours: T = number of 60-minute tutorials
- Practical hours: P ÷ 2 = number of 2-hour labs

✅ **Web-Based Interface**
- View all timetables online
- Upload new course data via drag & drop
- Export to Excel format
- Mobile-responsive design

✅ **Visual Enhancements**
- Color-coded courses by type
- Fractional tutorial visualization (60 min in 90 min slots)
- Clear time slot indicators
- Interactive navigation

### 2.3 System Components

1. **Python Generator (main.py)** - Core scheduling engine
2. **Web Frontend (Netlify)** - User interface for viewing timetables
3. **Backend API (Render)** - File upload and management
4. **HTML Exporter** - Converts timetables to web format
5. **Excel Exporter** - Generates downloadable .xlsx files

### 2.4 Supported Course Types

- **Regular Lectures** - 90-minute sessions
- **Tutorials** - 60-minute sessions (shown with fractional coloring)
- **Labs/Practicals** - 120-minute flexible sessions
- **Electives** - Multiple baskets with rotation strategy
- **Common Courses** - Shared across sections (same time, same classroom)
- **Cross-Department Courses** - Shared between DSAI and ECE

---

## 3. System Architecture

### 3.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│            https://beyondgamesclasssync.netlify.app/        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   View       │  │   Upload     │  │   Exam       │      │
│  │ Timetables   │  │    Data      │  │  Schedule    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS / API Calls
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    BACKEND SERVER                            │
│      https://automated-timetable-iiit-dharwad.onrender.com  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Flask API   │  │ File Upload  │  │    CORS      │      │
│  │   Server     │  │   Handler    │  │   Config     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ File Storage
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  LOCAL GENERATION SYSTEM                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   main.py    │  │   Excel      │  │    HTML      │      │
│  │  (Generator) │  │  Exporter    │  │  Converter   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  Input: CSV Files  →  Process  →  Output: Excel + HTML      │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow

1. **Input:** CSV files with course data (Course Code, Title, LTPSC, Semester, Classroom, Section, Electives)
2. **Processing:** Python generator schedules courses with constraint satisfaction
3. **Output:** 
   - 12 Excel timetables (.xlsx)
   - 12 HTML timetables (web view)
   - Exam schedules
   - Seating charts

### 3.3 Technology Stack

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Responsive design (mobile-friendly)
- Deployed on Netlify

**Backend:**
- Python 3.11.9
- Flask 3.0.0
- Gunicorn (WSGI server)
- Deployed on Render

**Data Processing:**
- Pandas (CSV/Excel handling)
- Custom scheduling algorithms
- Constraint satisfaction logic

---

## 4. Installation Guide

### 4.1 Prerequisites

**Required Software:**
- Python 3.11 or higher
- Git (for cloning repository)
- Web browser (Chrome, Firefox, Edge, Safari)

**Optional:**
- Code editor (VS Code, PyCharm)
- Excel viewer

### 4.2 Local Installation Steps

#### Step 1: Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad.git

# Navigate to project directory
cd Automated-TimeTable-IIIT-Dharwad
```

#### Step 2: Set Up Python Environment

```bash
# Check Python version
python --version  # Should be 3.11 or higher

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies

For local timetable generation only:
```bash
pip install pandas openpyxl
```

For running the upload server locally:
```bash
pip install -r requirements-backend.txt
```

#### Step 4: Verify Installation

```bash
# Navigate to timetable generator folder
cd timetable_generator

# Run the generator
python main.py
```

**Expected Output:**
```
🎓 IIIT Dharwad Timetable Generator v2.0
==========================================
Loading CSV files from: input_files/sdtt_inputs/
✓ Processing CSE Semester 2...
✓ Processing CSE Semester 4...
...
✓ All timetables generated successfully!
✓ Excel files saved to: timetable_outputs/
✓ HTML files saved to: timetable_html/
```

### 4.3 Directory Structure

```
Automated-TimeTable-IIIT-Dharwad/
├── timetable_generator/
│   ├── main.py                 # Main generator script
│   ├── timetable_to_html.py   # HTML converter
│   ├── input_files/
│   │   └── sdtt_inputs/        # CSV input files
│   │       ├── Even CSE.csv
│   │       ├── Even DSAI.csv
│   │       └── Even ECE.csv
│   ├── timetable_outputs/      # Generated Excel files
│   └── timetable_html/         # Generated HTML files
├── upload_server.py            # Backend server
├── requirements-backend.txt    # Backend dependencies
├── netlify.toml               # Frontend deployment config
├── render.yaml                # Backend deployment config
└── USER_MANUAL.md             # This file
```

### 4.4 Web Application Access

**No installation required!**

Simply visit: **https://beyondgamesclasssync.netlify.app/**

The web application is fully hosted and accessible from any device with internet connection.

---

## 5. Usage Scenarios

### 5.1 Scenario 1: Viewing Existing Timetables

**User Story:** Faculty member wants to check their teaching schedule.

**Steps:**

1. **Open Web Application**
   - Navigate to https://beyondgamesclasssync.netlify.app/
   
2. **Click "Daily Timetable" Card**
   - Main menu shows three cards: Daily Timetable, Exam Timetable, Upload Data
   
3. **Select Department and Semester**
   - Example: Click "CSE Sem 4 Section A"
   
4. **View Timetable**
   - Color-coded schedule appears
   - Each course shows: Course Code, Course Name, Room Number, Instructor
   - Time slots: Monday to Friday, 08:00 to 18:00

**Screenshot Locations:**
- Main Menu: Shows three card options
- Timetable Selection: Grid of 12 timetable options
- Timetable View: Full weekly schedule with color coding

**Features Available:**
- ✅ Back to selection button
- ✅ Main menu button
- ✅ Mobile-responsive layout
- ✅ Print functionality (browser print)

### 5.2 Scenario 2: Uploading New Course Data

**User Story:** Administrator needs to update course information for next semester.

**Steps:**

1. **Prepare CSV Files**
   - Format: `Even CSE.csv`, `Even DSAI.csv`, `Even ECE.csv`
   - Required columns: Course Code, Course Title, LTPSC, Semester, Classroom, Section, Electives

2. **Navigate to Upload Page**
   - Click "Upload Data" card from main menu
   - Or visit: https://beyondgamesclasssync.netlify.app/upload.html

3. **Check Server Status**
   - Green banner: "✓ Server Connected!" → Good to proceed
   - Red banner: "✕ Server Not Available" → Wait 30-60 seconds for server to wake up

4. **Upload Files**
   - **Option A - Drag & Drop:**
     - Drag CSV files onto the drop zone
     - Drop zone highlights when files hover over it
   
   - **Option B - Browse:**
     - Click "Browse Files" button
     - Select CSV files from file dialog
     - Click "Open"

5. **Review Selected Files**
   - File list appears below drop zone
   - Each file shows: name, size, status

6. **Process Upload**
   - Click "🚀 Upload Files" button
   - Watch progress:
     - "Uploading..." (blue)
     - "✓ Uploaded" (green)
     - "🔄 Regenerating Timetables..." (orange) *
     - "✓ Timetables Updated!" (green) *
   
   *Note: Regeneration currently requires local execution

7. **Confirmation**
   - Success message appears
   - Old files automatically deleted
   - New files saved to server

**Important Notes:**
- ✅ Multiple files can be uploaded simultaneously
- ✅ Old CSV files are automatically deleted before upload
- ✅ Only `.csv` files are accepted
- ✅ Maximum file size: 16MB per file
- ⚠️ Timetable regeneration must be done locally (see Scenario 3)

### 5.3 Scenario 3: Generating Timetables Locally

**User Story:** After uploading new data, administrator generates updated timetables.

**Steps:**

1. **Download Latest CSV Files** (if uploaded via web)
   - Access backend storage or use existing local files

2. **Place CSV Files in Correct Location**
   ```
   timetable_generator/input_files/sdtt_inputs/
   ├── Even CSE.csv
   ├── Even DSAI.csv
   └── Even ECE.csv
   ```

3. **Open Terminal/Command Prompt**
   ```bash
   cd path/to/Automated-TimeTable-IIIT-Dharwad/timetable_generator
   ```

4. **Run Generator**
   ```bash
   python main.py
   ```

5. **Monitor Progress**
   - Terminal shows real-time progress
   - Each department/semester processed sequentially
   - Success confirmations displayed

6. **Verify Outputs**
   - **Excel files**: `timetable_generator/timetable_outputs/`
   - **HTML files**: `timetable_generator/timetable_html/`

7. **Deploy to Web** (optional)
   ```bash
   # Commit and push to GitHub
   git add .
   git commit -m "Updated timetables for [semester/year]"
   git push origin main
   
   # Netlify auto-deploys in 1-2 minutes
   ```

**Expected Generation Time:**
- Small dataset (3 depts × 3 sems): 30-60 seconds
- Full dataset (all courses): 1-2 minutes

### 5.4 Scenario 4: Checking Common Courses

**User Story:** Verify that common courses are scheduled identically across sections.

**Steps:**

1. **Open Two Section Timetables**
   - Example: CSE Sem 2 Section A and Section B

2. **Locate Common Courses**
   - Common courses have empty "Section" field in CSV
   - Example: CS165 (Data Structures), HS205 (English)

3. **Verify Matching**
   - ✅ Same day
   - ✅ Same time slot
   - ✅ Same classroom (e.g., C004, C101)
   - ✅ Same instructor

**Why This Matters:**
- Students from both sections attend together
- Prevents classroom conflicts
- Ensures efficient use of large classrooms

### 5.5 Scenario 5: Understanding Tutorial Visualization

**User Story:** Identify 60-minute tutorials in 90-minute time slots.

**Visual Indicators:**
- **Regular 90-min lectures**: Full-width colored block
- **60-min tutorials**: Colored bar covering 66.67% width (2/3 of slot)
- **Text label**: "Tutorial (1 hour)" displayed on card

**Example:**
```
┌─────────────────────────────────┐
│ CS201 - Data Structures         │ ← Full 90-min lecture
│ Room: C301 | Dr. Smith          │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ CS201 Tutorial (1 hour)         │ ← 60-min tutorial
│ ██████████████████░░░░░░░       │ ← 66.67% colored
│ Room: C301 | Dr. Smith          │
└─────────────────────────────────┘
```

---

## 6. Sample Inputs & Configuration

### 6.1 CSV Input File Format

**Filename:** `Even CSE.csv`, `Even DSAI.csv`, `Even ECE.csv`

**Required Columns:**

| Column Name   | Description                          | Example Values                    |
|---------------|--------------------------------------|-----------------------------------|
| Course Code   | Unique course identifier             | CS101, MA201, EC305              |
| Course Title  | Full name of course                  | Data Structures, Linear Algebra  |
| LTPSC         | Lecture-Tutorial-Practical-Self-Credit | 3-1-0-0-4, 2-0-2-0-3           |
| Semester      | Semester number                      | 2, 4, 6                          |
| Classroom     | Assigned room                        | C101, C004, L201                 |
| Section       | Section identifier (blank for common)| A, B, or empty                   |
| Electives     | Elective basket (if applicable)      | PEC1, PEC2, OEC1, or empty      |

### 6.2 Sample CSV Content

```csv
Course Code,Course Title,LTPSC,Semester,Classroom,Section,Electives
CS101,Programming Fundamentals,3-1-0-0-4,2,C101,A,
CS101L,Programming Lab,0-0-2-0-1,2,L201,A,
CS165,Data Structures,3-1-0-0-4,2,C004,,
HS205,English Communication,2-0-0-0-2,2,C101,,
MA201,Linear Algebra,3-1-0-0-4,2,C202,A,
EC301,Digital Electronics,3-0-2-0-4,4,C301,A,PEC1
CS401,Machine Learning,3-0-0-0-3,6,C401,A,PEC2
```

### 6.3 LTPSC Format Explanation

**Format:** `L-T-P-S-C`

- **L (Lecture):** Contact hours per week
- **T (Tutorial):** Tutorial hours per week
- **P (Practical):** Lab hours per week
- **S (Self-study):** Self-study hours per week
- **C (Credits):** Total credits

**Conversion Rules:**

1. **Lectures:** `L ÷ 1.5 = number of 90-minute sessions`
   - Example: L=3 → 3÷1.5 = 2 sessions per week

2. **Tutorials:** `T = number of 60-minute sessions`
   - Example: T=1 → 1 session per week (shown as fractional)

3. **Labs:** `P ÷ 2 = number of 2-hour sessions`
   - Example: P=2 → 2÷2 = 1 lab per week

### 6.4 Special Course Types

#### Common Courses
- **Definition:** Courses attended by both Section A and Section B together
- **CSV Marker:** Leave "Section" column empty
- **Scheduling:** System ensures same time slot AND same classroom
- **Examples:** HS205 (English), CS165 (Data Structures)

#### Elective Courses
- **Definition:** Optional courses chosen from predefined baskets
- **CSV Marker:** "Electives" column contains basket code
- **Basket Types:**
  - `PEC1`, `PEC2`, `PEC3` - Program Elective Core
  - `OEC1`, `OEC2`, `OEC3` - Open Elective Core
- **Scheduling:** All electives in same basket get same time slots

#### Cross-Department Courses
- **Definition:** Courses shared between DSAI and ECE departments
- **Identification:** Automatically detected by system
- **Scheduling:** Coordinates schedules across departments

### 6.5 Configuration Files

#### netlify.toml (Frontend Deployment)
```toml
[build]
  command = "echo 'Static site - no build needed'"
  publish = "."

[build.environment]
  PYTHON_VERSION = ""

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
```

#### render.yaml (Backend Deployment)
```yaml
services:
  - type: web
    name: automated-timetable-iiit-dharwad
    env: python
    buildCommand: pip install --upgrade pip && pip install -r requirements-backend.txt
    startCommand: gunicorn upload_server:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
```

#### requirements-backend.txt (Backend Dependencies)
```
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

### 6.6 Time Slot Configuration

**Default Time Slots (Monday - Friday):**

| Slot | Time        | Duration | Type      |
|------|-------------|----------|-----------|
| 1    | 08:00-09:30 | 90 min   | Morning   |
| 2    | 09:30-11:00 | 90 min   | Morning   |
| 3    | 11:30-13:00 | 90 min   | Morning   |
| -    | 13:00-14:00 | 60 min   | Lunch     |
| 4    | 14:00-16:00 | 120 min  | Afternoon |
| 5    | 16:00-18:00 | 120 min  | Afternoon |

**Note:** Evening slot (18:30-20:00) removed as per optimization.

---

## 7. Web Application Guide

### 7.1 Main Menu Navigation

**URL:** https://beyondgamesclasssync.netlify.app/

**Three Main Cards:**

1. **📅 Daily Timetable**
   - View weekly schedules
   - 12 timetables available
   - Color-coded courses

2. **📝 Exam Timetable**
   - View examination schedules
   - Check seating arrangements
   - 324 seating charts

3. **📤 Upload Data**
   - Upload new CSV files
   - Drag & drop interface
   - Real-time server status

### 7.2 Timetable Viewer Features

**Color Coding:**
- Each course has unique color
- Same course = same color across all cells
- Tutorials have fractional coloring

**Information Display:**
- Course Code (e.g., CS101)
- Course Title (e.g., Programming Fundamentals)
- Classroom (e.g., C101)
- Instructor name
- Duration indicator (for tutorials)

**Navigation:**
- "Back to Selection" → Return to timetable grid
- "Main Menu" → Return to homepage
- Mobile-friendly responsive design

### 7.3 Upload Interface

**Server Status Indicator:**
- ✅ **Green Banner:** Server is online and ready
- ❌ **Red Banner:** Server is waking up (wait 30-60 seconds)

**Upload Methods:**

1. **Drag & Drop:**
   - Hover files over drop zone
   - Drop zone highlights
   - Release to upload

2. **Browse:**
   - Click "Browse Files" button
   - Select from file picker
   - Multiple selection allowed

**File Validation:**
- ✅ Only CSV files accepted
- ✅ Maximum 16MB per file
- ✅ Automatic old file deletion
- ❌ Non-CSV files rejected with error message

### 7.4 Mobile Responsiveness

**Features:**
- Automatic layout adjustment for small screens
- Touch-friendly buttons
- Scrollable timetables
- Optimized font sizes

**Tested Devices:**
- iPhone (iOS Safari)
- Android (Chrome)
- iPad (Safari)
- Desktop browsers (Chrome, Firefox, Edge, Safari)

---

## 8. Troubleshooting

### 8.1 Common Issues

#### Issue 1: Upload Server Not Connecting

**Symptoms:**
- Red banner: "Server Not Available"
- Upload button disabled

**Solutions:**

1. **Wait for Server Wake-up**
   - Render free tier sleeps after 15 min inactivity
   - First request takes 30-60 seconds
   - Refresh page after 1 minute

2. **Force Server Wake-up**
   - Visit: https://automated-timetable-iiit-dharwad.onrender.com/api/health
   - Wait for JSON response: `{"status": "healthy"}`
   - Return to upload page

3. **Check Server Status**
   - Visit Render dashboard
   - Verify service is "Live" not "Sleeping"

#### Issue 2: CSV File Rejected

**Symptoms:**
- Error message: "Please select CSV files only"
- File not added to list

**Solutions:**

1. **Verify File Extension**
   - Must be `.csv` not `.xlsx`, `.txt`, or `.xls`
   - Open in Excel → "Save As" → CSV (Comma delimited)

2. **Check File Size**
   - Maximum 16MB per file
   - Compress or split large files

3. **Verify File Format**
   - Must have required columns
   - No extra headers or footers
   - Proper encoding (UTF-8)

#### Issue 3: Timetable Generation Fails

**Symptoms:**
- Script crashes with error
- No output files generated

**Solutions:**

1. **Verify CSV Format**
   ```python
   # Check for required columns
   required = ['Course Code', 'Course Title', 'LTPSC', 
               'Semester', 'Classroom', 'Section', 'Electives']
   ```

2. **Check LTPSC Format**
   - Must be: `L-T-P-S-C` with numbers
   - Example: `3-1-0-0-4` ✅
   - Invalid: `3-1-0` ❌ or `3/1/0/0/4` ❌

3. **Verify Classroom Codes**
   - Must be non-empty strings
   - Example: `C101`, `L201`, `C004` ✅
   - Invalid: empty, NaN, or null ❌

4. **Check Python Version**
   ```bash
   python --version  # Should be 3.11+
   ```

#### Issue 4: Common Courses in Different Classrooms

**Symptoms:**
- Section A has CS165 in C004
- Section B has CS165 in C101

**Root Cause:**
- CSV has non-empty "Section" field for common course
- System treats it as section-specific

**Solution:**
- Ensure "Section" column is **completely empty** for common courses
- Not "COMMON", not "AB", just blank
- Re-run generator after fixing CSV

#### Issue 5: Netlify/Render Deployment Fails

**Solutions:**

1. **Netlify Issues:**
   - Ensure no `requirements.txt` in root (renamed to `requirements-backend.txt`)
   - Ensure no `runtime.txt` in root (renamed to `runtime-backend.txt`)
   - Check `netlify.toml` exists

2. **Render Issues:**
   - Verify `requirements-backend.txt` exists
   - Check Python version in `runtime-backend.txt`: `python-3.11.9`
   - Ensure `render.yaml` points to correct files

### 8.2 Performance Issues

#### Slow Timetable Generation

**Causes:**
- Large number of courses
- Complex elective baskets
- Many constraint conflicts

**Optimization:**
- Reduce elective basket complexity
- Ensure sufficient classrooms available
- Check for over-constrained schedules

#### Slow Web Page Loading

**Causes:**
- Large HTML files
- Many inline styles
- Server location (Render free tier)

**Solutions:**
- Enable browser caching
- Use CDN (already configured)
- Upgrade to Render paid tier for faster response

### 8.3 Error Messages Guide

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "No files provided" | Empty upload request | Select files before clicking upload |
| "Invalid file type" | Non-CSV file uploaded | Convert to CSV format |
| "File size too large" | File > 16MB | Split or compress file |
| "Server error 500" | Backend crash | Check backend logs on Render |
| "CORS error" | Frontend-backend mismatch | Verify Netlify domain in CORS config |
| "No valid CSV files" | All files rejected | Check file format and extension |

---

## 9. FAQ's

### General Questions

**Q1: Who can use this system?**

A: The system is designed for:
- Academic administrators
- Timetable coordinators
- Department heads
- Faculty members
- Students (view-only)

**Q2: Is an account required to view timetables?**

A: No, the web application is publicly accessible. No login or registration required.

**Q3: Can I download timetables?**

A: Yes, Excel files (.xlsx) are available in the `timetable_outputs/` folder. HTML timetables can be printed via browser print function (Ctrl+P).

**Q4: How often are timetables updated?**

A: Timetables are updated whenever:
- New CSV files are uploaded
- Generator is run locally
- Changes are pushed to GitHub (auto-deploys to Netlify)

**Q5: Is the system compatible with mobile devices?**

A: Yes, the web interface is fully responsive and works on:
- Smartphones (iOS/Android)
- Tablets
- Desktop computers
- All modern browsers

### Technical Questions

**Q6: What programming language is used?**

A: 
- **Backend:** Python 3.11
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Server:** Flask + Gunicorn

**Q7: Can I run this offline?**

A: Partially:
- Timetable generation: ✅ Can run locally offline
- Web viewing: ❌ Requires internet connection
- File upload: ❌ Requires backend server

**Q8: How do I backup my data?**

A:
- CSV files: Keep copies in separate folder
- Generated timetables: Download Excel files
- Code repository: Fork on GitHub

**Q9: Can I customize time slots?**

A: Yes, edit the time slots in `main.py`:
```python
self.time_slots = {
    'morning': ['08:00-09:30', '09:30-11:00', '11:30-13:00'],
    'afternoon': ['14:00-16:00', '16:00-18:00']
}
```

**Q10: How do I add a new department?**

A: 
1. Create new CSV file: `Even [DEPT].csv`
2. Place in `input_files/sdtt_inputs/`
3. Run generator - auto-detects new department
4. HTML files generated automatically

### Troubleshooting Questions

**Q11: Why is the upload server not responding?**

A: Render free tier spins down after 15 min inactivity. First request wakes it up (30-60 sec delay). Visit `/api/health` endpoint to wake server.

**Q12: Why do common courses appear in different rooms?**

A: Check CSV file - "Section" column must be completely empty (not "COMMON" or "AB"). System uses empty section field to identify common courses.

**Q13: What if two instructors have overlapping schedules?**

A: System prevents this automatically. If conflict detected:
- Error message shown
- Timetable generation paused
- Review CSV for instructor assignments

**Q14: Can I schedule Saturday classes?**

A: Yes, modify `self.days` in `main.py`:
```python
self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
```

**Q15: How do I report bugs?**

A: 
- GitHub Issues: https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad/issues
- Email: [Contact administrator]
- Include error messages and steps to reproduce

### Data Management Questions

**Q16: What happens when I upload new files?**

A: 
1. Old CSV files automatically deleted
2. New files uploaded to backend
3. Confirmation message shown
4. Manual timetable regeneration required

**Q17: Can I undo an upload?**

A: No automatic undo. Keep local backups of CSV files. Re-upload previous version if needed.

**Q18: How many files can I upload at once?**

A: Unlimited, but recommended:
- Upload 3 files (CSE, DSAI, ECE) simultaneously
- Maximum 16MB per file
- CSV format only

**Q19: Are uploads secure?**

A: Yes:
- HTTPS encrypted connection
- Secure filename handling
- File type validation
- Size limits enforced

**Q20: Where are uploaded files stored?**

A: 
- **Backend:** Render ephemeral storage (resets on redeploy)
- **Recommendation:** Keep local copies as backup
- **Production:** Consider cloud storage integration

---

## 10. Technical Specifications

### 10.1 System Requirements

**Minimum Requirements:**

| Component | Specification |
|-----------|---------------|
| OS | Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+) |
| Python | 3.11 or higher |
| RAM | 4 GB |
| Storage | 500 MB free space |
| Internet | Required for web features |
| Browser | Chrome 90+, Firefox 88+, Edge 90+, Safari 14+ |

**Recommended Requirements:**

| Component | Specification |
|-----------|---------------|
| OS | Windows 11, macOS 13+, Ubuntu 22.04+ |
| Python | 3.11.9 |
| RAM | 8 GB |
| Storage | 1 GB free space |
| Internet | Broadband (10 Mbps+) |
| Browser | Latest version of Chrome/Firefox |

### 10.2 Performance Metrics

**Timetable Generation:**
- 12 timetables: 30-60 seconds
- Average processing time: 5 seconds per timetable
- Memory usage: ~200 MB peak

**Web Performance:**
- Page load time: 1-2 seconds (first visit)
- Upload speed: Depends on internet connection
- Server response: <500ms (after wake-up)

**Scalability:**
- Supports: Up to 100 courses per department
- Classrooms: Up to 50 rooms
- Concurrent users: Unlimited (static frontend)

### 10.3 API Endpoints

**Backend API (https://automated-timetable-iiit-dharwad.onrender.com/):**

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/api/health` | GET | Check server status | `{"status": "healthy"}` |
| `/api/upload` | POST | Upload CSV files | `{"success": true, "files": [...]}` |
| `/api/list-files` | GET | List uploaded files | `{"files": [...]}` |
| `/api/delete-file` | DELETE | Delete specific file | `{"success": true}` |
| `/api/regenerate` | POST | Trigger timetable regen* | `{"success": true}` |

*Note: Regenerate endpoint requires pandas/numpy (not currently installed on Render)

### 10.4 File Formats

**Input Formats:**
- CSV (Comma Separated Values)
- Encoding: UTF-8
- Line endings: LF or CRLF

**Output Formats:**
- Excel (.xlsx) - OpenXML format
- HTML5 - Responsive web pages
- JSON (API responses)

### 10.5 Browser Compatibility

| Browser | Minimum Version | Status |
|---------|-----------------|--------|
| Chrome | 90+ | ✅ Fully supported |
| Firefox | 88+ | ✅ Fully supported |
| Edge | 90+ | ✅ Fully supported |
| Safari | 14+ | ✅ Fully supported |
| IE 11 | - | ❌ Not supported |

### 10.6 Security Features

**Frontend:**
- HTTPS encryption (Netlify SSL)
- Content Security Policy headers
- XSS protection enabled

**Backend:**
- CORS configured (whitelist only)
- Secure filename handling
- File type validation
- Size limit enforcement

**Data Privacy:**
- No user tracking
- No cookies required
- No personal data collection

---

## 11. Support & Contact

### 11.1 Getting Help

**Documentation:**
- User Manual: This document
- README.md: Quick start guide
- QUICK_START.md: Step-by-step setup
- HTML_VIEWER_README.md: Web interface guide

**Online Resources:**
- **GitHub Repository:** https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad
- **Live Demo:** https://beyondgamesclasssync.netlify.app/
- **Backend API:** https://automated-timetable-iiit-dharwad.onrender.com/

### 11.2 Reporting Issues

**GitHub Issues:**
1. Visit: https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad/issues
2. Click "New Issue"
3. Provide:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Error messages
   - System information

**Issue Template:**
```
**Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Screenshots:**
[Attach if relevant]

**Environment:**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.11.9]
- Browser: [e.g., Chrome 120]
```

### 11.3 Contributing

**How to Contribute:**

1. **Fork Repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR-USERNAME/Automated-TimeTable-IIIT-Dharwad.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow existing code style
   - Add comments
   - Test thoroughly

4. **Commit Changes**
   ```bash
   git commit -m "Add: description of changes"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### 11.4 Credits

**Development Team:**
- BeyondGames Team
- IIIT Dharwad

**Technologies Used:**
- Python, Flask, Pandas
- HTML, CSS, JavaScript
- Netlify, Render
- GitHub

**Special Thanks:**
- Faculty advisors
- Beta testers
- Open source community

### 11.5 License

**License Information:**
- Project is open source
- Check LICENSE file in repository
- Free for educational use

### 11.6 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | Nov 2025 | Web application, upload feature, auto-deploy |
| 1.5.0 | Oct 2025 | Tutorial visualization, common course fix |
| 1.0.0 | Sep 2025 | Initial release, CSV-based generator |

---

## Appendix

### A. Glossary

- **LTPSC:** Lecture-Tutorial-Practical-Self study-Credits
- **Common Course:** Course attended by multiple sections together
- **Elective Basket:** Group of elective courses scheduled together
- **Section:** Sub-division of students (typically A and B)
- **Tutorial:** 60-minute practice session
- **Lab/Practical:** 2-hour hands-on session
- **CORS:** Cross-Origin Resource Sharing (security feature)
- **API:** Application Programming Interface
- **CSV:** Comma Separated Values (file format)

### B. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+P | Print current page |
| Ctrl+F | Find text on page |
| F5 | Refresh page |
| Ctrl+- | Zoom out |
| Ctrl++ | Zoom in |
| Ctrl+0 | Reset zoom |

### C. Color Coding Legend

Timetables use unique colors for each course:
- Generated automatically by hash function
- Same course = same color across all cells
- Lighter shade for fractional tutorials
- High contrast for readability

### D. Quick Reference Commands

```bash
# Generate timetables
python main.py

# Start local upload server
python upload_server.py

# Convert to HTML
python timetable_to_html.py

# Check Python version
python --version

# Install dependencies
pip install pandas openpyxl
```

### E. Useful Links

- **Netlify Docs:** https://docs.netlify.com/
- **Render Docs:** https://render.com/docs
- **Flask Docs:** https://flask.palletsprojects.com/
- **Pandas Docs:** https://pandas.pydata.org/docs/

---

## Document Information

**Document Title:** Automated Timetable Generator - User Manual  
**Version:** 2.0.0  
**Date:** November 5, 2025  
**Author:** BeyondGames Team  
**Contact:** [GitHub Repository](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad)  
**Last Updated:** November 5, 2025  
**Status:** Current  

---

**End of User Manual**

© 2025 BeyondGames Team - IIIT Dharwad. All rights reserved.
