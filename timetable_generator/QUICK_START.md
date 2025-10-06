# 🎯 Quick Reference Guide

## ✅ **What Was Generated**

### **18 Complete Timetables**
- ✅ **CSE**: 6 files (Sem 2, 4, 6 × Sections A, B)
- ✅ **DSAI**: 6 files (Sem 2, 4, 6 × Sections A, B)  
- ✅ **ECE**: 6 files (Sem 2, 4, 6 × Sections A, B)

---

## 📋 **Key Features Delivered**

### ✅ **All Your Requirements Met:**

1. ✅ **CSV-based input** - Reads from Even CSE.csv, Even DSAI.csv, Even ECE.csv
2. ✅ **LTPSC parsing** - Lectures, Tutorials, Practicals from CSV
3. ✅ **No classroom conflicts** - Different subjects never share same room at same time
4. ✅ **Lunch break** - 1:00 PM to 2:30 PM (13:00-14:30) reserved
5. ✅ **15-min breaks** - Between all time slots
6. ✅ **8 AM - 8 PM schedule** - Extended day coverage
7. ✅ **Monday to Friday** - 5-day week
8. ✅ **Correct durations**:
   - Classes: 1.5 hours
   - Labs: 2 hours  
   - Tutorials: 1 hour
9. ✅ **No same-day repetition** - Each subject scheduled only once per day
10. ✅ **Common courses** - Use 240-seater (C004) for both sections together
11. ✅ **Section-wise scheduling** - Separate timetables for A and B
12. ✅ **Semester-wise** - Individual files for each semester
13. ✅ **CSV Output** - Easy to import into Excel/Google Sheets
14. ✅ **HTML Viewer** - Interactive web-based timetable viewer

---

## 🎯 **Timetable Format**

### **Time Slots** (with 15-min breaks)
```
08:00-09:30  Slot 1 - Early morning
   [15 min break]
09:45-11:15  Slot 2
   [15 min break]
11:30-13:00  Slot 3
   [15 min break]
13:00-14:30  🍽️ LUNCH BREAK
   [15 min break]
14:45-16:15  Slot 4
   [15 min break]
16:30-18:00  Slot 5
   [15 min break]
18:15-19:45  Slot 6 - Evening
```

### **Session Labels**
- `CS163-A | C202` - Lecture for Section A
- `CS310-Lab-A | C104` - Lab for Section A (2-hour session)
- `MA202 (Common) | C004` - Common course (both sections)
- `DS357-T-B | C004` - Tutorial for Section B

---

## 📁 **File Locations**

### **Input Files**
```
timetable_generator/input_files/sdtt_inputs/
├── Even CSE.csv
├── Even DSAI.csv
└── Even ECE.csv
```

### **Output Files**
```
timetable_generator/timetable_outputs/
├── CSE_Sem2_SectionA_Timetable.xlsx
├── CSE_Sem2_SectionB_Timetable.xlsx
... (18 files total)
```

### **Generator Script**
```
timetable_generator/csv_timetable_generator.py
```

---

## 🚀 **How to Run**

### **Generate All Timetables**
```bash
cd timetable_generator
py csv_timetable_generator.py
```

### **Output**
- Creates 18 Excel files
- Prints timetables to console
- Shows warnings for unscheduled courses

---

## 🎨 **Sample Timetable View**

```
                  09:00-10:30            10:45-12:15     ...
Monday         CS163-A | C202         MA163-A | C202     ...
Tuesday      HS153-T-A | C004         HS204-A | C202     ...
Wednesday  CS163-Lab-A | C202  CS163-Lab (cont.) | C202  ...
Thursday   CS163-Lab-A | C202  CS163-Lab (cont.) | C202  ...
Friday         CS163-A | C202         MA163-A | C202     ...
```

---

## ⚙️ **Customization Options**

### **Modify Time Slots**
Edit in `csv_timetable_generator.py`:
```python
self.time_slots = [
    ('09:00', '10:30'),  # Change times here
    ('10:45', '12:15'),
    ...
]
```

### **Change Lunch Time**
```python
self.lunch_slot = ('14:00', '15:30')  # Modify lunch timing
```

### **Update Large Auditorium**
```python
self.large_auditorium = 'C004'  # Change room for common courses
```

---

## ✨ **Features Highlight**

### **Intelligent Scheduling**
- ✅ Avoids classroom conflicts
- ✅ Prevents same-day course repetition
- ✅ Respects lunch break
- ✅ Handles common vs section-specific courses
- ✅ Allocates 2-hour lab sessions properly

### **CSV Integration**
- ✅ Reads course details directly from CSV
- ✅ Parses LTPSC format automatically
- ✅ Supports multiple departments
- ✅ Handles electives and basket courses

### **Multi-Department Support**
- ✅ CSE, DSAI, ECE in single run
- ✅ Separate configurations per department
- ✅ Common course detection
- ✅ Section-wise scheduling

---

## 🎓 **Perfect for IIIT Dharwad**

✨ **Production-ready timetables for:**
- Even semester scheduling
- Multi-department coordination
- Section-wise class management
- Efficient classroom utilization
- No scheduling conflicts

---

**Made with ❤️ by BeyondGames Team**
