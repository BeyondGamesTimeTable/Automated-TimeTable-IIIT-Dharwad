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
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']  # Default: Monday to Friday
        # Note: Saturday is added dynamically in generate_timetable() for ECE Sem 4
        
        # Elective rotation strategy: Only schedule certain baskets per semester
        # Even semesters (2, 4, 6): Baskets B1, B3, E1 (+ Minor for Sem 4 only)
        # Odd semesters would get: Baskets B2, B4, E2 (if implemented)
        self.elective_rotation = {
            2: ['B1', 'B3', 'B4', 'E1'],  # Semester 2: Allow B4 for now (HS courses)
            4: ['B1', 'B3', 'Minor'],     # Semester 4: Core electives + Minor
            6: ['B1', 'B3', 'E1']         # Semester 6: Advanced electives
        }
        
        # Morning/Regular time slots (1.5 hours each) for lectures and tutorials
        self.regular_slots = [
            ('08:00', '09:30'),  # 1.5 hours - Early morning slot
            ('09:45', '11:15'),  # 1.5 hours
            ('11:30', '13:00'),  # 1.5 hours
        ]
        
        # Lunch break
        self.lunch_slot = ('13:00', '14:30')
        
        # Afternoon 2-hour FLEXIBLE slots - can be used for:
        # - Labs (full 2 hours)
        # - Lectures (1.5 hours of the 2-hour slot)
        # - Tutorials (1 hour of the 2-hour slot)
        self.afternoon_flex_slots = [
            ('14:30', '16:30'),  # 2 hours - Flexible slot 1
            ('16:30', '18:30'),  # 2 hours - Flexible slot 2
        ]
        
        # Evening slot (1.5 hours) - for overflow classes
        self.evening_slot = [
            ('18:30', '20:00'),  # 1.5 hours - Evening slot
        ]
        
        # Combined time slots for timetable display
        self.time_slots = self.regular_slots + [self.lunch_slot] + self.afternoon_flex_slots + self.evening_slot
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
    
    def is_common_course(self, row):
        """Check if course is common across sections"""
        elective = str(row.get('Electives', '')).strip().upper()
        section = str(row.get('Section', '')).strip()
        
        # Common if it's a foundation course (F) without specific section
        return elective == 'F' and section == ''
    
    def is_elective_course(self, row):
        """Check if course is an elective (Type elective)"""
        elective = str(row.get('Electives', '')).strip().upper()
        return elective == 'T'
    
    def get_elective_basket(self, row):
        """Get the basket name for elective course"""
        return str(row.get('Basket', '')).strip()
    
    def parse_ltpsc(self, row):
        """Parse LTPSC values"""
        lectures = int(row.get('Lectures', 0))
        tutorials = int(row.get('Tutorials', 0))
        practicals = int(row.get('Practicals', 0))
        return lectures, tutorials, practicals
    
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
    
    def _find_available_large_classroom(self, day, time_str):
        """Find an available large classroom for common courses, trying C004 first, then backups"""
        # Try primary large auditorium first
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
        
        # Dynamic Saturday scheduling for ECE Semester 4 (high course load)
        if department == 'ECE' and semester == 4:
            self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            print(">> Saturday classes enabled for ECE Semester 4 (high load optimization)")
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
        
        print(f"\nTotal courses to schedule:")
        print(f"   Common courses: {len(common_courses)}")
        print(f"   Section-specific courses: {len(section_courses)}")
        
        # Schedule common courses first
        self._schedule_courses(common_courses, timetable, used_slots, 
                              lecture_schedule, tutorial_schedule, lab_schedule,
                              lab_usage, section, semester, is_common=True)
        
        # Schedule section-specific courses
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
            
            # Store elective info for later display
            if is_elective and basket:
                if basket not in self.elective_courses:
                    self.elective_courses[basket] = []
                self.elective_courses[basket].append({
                    'code': course_code,
                    'title': course_title,
                    'classroom': classroom,
                    'section': section,
                    'semester': semester
                })
                
                # Skip scheduling if we've already scheduled this basket
                if basket in scheduled_baskets:
                    continue
                
                # Mark basket as scheduled and use basket name as "course code" for scheduling
                scheduled_baskets.add(basket)
                course_code = f"ELECTIVE_{basket}"  # Use basket as unique identifier
            
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
            # Practicals value represents credits: 2 credits = 1 lab session (2 hours), 4 credits = 2 lab sessions
            num_lab_sessions = practicals // 2  # Each lab session is 2 hours (2 credits)
            for prac_num in range(num_lab_sessions):
                success = self._schedule_lab_session(
                    timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                    lab_usage, course_code, course_title, classroom,
                    section, is_common, is_elective, basket
                )
                if not success:
                    self.unscheduled_courses.append(f"{course_code} - Lab {prac_num+1}")
    
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
                
                # For common courses (classroom=None), find an available large classroom dynamically
                actual_classroom = classroom
                if is_common and classroom is None:
                    actual_classroom = self._find_available_large_classroom(day, time_str)
                    if actual_classroom is None:
                        continue  # No large classroom available in this slot
                
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
                label = self._create_session_label(course_code, session_type, section, is_common, is_elective, basket)
                timetable[day][time_str] = f"{label} | {actual_classroom}" if not (is_elective and basket) else label
                
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
                
                # For common courses (classroom=None), find an available large classroom dynamically
                actual_classroom = classroom
                if is_common and classroom is None:
                    actual_classroom = self._find_available_large_classroom(day, time_str)
                    if actual_classroom is None:
                        continue  # No large classroom available in this slot
                
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
                label = self._create_session_label(course_code, session_type, section, is_common, is_elective, basket)
                duration_display = f"{duration_minutes}min"
                
                if not (is_elective and basket):
                    timetable[day][time_str] = f"{label} [{duration_display}] | {actual_classroom}"
                else:
                    timetable[day][time_str] = f"{label} [{duration_display}]"
                
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
            
            # Try evening slot as last resort (1.5 hours)
            for time_slot in self.evening_slot:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                
                # Check if slot is free
                if timetable[day][time_str] != 'Free':
                    continue
                
                # For common courses (classroom=None), find an available large classroom dynamically
                actual_classroom = classroom
                if is_common and classroom is None:
                    actual_classroom = self._find_available_large_classroom(day, time_str)
                    if actual_classroom is None:
                        continue  # No large classroom available in this slot
                
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
                
                # Schedule in evening slot
                label = self._create_session_label(course_code, session_type, section, is_common, is_elective, basket)
                timetable[day][time_str] = f"{label} [EVENING] | {actual_classroom}" if not (is_elective and basket) else f"{label} [EVENING]"
                
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
                    'slot_capacity_minutes': 90,  # Evening slots are 1.5 hours
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
    
    def _create_session_label(self, course_code, session_type, section, is_common, is_elective, basket):
        """Create a label for a session"""
        if is_elective and basket:
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
                    for course in courses:
                        f.write(f"  • {course['code']}: {course['title']}\n")
                        f.write(f"    Classroom: {course['classroom']}\n")
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
    
    for dept in departments:
        for sem in semesters:
            for sec in sections:
                result = generator.generate_timetable(dept, sem, sec)
                
                if result:
                    timetable, electives, rotated_out = result
                    generator.print_timetable(timetable)
                    filename = f"{dept}_Sem{sem}_Section{sec}_Timetable.csv"
                    generator.export_to_csv(timetable, filename, electives, rotated_out)
    
    print("\nAll timetables generated successfully!")
    print(f"CSV Output location: timetable_outputs/")
    print(f"HTML Output location: timetable_html/")

if __name__ == "__main__":
    main()
