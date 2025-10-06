"""
BeyondGames Automated Timetable Generator - Main Module
=====================================================

This is the main timetable generation system for IIIT Dharwad.
It reads course data from CSV files and generates optimized weekly schedules.

Author: BeyondGames Team
Version: 2.0.0 (CSV-based)
"""
import pandas as pd
import os
from datetime import datetime, timedelta
import random

class TimetableGenerator:
    def __init__(self, csv_folder='input_files/sdtt_inputs'):
        self.csv_folder = csv_folder
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']  # Monday to Friday only
        
        # Extended time slots (8 AM - 8 PM, Lunch 1:30-2:30 PM)
        self.time_slots = [
            ('08:00', '09:30'),  # 1.5 hours - Early morning slot
            ('09:45', '11:15'),  # 1.5 hours
            ('11:30', '13:00'),  # 1.5 hours
            ('13:00', '14:30'),  # LUNCH BREAK
            ('14:45', '16:15'),  # 1.5 hours
            ('16:30', '18:00'),  # 1.5 hours
            ('18:15', '19:45'),  # 1.5 hours - Evening slot
        ]
        
        self.lunch_slot = ('13:00', '14:30')  # Updated lunch time
        self.large_auditorium = 'C004'  # 240-seater for common courses
        
        # Lab rooms for practical sessions
        self.lab_rooms = ['Lab-1', 'Lab-2', 'Lab-3', 'Lab-4', 'Lab-5']
        self.unscheduled_courses = []  # Track courses that couldn't be scheduled
        
        # Allow same course on same day if needed (for electives with many lectures)
        self.allow_same_day_repeat = True
        self.max_lectures_per_day = 4  # Maximum lectures per course per day (increased from 3)
        
    def load_department_data(self, department):
        """Load CSV data for a specific department"""
        csv_file = os.path.join(self.csv_folder, f'Even {department}.csv')
        if not os.path.exists(csv_file):
            print(f"Warning: {csv_file} not found")
            return None
        
        df = pd.read_csv(csv_file)
        # Clean column names
        df.columns = df.columns.str.strip()
        return df
    
    def get_courses_by_semester(self, df, semester):
        """Filter courses for a specific semester"""
        return df[df['Semester'] == semester].copy()
    
    def is_common_course(self, row):
        """Check if course is common across sections"""
        elective = str(row.get('Electives', '')).strip().upper()
        section = str(row.get('Section', '')).strip()
        
        # Common if it's a foundation course (F) without specific section
        return elective == 'F' and section == ''
    
    def parse_ltpsc(self, row):
        """Parse LTPSC values"""
        lectures = int(row.get('Lectures', 0))
        tutorials = int(row.get('Tutorials', 0))
        practicals = int(row.get('Practicals', 0))
        return lectures, tutorials, practicals
    
    def generate_timetable(self, department, semester, section='A'):
        """Generate timetable for a specific department, semester, and section"""
        print(f"\n{'='*80}")
        print(f"Generating Timetable: {department} - Semester {semester} - Section {section}")
        print(f"{'='*80}")
        
        # Reset unscheduled courses tracker
        self.unscheduled_courses = []
        
        df = self.load_department_data(department)
        if df is None:
            return None
        
        courses_df = self.get_courses_by_semester(df, semester)
        if courses_df.empty:
            print(f"No courses found for Semester {semester}")
            return None
        
        # Initialize timetable
        timetable = self._initialize_timetable()
        
        # Track used slots and available lab rooms per slot
        used_slots = {}  # {day: {time_slot: {'room': room, 'course': course}}}
        course_schedule = {}  # {course_code: {day: count}}
        lab_usage = {}  # {day: {time_slot: [used_labs]}}
        
        for day in self.days:
            used_slots[day] = {}
            lab_usage[day] = {}
            for time_slot in self.time_slots:
                lab_usage[day][f"{time_slot[0]}-{time_slot[1]}"] = []
        
        # First, schedule common courses (both sections together)
        common_courses = courses_df[courses_df.apply(self.is_common_course, axis=1)]
        section_courses = courses_df[~courses_df.apply(self.is_common_course, axis=1)]
        
        # Filter section-specific courses
        if not section_courses.empty and 'Section' in section_courses.columns:
            section_letter = str(semester) + section
            section_courses = section_courses[
                (section_courses['Section'].str.strip() == section_letter) |
                (section_courses['Section'].str.strip() == '') |
                (section_courses['Section'].isna())
            ]
        
        print(f"\n📚 Total courses to schedule:")
        print(f"   Common courses: {len(common_courses)}")
        print(f"   Section-specific courses: {len(section_courses)}")
        
        # Schedule common courses first
        self._schedule_courses(common_courses, timetable, used_slots, course_schedule, 
                              lab_usage, section, is_common=True)
        
        # Schedule section-specific courses
        self._schedule_courses(section_courses, timetable, used_slots, course_schedule, 
                              lab_usage, section, is_common=False)
        
        # Report unscheduled courses
        if self.unscheduled_courses:
            print(f"\n⚠️  WARNING: {len(self.unscheduled_courses)} sessions could not be scheduled:")
            for item in self.unscheduled_courses:
                print(f"   - {item}")
        else:
            print(f"\n✅ All courses scheduled successfully!")
        
        return timetable
    
    def _initialize_timetable(self):
        """Initialize empty timetable"""
        timetable = {}
        for day in self.days:
            timetable[day] = {}
            for time_slot in self.time_slots:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                if time_slot == self.lunch_slot:
                    timetable[day][time_str] = 'LUNCH BREAK'
                else:
                    timetable[day][time_str] = 'Free'
        return timetable
    
    def _schedule_courses(self, courses_df, timetable, used_slots, course_schedule, 
                         lab_usage, section, is_common=False):
        """Schedule courses into timetable"""
        for _, course in courses_df.iterrows():
            course_code = course['Course Code'].strip()
            course_title = course['Course Title'].strip()
            classroom = str(course.get('Classroom', '')).strip()
            
            # Use large auditorium for common courses
            if is_common:
                classroom = self.large_auditorium
            
            lectures, tutorials, practicals = self.parse_ltpsc(course)
            
            # Initialize course schedule tracking
            if course_code not in course_schedule:
                course_schedule[course_code] = {}
                for day in self.days:
                    course_schedule[course_code][day] = 0
            
            print(f"\n   Scheduling: {course_code} - L:{lectures} T:{tutorials} P:{practicals}")
            
            # Schedule lectures (1.5 hours each)
            for lec_num in range(lectures):
                success = self._schedule_session(
                    timetable, used_slots, course_schedule, lab_usage,
                    course_code, course_title, classroom,
                    'Lecture', section, is_common
                )
                if not success:
                    self.unscheduled_courses.append(f"{course_code} - Lecture {lec_num+1}")
            
            # Schedule tutorials (1 hour - use 1 slot)
            for tut_num in range(tutorials):
                success = self._schedule_session(
                    timetable, used_slots, course_schedule, lab_usage,
                    course_code, course_title, classroom,
                    'Tutorial', section, is_common, duration_hours=1
                )
                if not success:
                    self.unscheduled_courses.append(f"{course_code} - Tutorial {tut_num+1}")
            
            # Schedule practicals/labs (2 hours - use 2 consecutive slots)
            for prac_num in range(practicals):
                success = self._schedule_lab_session(
                    timetable, used_slots, course_schedule, lab_usage,
                    course_code, course_title, classroom,
                    section, is_common
                )
                if not success:
                    self.unscheduled_courses.append(f"{course_code} - Lab {prac_num+1}")
    
    def _schedule_session(self, timetable, used_slots, course_schedule, lab_usage,
                         course_code, course_title, classroom, session_type,
                         section, is_common, duration_hours=1.5):
        """Schedule a single session"""
        max_attempts = 200  # Increased from 50
        
        # Get available time slots (excluding lunch)
        available_slots = [slot for slot in self.time_slots if slot != self.lunch_slot]
        
        # Try each day systematically, then randomize within day
        for day in self.days:
            # Don't schedule same course too many times on same day
            if course_schedule[course_code][day] >= 2 and not self.allow_same_day_repeat:
                continue
            if course_schedule[course_code][day] >= self.max_lectures_per_day:
                continue
            
            # Try each time slot in this day
            for time_slot in available_slots:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                
                # Check if slot is free in timetable
                if timetable[day][time_str] != 'Free':
                    continue
                
                # Check classroom conflict (different courses can use different rooms at same time)
                conflict = False
                if day in used_slots and time_str in used_slots[day]:
                    for existing_slot in used_slots[day][time_str].values():
                        if existing_slot.get('room') == classroom:
                            conflict = True
                            break
                
                if conflict:
                    continue
                
                # Schedule the session
                if is_common:
                    label = f"{course_code} (Common)"
                else:
                    if session_type == 'Tutorial':
                        label = f"{course_code}-T-{section}"
                    elif session_type == 'Lab':
                        label = f"{course_code}-P-{section}"
                    else:
                        label = f"{course_code}-{section}"
                
                timetable[day][time_str] = f"{label} | {classroom}"
                
                # Mark as used (allow multiple entries for different rooms)
                if day not in used_slots:
                    used_slots[day] = {}
                if time_str not in used_slots[day]:
                    used_slots[day][time_str] = {}
                
                used_slots[day][time_str][course_code] = {'room': classroom, 'course': course_code}
                
                # Update course schedule
                course_schedule[course_code][day] += 1
                
                return True
        
        print(f"      ⚠️  Could not schedule {course_code} - {session_type}")
        return False
    
    def _schedule_lab_session(self, timetable, used_slots, course_schedule, lab_usage,
                             course_code, course_title, classroom, section, is_common):
        """Schedule a 2-hour lab session (2 consecutive slots) - uses Lab rooms"""
        
        # Find consecutive slots (excluding lunch)
        available_slots = [slot for slot in self.time_slots if slot != self.lunch_slot]
        
        # Try each day systematically
        for day in self.days:
            # Labs can be scheduled once per day
            if course_schedule[course_code][day] > 0:
                continue
            
            # Try consecutive slots
            for i in range(len(available_slots) - 1):
                slot1 = available_slots[i]
                slot2 = available_slots[i + 1]
                
                time_str1 = f"{slot1[0]}-{slot1[1]}"
                time_str2 = f"{slot2[0]}-{slot2[1]}"
                
                # Check both slots are free
                if (timetable[day][time_str1] != 'Free' or 
                    timetable[day][time_str2] != 'Free'):
                    continue
                
                # Find an available lab room for both slots
                used_labs_1 = lab_usage[day].get(time_str1, [])
                used_labs_2 = lab_usage[day].get(time_str2, [])
                
                available_lab = None
                for lab in self.lab_rooms:
                    if lab not in used_labs_1 and lab not in used_labs_2:
                        available_lab = lab
                        break
                
                if available_lab:
                    # Schedule both slots with lab room
                    if is_common:
                        label = f"{course_code}-Lab (Common)"
                    else:
                        label = f"{course_code}-Lab-{section}"
                    
                    timetable[day][time_str1] = f"{label} | {available_lab}"
                    timetable[day][time_str2] = f"{label} (cont.) | {available_lab}"
                    
                    # Mark lab as used
                    lab_usage[day][time_str1].append(available_lab)
                    lab_usage[day][time_str2].append(available_lab)
                    
                    # Mark in used_slots (allow multiple entries for different labs)
                    if day not in used_slots:
                        used_slots[day] = {}
                    if time_str1 not in used_slots[day]:
                        used_slots[day][time_str1] = {}
                    if time_str2 not in used_slots[day]:
                        used_slots[day][time_str2] = {}
                    
                    used_slots[day][time_str1][course_code] = {'room': available_lab, 'course': course_code}
                    used_slots[day][time_str2][course_code] = {'room': available_lab, 'course': course_code}
                    
                    # Update course schedule
                    course_schedule[course_code][day] += 2
                    
                    return True
        
        print(f"      ⚠️  Could not schedule lab for {course_code}")
        return False
    
    def export_to_csv(self, timetable, filename):
        """Export timetable to CSV"""
        if timetable is None:
            return False
        
        # Convert to DataFrame
        df = pd.DataFrame(timetable).T
        
        output_dir = 'timetable_outputs'
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Export to CSV with proper formatting
        df.to_csv(filepath, index=True, encoding='utf-8')
        
        print(f"✅ Timetable saved: {filepath}")
        return True
    
    def print_timetable(self, timetable):
        """Print timetable to console"""
        if timetable is None:
            return
        
        df = pd.DataFrame(timetable).T
        print("\n" + str(df))
        print("\n" + "="*80)

def main():
    """Main function to generate all timetables"""
    generator = TimetableGenerator()
    
    departments = ['CSE', 'DSAI', 'ECE']
    semesters = [2, 4, 6]
    sections = ['A', 'B']
    
    print("\n🎓 BeyondGames Enhanced Timetable Generator")
    print("="*80)
    print("Generating timetables from CSV files...")
    print("="*80)
    
    for dept in departments:
        for sem in semesters:
            for sec in sections:
                timetable = generator.generate_timetable(dept, sem, sec)
                
                if timetable:
                    generator.print_timetable(timetable)
                    filename = f"{dept}_Sem{sem}_Section{sec}_Timetable.csv"
                    generator.export_to_csv(timetable, filename)
    
    print("\n✅ All timetables generated successfully!")
    print(f"📁 CSV Output location: timetable_outputs/")
    print(f"📁 HTML Output location: timetable_html/")

if __name__ == "__main__":
    main()
