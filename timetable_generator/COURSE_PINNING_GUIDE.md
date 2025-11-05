# 📌 Course-Specific Time Slot Pinning Guide

## Overview
You can now **pin specific courses to specific time slots** in your timetable! This feature allows you to:
- ✅ Force a course to be scheduled at a specific day/time
- ✅ Prevent a course from being scheduled at certain times
- ✅ Set preferred time slots for different course types (Lectures, Labs, Tutorials)
- ✅ Configure different pinning for different departments/sections

All configurations are done in `time_config.py` - no code editing required!

---

## 🎯 Feature 1: Pin Courses to Specific Time Slots

### How to Use

Open `time_config.py` and edit the `COURSE_TIME_PINNING` dictionary:

```python
COURSE_TIME_PINNING = {
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',           # Optional
        'classroom': 'C004',         # Optional
    },
}
```

### Real-World Examples

#### Example 1: Pin a Common Course
Force CS165 (common course) to always be on Monday at 8:00 AM:

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

#### Example 2: Pin a Lab Session
Force CS163 lab to Wednesday afternoon:

```python
COURSE_TIME_PINNING = {
    'CS163': {
        'day': 'Wednesday',
        'slot': ('14:30', '16:30'),
        'type': 'Lab',
        'classroom': 'Lab-1',
    },
}
```

#### Example 3: Pin Multiple Sessions of Same Course
Pin all sessions of MA163 (2 lectures + 1 tutorial):

```python
COURSE_TIME_PINNING = {
    'MA163-Lecture-1': {
        'course_code': 'MA163',
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',
    },
    'MA163-Lecture-2': {
        'course_code': 'MA163',
        'day': 'Tuesday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',
    },
    'MA163-Tutorial': {
        'course_code': 'MA163',
        'day': 'Friday',
        'slot': ('09:45', '11:15'),
        'type': 'Tutorial',
    },
}
```

#### Example 4: Pin Multiple Courses
Pin several courses at once:

```python
COURSE_TIME_PINNING = {
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',
    },
    'HS205': {
        'day': 'Tuesday',
        'slot': ('09:45', '11:15'),
        'type': 'Lecture',
    },
    'CS307-Lab': {
        'course_code': 'CS307',
        'day': 'Wednesday',
        'slot': ('14:30', '16:30'),
        'type': 'Lab',
    },
}
```

---

## 🏢 Feature 2: Department/Section Specific Pinning

### How to Use

For different pinning rules per department/section, use `DEPT_COURSE_PINNING`:

```python
DEPT_COURSE_PINNING = {
    ('CSE', 2, 'A'): {
        'CS165': {...},
        'MA163': {...},
    },
    ('ECE', 4, 'A'): {
        'HS205': {...},
    },
}
```

### Real-World Examples

#### Example 1: Different Pinning for CSE Section A vs B

```python
DEPT_COURSE_PINNING = {
    # CSE Semester 2, Section A
    ('CSE', 2, 'A'): {
        'CS165': {
            'day': 'Monday',
            'slot': ('08:00', '09:30'),
            'classroom': 'C004',
        },
        'MA163': {
            'day': 'Tuesday',
            'slot': ('09:45', '11:15'),
            'classroom': 'C202',
        },
    },
    
    # CSE Semester 2, Section B
    ('CSE', 2, 'B'): {
        'CS165': {
            'day': 'Monday',
            'slot': ('08:00', '09:30'),
            'classroom': 'C004',  # Same room (common course)
        },
        'MA163': {
            'day': 'Tuesday',
            'slot': ('08:00', '09:30'),  # Different time
            'classroom': 'C203',
        },
    },
}
```

#### Example 2: ECE Semester 4 Specific Pinning

```python
DEPT_COURSE_PINNING = {
    ('ECE', 4, 'A'): {
        'HS205': {
            'day': 'Thursday',
            'slot': ('14:30', '16:30'),
            'type': 'Lecture',
        },
        'EC310': {
            'day': 'Monday',
            'slot': ('09:45', '11:15'),
            'type': 'Lecture',
        },
    },
}
```

---

## 🚫 Feature 3: Avoid Specific Time Slots

### How to Use

Prevent courses from being scheduled at certain times using `COURSE_AVOID_SLOTS`:

```python
COURSE_AVOID_SLOTS = {
    'CourseCode': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
        {'day': 'Friday', 'slot': ('16:30', '18:30')},
    ],
}
```

### Real-World Examples

#### Example 1: Avoid Monday Mornings
Don't schedule CS307 on Monday mornings (professor not available):

```python
COURSE_AVOID_SLOTS = {
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
        {'day': 'Monday', 'slot': ('09:45', '11:15')},
    ],
}
```

#### Example 2: Avoid Friday Afternoons
Keep Friday afternoons free for DS309:

