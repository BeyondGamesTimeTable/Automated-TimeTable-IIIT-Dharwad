# Global Elective Coordination System

## Overview

The timetable generator now implements **global elective coordination** across all departments and sections within the same semester. This means that all students in a given semester (regardless of their department or section) will have elective baskets scheduled at the same time slots.

## Benefits

### 1. **Resource Efficiency**
- Single elective class serves multiple departments/sections simultaneously
- Reduces total number of elective classes needed
- Optimizes faculty workload

### 2. **Expanded Student Choice**
- Students from CSE, DSAI, and ECE can attend the same elective session together
- Allows for larger class sizes and more diverse course offerings
- Facilitates inter-departmental learning

### 3. **Classroom Optimization**
- Shared elective sessions use large classrooms (C004 by default)
- Better utilization of classroom resources
- Reduces classroom scheduling conflicts

## How It Works

### Two-Phase Process

**Phase 1: First Department/Section**
- When the first department/section for a semester is generated, elective baskets are scheduled normally
- After scheduling, all time slots for each basket are saved to a global schedule
- Format: `{semester: {basket: [(day, time, duration, session_type, classroom), ...]}}`

**Phase 2: Subsequent Departments/Sections**
- When subsequent departments/sections are generated for the same semester
- System checks if the basket is already in the global schedule
- If yes, reuses the exact same time slots (day, time, classroom)
- If no, schedules normally and saves for others

### Example: Semester 2

**CSE Section A (First):**
- Schedules B3, B4, E1 electives
- Saves slots: 
  - B3: Monday 14:30, Tuesday 14:30, Wednesday 11:30, Thursday 14:30
  - B4: Monday 16:30, Tuesday 16:30, Wednesday 16:30, Friday 14:30
  - E1: Monday 11:30, Tuesday 11:30, Thursday 09:45, Friday 09:45

**CSE Section B (Second):**
- Reuses B3, B4, E1 slots from Section A
- All electives at same times as Section A ✅

**DSAI Section A (Third):**
- Reuses B3, B4 slots (doesn't have E1)
- B3 and B4 at same times as CSE sections ✅

**ECE Section A (Fourth):**
- Reuses B3, B4 slots (doesn't have E1)
- B3 and B4 at same times as other departments ✅

## Verification

### Semester 2 - Basket B3
All departments have B3 at these times:
- Monday 14:30
- Tuesday 14:30
- Wednesday 11:30
- Thursday 14:30

### Semester 2 - Basket B4
All departments have B4 at these times:
- Monday 16:30
- Tuesday 16:30
- Wednesday 16:30
- Friday 14:30

### Semester 6 - Basket B1
All departments have B1 at these times:
- Monday 09:45
- Tuesday 09:45
- Wednesday 09:45
- Friday 08:00

## Technical Implementation

### Global Schedule Dictionary
```python
self.global_elective_schedule = {
    2: {  # Semester 2
        'B3': [
            ('Monday', '14:30-16:30', 90, 'Lecture', 'C004'),
            ('Tuesday', '14:30-16:30', 90, 'Lecture', 'C004'),
            ...
        ],
        'B4': [...],
        'E1': [...]
    },
    4: {...},
    6: {...}
}
```

### Reuse Logic
When scheduling an elective basket:
1. Check if `semester` exists in `global_elective_schedule`
2. Check if `basket` exists in `global_elective_schedule[semester]`
3. If yes: Place elective at those exact slots, mark as used
4. If no: Schedule normally, then save slots to global schedule

### Saving Logic
After scheduling all sessions for an elective basket:
1. Scan timetable for all entries containing the basket name
2. Extract: day, time, duration, session type, classroom
3. Store tuple list in `global_elective_schedule[semester][basket]`

## Console Output

The system provides clear feedback during generation:

```
   Scheduling: ELECTIVE_B3 - L:3 T:1 P:0
   [GLOBAL] Saved 4 slots for B3 to global schedule
```

```
   [GLOBAL] Reusing existing slots for B3 from global schedule
```

This allows you to verify that coordination is working correctly during generation.

## Basket Rotation Strategy

Not all baskets are available in all semesters:

- **Semester 2**: B1, B3, B4, E1
- **Semester 4**: B1, B3, Minor
- **Semester 6**: B1, B3, E1

Only baskets that are rotated IN for a semester are scheduled and coordinated globally.

## Cross-Department + Elective Coordination

The system now has TWO types of global coordination:

### 1. Cross-Department Shared Courses (DSAI + ECE)
- Shared mandatory courses like CS162, CS164, HS161
- Same times, same classrooms for both departments
- Example: CS162 Monday 08:00 in C004 for both DSAI and ECE

### 2. Global Elective Coordination (All Depts/Sections)
- Elective baskets at same times across all departments/sections
- Example: B3 Monday 14:30 for CSE-A, CSE-B, DSAI, ECE

Together, these features ensure:
- DSAI and ECE attend shared courses together
- All students attend electives together (where baskets overlap)
- Efficient use of faculty and classroom resources
- Maximum flexibility for student elective choices

## Validation

You can verify coordination by checking the CSV timetables:

```powershell
Select-String "Elective \(B3\)" CSE_Sem2_SectionA_Timetable.csv, DSAI_Sem2_SectionA_Timetable.csv, ECE_Sem2_SectionA_Timetable.csv
```

All matches should show B3 at the same day/time across all files.

## Future Enhancements

Potential improvements:
- Dynamic basket capacity analysis (predict enrollment)
- Elective preference collection from students
- Automatic large classroom selection based on expected enrollment
- Cross-semester elective coordination (if beneficial)
