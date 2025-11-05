"""
Odd Semester Timetable Generator for IIIT Dharwad
Handles CSE, DSAI, ECE odd semester courses with classroom assignment from classroom.csv
"""
import pandas as pd
import os
import random
from collections import defaultdict

class OddSemesterTimetableGenerator:
    def __init__(self, input_folder='input_files/sdtt_inputs', classroom_file='../exam_timetable/inputs/classroom.csv'):
        self.input_folder = input_folder
        self.classroom_file = classroom_file
        
        # Load classrooms
        self.classrooms = self.load_classrooms()
        
        # Time slots
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.time_slots = {
            'morning': ['08:00-09:30', '09:30-11:00', '11:30-13:00'],
            'afternoon': ['14:00-16:00', '16:00-18:00']
        }
        
        # Track classroom usage: {day: {time_slot: classroom}}
        self.classroom_usage = defaultdict(lambda: defaultdict(set))
        
        # Track faculty schedules: {faculty: [(day, time_slot)]}
        self.faculty_schedule = defaultdict(list)
        
        # Common course schedules across departments/sections
        self.common_course_schedule = {}  # {course_code: [(day, time, classroom)]}
        
        # Timetables
        self.timetables = {}
        
    def load_classrooms(self):
        """Load classroom list from CSV"""
        try:
            df = pd.read_csv(self.classroom_file)
            classrooms = df['ID'].tolist()
            print(f"✓ Loaded {len(classrooms)} classrooms: {', '.join(classrooms[:5])}...")
            return classrooms
        except Exception as e:
            print(f"⚠ Could not load classrooms: {e}")
            # Fallback to default classrooms
            return ['C101', 'C102', 'C104', 'C201', 'C202', 'C203', 'C204', 'C205', 'C302', 
                    'C303', 'C304', 'L201', 'L202', 'L203', 'L301', 'L302']
    
    def is_classroom_available(self, day, time_slot, classroom):
        """Check if classroom is available at given time"""
        return classroom not in self.classroom_usage[day][time_slot]
    
    def get_available_classroom(self, day, time_slot, prefer_lab=False):
        """Get an available classroom for the given slot"""
        # Prefer labs for practicals
        if prefer_lab:
            for room in self.classrooms:
                if room.startswith('L') and self.is_classroom_available(day, time_slot, room):
                    return room
        
        # Otherwise, get any available classroom
        for room in self.classrooms:
            if self.is_classroom_available(day, time_slot, room):
                return room
        
        return None
    
    def mark_classroom_used(self, day, time_slot, classroom):
        """Mark a classroom as used"""
        self.classroom_usage[day][time_slot].add(classroom)
    
    def is_faculty_available(self, faculty, day, time_slot):
        """Check if faculty is available"""
        if pd.isna(faculty) or str(faculty).strip() in ['-', '']:
            return True
        return (day, time_slot) not in self.faculty_schedule[faculty]
    
    def mark_faculty_busy(self, faculty, day, time_slot):
        """Mark faculty as busy"""
        if not pd.isna(faculty) and str(faculty).strip() not in ['-', '']:
            self.faculty_schedule[faculty].append((day, time_slot))
    
    def schedule_course(self, course, day, time_slot, classroom):
        """Schedule a course in the timetable"""
        if day not in self.timetable_data:
            self.timetable_data[day] = {}
        
        if time_slot not in self.timetable_data[day]:
            self.timetable_data[day][time_slot] = []
        
        self.timetable_data[day][time_slot].append({
            'code': course['Course Code'] if 'Course Code' in course else course.get('course code', ''),
            'title': course['Course Title'] if 'Course Title' in course else course.get('course title', ''),
            'classroom': classroom,
            'faculty': course['Faculty'],
            'credits': course['Credits']
        })
        
        self.mark_classroom_used(day, time_slot, classroom)
        self.mark_faculty_busy(course['Faculty'], day, time_slot)
    
    def generate_timetable_for_dept_semester(self, df, dept, semester, section):
        """Generate timetable for specific department, semester, section"""
        print(f"\n  Processing {dept} Semester {semester} Section {section}...")
        
        self.timetable_data = {}
        available_slots = []
        for day in self.days:
            for time_type in ['morning', 'afternoon']:
                for time_slot in self.time_slots[time_type]:
                    available_slots.append((day, time_slot))
        
        random.shuffle(available_slots)
        slot_index = 0
        
        # Filter courses for this semester and section
        sem_courses = df[df['Semester'] == semester].copy()
        
        # Separate courses by type
        common_courses = []
        section_specific = []
        
        for idx, course in sem_courses.iterrows():
            course_code = course['Course Code'] if 'Course Code' in course else course.get('course code', '')
            
            # Skip empty courses
            if pd.isna(course_code) or str(course_code).strip() == '':
                continue
            
            # Check if common
            common_val = course.get('Common', course.get('common', 'N'))
            is_common = str(common_val).strip().upper() == 'Y'
            
            # Check section
            course_section = course.get('Section', '')
            
            if is_common:
                # Common across sections
                if course_code not in [c['Course Code'] if 'Course Code' in c else c.get('course code', '') 
                                       for c in common_courses]:
                    common_courses.append(course)
            elif pd.isna(course_section) or str(course_section).strip() == '':
                # No section specified, treat as common
                if course_code not in [c['Course Code'] if 'Course Code' in c else c.get('course code', '') 
                                       for c in common_courses]:
                    common_courses.append(course)
            elif str(course_section).strip().upper() == section:
                section_specific.append(course)
        
        # Schedule common courses first
        for course in common_courses:
            course_code = course['Course Code'] if 'Course Code' in course else course.get('course code', '')
            
            # Check if already scheduled (for Section B)
            schedule_key = f"{dept}_{semester}_{course_code}"
            if schedule_key in self.common_course_schedule:
                # Use existing schedule
                for day, time_slot, classroom in self.common_course_schedule[schedule_key]:
                    self.schedule_course(course, day, time_slot, classroom)
                continue
            
            # Schedule new
            lectures = course.get('Lectures', course.get('lectures', 0))
            tutorials = course.get('Tutorials', course.get('tutorials', 0))
            practicals = course.get('Practicals', course.get('Practicals', 0))
            
            # Convert to int
            try:
                lectures = int(lectures) if not pd.isna(lectures) else 0
                tutorials = int(tutorials) if not pd.isna(tutorials) else 0
                practicals = int(practicals) if not pd.isna(practicals) else 0
            except:
                lectures, tutorials, practicals = 0, 0, 0
            
            sessions = []
            if lectures > 0:
                num_lectures = int(lectures / 1.5) if lectures >= 1.5 else 1
                sessions.extend(['lecture'] * num_lectures)
            if tutorials > 0:
                sessions.extend(['tutorial'] * tutorials)
            if practicals > 0:
                num_labs = int(practicals / 2) if practicals >= 2 else 1
                sessions.extend(['lab'] * num_labs)
            
            scheduled_slots = []
            for session_type in sessions:
                while slot_index < len(available_slots):
                    day, time_slot = available_slots[slot_index]
                    slot_index += 1
                    
                    # Check faculty availability
                    if not self.is_faculty_available(course['Faculty'], day, time_slot):
                        continue
                    
                    # Get classroom
                    classroom = self.get_available_classroom(day, time_slot, prefer_lab=(session_type == 'lab'))
                    if classroom:
                        self.schedule_course(course, day, time_slot, classroom)
                        scheduled_slots.append((day, time_slot, classroom))
                        break
            
            # Save for Section B
            self.common_course_schedule[schedule_key] = scheduled_slots
        
        # Schedule section-specific courses
        for course in section_specific:
            lectures = course.get('Lectures', course.get('lectures', 0))
            tutorials = course.get('Tutorials', course.get('tutorials', 0))
            practicals = course.get('Practicals', course.get('Practicals', 0))
            
            try:
                lectures = int(lectures) if not pd.isna(lectures) else 0
                tutorials = int(tutorials) if not pd.isna(tutorials) else 0
                practicals = int(practicals) if not pd.isna(practicals) else 0
            except:
                lectures, tutorials, practicals = 0, 0, 0
            
            sessions = []
            if lectures > 0:
                num_lectures = int(lectures / 1.5) if lectures >= 1.5 else 1
                sessions.extend(['lecture'] * num_lectures)
            if tutorials > 0:
                sessions.extend(['tutorial'] * tutorials)
            if practicals > 0:
                num_labs = int(practicals / 2) if practicals >= 2 else 1
                sessions.extend(['lab'] * num_labs)
            
            for session_type in sessions:
                while slot_index < len(available_slots):
                    day, time_slot = available_slots[slot_index]
                    slot_index += 1
                    
                    if not self.is_faculty_available(course['Faculty'], day, time_slot):
                        continue
                    
                    classroom = self.get_available_classroom(day, time_slot, prefer_lab=(session_type == 'lab'))
                    if classroom:
                        self.schedule_course(course, day, time_slot, classroom)
                        break
        
        return self.timetable_data
    
    def export_to_excel(self, dept, semester, section):
        """Export timetable to Excel"""
        output_file = f"timetable_outputs/{dept}_Sem{semester}_Section{section}_Timetable.xlsx"
        
        # Create DataFrame
        rows = []
        for day in self.days:
            row = {'Day': day}
            for time_type in ['morning', 'afternoon']:
                for time_slot in self.time_slots[time_type]:
                    if day in self.timetable_data and time_slot in self.timetable_data[day]:
                        courses = self.timetable_data[day][time_slot]
                        cell_text = '\n'.join([f"{c['code']}\n{c['title']}\n{c['classroom']}\n{c['faculty']}" 
                                               for c in courses])
                        row[time_slot] = cell_text
                    else:
                        row[time_slot] = ''
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_excel(output_file, index=False)
        print(f"  ✓ Saved: {output_file}")
    
    def generate_all_timetables(self):
        """Generate timetables for all departments"""
        print("\n" + "="*60)
        print("🎓 ODD SEMESTER TIMETABLE GENERATOR - IIIT DHARWAD")
        print("="*60)
        
        # Create output directory
        os.makedirs('timetable_outputs', exist_ok=True)
        
        departments = {
            'CSE': 'CSE_course.csv',
            'DSAI': 'DSAI_course.csv',
            'ECE': 'ECE_course.csv'
        }
        
        for dept, filename in departments.items():
            file_path = os.path.join(self.input_folder, filename)
            
            if not os.path.exists(file_path):
                print(f"⚠ File not found: {file_path}")
                continue
            
            print(f"\n📚 Processing {dept}...")
            df = pd.read_csv(file_path)
            
            # Normalize column names
            df.columns = df.columns.str.strip()
            
            # Get unique semesters
            semesters = df['Semester'].unique()
            semesters = [s for s in semesters if not pd.isna(s)]
            
            for semester in sorted(semesters):
                for section in ['A', 'B']:
                    # Reset tracking for each timetable
                    self.classroom_usage = defaultdict(lambda: defaultdict(set))
                    self.faculty_schedule = defaultdict(list)
                    
                    timetable = self.generate_timetable_for_dept_semester(df, dept, semester, section)
                    self.export_to_excel(dept, int(semester), section)
        
        print("\n" + "="*60)
        print("✅ ALL TIMETABLES GENERATED SUCCESSFULLY!")
        print("="*60)

if __name__ == "__main__":
    generator = OddSemesterTimetableGenerator()
    generator.generate_all_timetables()