```python
COURSE_AVOID_SLOTS = {
    'DS309': [
        {'day': 'Friday', 'slot': ('14:30', '16:30')},
        {'day': 'Friday', 'slot': ('16:30', '18:30')},
    ],
}
```

#### Example 3: Multiple Courses with Avoidance

```python
COURSE_AVOID_SLOTS = {
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
    ],
    'HS205': [
        {'day': 'Friday', 'slot': ('16:30', '18:30')},
    ],
    'MA202': [
        {'day': 'Wednesday', 'slot': ('14:30', '16:30')},
        {'day': 'Wednesday', 'slot': ('16:30', '18:30')},
    ],
}
```

---

## ⭐ Feature 4: Preferred Time Slots by Course Type

### How to Use

Set preferences (not requirements) for when different types of sessions should be scheduled:

```python
PREFERRED_SLOTS = {
    'Lab': [
        ('14:30', '16:30'),
        ('16:30', '18:30'),
    ],
    'Tutorial': [
        ('09:45', '11:15'),
        ('11:30', '13:00'),
    ],
    'Lecture': [
        ('08:00', '09:30'),
        ('09:45', '11:15'),
    ],
}
```

**Note:** These are *preferences* - the scheduler will try to use these slots first, but will use other slots if needed.

### Customization Example

Prefer labs in the morning instead:

```python
PREFERRED_SLOTS = {
    'Lab': [
        ('09:45', '11:15'),  # Morning labs preferred
        ('11:30', '13:00'),
        ('14:30', '16:30'),  # Afternoon as backup
    ],
    'Tutorial': [
        ('14:30', '16:30'),  # Tutorials in afternoon
    ],
    'Lecture': [
        ('08:00', '09:30'),  # Early morning lectures
        ('09:45', '11:15'),
    ],
}
```

---

## 🔧 Complete Configuration Example

Here's a real-world example combining all features:

```python
# ============================================================================
# COURSE-SPECIFIC TIME SLOT PINNING
# ============================================================================

COURSE_TIME_PINNING = {
    # Pin CS165 (common course) for all sections
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',
        'classroom': 'C004',
    },
    
    # Pin HS205 common course
    'HS205': {
        'day': 'Tuesday',
        'slot': ('09:45', '11:15'),
        'type': 'Lecture',
        'classroom': 'C101',
    },
}

# ============================================================================
# DEPARTMENT/SEMESTER SPECIFIC COURSE PINNING
# ============================================================================

DEPT_COURSE_PINNING = {
    # CSE Semester 2, Section A
    ('CSE', 2, 'A'): {
        'MA163': {
            'day': 'Wednesday',
            'slot': ('08:00', '09:30'),
            'type': 'Lecture',
            'classroom': 'C202',
        },
        'CS163': {
            'day': 'Wednesday',
            'slot': ('14:30', '16:30'),
            'type': 'Lab',
            'classroom': 'Lab-1',
        },
    },
    
    # ECE Semester 4, Section A
    ('ECE', 4, 'A'): {
        'EC310': {
            'day': 'Friday',
            'slot': ('09:45', '11:15'),
            'type': 'Lecture',
        },
    },
}

# ============================================================================
# AVOID SPECIFIC TIME SLOTS FOR COURSES
# ============================================================================

COURSE_AVOID_SLOTS = {
    # Professor X not available Monday mornings
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
        {'day': 'Monday', 'slot': ('09:45', '11:15')},
    ],
    
    # Keep Friday afternoons light
    'DS309': [
        {'day': 'Friday', 'slot': ('14:30', '16:30')},
        {'day': 'Friday', 'slot': ('16:30', '18:30')},
    ],
}

# ============================================================================
# PREFERRED TIME SLOTS FOR COURSE TYPES
# ============================================================================

PREFERRED_SLOTS = {
    'Lab': [
        ('14:30', '16:30'),  # Prefer afternoon for labs
        ('16:30', '18:30'),
    ],
    'Tutorial': [
        ('09:45', '11:15'),  # Mid-morning for tutorials
        ('11:30', '13:00'),
    ],
    'Lecture': [
        ('08:00', '09:30'),  # Early lectures
        ('09:45', '11:15'),
    ],
}
```

---

## 📋 How to Test Your Configuration

### Step 1: Validate Configuration
```bash
cd timetable_generator
py time_config.py
```

This will show:
- ✓ Time slot validation
- All active configurations
- **Course pinning summary** (new!)
- Department-specific pinning
- Avoided slots

### Step 2: Generate Timetables
```bash
py main.py
```

The scheduler will automatically:
- Pin courses to specified slots
- Avoid blocked time slots
- Prefer suggested slots for course types

### Step 3: Verify Results
Open the generated CSV or HTML files to verify courses are scheduled correctly.

---

## 🎓 Use Cases

### Use Case 1: Faculty Availability
**Problem:** Prof. Smith only available Tuesdays and Thursdays

