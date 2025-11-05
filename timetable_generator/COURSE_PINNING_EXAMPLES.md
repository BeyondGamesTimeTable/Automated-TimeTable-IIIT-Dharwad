# 📌 Course Pinning - Quick Examples

## Copy-Paste Ready Examples

### Example 1: Pin CS165 to Monday 8:00 AM (Common Course)

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

**Visual:**
```
Monday Schedule:
08:00-09:30: CS165 (Lecture) in C004  ← PINNED!
09:45-11:15: [AUTO-SCHEDULED]
11:30-13:00: [AUTO-SCHEDULED]
```

---

### Example 2: Pin Lab to Wednesday Afternoon

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

**Visual:**
```
Wednesday Schedule:
08:00-09:30: [AUTO-SCHEDULED]
09:45-11:15: [AUTO-SCHEDULED]
11:30-13:00: [AUTO-SCHEDULED]
13:00-14:30: LUNCH
14:30-16:30: CS163 Lab in Lab-1  ← PINNED!
```

---

### Example 3: Pin Multiple Sessions of MA163

```python
COURSE_TIME_PINNING = {
    'MA163-L1': {
        'course_code': 'MA163',
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',
    },
    'MA163-L2': {
        'course_code': 'MA163',
        'day': 'Tuesday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',
    },
    'MA163-T': {
        'course_code': 'MA163',
        'day': 'Friday',
        'slot': ('09:45', '11:15'),
        'type': 'Tutorial',
    },
}
```

**Visual:**
```
Week Schedule for MA163:
Mon 08:00-09:30: MA163 Lecture 1  ← PINNED!
Tue 08:00-09:30: MA163 Lecture 2  ← PINNED!
Fri 09:45-11:15: MA163 Tutorial   ← PINNED!
```

---

### Example 4: Different Pinning for Section A vs B

```python
DEPT_COURSE_PINNING = {
    ('CSE', 2, 'A'): {
        'MA163': {
            'day': 'Monday',
            'slot': ('09:45', '11:15'),
            'classroom': 'C202',
        },
    },
    ('CSE', 2, 'B'): {
        'MA163': {
            'day': 'Monday',
            'slot': ('11:30', '13:00'),
            'classroom': 'C203',
        },
    },
}
```

**Visual:**
```
Monday Schedule:
              Section A          Section B
08:00-09:30   [AUTO]            [AUTO]
09:45-11:15   MA163 in C202 ←   [AUTO]
11:30-13:00   [AUTO]            MA163 in C203 ←
```

---

### Example 5: Avoid Monday Mornings for CS307

```python
COURSE_AVOID_SLOTS = {
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
        {'day': 'Monday', 'slot': ('09:45', '11:15')},
    ],
}
```

**Visual:**
```
Monday Schedule:
08:00-09:30: ❌ CS307 NOT HERE
09:45-11:15: ❌ CS307 NOT HERE
11:30-13:00: ✅ CS307 can be scheduled here
14:30-16:30: ✅ CS307 can be scheduled here
```

---

### Example 6: Keep Friday Afternoons Free

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

**Visual:**
```
Friday Schedule:
08:00-09:30: ✅ Electives can be here
09:45-11:15: ✅ Electives can be here
11:30-13:00: ✅ Electives can be here
13:00-14:30: LUNCH
14:30-16:30: ❌ No electives (FREE TIME)
16:30-18:30: ❌ No electives (FREE TIME)
```

---

### Example 7: Complete Real-World Configuration

```python
# Pin common courses
COURSE_TIME_PINNING = {
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'type': 'Lecture',
        'classroom': 'C004',
    },
    'HS205': {
        'day': 'Tuesday',
        'slot': ('09:45', '11:15'),
        'type': 'Lecture',
        'classroom': 'C101',
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
    ('ECE', 4, 'A'): {
        'EC310': {
            'day': 'Friday',
            'slot': ('09:45', '11:15'),
        },
    },
}

# Avoid certain slots
COURSE_AVOID_SLOTS = {
    'CS307': [
        {'day': 'Monday', 'slot': ('08:00', '09:30')},
    ],
    'DS309': [
        {'day': 'Friday', 'slot': ('14:30', '16:30')},
        {'day': 'Friday', 'slot': ('16:30', '18:30')},
    ],
}
```

