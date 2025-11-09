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

# Import time configuration
try:
    from time_config import (
        get_active_config, 
        SATURDAY_ENABLED_FOR,
        validate_time_config,
        print_time_config
    )
    USE_TIME_CONFIG = True
except ImportError:
    print("Warning: time_config.py not found. Using default time slots.")
    USE_TIME_CONFIG = False

class TimetableGenerator:
    def __init__(self, csv_folder='input_files/sdtt_inputs'):
        self.csv_folder = csv_folder
        
        # Load time configuration from time_config.py
        if USE_TIME_CONFIG:
            config = get_active_config()
            self.days = config['working_days']
            self.regular_slots = config['regular_slots']
            self.lunch_slot = config['lunch_slot']
            self.afternoon_flex_slots = config['afternoon_slots']
            
            # Print loaded configuration
            print("\n" + "="*80)
            print("TIME CONFIGURATION LOADED FROM time_config.py")
            print("="*80)
            print(f"Working Days: {', '.join(self.days)}")
            print(f"Regular Slots: {len(self.regular_slots)} slots")
            print(f"Afternoon Slots: {len(self.afternoon_flex_slots)} slots")
            print("="*80 + "\n")
        else:
            # Fallback to default configuration
            self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            self.regular_slots = [
                ('08:00', '09:30'),
                ('09:45', '11:15'),
                ('11:30', '13:00'),
            ]
            self.lunch_slot = ('13:00', '14:30')
            self.afternoon_flex_slots = [
                ('14:30', '16:30'),
                ('16:30', '18:30'),
            ]
        
        # Track cross-department shared courses (DSAI + ECE)
        # Format: {semester: {course_code: {day: ..., time: ..., classroom: ...}}}
        self.cross_dept_shared_schedule = {}
        
        # Track global elective schedule - all departments/sections use same slots per basket per semester
        # Format: {semester: {basket: [(day, time_str, duration_minutes), ...]}}
        self.global_elective_schedule = {}
        
        # Track elective classroom assignments for summary display
        # Format: {course_code: classroom} - tracks ACTUAL assigned classrooms per individual course
        self.elective_classroom_assignments = {}
        
        # Elective rotation strategy: Only schedule certain baskets per semester
        # Even semesters (2, 4, 6): Baskets B1, B3, E1 (+ Minor for Sem 4 only)
        # Odd semesters would get: Baskets B2, B4, E2 (if implemented)
        self.elective_rotation = {
            2: ['B1', 'B3', 'B4', 'E1'],  # Semester 2: Allow B4 for now (HS courses)
            4: ['B1', 'B3', 'Minor'],     # Semester 4: Core electives + Minor
            6: ['B1', 'B3', 'E1']         # Semester 6: Advanced electives
        }
        
        # Combined time slots for timetable display
        self.time_slots = self.regular_slots + [self.lunch_slot] + self.afternoon_flex_slots
        self.large_auditorium = 'C004'  # 240-seater for common courses (primary)
        
        # Backup large classrooms for common courses when C004 is unavailable
        # These can accommodate multiple sections together
        self.backup_large_classrooms = ['C101', 'C102', 'C103', 'C202', 'C203', 'C204', 'C205']
        
        # Lab rooms for practical sessions
        self.lab_rooms = ['Lab-1', 'Lab-2', 'Lab-3', 'Lab-4', 'Lab-5']
        self.unscheduled_courses = []  # Track courses that couldn't be scheduled
        self.elective_courses = {}  # Track elective courses by basket
        
        # GLOBAL classroom tracker - shared across ALL semesters and sections
        # Format: global_classroom_usage[day][time_str][classroom] = {'dept': ..., 'semester': ..., 'section': ..., 'course': ...}
        self.global_classroom_usage = {}
        
        # COMMON COURSE SCHEDULE - shared within department across sections (e.g., CSE A+B together)
        # Format: common_course_schedule[dept][semester] = {course_code: [(day, time_str, classroom, label), ...]}
        self.common_course_schedule = {}
        
        # Strict scheduling rules: max 1 lecture/tutorial/lab per course per day
        # But allow lecture+lab or tutorial+lab on same day
        self.max_lectures_per_day = 1
        self.max_tutorials_per_day = 1
        self.max_labs_per_day = 1
        
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
    
    def find_cross_dept_shared_courses(self, semester):
        """
        Find courses that are shared between DSAI and ECE for a given semester.
        Returns dict of {course_code: course_details_from_either_dept}
        """
        dsai_df = self.load_department_data('DSAI')
        ece_df = self.load_department_data('ECE')
        
        if dsai_df is None or ece_df is None:
            return {}
        
        dsai_courses = self.get_courses_by_semester(dsai_df, semester)
        ece_courses = self.get_courses_by_semester(ece_df, semester)
        
        if dsai_courses.empty or ece_courses.empty:
            return {}
        
        # Find common course codes
        dsai_codes = set(dsai_courses['Course Code'].str.strip())
        ece_codes = set(ece_courses['Course Code'].str.strip())
        
        shared_codes = dsai_codes.intersection(ece_codes)
        
        # Get course details for shared courses (use DSAI version)
        shared_courses = {}
        for code in shared_codes:
            course_row = dsai_courses[dsai_courses['Course Code'].str.strip() == code].iloc[0]
            shared_courses[code] = course_row.to_dict()
        
        if shared_courses:
            print(f"\n   >> Found {len(shared_courses)} shared courses between DSAI and ECE:")
            for code in shared_courses.keys():
                print(f"      - {code}: {shared_courses[code].get('Course Title', 'N/A')}")
        
        return shared_courses
    
    def is_common_course(self, row):
        """Check if course is common across sections"""
        import pandas as pd
        elective = str(row.get('Electives', '')).strip().upper()
        section = row.get('Section', '')
        
        # Common if it's a foundation course (F) without specific section
        # Section is empty if it's NaN, None, or empty string
        section_empty = pd.isna(section) or str(section).strip() == ''
        return elective == 'F' and section_empty
    
    def is_elective_course(self, row):
        """Check if course is an elective (Type elective)"""
        elective = str(row.get('Electives', '')).strip().upper()
        return elective == 'T'
    
    def get_elective_basket(self, row):
        """Get the basket name for elective course"""
        return str(row.get('Basket', '')).strip()
    
    def parse_ltpsc(self, row):
        """
        Parse LTPSC values and convert to number of sessions per week.
        
        LTPSC Interpretation:
        - L (Lectures): Total lecture HOURS per week
          Each lecture session = 1.5 hours (90 minutes)
          Number of lecture sessions = L / 1.5 = L * 2 / 3
          Example: L=3 means 3 hours/week = 2 sessions of 1.5 hours each
        
        - T (Tutorials): Total tutorial HOURS per week
          Each tutorial session = 1 hour (60 minutes)
          Number of tutorial sessions = T / 1 = T
          Example: T=1 means 1 hour/week = 1 session of 1 hour
        
        - P (Practicals): Total practical/lab HOURS per week
          Each lab session = 2 hours (120 minutes)
          Number of lab sessions = P / 2
          Example: P=2 means 2 hours/week = 1 session of 2 hours
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
    
    def _get_day_priority_order(self, timetable):
        """
        Calculate priority order for days based on current usage.
        Returns days sorted by number of free slots (most free first).
        This helps fill underutilized days like Friday.
        """
        day_free_count = {}
        
        for day in self.days:
            free_count = 0
            for time_slot in self.time_slots:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                if time_slot != self.lunch_slot and timetable[day][time_str] == 'Free':
                    free_count += 1
            day_free_count[day] = free_count
        
        # Sort days by free slots (descending) - prioritize days with most free slots
        # This will schedule to Friday (usually has most free) before it fills up Monday-Thursday
        sorted_days = sorted(self.days, key=lambda d: day_free_count[d], reverse=True)
        return sorted_days
    
    def _record_global_classroom_usage(self, day, time_str, classroom, department, semester, section, course_code):
        """Record classroom usage globally across all semesters to prevent double-booking"""
        if day not in self.global_classroom_usage:
            self.global_classroom_usage[day] = {}
        if time_str not in self.global_classroom_usage[day]:
            self.global_classroom_usage[day][time_str] = {}
        
        self.global_classroom_usage[day][time_str][classroom] = {
            'dept': department,
            'semester': semester,
            'section': section,
            'course': course_code
        }
    
    def _find_available_large_classroom(self, day, time_str, is_elective=False):
        """Find an available large classroom for common courses or electives.
        
        Args:
            day: Day of the week
            time_str: Time slot string
            is_elective: If True, skip C004 and only use backup classrooms
        
        Returns:
            Classroom name or None if no classroom available
        """
        # DEBUG: Print what we're doing
        # print(f"      [DEBUG] Finding classroom for {day} {time_str}, is_elective={is_elective}")
        
        # For electives: NEVER use C004, only backup classrooms
        if is_elective:
            # Skip C004 entirely for electives
            if day not in self.global_classroom_usage or time_str not in self.global_classroom_usage[day]:
                # Return first backup classroom
                result = self.backup_large_classrooms[0] if self.backup_large_classrooms else None
                # print(f"      [DEBUG] Elective: No conflicts, using {result}")
                return result
            
            # Try backup classrooms only
            for backup_classroom in self.backup_large_classrooms:
                if backup_classroom not in self.global_classroom_usage[day][time_str]:
                    # print(f"      [DEBUG] Elective: Found available backup {backup_classroom}")
                    return backup_classroom
            
            # All backup classrooms taken
            # print(f"      [DEBUG] Elective: All backup classrooms taken!")
            return None
        
        # For common courses: Try C004 first, then backups
        if day not in self.global_classroom_usage or time_str not in self.global_classroom_usage[day]:
            return self.large_auditorium
        
        if self.large_auditorium not in self.global_classroom_usage[day][time_str]:
            return self.large_auditorium
        
        # C004 is taken, try backup classrooms
        for backup_classroom in self.backup_large_classrooms:
            if backup_classroom not in self.global_classroom_usage[day][time_str]:
                return backup_classroom
        
        # All large classrooms taken
        return None
    
    def generate_timetable(self, department, semester, section='A'):
        """Generate timetable for a specific department, semester, and section"""
        print(f"\n{'='*80}")
        print(f"Generating Timetable: {department} - Semester {semester} - Section {section}")
        print(f"{'='*80}")
        
        # Dynamic Saturday scheduling based on configuration
        if USE_TIME_CONFIG:
            config = get_active_config()
            dept_key = (department, semester)
            if dept_key in SATURDAY_ENABLED_FOR and SATURDAY_ENABLED_FOR[dept_key]:
                if 'Saturday' in config['working_days']:
                    self.days = config['working_days']
                    print(f">> Saturday classes enabled for {department} Semester {semester} (high load optimization)")
                else:
                    # If Saturday not in config, use Mon-Fri
                    self.days = [day for day in config['working_days'] if day != 'Saturday']
            else:
                # Use configured working days without Saturday
                self.days = [day for day in config['working_days'] if day != 'Saturday']
        else:
            # Fallback to hardcoded behavior
            if department == 'ECE' and semester == 4:
                self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                print(f">> Saturday classes enabled for ECE Semester 4 (high load optimization)")
            else:
                self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        # Store current context for global classroom tracking
        self.current_department = department
        self.current_semester = semester
        self.current_section = section
        
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
        
        # Track session types separately for each course
        lecture_schedule = {}  # {course_code: {day: count}}
        tutorial_schedule = {}  # {course_code: {day: count}}
        lab_schedule = {}  # {course_code: {day: count}}
        lab_usage = {}  # {day: {time_slot: [used_labs]}}
        
        # Reset elective tracking
        self.elective_courses = {}
        self.rotated_out_electives = {}  # Track electives rotated out for "After Midsems"
        
        for day in self.days:
            used_slots[day] = {}
            lab_usage[day] = {}
            for time_slot in self.time_slots:
                lab_usage[day][f"{time_slot[0]}-{time_slot[1]}"] = []
        
        # Handle cross-department shared courses for DSAI and ECE
        if department in ['DSAI', 'ECE'] and semester in self.cross_dept_shared_schedule:
            # Find which courses in this department's schedule are shared
            shared_course_codes = self.find_cross_dept_shared_courses(semester).keys()
            courses_df['Course Code Stripped'] = courses_df['Course Code'].str.strip()
            cross_dept_courses = courses_df[courses_df['Course Code Stripped'].isin(shared_course_codes)]
            print(f"\n   >> {len(cross_dept_courses)} cross-department shared courses found for {department}")
        else:
            # For CSE or when no shared courses exist, use empty DataFrame
            cross_dept_courses = courses_df[courses_df['Course Code'] == 'NONEXISTENT']  # Empty DataFrame
        
        # First, schedule common courses (both sections together)
        common_courses = courses_df[courses_df.apply(self.is_common_course, axis=1)]
        section_courses = courses_df[~courses_df.apply(self.is_common_course, axis=1)]
        
        # IMPORTANT: Exclude cross-department courses from common courses to avoid double-scheduling
        if not cross_dept_courses.empty:
            cross_dept_course_codes = cross_dept_courses['Course Code'].str.strip().tolist()
            common_courses = common_courses[~common_courses['Course Code'].str.strip().isin(cross_dept_course_codes)]
        
        # Filter section-specific courses
        # Include: courses with matching section OR courses that are electives (empty section but Type=T)
        if not section_courses.empty and 'Section' in section_courses.columns:
            section_letter = str(semester) + section
            section_courses = section_courses[
                (section_courses['Section'].str.strip() == section_letter) |
                ((section_courses['Section'].str.strip() == '') & (section_courses['Electives'].str.strip().str.upper() == 'T')) |
                (section_courses['Section'].isna() & (section_courses['Electives'].str.strip().str.upper() == 'T'))
            ]
        
        print(f"\nTotal courses to schedule:")
        print(f"   Cross-department shared (DSAI+ECE): {len(cross_dept_courses)}")
        print(f"   Common courses (within dept): {len(common_courses)}")
        print(f"   Section-specific courses: {len(section_courses)}")
        
        # PRIORITY 1: Schedule cross-department shared courses (DSAI + ECE together)
        if not cross_dept_courses.empty:
            self._schedule_cross_dept_courses(cross_dept_courses, timetable, used_slots, 
                                             lecture_schedule, tutorial_schedule, lab_schedule,
                                             lab_usage, section, semester, department)
        
        # PRIORITY 2: Schedule common courses (within department, both sections together)
        # For DSAI/ECE (no sections), don't mark as "common" - they're just regular courses
        is_truly_common = True if department not in ['DSAI', 'ECE'] else False
        
        if is_truly_common and not common_courses.empty:
            # Check if common courses are already scheduled (for Section B, copy from Section A)
            if section == 'B' and department in self.common_course_schedule and semester in self.common_course_schedule[department]:
                # Copy Section A's common course schedule to Section B
                print(f"   >> Reusing common course schedule from Section A (same times + classrooms)")
                self._copy_common_course_schedule(timetable, used_slots, department, semester)
            elif section == 'A':
                # For Section A, schedule common courses and save the schedule
                self._schedule_courses(common_courses, timetable, used_slots, 
                                      lecture_schedule, tutorial_schedule, lab_schedule,
                                      lab_usage, section, semester, is_common=True)
                # Save the scheduled common courses for Section B to reuse
                self._save_common_course_schedule(timetable, common_courses, department, semester)
        else:
            # For DSAI/ECE or non-common courses, schedule normally
            self._schedule_courses(common_courses, timetable, used_slots, 
                                  lecture_schedule, tutorial_schedule, lab_schedule,
                                  lab_usage, section, semester, is_common=False)
        
        # PRIORITY 3: Schedule section-specific courses
        self._schedule_courses(section_courses, timetable, used_slots,
                              lecture_schedule, tutorial_schedule, lab_schedule,
                              lab_usage, section, semester, is_common=False)
        
        # Report unscheduled courses
        if self.unscheduled_courses:
            print(f"\nWARNING: {len(self.unscheduled_courses)} sessions could not be scheduled:")
            for item in self.unscheduled_courses:
                print(f"   - {item}")
        else:
            print(f"\nAll courses scheduled successfully!")
        
        # Return timetable with elective information and rotated-out courses
        return timetable, self.elective_courses, self.rotated_out_electives
    
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
    
    def _schedule_cross_dept_courses(self, courses_df, timetable, used_slots,
                                     lecture_schedule, tutorial_schedule, lab_schedule,
                                     lab_usage, section, semester, department):
        """
        Schedule courses that are shared between DSAI and ECE departments.
        These courses must be scheduled at the same time for both departments.
        """
        for _, course in courses_df.iterrows():
            course_code = course['Course Code'].strip()
            
            # Check if this course has already been scheduled by the other department
            if semester in self.cross_dept_shared_schedule and \
               course_code in self.cross_dept_shared_schedule[semester]:
                # Use ALL pre-scheduled time slots
                scheduled_slots = self.cross_dept_shared_schedule[semester][course_code]
                
                print(f"   [OK] {course_code} - Using {len(scheduled_slots)} pre-scheduled slots (Shared with {'ECE' if department=='DSAI' else 'DSAI'})")
                
                for slot_info in scheduled_slots:
                    day = slot_info['day']
                    time_slot = slot_info['time_slot']
                    classroom = slot_info['classroom']
                    session_type = slot_info['session_type']
                    time_str = slot_info['time_str']
                    
                    # Add to timetable
                    timetable[day][time_str] = f"{course_code}\n({session_type})\n{classroom}\n[Shared: DSAI+ECE]"
                    
                    # Mark slot as used
                    if day not in used_slots:
                        used_slots[day] = {}
                    used_slots[day][time_str] = {'room': classroom, 'course': course_code}
                    
                    print(f"       • {day} {time_str} ({session_type}) in {classroom}")
                continue
            
            # This is the first department scheduling this course - schedule it normally
            # but save the schedule for the other department to use
            # Schedule with highest priority using large classrooms
            # Create a single-row DataFrame for this course
            single_course_df = pd.DataFrame([course])
            self._schedule_courses(single_course_df, timetable, used_slots,
                                 lecture_schedule, tutorial_schedule, lab_schedule,
                                 lab_usage, section, semester, is_common=True)
            
            # After scheduling, save ALL schedules for the other department
            # Find ALL slots where this course was scheduled in the timetable
            course_slots = []
            for day in timetable:
                for time_str, entry in timetable[day].items():
                    if course_code in str(entry) and entry != 'Free' and time_str != '13:00-14:30':
                        # Parse time_str back to time_slot tuple
                        start_time, end_time = time_str.split('-')
                        time_slot = (start_time, end_time)
                        
                        # Extract classroom and session type from entry
                        # Format is: "CS162 (Common) | C004" or "CS162-Lecture | C101"
                        entry_str = str(entry)
                        
                        # Extract classroom (after the | symbol)
                        if '|' in entry_str:
                            classroom = entry_str.split('|')[-1].strip()
                        else:
                            classroom = 'C004'  # Default to large auditorium
                        
                        # Extract session type (from parentheses or dash)
                        if '(Common)' in entry_str:
                            session_type = 'Lecture'
                        elif '-Lab' in entry_str:
                            session_type = 'Lab'
                        elif '-T-' in entry_str:
                            session_type = 'Tutorial'
                        else:
                            session_type = 'Lecture'
                        
                        course_slots.append({
                            'day': day,
                            'time_slot': time_slot,
                            'time_str': time_str,
                            'classroom': classroom,
                            'session_type': session_type
                        })
            
            # Save ALL slots for other department
            if course_slots:
                if semester not in self.cross_dept_shared_schedule:
                    self.cross_dept_shared_schedule[semester] = {}
                
                self.cross_dept_shared_schedule[semester][course_code] = course_slots
                
                print(f"   [OK] {course_code} - Scheduled {len(course_slots)} sessions for both DSAI and ECE")
                for slot in course_slots:
                    print(f"       • {slot['day']} {slot['time_str']} ({slot['session_type']}) in {slot['classroom']}")
    
    def _save_common_course_schedule(self, timetable, common_courses_df, department, semester):
        """
        Save common course schedule from Section A for Section B to reuse.
        Ensures both sections have SAME time slots AND classrooms.
        """
        if department not in self.common_course_schedule:
            self.common_course_schedule[department] = {}
        if semester not in self.common_course_schedule[department]:
            self.common_course_schedule[department][semester] = {}
        
        # Extract all common course slots from the current timetable
        for _, course in common_courses_df.iterrows():
            course_code = course['Course Code'].strip()
            course_slots = []
            
            for day in timetable:
                for time_str, entry in timetable[day].items():
                    if course_code in str(entry) and entry not in ['Free', 'LUNCH BREAK']:
                        # Parse classroom from entry
                        entry_str = str(entry)
                        if '|' in entry_str:
                            classroom = entry_str.split('|')[-1].strip()
                        else:
                            classroom = 'C004'
                        
                        course_slots.append({
                            'day': day,
                            'time_str': time_str,
                            'classroom': classroom,
                            'entry': entry_str
                        })
            
            if course_slots:
                self.common_course_schedule[department][semester][course_code] = course_slots
                print(f"   [SAVED] {course_code} - {len(course_slots)} slots saved for Section B reuse")
    
    def _copy_common_course_schedule(self, timetable, used_slots, department, semester):
        """
        Copy Section A's common course schedule to Section B.
        Both sections will have identical time slots and classrooms.
        """
        if department not in self.common_course_schedule or semester not in self.common_course_schedule[department]:
            return
        
        saved_schedule = self.common_course_schedule[department][semester]
        
        for course_code, course_slots in saved_schedule.items():
            for slot_info in course_slots:
                day = slot_info['day']
                time_str = slot_info['time_str']
                classroom = slot_info['classroom']
                entry = slot_info['entry']
                
                # Copy to timetable
                timetable[day][time_str] = entry
                
                # Mark slot as used
                if day not in used_slots:
                    used_slots[day] = {}
                used_slots[day][time_str] = {'room': classroom, 'course': course_code}
                
                # Mark classroom as used globally
                if day not in self.global_classroom_usage:
                    self.global_classroom_usage[day] = {}
                if time_str not in self.global_classroom_usage[day]:
                    self.global_classroom_usage[day][time_str] = {}
                
                self.global_classroom_usage[day][time_str][classroom] = {
                    'dept': department,
                    'semester': semester,
                    'section': 'B',
                    'course': course_code
                }
            
            print(f"   [COPIED] {course_code} - {len(course_slots)} slots copied from Section A")
    
    def _schedule_courses(self, courses_df, timetable, used_slots,
                         lecture_schedule, tutorial_schedule, lab_schedule,
                         lab_usage, section, semester, is_common=False):
        """Schedule courses into timetable"""
        
        # Track which baskets we've already scheduled
        scheduled_baskets = set()
        
        for _, course in courses_df.iterrows():
            course_code = course['Course Code'].strip()
            course_title = course['Course Title'].strip()
            classroom = str(course.get('Classroom', '')).strip()
            
            # Check if this is an elective course
            is_elective = self.is_elective_course(course)
            basket = self.get_elective_basket(course) if is_elective else None
            
            # ELECTIVE ROTATION: Skip baskets not allowed for this semester
            if is_elective and basket and semester in self.elective_rotation:
                if basket not in self.elective_rotation[semester]:
                    print(f"   Skipping {basket} (rotated out for Semester {semester})")
                    # Store rotated out elective for "After Midsems" display
                    if basket not in self.rotated_out_electives:
                        self.rotated_out_electives[basket] = []
                    self.rotated_out_electives[basket].append({
                        'code': course_code,
                        'title': course_title,
                        'classroom': classroom,
                        'section': section,
                        'semester': semester
                    })
                    continue
            
            # Store elective info for later display (avoid duplicates)
            if is_elective and basket:
                if basket not in self.elective_courses:
                    self.elective_courses[basket] = []
                # Only add if not already present
                course_info = {
                    'code': course_code,
                    'title': course_title,
                    'classroom': classroom,
                    'section': section,
                    'semester': semester
                }
                if not any(c['code'] == course_code for c in self.elective_courses[basket]):
                    self.elective_courses[basket].append(course_info)
                
                # Skip scheduling if we've already scheduled this basket IN THIS TIMETABLE
                if basket in scheduled_baskets:
                    continue
                
                # Mark basket as scheduled and use basket name as "course code" for scheduling
                scheduled_baskets.add(basket)
                course_code_original = course_code  # Store original course code
                course_code = f"ELECTIVE_{basket}"  # Use basket as unique identifier
                
                # CHECK GLOBAL ELECTIVE SCHEDULE: If this basket is already scheduled globally,
                # reuse those slots for consistency across all departments/sections
                if semester in self.global_elective_schedule and basket in self.global_elective_schedule[semester]:
                    print(f"   [GLOBAL] Reusing existing slots for {basket} from global schedule")
                    existing_slots = self.global_elective_schedule[semester][basket]
                    
                    # Place the elective in the same slots as other departments/sections
                    for slot_info in existing_slots:
                        day, time_str, duration_minutes, session_type, classroom_used = slot_info
                        
                        # Create the session label with classroom inline (for electives)
                        session_label = self._create_session_label(course_code, session_type, section, 
                                                                   is_common=False, is_elective=True, basket=basket, classroom=classroom_used)
                        
                        # For electives, classroom is already in label - no need for | separator
                        full_label = session_label
                        
                        # Mark the slot as used in timetable
                        if day not in timetable:
                            timetable[day] = {}
                        timetable[day][time_str] = full_label
                        
                        # Mark slot as used in the nested dict structure
                        if day not in used_slots:
                            used_slots[day] = {}
                        if time_str not in used_slots[day]:
                            used_slots[day][time_str] = {}
                        used_slots[day][time_str][course_code] = {
                            'room': classroom_used,
                            'course': course_code,
                            'type': session_type,
                            'duration_minutes': duration_minutes,
                            'is_elective': True,
                            'basket': basket
                        }
                        
                        # Mark classroom as used globally
                        if day not in self.global_classroom_usage:
                            self.global_classroom_usage[day] = {}
                        if time_str not in self.global_classroom_usage[day]:
                            self.global_classroom_usage[day][time_str] = {}
                        self.global_classroom_usage[day][time_str][classroom_used] = True
                    
                    # Skip normal scheduling - we've already placed this elective
                    continue
            
            # For common courses, we'll find available large classroom dynamically during scheduling
            # Don't assign C004 upfront - let the scheduler find the best available classroom
            if is_common:
                classroom = None  # Will be assigned dynamically
            
            lectures, tutorials, practicals = self.parse_ltpsc(course)
            
            # For electives: Use the ACTUAL L, T, P values from the course LTPSC
            # NOT the maximum across the basket - this was causing over-allocation
            # Example: If course has L=2, T=1, P=0, schedule exactly 2 lectures + 1 tutorial
            if is_elective and basket:
                # Already have lectures, tutorials, practicals from parse_ltpsc above
                # No need to find max - just use the course's own LTPSC values
                pass
            
            # Initialize course schedule tracking
            if course_code not in lecture_schedule:
                lecture_schedule[course_code] = {}
                tutorial_schedule[course_code] = {}
                lab_schedule[course_code] = {}
                for day in self.days:
                    lecture_schedule[course_code][day] = 0
                    tutorial_schedule[course_code][day] = 0
                    lab_schedule[course_code][day] = 0
            
            print(f"\n   Scheduling: {course_code} - L:{lectures} T:{tutorials} P:{practicals}")
            
            # Schedule lectures (1.5 hours each)
            for lec_num in range(lectures):
                success = self._schedule_session(
                    timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                    lab_usage, course_code, course_title, classroom,
                    'Lecture', section, is_common, is_elective, basket
                )
                if not success:
                    self.unscheduled_courses.append(f"{course_code} - Lecture {lec_num+1}")
            
            # Schedule tutorials (1 hour - use 1 slot)
            for tut_num in range(tutorials):
                success = self._schedule_session(
                    timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                    lab_usage, course_code, course_title, classroom,
                    'Tutorial', section, is_common, is_elective, basket, duration_hours=1
                )
                if not success:
                    self.unscheduled_courses.append(f"{course_code} - Tutorial {tut_num+1}")
            
            # Schedule practicals/labs (2 hours per lab session)
            # Note: 'practicals' is already converted to number of sessions in parse_ltpsc()
            for prac_num in range(practicals):
                success = self._schedule_lab_session(
                    timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                    lab_usage, course_code, course_title, classroom,
                    section, is_common, is_elective, basket
                )
                if not success:
                    self.unscheduled_courses.append(f"{course_code} - Lab {prac_num+1}")
            
            # SAVE ELECTIVE SLOTS TO GLOBAL SCHEDULE: After scheduling all sessions for this basket,
            # save the slots so other departments/sections can reuse them
            if is_elective and basket:
                # Check if this basket was NOT in the global schedule (i.e., we just scheduled it fresh)
                if semester not in self.global_elective_schedule:
                    self.global_elective_schedule[semester] = {}
                
                if basket not in self.global_elective_schedule[semester]:
                    # Collect all slots used by this basket from the timetable
                    basket_slots = []
                    for day in timetable:
                        for time_str in timetable[day]:
                            entry = timetable[day][time_str]
                            # Check if this slot contains this basket (format: "Elective (B3)" or "Elective (B3) [90min]")
                            if isinstance(entry, str) and f"Elective ({basket})" in entry:
                                # Parse the entry to extract session type
                                # Classroom is stored separately in self.elective_classroom_assignments
                                
                                # Determine session type from the entry
                                if '(L)' in entry:
                                    session_type = 'Lecture'
                                    duration_minutes = 90
                                elif '(T)' in entry:
                                    session_type = 'Tutorial'
                                    duration_minutes = 60
                                elif '(P)' in entry:
                                    session_type = 'Lab'
                                    duration_minutes = 120
                                else:
                                    # Default to lecture if unclear
                                    session_type = 'Lecture'
                                    duration_minutes = 90
                                
                                # Get classroom from tracking dictionary
                                classroom_used = self.elective_classroom_assignments.get(basket, None)
                                if not classroom_used:
                                    # Fallback: try to extract from pipe separator (old format compatibility)
                                    if '|' in entry:
                                        classroom_used = entry.split('|')[-1].strip()
                                    else:
                                        # No classroom found - this shouldn't happen, but use None to trigger error
                                        classroom_used = None
                                
                                basket_slots.append((day, time_str, duration_minutes, session_type, classroom_used))
                    
                    # Save to global schedule
                    if basket_slots:
                        self.global_elective_schedule[semester][basket] = basket_slots
                        print(f"   [GLOBAL] Saved {len(basket_slots)} slots for {basket} to global schedule")
    
    def _schedule_session(self, timetable, used_slots, lecture_schedule, tutorial_schedule,
                         lab_schedule, lab_usage, course_code, course_title, classroom,
                         session_type, section, is_common, is_elective, basket, duration_hours=1.5):
        """Schedule a single session (Lecture or Tutorial) - can use regular or flexible afternoon slots"""
        
        # Determine which schedule tracker to use
        if session_type == 'Lecture':
            session_schedule = lecture_schedule
            max_per_day = self.max_lectures_per_day
            duration_minutes = 90  # 1.5 hours
        elif session_type == 'Tutorial':
            session_schedule = tutorial_schedule
            max_per_day = self.max_tutorials_per_day
            duration_minutes = 60  # 1 hour
        else:
            session_schedule = lecture_schedule  # Fallback
            max_per_day = 1
            duration_minutes = 90
        
        # Try days with priority order - prioritize underutilized days like Friday
        # This helps fill Friday slots before they're left empty
        day_priority = self._get_day_priority_order(timetable)
        
        # Try each day in priority order
        for day in day_priority:
            # Enforce strict rule: max 1 lecture/tutorial per course per day
            if session_schedule[course_code][day] >= max_per_day:
                continue
            
            # Additional check: if this is a lecture, ensure no tutorial on same day, and vice versa
            if session_type == 'Lecture' and tutorial_schedule[course_code][day] > 0:
                continue
            elif session_type == 'Tutorial' and lecture_schedule[course_code][day] > 0:
                continue
            
            # Try regular morning slots first (1.5 hours each)
            for time_slot in self.regular_slots:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                
                # Check if slot is free
                if timetable[day][time_str] != 'Free':
                    continue
                
                # For electives: ALWAYS find dynamic classroom (ignore CSV classroom - enforce non-C004 rule)
                # For common courses: Find classroom if not specified
                # For regular courses: Use specified classroom
                actual_classroom = classroom
                if is_elective and basket:
                    # Electives must use dynamic assignment to avoid C004
                    actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=True)
                    if actual_classroom is None:
                        continue  # No non-C004 classroom available in this slot
                elif classroom is None:
                    # Common courses or other courses without pre-assigned classroom
                    actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=False)
                    if actual_classroom is None:
                        continue  # No classroom available in this slot
                
                # Check classroom conflict (local within this timetable)
                conflict = False
                if day in used_slots and time_str in used_slots[day]:
                    for existing_slot in used_slots[day][time_str].values():
                        if existing_slot.get('room') == actual_classroom:
                            conflict = True
                            break
                
                # Check GLOBAL classroom conflict (across all semesters)
                if not conflict and day in self.global_classroom_usage and time_str in self.global_classroom_usage[day]:
                    if actual_classroom in self.global_classroom_usage[day][time_str]:
                        conflict = True
                
                if conflict:
                    continue
                
                # Schedule in regular slot
                label = self._create_session_label(course_code, session_type, section, is_common, is_elective, basket, actual_classroom)
                
                # Add duration indicator for tutorials (60 min) in 90-min slots to show actual duration
                if session_type == 'Tutorial' and duration_minutes == 60:
                    label_with_duration = f"{label} [60min]"
                else:
                    label_with_duration = label
                
                # For non-electives: show classroom in time slot header (| classroom)
                # For electives: classroom shown in summary below timetable, not in grid
                if not (is_elective and basket):
                    timetable[day][time_str] = f"{label_with_duration} | {actual_classroom}"
                else:
                    timetable[day][time_str] = label_with_duration
                    # Track elective classroom assignment for summary display (per course, not per basket)
                    if basket and course_code:
                        # Use the original course code (before it was changed to ELECTIVE_basket)
                        original_course_code = course_code.replace(f"ELECTIVE_{basket}", "").strip()
                        # If we have the original course code in context, use it; otherwise track by basket+classroom
                        self.elective_classroom_assignments[course_code] = actual_classroom
                
                # Mark as used
                if day not in used_slots:
                    used_slots[day] = {}
                if time_str not in used_slots[day]:
                    used_slots[day][time_str] = {}
                
                used_slots[day][time_str][course_code] = {
                    'room': actual_classroom,
                    'course': course_code,
                    'type': session_type,
                    'duration_minutes': duration_minutes,
                    'slot_capacity_minutes': 90,  # Regular slots are 1.5 hours
                    'is_elective': is_elective,
                    'basket': basket
                }
                
                # Record GLOBAL classroom usage to prevent double-booking across semesters
                self._record_global_classroom_usage(
                    day, time_str, actual_classroom,
                    self.current_department, self.current_semester, self.current_section, course_code
                )
                
                session_schedule[course_code][day] += 1
                return True
            
            # Try afternoon flexible slots (2-hour capacity)
            for time_slot in self.afternoon_flex_slots:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                
                # Check if slot is free
                if timetable[day][time_str] != 'Free':
                    continue
                
                # For electives: ALWAYS find dynamic classroom (ignore CSV classroom - enforce non-C004 rule)
                # For common courses: Find classroom if not specified
                # For regular courses: Use specified classroom
                actual_classroom = classroom
                if is_elective and basket:
                    # Electives must use dynamic assignment to avoid C004
                    actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=True)
                    if actual_classroom is None:
                        continue  # No non-C004 classroom available in this slot
                elif classroom is None:
                    # Common courses or other courses without pre-assigned classroom
                    actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=False)
                    if actual_classroom is None:
                        continue  # No classroom available in this slot
                
                # Check classroom conflict (local within this timetable)
                conflict = False
                if day in used_slots and time_str in used_slots[day]:
                    for existing_slot in used_slots[day][time_str].values():
                        if existing_slot.get('room') == actual_classroom:
                            conflict = True
                            break
                
                # Check GLOBAL classroom conflict (across all semesters)
                if not conflict and day in self.global_classroom_usage and time_str in self.global_classroom_usage[day]:
                    if actual_classroom in self.global_classroom_usage[day][time_str]:
                        conflict = True
                
                if conflict:
                    continue
                
                # Schedule in afternoon flexible slot with duration info
                label = self._create_session_label(course_code, session_type, section, is_common, is_elective, basket, actual_classroom)
                duration_display = f"{duration_minutes}min"
                
                if not (is_elective and basket):
                    timetable[day][time_str] = f"{label} [{duration_display}] | {actual_classroom}"
                else:
                    timetable[day][time_str] = f"{label} [{duration_display}]"
                    # Track elective classroom assignment for summary display
                    if basket and basket not in self.elective_classroom_assignments:
                        self.elective_classroom_assignments[basket] = actual_classroom
                
                # Mark as used with duration info
                if day not in used_slots:
                    used_slots[day] = {}
                if time_str not in used_slots[day]:
                    used_slots[day][time_str] = {}
                
                used_slots[day][time_str][course_code] = {
                    'room': actual_classroom,
                    'course': course_code,
                    'type': session_type,
                    'duration_minutes': duration_minutes,
                    'slot_capacity_minutes': 120,  # Afternoon flex slots are 2 hours
                    'is_elective': is_elective,
                    'basket': basket
                }
                
                # Record GLOBAL classroom usage to prevent double-booking across semesters
                self._record_global_classroom_usage(
                    day, time_str, actual_classroom,
                    self.current_department, self.current_semester, self.current_section, course_code
                )
                
                session_schedule[course_code][day] += 1
                return True
        
        print(f"      WARNING: Could not schedule {course_code} - {session_type}")
        return False
    
    def _create_session_label(self, course_code, session_type, section, is_common, is_elective, basket, classroom=None):
        """Create a label for a session
        
        Args:
            classroom: Provided but NOT used in label for electives (shown in summary instead)
        """
        if is_elective and basket:
            # For electives: DON'T include classroom in label (it goes in summary below timetable)
            return f"Elective ({basket})"
        elif is_common:
            return f"{course_code} (Common)"
        else:
            if session_type == 'Tutorial':
                return f"{course_code}-T-{section}"
            else:
                return f"{course_code}-{section}"
    
    def _schedule_lab_session(self, timetable, used_slots, lecture_schedule, tutorial_schedule,
                             lab_schedule, lab_usage, course_code, course_title, classroom,
                             section, is_common, is_elective, basket):
        """Schedule a 2-hour lab session in dedicated afternoon flexible slots"""
        
        # Labs are 2 hours and should use the afternoon 2-hour flexible slots
        # This gives priority to labs for these slots
        
        # Get day priority order (prioritize underutilized days like Friday)
        day_priority = self._get_day_priority_order(timetable)
        
        # Try each day in priority order
        for day in day_priority:
            # Enforce: Max 1 lab session per course per day
            if lab_schedule[course_code][day] >= self.max_labs_per_day:
                continue
            
            # Try afternoon flexible slots (perfect for 2-hour labs)
            for time_slot in self.afternoon_flex_slots:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                
                # Check if slot is free
                if timetable[day][time_str] != 'Free':
                    continue
                
                # Find an available lab room
                used_labs = lab_usage[day].get(time_str, [])
                available_lab = None
                for lab in self.lab_rooms:
                    if lab not in used_labs:
                        # Also check GLOBAL usage
                        global_conflict = False
                        if day in self.global_classroom_usage and time_str in self.global_classroom_usage[day]:
                            if lab in self.global_classroom_usage[day][time_str]:
                                global_conflict = True
                        
                        if not global_conflict:
                            available_lab = lab
                            break
                
                if not available_lab:
                    continue
                
                # Create label for lab session
                if is_elective and basket:
                    label = f"Elective Lab ({basket})"
                elif is_common:
                    label = f"{course_code}-Lab (Common)"
                else:
                    label = f"{course_code}-Lab-{section}"
                
                # Schedule the lab (full 2 hours)
                timetable[day][time_str] = f"{label} [120min] | {available_lab}"
                
                # Mark lab as used
                if time_str not in lab_usage[day]:
                    lab_usage[day][time_str] = []
                lab_usage[day][time_str].append(available_lab)
                
                # Mark in used_slots with duration info
                if day not in used_slots:
                    used_slots[day] = {}
                if time_str not in used_slots[day]:
                    used_slots[day][time_str] = {}
                
                used_slots[day][time_str][course_code] = {
                    'room': available_lab,
                    'course': course_code,
                    'type': 'Lab',
                    'duration_minutes': 120,  # Full 2 hours
                    'slot_capacity_minutes': 120,  # Afternoon slots are 2 hours
                    'is_elective': is_elective,
                    'basket': basket
                }
                
                # Record GLOBAL classroom usage to prevent double-booking across semesters
                self._record_global_classroom_usage(
                    day, time_str, available_lab,
                    self.current_department, self.current_semester, self.current_section, course_code
                )
                
                # Update lab schedule
                lab_schedule[course_code][day] += 1
                
                return True
        
        print(f"      WARNING: Could not schedule lab for {course_code}")
        return False
    
    def export_to_csv(self, timetable, filename, electives=None, rotated_out=None):
        """Export timetable to CSV with elective information"""
        if timetable is None:
            return False
        
        # Convert to DataFrame
        df = pd.DataFrame(timetable).T
        
        output_dir = 'timetable_outputs'
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Export timetable to CSV
        df.to_csv(filepath, index=True, encoding='utf-8')
        
        # Also export elective information if available
        if electives and len(electives) > 0:
            elective_file = filepath.replace('.csv', '_Electives.txt')
            with open(elective_file, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("ELECTIVE COURSES - Choose ONE from each basket\n")
                f.write("="*80 + "\n\n")
                
                for basket, courses in sorted(electives.items()):
                    f.write(f"Basket {basket}:\n")
                    f.write("-" * 40 + "\n")
                    
                    # Assign different classrooms to each course in the basket
                    # Since all courses in a basket run at the same time, they need different classrooms
                    available_classrooms = self.backup_large_classrooms.copy()
                    
                    for idx, course in enumerate(courses):
                        # Assign a different classroom to each course
                        if idx < len(available_classrooms):
                            assigned_classroom = available_classrooms[idx]
                        else:
                            # If we run out of classrooms, cycle through them
                            assigned_classroom = available_classrooms[idx % len(available_classrooms)]
                        
                        f.write(f"  • {course['code']}: {course['title']}\n")
                        f.write(f"    Classroom: {assigned_classroom}\n")
                    f.write("\n")
                
                # Add "After Midsems" section for rotated-out electives
                if rotated_out and len(rotated_out) > 0:
                    f.write("\n" + "="*80 + "\n")
                    f.write("AFTER MIDSEMS - These electives will be offered after mid-semester exams\n")
                    f.write("="*80 + "\n\n")
                    
                    for basket, courses in sorted(rotated_out.items()):
                        f.write(f"Basket {basket} (After Midsems):\n")
                        f.write("-" * 40 + "\n")
                        for course in courses:
                            f.write(f"  • {course['code']}: {course['title']}\n")
                            f.write(f"    Classroom: {course['classroom']}\n")
                        f.write("\n")
        
        print(f"Timetable saved: {filepath}")
        return True
    
    def print_timetable(self, timetable):
        """Print timetable to console"""
        if timetable is None:
            return
        
        df = pd.DataFrame(timetable).T
        print("\n" + str(df))
        
        # Print elective classroom assignments summary
        if self.elective_courses and len(self.elective_courses) > 0:
            print("\n" + "-"*80)
            print("ELECTIVE CLASSROOM ASSIGNMENTS:")
            print("-"*80)
            
            available_classrooms = self.backup_large_classrooms.copy()
            
            for basket in sorted(self.elective_courses.keys()):
                courses = self.elective_courses[basket]
                print(f"\n{basket}:")
                for idx, course in enumerate(courses):
                    # Assign different classroom to each course
                    if idx < len(available_classrooms):
                        assigned_classroom = available_classrooms[idx]
                    else:
                        assigned_classroom = available_classrooms[idx % len(available_classrooms)]
                    print(f"   {course['code']}: {assigned_classroom}")
        
        print("\n" + "="*80)

def main():
    """Main function to generate all timetables"""
    generator = TimetableGenerator()
    
    departments = ['CSE', 'DSAI', 'ECE']
    semesters = [2, 4, 6]
    sections = ['A', 'B']
    
    print("\nBeyondGames Enhanced Timetable Generator")
    print("="*80)
    print("Generating timetables from CSV files...")
    print("="*80)
    
    # PRE-STEP: Identify cross-department shared courses for DSAI and ECE
    print("\nPhase 1: Identifying cross-department shared courses (DSAI + ECE)...")
    print("="*80)
    for sem in semesters:
        shared_courses = generator.find_cross_dept_shared_courses(sem)
        if shared_courses:
            generator.cross_dept_shared_schedule[sem] = {}
    
    print("\nPhase 2: Generating individual timetables...")
    print("="*80)
    
    for dept in departments:
        for sem in semesters:
            # DSAI and ECE don't have sections - generate only Section A
            if dept in ['DSAI', 'ECE']:
                result = generator.generate_timetable(dept, sem, 'A')
                
                if result:
                    timetable, electives, rotated_out = result
                    generator.print_timetable(timetable)
                    filename = f"{dept}_Sem{sem}_SectionA_Timetable.csv"
                    generator.export_to_csv(timetable, filename, electives, rotated_out)
            else:
                # CSE has sections A and B
                for sec in sections:
                    result = generator.generate_timetable(dept, sem, sec)
                    
                    if result:
                        timetable, electives, rotated_out = result
                        generator.print_timetable(timetable)
                        filename = f"{dept}_Sem{sem}_Section{sec}_Timetable.csv"
                        generator.export_to_csv(timetable, filename, electives, rotated_out)
    
    print("\n>> All timetables generated successfully!")
    print(f"CSV Output location: timetable_outputs/")
    print(f"HTML Output location: timetable_html/")

if __name__ == "__main__":
    main()