**Solution:**
```python
COURSE_TIME_PINNING = {
    'CS307': {
        'day': 'Tuesday',
        'slot': ('09:45', '11:15'),
    },
}

COURSE_AVOID_SLOTS = {
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
        {'day': 'Wednesday', 'slot': ('09:45', '11:15')},
        {'day': 'Friday', 'slot': ('11:30', '13:00')},
    ],
}
```

### Use Case 2: Shared Resources
**Problem:** Lab-1 used by another department Monday afternoons

**Solution:**
```python
COURSE_AVOID_SLOTS = {
    'CS163': [  # CS163 uses Lab-1
        {'day': 'Monday', 'slot': ('14:30', '16:30')},
        {'day': 'Monday', 'slot': ('16:30', '18:30')},
    ],
}
```

### Use Case 3: Common Course Coordination
**Problem:** CS165 must be same time for all sections

**Solution:**
```python
COURSE_TIME_PINNING = {
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'classroom': 'C004',
    },
}
```

### Use Case 4: Student Preferences
**Problem:** Students prefer no classes on Friday afternoons

**Solution:**
```python
COURSE_AVOID_SLOTS = {
    'ELECTIVE_B1': [
        {'day': 'Friday', 'slot': ('14:30', '16:30')},
        {'day': 'Friday', 'slot': ('16:30', '18:30')},
    ],
    'ELECTIVE_B2': [
        {'day': 'Friday', 'slot': ('14:30', '16:30')},
        {'day': 'Friday', 'slot': ('16:30', '18:30')},
    ],
}
```

---

## 🔍 Viewing Your Configuration

### Command Line Viewing
```bash
py time_config.py
```

Output includes:
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
```

---

## ⚠️ Important Notes

### Priority Order
1. **DEPT_COURSE_PINNING** - Highest priority (section-specific)
2. **COURSE_TIME_PINNING** - Medium priority (global)
3. **PREFERRED_SLOTS** - Lowest priority (suggestions only)

### Conflict Resolution
- If pinned slot conflicts with another course: **Warning shown, pinning may be ignored**
- If avoided slot is only option: **Warning shown, slot will be used**
- Preferences are always optional: **No warnings if not followed**

### Field Requirements

**Required Fields:**
- `day` - Must be valid day name
- `slot` - Must be tuple of two time strings

**Optional Fields:**
- `type` - 'Lecture', 'Tutorial', or 'Lab'
- `classroom` - Specific room code
- `course_code` - Used for multi-session pinning

---

## 📝 Configuration Template

Copy this template to get started:

```python
# ============================================================================
# YOUR COURSE PINNING CONFIGURATION
# ============================================================================

COURSE_TIME_PINNING = {
    # Add your global course pins here:
    # 'COURSE_CODE': {
    #     'day': 'DayName',
    #     'slot': ('HH:MM', 'HH:MM'),
    #     'type': 'Lecture/Tutorial/Lab',
    #     'classroom': 'RoomCode',
    # },
}

DEPT_COURSE_PINNING = {
    # Add department-specific pins here:
    # ('DEPT', SEMESTER, 'SECTION'): {
    #     'COURSE_CODE': {
    #         'day': 'DayName',
    #         'slot': ('HH:MM', 'HH:MM'),
    #     },
    # },
}

COURSE_AVOID_SLOTS = {
    # Add slots to avoid here:
    # 'COURSE_CODE': [
    #     {'day': 'DayName', 'slot': ('HH:MM', 'HH:MM')},
    # ],
}
```

---

## 🚀 Quick Start Checklist

- [ ] Open `time_config.py`
- [ ] Find the `COURSE_TIME_PINNING` section
- [ ] Add your course pinning configurations
- [ ] (Optional) Add department-specific pinning
- [ ] (Optional) Add avoided time slots
- [ ] Run `py time_config.py` to validate
- [ ] Run `py main.py` to generate timetables
- [ ] Verify courses are pinned correctly

---

## 💡 Tips & Best Practices

1. **Start Small:** Pin 1-2 critical courses first, test, then add more
2. **Test Often:** Run `py time_config.py` after each change
3. **Use Comments:** Document why courses are pinned (faculty availability, lab constraints, etc.)
4. **Section-Specific First:** Use `DEPT_COURSE_PINNING` for section-specific needs
5. **Preferences Over Pins:** Use `PREFERRED_SLOTS` when flexibility is okay
6. **Avoid Over-Pinning:** Too many pins can make scheduling impossible

---

## 📚 Related Documentation

- **TIME_CONFIGURATION_GUIDE.md** - How to change time slots
- **QUICK_REFERENCE_TIME_CONFIG.md** - Quick reference for time config
- **USER_MANUAL.md** - Complete system documentation

---

**Version:** 2.2.0  
**Last Updated:** December 2024  
**Feature:** Course-Specific Time Slot Pinning
