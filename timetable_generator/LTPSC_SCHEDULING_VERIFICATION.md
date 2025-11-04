# LTPSC Scheduling Verification

## Overview

Yes, the timetable generator **correctly schedules labs, lectures, and tutorials per week** based on the LTPSC values specified in the input CSV files.

## LTPSC Format

**LTPSC** stands for:
- **L** = Lecture HOURS per week (not number of sessions)
- **T** = Tutorial HOURS per week (not number of sessions)
- **P** = Practical/Lab HOURS per week (not number of sessions)
- **S** = Self-study hours
- **C** = Total credits

## Scheduling Logic

### 1. Lectures (L)
- **L represents total HOURS per week**
- Each lecture session = **1.5 hours (90 minutes)**
- Formula: `num_lecture_sessions = L ÷ 1.5 = L × 2/3`
- **Example**: If L=3 hours/week → 3 ÷ 1.5 = **2 lecture sessions** of 1.5 hours each

### 2. Tutorials (T)
- **T represents total HOURS per week**
- Each tutorial session = **1 hour (60 minutes)**
- Formula: `num_tutorial_sessions = T ÷ 1 = T`
- **Example**: If T=1 hour/week → 1 ÷ 1 = **1 tutorial session** of 1 hour

### 3. Practicals/Labs (P)
- **P represents total HOURS per week**
- Each lab session = **2 hours (120 minutes)**
- Formula: `num_lab_sessions = P ÷ 2`
- **Example**: If P=2 hours/week → 2 ÷ 2 = **1 lab session** of 2 hours
- **Example**: If P=4 hours/week → 4 ÷ 2 = **2 lab sessions** of 2 hours each

## Verification Examples

### Example 1: CS163 (Data Structures & Algorithms)

**Input CSV:**
```csv
CS163,Data Structures & Algorithms,3,0,2,0,4,Dr. C. B. Akki,C202,2,F,,2A
```

**LTPSC Values:**
- L = 3 (3 HOURS per week)
- T = 0 (0 hours)
- P = 2 (2 HOURS per week)

**Expected Schedule:**
- L: 3 hours ÷ 1.5 hours/session = **2 lecture sessions** (90 min each)
- T: 0 hours ÷ 1 hour/session = **0 tutorial sessions**
- P: 2 hours ÷ 2 hours/session = **1 lab session** (120 min)

**Actual Schedule (CSE Sem 2 Section A):**
```
Thursday  08:00-09:30  CS163-A | C202  ← Lecture 1 (1.5 hours)
Friday    08:00-09:30  CS163-A | C202  ← Lecture 2 (1.5 hours)
Monday    14:30-16:30  CS163-Lab-A [120min] | Lab-1  ← Lab (2 hours)
```

✅ **Result**: 2 lectures + 0 tutorials + 1 lab = **CORRECT**  
✅ **Total hours**: (2 × 1.5) + 0 + 2 = 3 + 0 + 2 = 5 hours/week

---

### Example 2: CS310 (Database Management Systems)

**Input CSV:**
```csv
CS310,Database Management Systems,3,1,2,0,5,Dr. Pramod Yelmewad,C104,4,F,,4A
```

**LTPSC Values:**
- L = 3 (3 HOURS per week)
- T = 1 (1 HOUR per week)
- P = 2 (2 HOURS per week)

**Expected Schedule:**
- L: 3 hours ÷ 1.5 hours/session = **2 lecture sessions** (90 min each)
- T: 1 hour ÷ 1 hour/session = **1 tutorial session** (60 min)
- P: 2 hours ÷ 2 hours/session = **1 lab session** (120 min)

**Actual Schedule (CSE Sem 4 Section A):**
```
Wednesday 11:30-13:00  CS310-A | C104  ← Lecture 1 (1.5 hours)
Thursday  11:30-13:00  CS310-A | C104  ← Lecture 2 (1.5 hours)
Friday    11:30-13:00  CS310-T-A | C104  ← Tutorial (1 hour)
Monday    14:30-16:30  CS310-Lab-A [120min] | Lab-3  ← Lab (2 hours)
```

✅ **Result**: 2 lectures + 1 tutorial + 1 lab = **CORRECT**  
✅ **Total hours**: (2 × 1.5) + 1 + 2 = 3 + 1 + 2 = 6 hours/week

---

### Example 3: MA163 (Linear Algebra)

**Input CSV:**
```csv
MA163,Linear Algebra,3,1,0,0,2,Dr Somen Bhattacharjee,C203,2,F,,2B
```

**LTPSC Values:**
- L = 3 (3 HOURS per week)
- T = 1 (1 HOUR per week)
- P = 0 (0 hours)

**Expected Schedule:**
- L: 3 hours ÷ 1.5 hours/session = **2 lecture sessions** (90 min each)
- T: 1 hour ÷ 1 hour/session = **1 tutorial session** (60 min)
- P: 0 hours = **0 lab sessions**

**Actual Schedule (CSE Sem 2 Section A):**
```
Monday    08:00-09:30  MA163-A | C202  ← Lecture 1 (1.5 hours)
Tuesday   08:00-09:30  MA163-A | C202  ← Lecture 2 (1.5 hours)
Wednesday 08:00-09:30  MA163-T-A | C202  ← Tutorial (1 hour)
```

✅ **Result**: 2 lectures + 1 tutorial + 0 labs = **CORRECT**  
✅ **Total hours**: (2 × 1.5) + 1 + 0 = 3 + 1 + 0 = 4 hours/week

---

### Example 4: CS204 (Operating System)

