# Technology Stack - Automated Timetable Generator

## Programming Language
- **Python 3.12+** - Core application development with object-oriented design

## Core Libraries
| Library | Purpose |
|---------|---------|
| **pandas** | CSV data processing, DataFrame operations, timetable export |
| **os** | File system operations, directory management |
| **datetime** | Time slot management (08:00-19:45), schedule timing |
| **random** | Randomized slot assignment for timetable variation |
| **pathlib** | Modern cross-platform path handling |

## Frontend Technologies
- **HTML5** - Structure for interactive timetable viewer
- **CSS3** - Styling with gradients, flexbox, grid, animations, responsive design
- **No JavaScript** - Pure HTML/CSS for fast, lightweight viewing

## Data Formats
- **CSV** - Input (course data) and output (timetables) - 18 generated files
- **TXT** - Elective course details (18 files) - human-readable format
- **HTML** - Interactive web viewer (19 files) - standalone, no server required

## Development Tools
- **Visual Studio Code** - IDE with Python extensions
- **Git/GitHub** - Version control and repository hosting
- **Configuration Files**: `.vscode/` (launch.json, settings.json, tasks.json)

## Architecture & Design
- **Dual Implementation Available**:
  - **Object-Oriented (main.py)** - Class-based design with `TimetableGenerator` class (529 lines)
  - **Functional (main_functional.py)** - Pure functions with explicit data flow (699 lines)
  - Both produce 100% identical outputs - choose based on preference!
- **Constraint-Based Scheduling** - Backtracking algorithm with conflict detection
- **Data Structures**: Dictionaries (schedules), Sets (duplicate prevention), DataFrames (data manipulation)
- **Design Patterns**: Builder pattern (schedule construction), Template pattern (HTML generation)

## Key Features
- **Zero Dependencies** - Only pandas required (built-in Python libraries for rest)
- **No Database** - CSV-based approach for simplicity
- **No Web Server** - Static HTML generation for offline viewing
- **Cross-Platform** - Works on Windows, Linux, macOS

## System Components
```
Input: 3 CSV files (Even CSE.csv, Even DSAI.csv, Even ECE.csv)
       ↓
Processing: Choose one:
  • Python (main.py - 529 lines) - Class-based OOP approach
  • Python (main_functional.py - 699 lines) - Functional approach
  Both produce identical outputs!
       ↓
Output: 18 CSV timetables + 16 TXT elective details
       ↓
Conversion: Python (timetable_to_html.py - works with both versions)
       ↓
Viewer: 19 HTML files (1 index + 18 timetables)
```

## Performance
- **Generation Time**: ~30 seconds for all 18 timetables
- **File Size**: CSV files 90% smaller than Excel format
- **Success Rate**: 100% conflict-free scheduling
- **Compliance**: 91.7% (11/12 requirements satisfied)

## Implementation Choices

### Dual Version Available
- **main.py (Class-Based)**: OOP design with encapsulation, state management
- **main_functional.py (Functional)**: Pure functions, explicit data flow, easier testing
- **Interchangeable**: Both produce byte-for-byte identical outputs
- **Choose based on**: Team preference (OOP vs Functional programming style)

## Why This Stack?
✅ **Simple** - Minimal setup, only pandas installation required  
✅ **Fast** - Pandas vectorization for efficient data processing  
✅ **Portable** - Pure Python, runs anywhere  
✅ **Maintainable** - Clean design (OOP or Functional), well-documented code  
✅ **Flexible** - Two implementation styles for different coding preferences  
✅ **Production-Ready** - Battle-tested libraries, proven approach  
