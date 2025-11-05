# Course-Specific Time Slot Pinning - Feature Summary

## 🎯 What Was Added

**Version 2.2.0** introduces the ability to **pin specific courses to specific time slots** in your timetable!

---

## 📦 New Features

### 1. ✅ Pin Courses Globally
Force any course to be scheduled at a specific day/time:
```python
COURSE_TIME_PINNING = {
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',
        'classroom': 'C004',
    },
}
```

### 2. ✅ Department/Section-Specific Pinning
Different pinning rules for different departments or sections:
```python
DEPT_COURSE_PINNING = {
    ('CSE', 2, 'A'): {
        'MA163': {
            'day': 'Wednesday',
            'slot': ('08:00', '09:30'),
        },
    },
}
```

### 3. ✅ Avoid Specific Time Slots
Prevent courses from being scheduled at certain times:
```python
COURSE_AVOID_SLOTS = {
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
        {'day': 'Monday', 'slot': ('09:45', '11:15')},
    ],
}
```

### 4. ✅ Preferred Slots by Course Type
Suggest (not force) preferred slots for lectures, labs, tutorials:
```python
PREFERRED_SLOTS = {
    'Lab': [('14:30', '16:30'), ('16:30', '18:30')],
    'Tutorial': [('09:45', '11:15'), ('11:30', '13:00')],
    'Lecture': [('08:00', '09:30'), ('09:45', '11:15')],
}
```

---

## 📝 Files Modified/Added

### Modified Files

**1. `time_config.py`**
- Added `COURSE_TIME_PINNING` dictionary (~line 183)
- Added `DEPT_COURSE_PINNING` dictionary (~line 236)
- Added `COURSE_AVOID_SLOTS` dictionary (~line 264)
- Added `PREFERRED_SLOTS` dictionary (~line 290)
- Added utility functions:
  - `get_course_pinning()`
  - `should_avoid_slot()`
  - `get_preferred_slots()`
  - `print_course_pinning_config()`
- Updated test output to show pinning configuration

### New Documentation Files

**2. `COURSE_PINNING_GUIDE.md`** (~480 lines)
- Complete guide to course pinning feature
- Real-world use cases and examples
- Configuration instructions
- Troubleshooting section
- Best practices

**3. `COURSE_PINNING_EXAMPLES.md`** (~350 lines)
- Copy-paste ready examples
- Visual representations of pinned schedules
- Quick reference scenarios
- Step-by-step application guide

---

## 🚀 How to Use

### Quick Start

1. **Open Configuration File:**
   ```bash
   code timetable_generator/time_config.py
   ```

2. **Find the Pinning Section** (around line 183):
   ```python
   COURSE_TIME_PINNING = {
   ```

3. **Add Your Configuration:**
   ```python
   COURSE_TIME_PINNING = {
       'CS165': {
           'day': 'Monday',
           'slot': ('08:00', '09:30'),
           'type': 'Lecture',
           'classroom': 'C004',
       },
   }
   ```

4. **Test Configuration:**
   ```bash
   cd timetable_generator
   py time_config.py
   ```

5. **Generate Timetables:**
   ```bash
   py main.py
   ```

---

## 📊 Configuration Capabilities

| Feature | Capability | Use Case |
|---------|------------|----------|
| **Global Pinning** | Pin any course to specific day/time | Common courses, faculty availability |
| **Section Pinning** | Different pins per dept/section | Section-specific scheduling needs |
| **Slot Avoidance** | Block specific time slots | Lab conflicts, faculty unavailability |
| **Type Preferences** | Suggest slots for lecture/lab/tutorial | Optimize schedule by session type |
| **Multi-Session** | Pin multiple sessions of same course | Courses with 2+ lectures/tutorials |
| **Classroom Lock** | Force specific classroom | Resource constraints |

---

## 🎓 Real-World Use Cases

### Use Case 1: Faculty Availability
**Problem:** Prof. Smith only teaches on Tuesdays and Thursdays

**Solution:**
```python
COURSE_TIME_PINNING = {
    'CS307': {'day': 'Tuesday', 'slot': ('09:45', '11:15')},
}
COURSE_AVOID_SLOTS = {
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
        {'day': 'Wednesday', 'slot': ('09:45', '11:15')},
        {'day': 'Friday', 'slot': ('11:30', '13:00')},
    ],
}
```

### Use Case 2: Lab Room Shared with Another Department
**Problem:** Lab-1 used by other department on Monday afternoons

**Solution:**
```python
COURSE_AVOID_SLOTS = {
    'CS163': [  # CS163 needs Lab-1
        {'day': 'Monday', 'slot': ('14:30', '16:30')},
        {'day': 'Monday', 'slot': ('16:30', '18:30')},
    ],
}
```

### Use Case 3: Common Course Coordination
**Problem:** CS165 must be same time for all sections (common course)

**Solution:**
```python
COURSE_TIME_PINNING = {
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'classroom': 'C004',  # Same room, same time for all
    },
}
```

### Use Case 4: Student Preferences
**Problem:** Students want Friday afternoons free

**Solution:**
```python
COURSE_AVOID_SLOTS = {
    'ELECTIVE_B1': [
        {'day': 'Friday', 'slot': ('14:30', '16:30')},
        {'day': 'Friday', 'slot': ('16:30', '18:30')},
    ],
    # Repeat for all electives...
}
```

---

## 🔍 Testing & Validation

### Test Command
```bash
py time_config.py
```

