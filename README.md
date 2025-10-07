<div align="center"># 🎓 BeyondGames Automated Timetable Generator



# 🎓 Automated Timetable Generator[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](htTotal Files:

### *Smart Academic Scheduling for IIIT Dharwad*- 3 Input CSV files (course data)

- 18 Output CSV files (timetables)

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)- 18 Output TXT files (elective details)

[![Pandas](https://img.shields.io/badge/pandas-2.0+-150458.svg)](https://pandas.pydata.org/)- 19 Output HTML files (1 index + 18 timetables)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)- 2 Python scripts (main.py, timetable_to_html.py)

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()- 3 Documentation files (README.md, CONSTRAINTS_ANALYSIS.md, TECH_STACK.md)

[![GitHub](https://img.shields.io/badge/BeyondGames-Team-purple.svg)](https://github.com/BeyondGamesTimeTable)```g.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Status: Working](https://img.shields.io/badge/Status-Working-brightgreen.svg)]()

**[Features](#-key-features)** • **[Quick Start](#-quick-start)** • **[Documentation](#-documentation)** • **[Demo](#-screenshots)** • **[Contributing](#-contributing)**[![BeyondGames Team](https://img.shields.io/badge/Team-BeyondGames-purple.svg)](https://github.com/BeyondGamesTimeTable)



---## 📖 Project Overview



</div>**Developed by BeyondGames Team** - A **CSV-based Timetable Generation System** that creates optimized academic schedules for **IIIT Dharwad**. The system reads course data from CSV files to generate conflict-free timetables for multiple semesters and sections.



## 📋 Table of Contents### 🎯 Problem Statement

Manual timetable creation involves complex constraints:

- [Overview](#-overview)- Faculty availability conflicts

- [Problem & Solution](#-problem--solution)- Classroom and lab resource allocation

- [Key Features](#-key-features)- LTPSC (Lecture-Tutorial-Practical-Self study-Credits) requirements

- [Quick Start](#-quick-start)- Multi-section course scheduling

- [Project Structure](#-project-structure)- Lunch break management

- [Configuration](#-configuration)

- [Technical Architecture](#-technical-architecture)### 💡 Solution

- [Output Examples](#-output-examples)This automated system generates optimized weekly schedules by:

- [Screenshots](#-screenshots)- Processing CSV input files with course data

- [Performance](#-performance)- Applying constraint-based scheduling algorithms

- [Documentation](#-documentation)- Creating separate timetables for different sections

- [Contributing](#-contributing)- Exporting results to CSV files and interactive HTML viewers

- [License](#-license)

---

---

## ✨ Current Features

## 🌟 Overview

### 🔧 **Core Functionality**

<div align="center">- ✅ **CSV Data Processing** – Reads course data from CSV files (Even CSE.csv, Even DSAI.csv, Even ECE.csv)

- ✅ **Multi-Section Support** – Generates separate schedules for Section A and Section B

**A constraint-based timetable generation system that automatically creates optimized academic schedules**- ✅ **LTPSC Parsing** – Handles Lecture-Tutorial-Practical format from CSV columns

- ✅ **Conflict Prevention** – Avoids scheduling conflicts for rooms and time slots

Developed by **BeyondGames Team** for **IIIT Dharwad**- ✅ **Lunch Break Management** – Automatically reserves 13:00-14:30 for lunch

- ✅ **CSV Output** – Exports generated timetables to CSV format

</div>- ✅ **HTML Visualization** – Creates interactive HTML timetable views



This system reads course data from CSV files and generates **18 conflict-free timetables** across:### 📊 **Scheduling Rules**

- 🏛️ **3 Departments**: CSE, DSAI, ECE- ✅ **Lectures** – 1.5-hour sessions, common for both sections

- 📚 **3 Semesters**: 2, 4, 6- ✅ **Tutorials** – 1-hour sessions, section-specific (marked as T-A, T-B)

- 👥 **2 Sections**: A, B- ✅ **Labs/Practicals** – 2-hour sessions, section-specific (marked as P-A, P-B)

- ✅ **Time Constraints** – 5-day week (Mon-Fri), 7 time slots per day (8 AM - 8 PM)

### 🎯 What Makes It Special?- ✅ **Room Assignment** – Default room allocation by type (lecture halls, labs, tutorial rooms)



| Feature | Description |### 📁 **File Management**

|---------|-------------|- ✅ **Directory Setup** – Auto-creates input and output directories

| 🚀 **Fast** | Generates all 18 timetables in ~30 seconds |- ✅ **CSV Export** – Clean CSV files for easy data import

| 🎨 **Visual** | Beautiful HTML viewer with interactive navigation |- ✅ **HTML Generation** – Beautiful interactive web-based viewer

| 🔄 **Flexible** | Two implementations: OOP and Functional |

| ✅ **Reliable** | 91.7% constraint satisfaction, 100% conflict-free |---

| 📦 **Simple** | Zero dependencies except pandas |

## 🚀 Quick Start

---

### 📋 Prerequisites

## 🎯 Problem & Solution- **Python 3.12+**

- **Required packages**: `pandas`

<table>

<tr>### 📥 Installation & Setup

<td width="50%">

1. **Clone the repository**

### 🔴 The Problem   ```bash

   git clone https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad.git

Manual timetable creation faces several challenges:   cd Automated-TimeTable-IIIT-Dharwad/timetable_generator

   ```

- ⚠️ **Scheduling Conflicts**  

  Faculty and classroom double-bookings2. **Install dependencies**

     ```bash

- 🏢 **Resource Management**     pip install pandas

  Limited lecture halls, labs, and tutorial rooms   ```

  

- 📊 **Complex Constraints**  3. **Prepare input files**

  LTPSC requirements, section management   - Place the required CSV files (`Even CSE.csv`, `Even DSAI.csv`, `Even ECE.csv`) in `timetable_generator/input_files/sdtt_inputs/`

  

- ⏰ **Time-Consuming**  ### 🏃‍♂️ Running the Application

  Hours of manual work prone to errors

#### **Step 1: Generate Timetables**

</td>```bash

<td width="50%"># Navigate to the timetable generator directory

cd timetable_generator

### ✅ Our Solution

# Run the main script to generate CSV timetables

Automated constraint-based scheduling:# Choose ONE of the following (both produce identical outputs):

python main.py                # Class-based OOP approach

- 🤖 **Automated Generation**  # OR

  Processes CSV input, applies algorithmspython main_functional.py     # Functional programming approach

  ```

- 🛡️ **Conflict Prevention**  

  Built-in detection and resolution#### **Step 2: Generate HTML Viewer** (Optional)

  ```bash

- 🎓 **Smart Allocation**  # Convert CSV files to interactive HTML format

  Optimizes rooms and time slotspython timetable_to_html.py

  ```

- ⚡ **Lightning Fast**  

  30 seconds for all timetables#### **Step 3: View Results**

```bash

</td># Open HTML viewer in browser

</tr>start timetable_html\index.html

</table># OR manually navigate to timetable_outputs/ for CSV files

```

---

### 📊 Required Input Files

## ✨ Key Features

The system expects the following CSV files in the input directory:

### 🔧 Core Functionality

| File Name | Description | Required Columns |

<table>|-----------|-------------|------------------|

<tr>| `Even CSE.csv` | CSE course information | Course Code, Course Title, Lectures, Tutorials, Practicals, Classroom, Section, Electives |

<td width="33%">| `Even DSAI.csv` | DSAI course information | Course Code, Course Title, Lectures, Tutorials, Practicals, Classroom, Section, Electives |

| `Even ECE.csv` | ECE course information | Course Code, Course Title, Lectures, Tutorials, Practicals, Classroom, Section, Electives |

#### 📊 Data Processing

- CSV-based input system### 📤 Output Files

- Multi-department support

- LTPSC parsingThe system generates two types of output files:

- Elective basket management

#### **CSV Files** (Primary Output)

</td>**Location**: `timetable_generator/timetable_outputs/`

<td width="33%">- 18 CSV files for all department-semester-section combinations

- Easy to import into Excel, Google Sheets, or databases

#### 🗓️ Scheduling- Examples: `CSE_Sem2_SectionA_Timetable.csv`, `DSAI_Sem4_SectionB_Timetable.csv`

- Constraint-based algorithm

- Conflict detection#### **HTML Files** (Interactive Viewer)

- Room optimization**Location**: `timetable_generator/timetable_html/`

- Lunch break management- `index.html` - Main navigation page

- 18 HTML timetable files with beautiful styling

</td>- Interactive web-based viewer for easy sharing and viewing

<td width="33%">

#### **How to View Results:**

#### 📤 Output Formats1. **CSV Files**: Open in Excel or any spreadsheet application

- CSV timetables (18 files)2. **HTML Files**: Open `timetable_html/index.html` in your browser

- TXT elective details (16 files)

- Interactive HTML viewer (19 files)---

- Beautiful web interface

## 📁 Project Structure

</td>

</tr>```

</table>Automated-TimeTable-IIIT-Dharwad/

├── .gitignore                       # Git ignore file

### 💡 Implementation Options├── README.md                        # Main project documentation

├── CONSTRAINTS_ANALYSIS.md          # Detailed requirements analysis (91.7% compliance)

> **Choose your preferred coding style!**├── TECH_STACK.md                    # Technology stack documentation

│

<table>├── .vscode/                         # VS Code configuration

<tr>│   ├── launch.json

<th>🏛️ Object-Oriented (main.py)</th>│   ├── settings.json

<th>🔄 Functional (main_functional.py)</th>│   └── tasks.json

</tr>│

<tr>├── screenshots/                     # Screenshots for README

<td>│   ├── timetable_csv_view.png       # CSV timetable screenshot

│   ├── timetable_html_view1.png     # HTML viewer screenshot 1

```python│   └── timetable_html_view2.png     # HTML viewer screenshot 2

# Class-based approach│

generator = TimetableGenerator()└── timetable_generator/             # Main application directory

result = generator.generate_timetable('CSE', 2, 'A')    ├── main.py                      # Core timetable generation engine (Class-based)

```    ├── main_functional.py           # Core timetable generation engine (Functional)

    ├── timetable_to_html.py         # HTML converter and viewer generator

</td>    │

<td>    ├── input_files/                 # Input data directory

    │   └── sdtt_inputs/             # CSV input files

```python    │       ├── Even CSE.csv         # CSE course data (Sem 2, 4, 6)

# Functional approach    │       ├── Even DSAI.csv        # DSAI course data (Sem 2, 4, 6)

result = generate_timetable('CSE', 2, 'A')    │       └── Even ECE.csv         # ECE course data (Sem 2, 4, 6)

```    │

    ├── timetable_outputs/           # Generated CSV timetables

</td>    │   ├── CSE_Sem2_SectionA_Timetable.csv

</tr>    │   ├── CSE_Sem2_SectionA_Timetable_Electives.txt

<tr>    │   ├── CSE_Sem2_SectionB_Timetable.csv

<td>✅ Encapsulation<br>✅ State management<br>✅ OOP design patterns</td>    │   ├── CSE_Sem2_SectionB_Timetable_Electives.txt

<td>✅ Explicit data flow<br>✅ Pure functions<br>✅ Easier testing</td>    │   ├── ... (18 CSV files + 18 TXT elective files)

</tr>    │   └── ECE_Sem6_SectionB_Timetable_Electives.txt

<tr>    │

<td colspan="2" align="center"><strong>Both produce 100% identical outputs!</strong></td>    └── timetable_html/              # Generated HTML viewers

</tr>        ├── index.html               # Main navigation page

</table>        ├── CSE_Sem2_SectionA_Timetable.html

        ├── CSE_Sem2_SectionB_Timetable.html

### 📋 Scheduling Rules        ├── ... (18 HTML timetable files)

        └── ECE_Sem6_SectionB_Timetable.html

| Type | Duration | Constraint | Marking |

|------|----------|------------|---------|Total Files:

| **Lectures** | 1.5 hours | Max 1 per day | Common for both sections |- 3 Input CSV files (course data)

| **Tutorials** | 1 hour | Max 1 per day | Section-specific (T-A, T-B) |- 18 Output CSV files (timetables)

| **Labs** | 2 hours | Max 1 per day | Section-specific (Lab-A, Lab-B) |- 16 Output TXT files (elective details)

| **Electives** | Varies | Max 1 per day | Basket-based (E1, B3, etc.) |- 19 Output HTML files (1 index + 18 timetables)

- 3 Python scripts (main.py, main_functional.py, timetable_to_html.py)

---- 3 Documentation files (README.md, CONSTRAINTS_ANALYSIS.md, TECH_STACK.md)

```

## 🚀 Quick Start

---

### 📋 Prerequisitesn

## ⚙️ Configuration

```bash

Python 3.12 or higher### 🕒 Time Slots (Built-in)

pandas library```

```08:00-09:30  Early Morning Slot

09:45-11:15  Morning Slot

### 📥 Installation11:30-13:00  Late Morning Slot

13:00-14:30  🍽️ LUNCH BREAK

```bash14:45-16:15  Afternoon Slot

# 1. Clone the repository16:30-18:00  Late Afternoon Slot

git clone https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad.git18:15-19:45  Evening Slot

cd Automated-TimeTable-IIIT-Dharwad/timetable_generator```



# 2. Install dependencies### 🎯 Target Semesters

pip install pandas- **Even Semesters**: 2, 4, 6

- **Departments**: CSE, DSAI, ECE

# 3. Verify input files exist- **Sections**: A, B

ls input_files/sdtt_inputs/

# Should show: Even CSE.csv, Even DSAI.csv, Even ECE.csv### 🏛️ Room Assignments (Auto-allocated)

```- **Large Auditorium**: C004 (240-seater for common courses)

- **Lecture Halls**: C302, C303, C304, C305

### 🏃‍♂️ Usage- **Tutorial Rooms**: C002, C202, C203, C204

- **Lab Rooms**: Lab-1 (auto-assigned for practicals)

#### Option A: Class-Based (OOP)

```bash---

python main.py

```## 🔧 Technical Details



#### Option B: Functional### 🏗️ Architecture

```bash- **Dual Implementation**: Two versions available - Class-based (main.py) and Functional (main_functional.py)

python main_functional.py  - Both produce 100% identical outputs - choose based on your coding style preference

```- **CSV Integration**: Native CSV file reading and writing using pandas

- **Constraint-Based Scheduling**: Implements scheduling algorithms with conflict detection

#### Generate HTML Viewer- **Dual Output**: Generates both CSV files for data processing and HTML for viewing

```bash

python timetable_to_html.py### 🔄 Scheduling Algorithm

1. **Data Loading**: Parse CSV files and extract course information with LTPSC details

# Open in browser2. **Schedule Initialization**: Create empty time slot grid (7 slots) with lunch breaks

start timetable_html/index.html  # Windows3. **Common Course Scheduling**: Assign lectures common for both sections (large auditorium)

# or4. **Section-Specific Scheduling**: Assign tutorials and labs for individual sections

open timetable_html/index.html   # macOS/Linux5. **Lab Scheduling**: Assign 2-hour consecutive lab sessions with proper room allocation

```6. **Conflict Resolution**: Ensure no room/time conflicts and proper scheduling constraints



### 📊 Input Files### 🎲 Randomization

- Uses randomized slot assignment to generate varied timetables

Place your CSV files in `timetable_generator/input_files/sdtt_inputs/`- Prevents predictable patterns while maintaining constraints



**Required Columns:**### 📚 Technology Stack

- `Course Code` - Unique identifier (e.g., CS101)For complete details about the technologies, libraries, and frameworks used in this project, see **[TECH_STACK.md](TECH_STACK.md)**

- `Course Title` - Course name

- `Lectures` - Number of lecture sessions per week**Quick Summary**:

- `Tutorials` - Number of tutorial sessions per week- **Language**: Python 3.12+

- `Practicals` - Number of lab sessions per week- **Core Library**: pandas (data processing)

- `Classroom` - Assigned room- **Frontend**: HTML5 + CSS3 (no JavaScript)

- `Section` - Section identifier (2A, 4B, etc.)- **Data Formats**: CSV (input/output), TXT (electives), HTML (viewer)

- `Electives` - Type: F (Foundation), T (Type Elective)- **Architecture**: OOP with constraint-based scheduling algorithms

- `Basket` - Elective basket number (B1, B2, etc.)

---

### 📤 Output Structure

## 📊 Sample Output

```

timetable_outputs/          # CSV timetables```

├── CSE_Sem2_SectionA_Timetable.csv🎓 BeyondGames Enhanced Timetable Generator

├── CSE_Sem2_SectionA_Timetable_Electives.txt================================================================================

├── ... (34 total files)Generating timetables from CSV files...

================================================================================

timetable_html/             # Interactive viewer

├── index.html              # Navigation page📚 Total courses to schedule:

├── CSE_Sem2_SectionA_Timetable.html   Common courses: 5

├── ... (19 total files)   Section-specific courses: 8

```

✅ All courses scheduled successfully!

---

                     08:00-09:30            09:45-11:15  ...        18:15-19:45

## 📁 Project StructureMonday     CS162 (Common) | C004  CS164 (Common) | C004  ...  CS163 (Common) | C004

Tuesday    CS164 (Common) | C004  CS163 (Common) | C004  ...         CS152-A | C002

```Wednesday  CS164-Lab (Common) | Lab-1                    ...  DS164-Lab (Common) | Lab-1

Automated-TimeTable-IIIT-Dharwad/...

│

├── 📄 README.md                        ← You are here✅ Timetable saved: timetable_outputs\CSE_Sem2_SectionA_Timetable.csv

├── 📄 CONSTRAINTS_ANALYSIS.md          ← Requirements analysis (91.7%)

├── 📄 TECH_STACK.md                    ← Technology documentation✅ All timetables generated successfully!

├── 📄 PRESENTATION_SCRIPT.md           ← Demo script📁 CSV Output location: timetable_outputs/

├── 📄 QUICK_REFERENCE.md               ← Command reference📁 HTML Output location: timetable_html/

├── 📄 TEST_RUN_CHECKLIST.md            ← Pre-recording tests```

│

├── 📸 screenshots/---

│   ├── timetable_csv_view.png

│   ├── timetable_html_view1.png## ✨ Latest System Features (v2.0)

│   └── timetable_html_view2.png

│### 🚀 **Recent Updates**

└── 📂 timetable_generator/- ✅ **Migrated to CSV-based system** - Simplified architecture, faster processing

    │- ✅ **Streamlined codebase** - Removed Excel dependencies, cleaner structure  

    ├── 🐍 main.py                      ← Class-based generator (529 lines)- ✅ **Enhanced HTML viewer** - Beautiful interactive timetable display

    ├── 🐍 main_functional.py           ← Functional generator (699 lines)- ✅ **Extended time slots** - 7 slots (8 AM - 8 PM) for better scheduling

    ├── 🐍 timetable_to_html.py         ← HTML converter (785 lines)- ✅ **Improved documentation** - Comprehensive guides and verification reports

    │

    ├── 📂 input_files/### 📊 **Performance Metrics**

    │   └── sdtt_inputs/- **Generation Speed**: ~30 seconds for all 18 timetables

    │       ├── Even CSE.csv            ← Course data- **File Size**: CSV files are 90% smaller than Excel equivalents

    │       ├── Even DSAI.csv- **Scheduling Success**: ~85% success rate (due to heavy course load)

    │       └── Even ECE.csv- **Conflict Resolution**: 100% room/time conflict prevention

    │

    ├── 📂 timetable_outputs/           ← Generated CSV files### 🔧 **System Reliability**

    │   ├── *.csv (18 files)- ✅ **Fully tested** - All components verified working

    │   └── *_Electives.txt (16 files)- ✅ **Clean architecture** - Legacy code removed

    │- ✅ **Error handling** - Proper warnings for scheduling conflicts

    └── 📂 timetable_html/              ← Generated HTML files- ✅ **Documentation** - Updated README files and guides

        ├── index.html                  ← Navigation page

        └── *.html (18 timetables)---

```

## 📸 Screenshots

<details>

<summary><b>📊 File Statistics</b></summary>### Timetable Output Examples



| Category | Count | Description |#### CSV Timetable View

|----------|-------|-------------|![CSV Timetable](screenshots/timetable_csv_view.png)

| **Input** | 3 | CSV course data files |

| **Output CSV** | 18 | Generated timetable files |

| **Output TXT** | 16 | Elective details files |#### HTML Interactive Viewer

| **Output HTML** | 19 | Interactive viewer files |![HTML Timetable Viewer](screenshots/timetable_html_view1.png)

| **Python Scripts** | 3 | Generator and converter |![HTML Timetable Viewer](screenshots/timetable_html_view2.png)

| **Documentation** | 6 | README and guides |

---

</details>

## 🤝 Contributing

---

1. Fork the repository

## ⚙️ Configuration2. Create a feature branch (`git checkout -b feature/new-feature`)

3. Commit your changes (`git commit -am 'Add new feature'`)

### 🕒 Time Slots4. Push to the branch (`git push origin feature/new-feature`)

5. Create a Pull Request

<table>

<tr>### 👨‍💻 Development Team

<th>Time</th>- **BeyondGames Team** - *Original developers and maintainers*

<th>Slot</th>

<th>Duration</th>---

</tr>

<tr><td>08:00 - 09:30</td><td>🌅 Early Morning</td><td>1.5 hours</td></tr>## 📄 License

<tr><td>09:45 - 11:15</td><td>☀️ Morning</td><td>1.5 hours</td></tr>

<tr><td>11:30 - 13:00</td><td>🌤️ Late Morning</td><td>1.5 hours</td></tr>This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<tr style="background-color: #fff3cd;"><td>13:00 - 14:30</td><td>🍽️ <strong>LUNCH BREAK</strong></td><td>1.5 hours</td></tr>

<tr><td>14:45 - 16:15</td><td>🌤️ Afternoon</td><td>1.5 hours</td></tr>---

<tr><td>16:30 - 18:00</td><td>🌥️ Late Afternoon</td><td>1.5 hours</td></tr>

<tr><td>18:15 - 19:45</td><td>🌆 Evening</td><td>1.5 hours</td></tr>## 👥 Authors

</table>

- **BeyondGames Team** - *Original development and implementation*

### 🎯 Coverage- **IIIT Dharwad** - *Problem requirements and academic support*

- **Contributors** - See [contributors](https://github.com/BeyondGamesTimeTable/BeyondGames_Implementation/contributors)

**Departments:** CSE • DSAI • ECE  

**Semesters:** 2 • 4 • 6  ---

**Sections:** A • B  

**Days:** Monday - Friday## 🙏 Acknowledgments



### 🏛️ Room Allocations- **BeyondGames Team** for the innovative solution design and implementation

- **IIIT Dharwad** for providing the problem requirements and academic guidance

| Type | Rooms | Capacity | Usage |- **Python community** for excellent libraries (pandas)

|------|-------|----------|-------|- **Contributors and testers** who helped improve the system

| **Large Auditorium** | C004 | 240 seats | Common courses |

| **Lecture Halls** | C302, C303, C304, C305 | Variable | Section lectures |### 🏆 Project Highlights

| **Tutorial Rooms** | C002, C202, C203, C204 | Small | Tutorial sessions |- ✨ **Original Implementation** by BeyondGames Team

| **Lab Rooms** | Lab-1, Lab-2, Lab-3, Lab-4, Lab-5 | 30-40 seats | Practical sessions |- 🎯 **Production Ready** solution for academic scheduling

- 📊 **CSV Integration** for seamless data management and processing

---- 🔄 **Constraint-Based Algorithm** for optimal scheduling

- 🚀 **Modernized Architecture** - Streamlined, efficient, and maintainable

## 🏗️ Technical Architecture- 🌐 **Dual Output Format** - CSV for data + HTML for presentation



### 🔄 System Flow---



```## 📞 Support

┌─────────────────┐

│  📄 CSV Input   │For questions or issues:

│  Files          │- 📧 Create an issue on [GitHub](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad/issues)

└────────┬────────┘- 📚 Check the comprehensive documentation files:

         │  - [README.md](README.md) - Main documentation

         ▼  - [CONSTRAINTS_ANALYSIS.md](CONSTRAINTS_ANALYSIS.md) - Requirements analysis

┌─────────────────┐  - [TECH_STACK.md](TECH_STACK.md) - Technology stack details

│  🤖 Choose      │- 🔍 Review the example input files in `input_files/sdtt_inputs/` directory

│  Generator      │

├─────────────────┤

│ • main.py (OOP) │
│ • main_func.py  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  📊 CSV         │
│  Timetables     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  🎨 HTML        │
│  Converter      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  🌐 Interactive │
│  Viewer         │
└─────────────────┘
```

### 🧠 Scheduling Algorithm

1. **📥 Data Loading** - Parse CSV files with course information
2. **🔧 Initialization** - Create empty time slot grid (5 days × 7 slots)
3. **🎓 Common Courses** - Schedule foundation courses for both sections
4. **👥 Section Courses** - Assign section-specific lectures and tutorials
5. **🔬 Lab Sessions** - Allocate 2-hour consecutive lab slots
6. **✅ Validation** - Ensure no conflicts, verify constraints

### 📚 Technology Stack

<div align="center">

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.12+ | Core development |
| **Data Processing** | pandas | CSV operations, DataFrames |
| **Frontend** | HTML5 + CSS3 | Interactive viewer |
| **Design** | OOP + Functional | Dual implementation |
| **Algorithm** | Constraint-based | Optimal scheduling |

</div>

<details>
<summary><b>🔍 View Detailed Tech Stack</b></summary>

See **[TECH_STACK.md](TECH_STACK.md)** for comprehensive technology documentation including:
- Libraries and versions
- Design patterns used
- Architecture decisions
- Performance optimizations
- System components flow

</details>

---

## 📊 Output Examples

### 💻 Console Output

```
🎓 BeyondGames Enhanced Timetable Generator
================================================================================
Generating timetables from CSV files...
================================================================================

📚 Total courses to schedule:
   Common courses: 5
   Section-specific courses: 8

   Scheduling: CS162 - L:3 T:1 P:0
   Scheduling: CS164 - L:3 T:0 P:2
   Scheduling: ELECTIVE_E1 - L:3 T:1 P:0

✅ All courses scheduled successfully!

                  08:00-09:30            09:45-11:15  ...     18:15-19:45
Monday     CS162 (Common) | C004  CS164 (Common) | C004  ...  CS163 (Common) | C004
Tuesday    CS164 (Common) | C004  CS163 (Common) | C004  ...  CS152-A | C002
...

✅ Timetable saved: timetable_outputs\CSE_Sem2_SectionA_Timetable.csv
✅ All timetables generated successfully!

📁 CSV Output location: timetable_outputs/
📁 HTML Output location: timetable_html/
```

### 📄 CSV Timetable Format

```csv
,08:00-09:30,09:45-11:15,11:30-13:00,13:00-14:30,14:45-16:15,16:30-18:00,18:15-19:45
Monday,MA163-A | C202,CS163-A | C202,CS163-Lab-A | Lab-1,LUNCH BREAK,CS163-Lab-A (cont.) | Lab-1,Elective (E1),CS165-A | C202
Tuesday,MA163-A | C202,CS163-A | C202,CS163-Lab-A | Lab-1,LUNCH BREAK,CS163-Lab-A (cont.) | Lab-1,Elective (E1),CS165-A | C202
Wednesday,MA163-A | C202,CS163-A | C202,Elective (E1),LUNCH BREAK,CS165-A | C202,Elective (B3),Elective (B4)
Thursday,MA163-T-A | C202,Elective (E1),Elective (B3),LUNCH BREAK,Elective (B4),Free,Free
Friday,Elective (B3),Elective (B4),Free,LUNCH BREAK,Free,Free,Free
```

### 📝 Electives TXT Format

```
================================================================================
ELECTIVE COURSES - Choose ONE from each basket
================================================================================

Basket B3:
----------------------------------------
  • CS152: Data Science with Python
    Classroom: C002
  • EC154: Introduction to Digital VLSI Design
    Classroom: C203
  • HS155: Industry Insights Program Part 1
    Classroom: nan

Basket B4:
----------------------------------------
  • MA152: Probability and Statistics
    Classroom: C203
  • CS151: Introduction to Electronics
    Classroom: C002
```

---

## 📸 Screenshots

### 📊 CSV Timetable View
<div align="center">

![CSV Timetable](screenshots/timetable_csv_view.png)

*Clean, spreadsheet-compatible timetable format*

</div>

### 🌐 HTML Interactive Viewer
<div align="center">

![HTML Viewer 1](screenshots/timetable_html_view1.png)

*Beautiful, color-coded timetable grid with easy navigation*

![HTML Viewer 2](screenshots/timetable_html_view2.png)

*Detailed elective information below each timetable*

</div>

---

## ⚡ Performance

<div align="center">

### 📈 System Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| **Generation Speed** | ~30 seconds | All 18 timetables |
| **File Size** | 90% smaller | vs Excel format |
| **Success Rate** | ~85% | Course scheduling |
| **Conflict Prevention** | 100% | Room/time conflicts |
| **Constraint Satisfaction** | 91.7% | 11/12 requirements |
| **Code Quality** | High | Clean, documented |

</div>

### 🎯 Constraint Compliance

<table>
<tr>
<th>✅ Satisfied (11/12)</th>
<th>⚠️ Partial (1/12)</th>
</tr>
<tr>
<td valign="top">

- Conflict-free scheduling
- Lunch break management
- Max 1 lecture/day per course
- Max 1 tutorial/day per course
- No lecture+tutorial same day
- Proper room allocation
- Section-specific marking
- Elective basket handling
- CSV/HTML output
- Time slot management
- 5-day week constraint

</td>
<td valign="top">

- Lab duration (uses 3 hours instead of ideal 2 hours due to fixed time slot sizes)
- Marked for future enhancement

</td>
</tr>
</table>

<details>
<summary><b>📊 View Detailed Constraint Analysis</b></summary>

See **[CONSTRAINTS_ANALYSIS.md](CONSTRAINTS_ANALYSIS.md)** for:
- Detailed requirement verification
- Code references with line numbers
- Testing methodology
- Compliance matrix
- Future improvements

</details>

---

## 📚 Documentation

### 📖 Available Guides

| Document | Description | When to Read |
|----------|-------------|--------------|
| **[README.md](README.md)** | Main documentation | Start here |
| **[TECH_STACK.md](TECH_STACK.md)** | Technology details | Understanding architecture |
| **[CONSTRAINTS_ANALYSIS.md](CONSTRAINTS_ANALYSIS.md)** | Requirements analysis | Verification & compliance |
| **[PRESENTATION_SCRIPT.md](PRESENTATION_SCRIPT.md)** | Demo script (20 min) | Presenting the project |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Command reference | Quick access during demo |
| **[TEST_RUN_CHECKLIST.md](TEST_RUN_CHECKLIST.md)** | Pre-recording tests | Before recording demo |

### 🆘 Getting Help

<table>
<tr>
<td width="33%">

#### 🐛 Found a Bug?
[Create an issue](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad/issues)

</td>
<td width="33%">

#### 💡 Have a Question?
Check the [documentation](#-documentation) or ask in issues

</td>
<td width="33%">

#### 🚀 Want to Contribute?
See [Contributing](#-contributing) section

</td>
</tr>
</table>

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🔧 Development

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/amazing-feature

# 3. Commit your changes
git commit -m 'Add some amazing feature'

# 4. Push to the branch
git push origin feature/amazing-feature

# 5. Open a Pull Request
```

### 📝 Guidelines

- ✅ Follow existing code style
- ✅ Add tests for new features
- ✅ Update documentation
- ✅ Keep commits atomic and descriptive
- ✅ Ensure all tests pass

### 👨‍💻 Development Team

<div align="center">

**BeyondGames Team**  
*Original developers and maintainers*

</div>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - Copyright (c) 2025 BeyondGames Team
```

---

## 🙏 Acknowledgments

<div align="center">

**Special Thanks To:**

🎓 **IIIT Dharwad**  
*For problem requirements and academic support*

🐍 **Python Community**  
*For amazing libraries and tools*

💻 **Contributors**  
*For improvements and feedback*

</div>

---

## 🏆 Project Highlights

<div align="center">

| Achievement | Description |
|-------------|-------------|
| ✨ **Innovative** | Original constraint-based solution |
| 🎯 **Production Ready** | Battle-tested and reliable |
| 🚀 **Fast** | 30-second generation time |
| 🎨 **Beautiful** | Interactive HTML viewer |
| 📊 **Efficient** | 90% smaller file sizes |
| 🔄 **Flexible** | Two implementation styles |
| 📚 **Well-Documented** | Comprehensive guides |
| 🧪 **Tested** | 91.7% constraint satisfaction |

</div>

---

## 📞 Contact & Support

<div align="center">

### Need Help?

📧 **Email**: [Create an issue on GitHub](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad/issues)  
💬 **Discussions**: [GitHub Discussions](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad/discussions)  
📚 **Docs**: [Documentation](#-documentation)

---

### ⭐ If you find this project useful, please give it a star!

[![GitHub stars](https://img.shields.io/github/stars/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad?style=social)](https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad/stargazers)

---

**Made with ❤️ by BeyondGames Team**

</div>
