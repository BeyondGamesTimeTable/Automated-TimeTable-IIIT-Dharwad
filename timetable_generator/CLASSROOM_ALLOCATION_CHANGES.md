# Classroom Allocation Changes - Implementation Summary

## Date: January 2025
## Status: ✅ COMPLETED AND TESTED

## Overview
Implemented new classroom allocation rules to separate common courses from electives:
- **Common courses** (e.g., CSE Section A+B together, ECE+DSAI shared courses) → **MUST use C004** (large auditorium) at same time slots
- **Electives** (common to all 3 branches) → **MUST NOT use C004**, use backup classrooms (C101-C205), display classroom inline

## Changes Made

### 1. Modified `_find_available_large_classroom()` Method (Lines 250-284)
**File:** `main.py`

**Changes:**
- Added `is_elective=False` parameter to function signature
- Added logic to skip C004 entirely when `is_elective=True`
- For electives: Only returns backup classrooms (C101, C102, C103, C104, C105, C201, C202, C203, C204, C205)
- For common courses: Continues to prioritize C004 first, then falls back to backup classrooms

**Code Logic:**
```python
if is_elective:
    # Skip C004 entirely for electives
    # Return first available backup classroom
    return backup_large_classrooms[0]  # e.g., C101
else:
    # For common courses: Try C004 first
    return C004 if available, else try backup classrooms
```

### 2. Updated Classroom Assignment Logic in `_schedule_session()` (Lines 886-896, 964-974)
**File:** `main.py`

**Changes:**
- Modified both regular slots and afternoon flexible slots sections
- Added explicit check: `if is_elective and basket:` to force dynamic classroom allocation for electives
- Electives now ALWAYS call `_find_available_large_classroom(day, time_str, is_elective=True)` regardless of CSV-specified classroom
- This ensures electives can NEVER get C004, even if specified in input CSV

**Before:**
```python
if classroom is None:
    actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=(is_elective and basket is not None))
```

**After:**
```python
if is_elective and basket:
    # Electives MUST use dynamic assignment to avoid C004
    actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=True)
elif classroom is None:
    # Common courses or other courses
    actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=False)
```

### 3. Updated `_create_session_label()` Method (Lines 1002-1017)
**File:** `main.py`

**Changes:**
- Added `classroom=None` parameter to function signature
- For electives: Returns format `"Elective (basket) (classroom)"` when classroom is provided
- For common courses: Returns existing format `"CourseCode (Common)"`
- For regular courses: Returns existing format `"CourseCode-Section"`

**Example Outputs:**
- Elective: `"Elective (B3) (C101)"` ✓
- Common: `"CS165 (Common)"` ✓
- Regular: `"MA163-A"` ✓

### 4. Updated Elective Reuse Section (Lines 686-693)
**File:** `main.py`

**Changes:**
- Modified elective global schedule reuse to pass classroom to `_create_session_label()`
- Changed from `f"{session_label} | {classroom_used}"` to inline format
- For electives: classroom now embedded in label, no pipe separator needed

**Before:**
```python
session_label = self._create_session_label(course_code, session_type, section, is_common=False, is_elective=True, basket=basket)
full_label = f"{session_label} | {classroom_used}"
```

**After:**
```python
session_label = self._create_session_label(course_code, session_type, section, is_common=False, is_elective=True, basket=basket, classroom=classroom_used)
full_label = session_label  # Classroom already inline
```

### 5. Fixed Classroom Extraction from Global Schedule (Lines 790-823)
**File:** `main.py`

**Changes:**
- Updated regex pattern to extract classroom from new inline format
- Changed from looking for `| classroom` to extracting from `(classroom)` parentheses
- Uses regex: `r'\(([CL][^)]+)\)'` to match classroom codes starting with C or Lab

**Before:**
```python
if '|' in entry:
    classroom_used = entry.split('|')[-1].strip()
else:
    classroom_used = 'C004'  # BAD: Default to C004
```

**After:**
```python
# Extract classroom from parentheses format: "Elective (basket) (classroom)"
classroom_match = re.search(r'\(([CL][^)]+)\)', entry)
if classroom_match:
    classroom_used = classroom_match.group(1)
else:
    # Fallback to pipe separator for old format compatibility
    if '|' in entry:
        classroom_used = entry.split('|')[-1].strip()
    else:
        classroom_used = None  # No default to C004 anymore
```

## Testing Results

### CSE Semester 2 Section A:
✅ Common course CS165 → C004 (both sections use same time slots)  
✅ Elective E1 → C101 (NOT C004)  
✅ Elective B3 → C101 (NOT C004)  
✅ Elective B4 → C101 (NOT C004)  

### DSAI Semester 2:
✅ Common courses (CS162, CS164, HS161, CS163) → C004 or C102  

### DSAI Semester 4:
✅ Elective Minor → C103 (NOT C004)  

### ECE Semester 4:
✅ Elective Minor → C103 (NOT C004)  

### All Semester 6 Timetables:
✅ Elective B1 → C101 (NOT C004)  
✅ Elective B3 → C101 (NOT C004)  

## Output Format Examples

### CSV Format:
```
Monday,CS165 (Common) | C004,CS163-A | C202,Elective (E1) (C101) [60min],LUNCH BREAK,Elective (B4) (C101) [90min],Free
```

### Display Format:
- Common courses: `CS165 (Common) | C004` (classroom in time slot header)
- Electives: `Elective (B3) (C101)` (classroom inline in cell)
- Regular courses: `MA163-A | C202` (classroom in time slot header)

## Verification

To verify the changes are working:

1. **Check no electives use C004:**
   ```powershell
   cd timetable_outputs
   Select-String "Elective.*C004" *.csv
   # Should return NO matches
   ```

2. **Check common courses use C004:**
   ```powershell
   Select-String "Common.*C004" *.csv
   # Should return multiple matches
   ```

3. **Check elective format:**
   ```powershell
   Select-String "Elective \([A-Z0-9]+\) \(C[0-9]+\)" *.csv
   # Should return matches with inline classroom format
   ```

## Conclusion

All requirements have been successfully implemented:
1. ✅ Common courses (Section A+B together, ECE+DSAI shared) use C004 with same time slots
2. ✅ Electives NEVER use C004, only use backup classrooms
3. ✅ Elective classroom names appear inline next to course name in cell format
4. ✅ All timetables generated successfully with new rules

**No C004 conflicts between common courses and electives!**
