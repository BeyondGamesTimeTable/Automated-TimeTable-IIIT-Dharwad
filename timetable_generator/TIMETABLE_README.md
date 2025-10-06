# 🎓 BeyondGames Even Semester Timetable Generator

## 📊 Successfully Generated Timetables

### ✅ **Complete Output**
- **3 Departments**: CSE, DSAI, ECE
- **3 Semesters**: 2, 4, 6 (Even semesters)
- **2 Sections**: A and B
- **Total Files**: 18 CSV timetable files + 18 HTML viewer files

---

## 📁 **Generated Files**

### **CSV Output (timetable_outputs/)**
1. `CSE_Sem2_SectionA_Timetable.csv` - `CSE_Sem2_SectionB_Timetable.csv`
2. `CSE_Sem4_SectionA_Timetable.csv` - `CSE_Sem4_SectionB_Timetable.csv`
3. `CSE_Sem6_SectionA_Timetable.csv` - `CSE_Sem6_SectionB_Timetable.csv`
4. `DSAI_Sem2_SectionA_Timetable.csv` - `DSAI_Sem2_SectionB_Timetable.csv`
5. `DSAI_Sem4_SectionA_Timetable.csv` - `DSAI_Sem4_SectionB_Timetable.csv`
6. `DSAI_Sem6_SectionA_Timetable.csv` - `DSAI_Sem6_SectionB_Timetable.csv`
7. `ECE_Sem2_SectionA_Timetable.csv` - `ECE_Sem2_SectionB_Timetable.csv`
8. `ECE_Sem4_SectionA_Timetable.csv` - `ECE_Sem4_SectionB_Timetable.csv`
9. `ECE_Sem6_SectionA_Timetable.csv` - `ECE_Sem6_SectionB_Timetable.csv`

### **HTML Output (timetable_html/)**
- **index.html** - Main navigation page
- Matching HTML files for each CSV timetable
- Interactive web viewer with styling

---

## ⚙️ **Timetable Configuration**

### **Time Schedule** (8 AM - 8 PM)
```
08:00 - 09:30  (1.5 hours - Early morning slot)
09:45 - 11:15  (1.5 hours - Morning slot)
11:30 - 13:00  (1.5 hours - Late morning slot)
13:00 - 14:30  🍽️ LUNCH BREAK
14:45 - 16:15  (1.5 hours - Afternoon slot)
16:30 - 18:00  (1.5 hours - Late afternoon slot)
18:15 - 19:45  (1.5 hours - Evening slot)
```

### **Break Schedule**
- ✅ **15-minute breaks** between each time slot
- ✅ **1-hour lunch break** from 2:00 PM to 3:00 PM
- ✅ **5 working days**: Monday to Friday

### **Session Durations**
- **Lectures**: 1.5 hours (1 time slot)
- **Tutorials**: 1 hour (1 time slot)
- **Labs/Practicals**: 2 hours (2 consecutive time slots)

---

## 🎯 **Key Features Implemented**

### ✅ **Classroom Conflict Prevention**
- No two subjects share the same classroom at the same time
- Proper room allocation based on CSV data
- Common courses use C004 (240-seater auditorium)

### ✅ **No Same-Day Repetition**
- A subject never has multiple lectures on the same day
- A subject never has multiple tutorials on the same day
- A subject never has multiple labs on the same day

### ✅ **Common Course Handling**
- Foundation courses (marked as 'F' in CSV) are scheduled for both sections together
- Automatically uses the 240-seater auditorium (C004)
- Both Section A and Section B attend together

### ✅ **Section-Specific Courses**
- Tutorials marked as T-A or T-B for respective sections
- Labs marked as Lab-A or Lab-B for respective sections
- Proper section isolation

### ✅ **LTPSC Integration**
- Reads Lectures, Tutorials, Practicals directly from CSV
- Automatically schedules correct number of sessions
- Respects credit distribution

---

## 📋 **Timetable Format**

### **Example Entry**
```
CS163-A | C202          → Course CS163, Section A, Room C202
CS310-Lab-B | C104      → Lab for CS310, Section B, Room C104
MA202 (Common) | C004   → Common course MA202, Large auditorium C004
DS357-T-A | C004        → Tutorial for DS357, Section A
```

### **Legend**
- **Course-A/B**: Section-specific lecture
- **Course-T-A/T-B**: Section-specific tutorial
- **Course-Lab-A/Lab-B**: Section-specific lab
- **Course (Common)**: Common course for both sections
- **| Room**: Classroom location

---

## 📊 **Statistics**

### **Courses Scheduled**
- **Semester 2**: Foundation courses + Basket electives
- **Semester 4**: Core courses + Minor courses
- **Semester 6**: Advanced courses + Basket selections + Minors

### **Room Utilization**
- **C004**: Large auditorium (240-seater) for common courses
- **C101-C205**: Regular classrooms for section-specific courses
- **C302-C305**: Specialized classrooms for electives
- **Labs**: Dedicated lab spaces for practical sessions

---

## ⚠️ **Notes & Warnings**

### **Scheduling Warnings**
Some courses could not be fully scheduled due to:
1. **Limited time slots**: With 5 slots/day × 5 days = 25 slots, heavily loaded semesters may exceed capacity
2. **Classroom conflicts**: Some courses require specific rooms that were already occupied
3. **Basket electives**: Multiple basket options competing for same time slots

### **Recommendations**
1. **Review warnings**: Check console output for courses that couldn't be scheduled
2. **Manual adjustment**: Some courses may need manual scheduling
3. **Elective management**: Consider spreading basket electives across different time slots
4. **Room flexibility**: Some courses may need room reassignment

---

## 🚀 **How to Use**

### **View Timetables**
1. Navigate to `timetable_outputs/` folder
2. Open any Excel file
3. View department-specific, semester-specific, section-specific schedules

### **Regenerate Timetables**
```bash
cd timetable_generator
py csv_timetable_generator.py
```

### **Modify Scheduling Rules**
Edit `csv_timetable_generator.py`:
- Change time slots in `self.time_slots`
- Modify lunch break time
- Adjust scheduling algorithms
- Customize room allocations

---

## 📞 **Support**

For questions or issues:
- Review the generated Excel files in `timetable_outputs/`
- Check console warnings for unscheduled courses
- Modify CSV files if course details need updating
- Re-run generator after any changes

---

## ✨ **Made with ❤️ by BeyondGames Team**

**Automated Timetable Generation System**
- Smart conflict resolution
- CSV-based configuration
- Multi-department support
- Section-wise scheduling
- Production-ready output
