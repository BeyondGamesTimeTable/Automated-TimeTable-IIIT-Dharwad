# Elective Scheduling Requirements

## Current Behavior
- Electives are scheduled in C004 (large auditorium) along with common courses
- All elective baskets compete for the same classrooms as common courses

## New Requirements

### 1. Common Courses (Foundation courses - Type F)
**Examples:**
- Courses common to CSE Section A + B
- Courses common to ECE + DSAI

**Scheduling Rules:**
- ✅ **MUST** be scheduled in **C004** (240-seater auditorium)
- ✅ **MUST** have the **same time slot** for both sections/departments
- ✅ If C004 is unavailable, use backup large classrooms (C101-C205)

### 2. Elective Courses (Type T - Baskets B1, B3, B4, E1, Minor)
**Examples:**
- Electives common to all 3 branches (CSE, DSAI, ECE) of same semester

**Scheduling Rules:**
- ❌ **DO NOT** schedule in C004
- ✅ Schedule in **other classrooms** (C101-C205, Lab-1 to Lab-5, etc.)
- ✅ Show classroom name **next to the course name** in the timetable cell
  - Example: "Machine Learning (C101)" instead of showing C101 in the time slot header
- ✅ Keep time slot header clean (no classroom for electives)

## Implementation Changes Needed

### In `main.py`:

1. **Modify `find_available_large_classroom()` function** (line ~251):
   - Add parameter: `is_elective=False`
   - If `is_elective=True`: 
     - Skip C004 entirely
     - Only check backup classrooms (C101-C205)
     - Or assign dedicated elective classrooms

2. **Update elective scheduling logic**:
   - When scheduling electives, pass `is_elective=True`
   - Store classroom info with the course entry
   - Format display: `course_name (classroom)`

3. **Ensure common course priority**:
   - Schedule all common courses FIRST before electives
   - Reserve C004 primarily for common courses

### Display Format

**Current (Wrong):**
```
Time Slot Header: 09:00-10:30 (C004)
Cell: Machine Learning
```

**New (Correct for Electives):**
```
Time Slot Header: 09:00-10:30
Cell: Machine Learning (C101)
```

**Correct for Common Courses:**
```
Time Slot Header: 09:00-10:30 (C004)
Cell: Data Structures
```

## Files to Modify
1. `timetable_generator/main.py` - Core scheduling logic
2. `timetable_generator/csv_timetable_generator.py` - CSV output formatting (if used)
3. `timetable_generator/timetable_to_html.py` - HTML display formatting

## Testing After Changes
1. Generate timetables for all semesters
2. Verify:
   - ✅ All common courses are in C004 with same time slots
   - ✅ No electives appear in C004
   - ✅ Elective classroom names appear next to course names
   - ✅ Time slot headers don't show classrooms for electives