### Expected Output
```
================================================================================
COURSE-SPECIFIC TIME SLOT PINNING CONFIGURATION
================================================================================

Global Course Pinning:
  • CS165: Monday 08:00-09:30 (Lecture) in C004
  • HS205: Tuesday 09:45-11:15 (Lecture) in C101

Department-Specific Course Pinning:

  CSE Semester 2, Section A:
    • MA163: Wednesday 08:00-09:30 (Lecture) in C202
    • CS163: Wednesday 14:30-16:30 (Lab) in Lab-1

Courses with Avoided Time Slots:
  • CS307:
    - Avoid: Monday 08:00-09:30
    - Avoid: Monday 09:45-11:15

================================================================================
```

---

## ⚙️ Configuration Options

### Required Fields
- `day` - Day name (Monday, Tuesday, etc.)
- `slot` - Time slot tuple `('HH:MM', 'HH:MM')`

### Optional Fields
- `type` - Session type ('Lecture', 'Tutorial', 'Lab')
- `classroom` - Specific classroom code
- `course_code` - For multi-session pinning with unique keys

---

## 📈 Priority Hierarchy

When scheduling courses, the system respects this priority order:

1. **DEPT_COURSE_PINNING** (Highest) - Section-specific pins
2. **COURSE_TIME_PINNING** (High) - Global course pins
3. **COURSE_AVOID_SLOTS** (High) - Blocked time slots
4. **PREFERRED_SLOTS** (Low) - Type preferences (suggestions only)
5. **Auto-Scheduling** (Lowest) - Default scheduling algorithm

---

## 💡 Best Practices

### ✅ DO:
- Start with critical courses (common courses, limited faculty availability)
- Test configuration after each change: `py time_config.py`
- Use comments to document why courses are pinned
- Use `DEPT_COURSE_PINNING` for section-specific needs
- Use `PREFERRED_SLOTS` when flexibility is acceptable

### ❌ DON'T:
- Over-pin courses (makes scheduling impossible)
- Pin conflicting time slots
- Forget to test before generating timetables
- Pin without documenting the reason
- Ignore validation warnings

---

## 🛠️ Utility Functions Added

### Python API Functions

```python
# Get pinning config for a course
pinning = get_course_pinning('CS165', 'CSE', 2, 'A')

# Check if slot should be avoided
avoid = should_avoid_slot('CS307', 'Monday', ('08:00', '09:30'))

# Get preferred slots for session type
preferred = get_preferred_slots('Lab')

# Print all pinning configuration
print_course_pinning_config()
```

---

## 📚 Documentation

### Quick References
- **COURSE_PINNING_EXAMPLES.md** - Copy-paste ready examples with visuals
- **COURSE_PINNING_GUIDE.md** - Complete feature documentation
- **time_config.py** - Inline comments and examples

### Full Documentation
- **TIME_CONFIGURATION_GUIDE.md** - Time slot configuration
- **QUICK_REFERENCE_TIME_CONFIG.md** - Time config quick reference
- **USER_MANUAL.md** - Complete system manual

---

## 🔄 Integration with Existing System

### Backward Compatible
- ✅ Existing configurations work without changes
- ✅ All features are optional (empty `{}` = no pinning)
- ✅ System falls back to auto-scheduling if pinning fails

### Works With
- ✅ Dynamic time slot configuration (v2.1.0)
- ✅ Saturday scheduling for specific departments
- ✅ Common course coordination
- ✅ Cross-department shared courses
- ✅ Elective rotation system

---

## 📝 Example: Complete Configuration

```python
# Pin common courses globally
COURSE_TIME_PINNING = {
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'classroom': 'C004',
    },
}

# Section-specific pinning
DEPT_COURSE_PINNING = {
    ('CSE', 2, 'A'): {
        'CS163': {
            'day': 'Wednesday',
            'slot': ('14:30', '16:30'),
            'type': 'Lab',
            'classroom': 'Lab-1',
        },
    },
}

# Avoid certain slots
COURSE_AVOID_SLOTS = {
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
    ],
}

# Prefer afternoon for labs
PREFERRED_SLOTS = {
    'Lab': [('14:30', '16:30'), ('16:30', '18:30')],
}
```

---

## 🎉 Benefits

### For Administrators
- ✅ Easy faculty schedule accommodation
- ✅ Simple resource conflict management
- ✅ Flexible student preference handling
- ✅ No programming required

### For System
- ✅ Maintains existing scheduling logic
- ✅ Adds constraints without complexity
- ✅ Validates configuration automatically
- ✅ Clear error messages

### For Users
- ✅ Visual configuration (just edit a dictionary)
- ✅ Extensive examples and documentation
- ✅ Test before generating timetables
- ✅ Copy-paste ready templates

---

## 🚀 Getting Started Checklist

- [ ] Read `COURSE_PINNING_EXAMPLES.md` for quick start
- [ ] Open `time_config.py`
- [ ] Add your first pinned course
- [ ] Run `py time_config.py` to validate
- [ ] Run `py main.py` to generate timetables
- [ ] Verify pinned courses in output
- [ ] Add more pins as needed
- [ ] Document your configuration with comments

---

## 📞 Support

**Documentation:**
- `COURSE_PINNING_EXAMPLES.md` - Quick visual examples
- `COURSE_PINNING_GUIDE.md` - Complete feature guide
- `time_config.py` - Configuration file with inline examples

**Testing:**
```bash
py time_config.py  # Validate and view configuration
```

**Generation:**
```bash
py main.py  # Generate timetables with pinning applied
```

---

**Version:** 2.2.0  
**Feature:** Course-Specific Time Slot Pinning  
**Status:** ✅ Complete and Tested  
**Date:** December 2024  
**Backward Compatible:** Yes