**Visual Weekly Overview:**
```
         Monday          Tuesday         Wednesday       Thursday        Friday
08:00    CS165 (ALL) ←   [AUTO]         [AUTO]          [AUTO]          [AUTO]
09:45    [AUTO]          HS205 (ALL) ←  [AUTO]          [AUTO]          EC310(ECE4A) ←
11:30    [AUTO]          [AUTO]         [AUTO]          [AUTO]          [AUTO]
13:00    ----------- LUNCH BREAK ---------------------
14:30    [AUTO]          [AUTO]         CS163 Lab(CSE2A)← [AUTO]        [FREE]
16:30    [AUTO]          [AUTO]         [AUTO]          [AUTO]          [FREE]

Legend:
← = Pinned
[AUTO] = Auto-scheduled
[FREE] = Avoided (kept free)
```

---

## 🎯 How to Apply These Examples

### Step 1: Open the Configuration File
```bash
code timetable_generator/time_config.py
# OR
notepad timetable_generator/time_config.py
```

### Step 2: Find the Pinning Section
Look for these sections around line 160:
```python
# ============================================================================
# COURSE-SPECIFIC TIME SLOT PINNING
# ============================================================================
COURSE_TIME_PINNING = {
```

### Step 3: Copy-Paste Your Example
Delete the empty `{}` and paste your configuration:
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

### Step 4: Test Configuration
```bash
cd timetable_generator
py time_config.py
```

Look for:
```
COURSE-SPECIFIC TIME SLOT PINNING CONFIGURATION
Global Course Pinning:
  • CS165: Monday 08:00-09:30 (Lecture) in C004
```

### Step 5: Generate Timetables
```bash
py main.py
```

### Step 6: Verify in Output
Open the CSV/HTML files and check that CS165 is on Monday 08:00-09:30!

---

## 🔧 Mix & Match Template

```python
# ============================================================================
# YOUR CUSTOM CONFIGURATION
# ============================================================================

# Pin specific courses globally
COURSE_TIME_PINNING = {
    # Add your pinned courses here
    # 'COURSE_CODE': {
    #     'day': 'Monday/Tuesday/etc',
    #     'slot': ('HH:MM', 'HH:MM'),
    #     'type': 'Lecture/Tutorial/Lab',  # Optional
    #     'classroom': 'RoomCode',         # Optional
    # },
}

# Pin courses for specific departments/sections
DEPT_COURSE_PINNING = {
    # Add section-specific pins here
    # ('DEPT', SEM, 'SEC'): {
    #     'COURSE_CODE': {...},
    # },
}

# Avoid specific slots
COURSE_AVOID_SLOTS = {
    # Add avoided slots here
    # 'COURSE_CODE': [
    #     {'day': 'DayName', 'slot': ('HH:MM', 'HH:MM')},
    # ],
}
```

---

## 📱 Quick Reference Card

| I want to... | Use this... | Example |
|--------------|-------------|---------|
| Pin a course to specific day/time | `COURSE_TIME_PINNING` | See Example 1 |
| Pin different times for sections | `DEPT_COURSE_PINNING` | See Example 4 |
| Block a time slot | `COURSE_AVOID_SLOTS` | See Example 5 |
| Pin multiple sessions | `COURSE_TIME_PINNING` with unique keys | See Example 3 |
| Keep time slots free | `COURSE_AVOID_SLOTS` | See Example 6 |

---

## ⚡ Common Scenarios

### Scenario: Faculty Only Available Tuesdays
```python
COURSE_TIME_PINNING = {
    'CS307': {
        'day': 'Tuesday',
        'slot': ('09:45', '11:15'),
    },
}
```

### Scenario: Lab Room Conflict
```python
COURSE_AVOID_SLOTS = {
    'CS163': [
        {'day': 'Monday', 'slot': ('14:30', '16:30')},  # Lab-1 used by others
    ],
}
```

### Scenario: Student Assembly on Thursday 2 PM
```python
COURSE_AVOID_SLOTS = {
    'ELECTIVE_B1': [{'day': 'Thursday', 'slot': ('14:30', '16:30')}],
    'ELECTIVE_B2': [{'day': 'Thursday', 'slot': ('14:30', '16:30')}],
    'ELECTIVE_B3': [{'day': 'Thursday', 'slot': ('14:30', '16:30')}],
}
```

### Scenario: Coordinate Common Course Across Sections
```python
COURSE_TIME_PINNING = {
    'CS165': {
        'day': 'Monday',
        'slot': ('08:00', '09:30'),
        'classroom': 'C004',  # Same time/place for all sections
    },
}
```

---

## 🎓 Pro Tips

1. **Always test after changes:** `py time_config.py`
2. **Start with critical courses:** Pin must-have slots first
3. **Use comments:** Document why courses are pinned
4. **Check conflicts:** Ensure pinned slots don't overlap
5. **Be flexible:** Don't pin too many courses (makes scheduling harder)

---

**Need more help? See:** `COURSE_PINNING_GUIDE.md` for complete documentation