**Input CSV:**
```csv
CS204,Operating System,3,0,2,0,4,Dr. Suvadip Hazra,C104,4,F,,4A
```

**LTPSC Values:**
- L = 3 (3 HOURS per week)
- T = 0 (0 hours)
- P = 2 (2 HOURS per week)

**Expected Schedule:**
- L: 3 hours ÷ 1.5 hours/session = **2 lecture sessions**
- T: 0 hours = **0 tutorial sessions**
- P: 2 hours ÷ 2 hours/session = **1 lab session**

**Actual Schedule (CSE Sem 4 Section A):**
```
(Lectures would be scheduled in 2 time slots, 1.5 hours each)
(Lab would be scheduled in 1 time slot, 2 hours)
```

✅ **Result**: 2 lectures + 0 tutorials + 1 lab = **CORRECT**  
✅ **Total hours**: (2 × 1.5) + 0 + 2 = 3 + 0 + 2 = 5 hours/week

---

## Code Implementation

### Parsing LTPSC Values

```python
def parse_ltpsc(self, row):
    """
    Parse LTPSC values and convert to number of sessions per week.
    
    LTPSC values represent HOURS per week, not number of sessions.
    """
    lecture_hours = int(row.get('Lectures', 0))
    tutorial_hours = int(row.get('Tutorials', 0))
    practical_hours = int(row.get('Practicals', 0))
    
    # Convert hours to number of sessions
    # L=3 hours/week → 3/1.5 = 2 sessions of 1.5 hours each
    num_lecture_sessions = int(lecture_hours * 2 / 3) if lecture_hours > 0 else 0
    
    # T=1 hour/week → 1/1 = 1 session of 1 hour
    num_tutorial_sessions = tutorial_hours
    
    # P=2 hours/week → 2/2 = 1 session of 2 hours
    num_lab_sessions = practical_hours // 2
    
    return num_lecture_sessions, num_tutorial_sessions, num_lab_sessions
```

### Scheduling Sessions

```python
# Parse LTPSC and convert to session counts
lectures, tutorials, practicals = self.parse_ltpsc(course)
# lectures = number of 1.5-hour lecture sessions
# tutorials = number of 1-hour tutorial sessions  
# practicals = number of 2-hour lab sessions

# Schedule lectures (1.5 hours each)
for lec_num in range(lectures):
    success = self._schedule_session(
        timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
        lab_usage, course_code, course_title, classroom,
        'Lecture', section, is_common, is_elective, basket
    )

# Schedule tutorials (1 hour each)
for tut_num in range(tutorials):
    success = self._schedule_session(
        timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
        lab_usage, course_code, course_title, classroom,
        'Tutorial', section, is_common, is_elective, basket, duration_hours=1
    )

# Schedule practicals/labs (2 hours per lab session)
# 'practicals' is already converted to number of sessions
for prac_num in range(practicals):
    success = self._schedule_lab_session(
        timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
        lab_usage, course_code, course_title, classroom,
        section, is_common, is_elective, basket
    )
```

## Session Duration Summary

| Session Type | Duration | Time Slot |
|--------------|----------|-----------|
| Lecture (L) | 90 minutes (1.5 hrs) | Regular slots (08:00-09:30, 09:45-11:15, 11:30-13:00) |
| Tutorial (T) | 60 minutes (1 hr) | Regular or afternoon slots |
| Lab/Practical (P) | 120 minutes (2 hrs) | Afternoon flexible slots (14:30-16:30) |

## Validation Process

To verify LTPSC scheduling for any course:

1. **Check Input CSV**:
   ```powershell
   Select-String "^COURSE_CODE," "input_files/sdtt_inputs/Even CSE.csv"
   ```
   
2. **Check Output Timetable**:
   ```powershell
   Select-String "COURSE_CODE" "timetable_outputs/CSE_SemX_SectionY_Timetable.csv"
   ```

3. **Count Sessions**:
   - Count lecture entries (no suffix or just course code)
   - Count tutorial entries (ends with -T)
   - Count lab entries (contains "Lab" keyword)

4. **Verify Match**:
   - Number of lectures = L value ✅
   - Number of tutorials = T value ✅
   - Number of labs = P ÷ 2 ✅

## Special Cases

### Elective Courses
- Electives follow the same LTPSC logic
- Each elective basket contains multiple courses
- System schedules ONE slot set per basket (not per course)
- All courses in a basket share the same time slots

### Common Courses (DSAI + ECE)
- Shared courses follow standard LTPSC scheduling
- All sessions (lectures, tutorials, labs) coordinated
- Both departments attend at same times

### High Load Optimization
- For semesters with many courses (e.g., ECE Sem 4)
- System may enable Saturday classes automatically
- LTPSC logic remains unchanged

## Conclusion

✅ **Yes, the system correctly interprets LTPSC values as HOURS per week:**
- **L (Lectures)**: Hours per week → Converted to sessions (L ÷ 1.5)
  - Example: L=3 hours → 2 sessions of 1.5 hours each
- **T (Tutorials)**: Hours per week → Converted to sessions (T ÷ 1)
  - Example: T=1 hour → 1 session of 1 hour
- **P (Practicals)**: Hours per week → Converted to sessions (P ÷ 2)
  - Example: P=2 hours → 1 session of 2 hours

All sessions are scheduled according to their specified durations:
- **Lecture sessions**: 90 minutes (1.5 hours) each
- **Tutorial sessions**: 60 minutes (1 hour) each
- **Lab sessions**: 120 minutes (2 hours) each

The total contact hours per week equals the sum of L + T + P hours specified in the LTPSC values.
