# -*- coding: utf-8 -*-
"""
BeyondGames Automated Timetable Generator - Main Module
=====================================================

This is the main timetable generation system for IIIT Dharwad.
It reads course data from CSV files and generates optimized weekly schedules.

Author: BeyondGames Team
Version: 2.0.0 (CSV-based)
"""
import sys
import io

# Configure stdout for UTF-8 encoding to prevent UnicodeEncodeError on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
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
        # Even semesters (2, 4, 6, 8): Baskets B1, B3, E1 (+ Minor for Sem 4 only, + B4 for Sem 2)
        # Odd semesters (1, 3, 5, 7): Baskets B2, B4, E2 (customizable per semester)
        self.elective_rotation = {
            # Even semesters
            2: ['B1', 'B3', 'B4', 'E1'],  # Semester 2: Allow B4 for now (HS courses)
            4: ['B1', 'B3', 'Minor'],     # Semester 4: Core electives + Minor
            6: ['B1', 'B3', 'E1'],        # Semester 6: Advanced electives
            8: ['B1', 'B3', 'E1'],        # Semester 8: Advanced electives
            
            # Odd semesters
            1: ['B2', 'B4'],              # Semester 1: Foundational electives
            3: ['B2', 'B4', 'E2'],        # Semester 3: Core electives
            5: ['B2', 'B4', 'E2'],        # Semester 5: Advanced electives  
            7: ['B2', 'B4', 'E2']         # Semester 7: Advanced electives
        }
        
        # Combined time slots for timetable display
        self.time_slots = self.regular_slots + [self.lunch_slot] + self.afternoon_flex_slots
        
        # Section sizes for capacity calculation (typical IIIT Dharwad section strength)
        self.section_size = {
            'CSE': 80,   # CSE sections have 80 students each
            'ECE': 80,   # ECE sections have 80 students  
            'DSAI': 80   # DSAI sections have 80 students
        }
        # When DSAI + ECE share courses, combined = ~160 students
        # When CSE A + B together, combined = ~160 students
        
        # Load classrooms from CSV file
        self.classrooms = self._load_classrooms()
        
        # Categorize classrooms by type
        self.large_auditorium = self._get_auditorium()
        self.backup_large_classrooms = self._get_large_classrooms()
        self.lab_rooms = self._get_lab_rooms()
        self.regular_classrooms = self._get_regular_classrooms()
        
        self.unscheduled_courses = []  # Track courses that couldn't be scheduled
        self.elective_courses = {}  # Track elective courses by basket
        
        # Track which elective baskets are used in each timetable
        # Format: {(dept, semester, section): ['HSS', 'Elective A', 'Elective C']}
        self.timetable_basket_usage = {}
        
        # GLOBAL classroom tracker - shared across ALL semesters and sections
        # Format: global_classroom_usage[day][time_str][classroom] = {'dept': ..., 'semester': ..., 'section': ..., 'course': ...}
        self.global_classroom_usage = {}
        
        # COMMON COURSE SCHEDULE - shared within department across sections (e.g., CSE A+B together)
        # Format: common_course_schedule[dept][semester] = {course_code: [(day, time_str, classroom, label), ...]}
        self.common_course_schedule = {}
        
        # ELECTIVE BASKET SCHEDULE - shared across sections of SAME branch for same semester
        # Format: elective_basket_schedule[department][semester] = {basket_name: [(day, time_str, classrooms_dict), ...]}
        # This ensures sections within same branch (e.g., CSE A and B) use SAME time slots
        # But different branches (CSE vs DSAI vs ECE) can have different times
        self.elective_basket_schedule = {}
        
        # Strict scheduling rules: max 1 lecture/tutorial/lab per course per day
        # But allow lecture+lab or tutorial+lab on same day
        self.max_lectures_per_day = 1
        self.max_tutorials_per_day = 1
        self.max_labs_per_day = 1
    
    def _load_classrooms(self):
        """Load classroom data from classrooms.csv"""
        classrooms_file = os.path.join(self.csv_folder, 'classrooms.csv')
        if not os.path.exists(classrooms_file):
            print(f"Warning: {classrooms_file} not found, using default classrooms")
            # Return default classrooms if file doesn't exist
            return {
                'C004': {'capacity': 240, 'type': 'Auditorium'},
                'C002': {'capacity': 116, 'type': 'large classroom'},
                'C003': {'capacity': 135, 'type': 'large classroom'},
                'C101': {'capacity': 96, 'type': 'classroom'},
                'C102': {'capacity': 96, 'type': 'classroom'},
                'C104': {'capacity': 96, 'type': 'classroom'},
                'C202': {'capacity': 96, 'type': 'classroom'},
                'C203': {'capacity': 96, 'type': 'classroom'},
                'C204': {'capacity': 96, 'type': 'classroom'},
                'C205': {'capacity': 96, 'type': 'classroom'},
                'L105': {'capacity': 40, 'type': 'Hardware Lab'},
                'L106': {'capacity': 40, 'type': 'Software Lab'},
                'L107': {'capacity': 40, 'type': 'Software Lab'},
                'L206': {'capacity': 40, 'type': 'Hardware Lab'},
                'L207': {'capacity': 40, 'type': 'Software Lab'},
                'L208': {'capacity': 40, 'type': 'Software Lab'},
            }
        
        try:
            df = pd.read_csv(classrooms_file)
            df.columns = df.columns.str.strip()
            
            classrooms = {}
            for _, row in df.iterrows():
                room = str(row['Room']).strip()
                description = str(row['Description']).strip()
                
                # Parse capacity
                capacity_str = str(row['Seating Capacity']).strip()
                if capacity_str.lower() in ['nil', 'nan', '']:
                    capacity = 0
                else:
                    try:
                        capacity = int(capacity_str)
                    except ValueError:
                        capacity = 0
                
                # For labs with empty capacity, use default of 40
                if capacity == 0 and 'lab' in description.lower():
                    capacity = 40
                
                # Skip rooms with no capacity (like recreation, library, examination room)
                # But keep labs even if they have no specified capacity
                if capacity == 0:
                    continue
                
                classrooms[room] = {
                    'capacity': capacity,
                    'type': description
                }
            
            print(f"\n[OK] Loaded {len(classrooms)} classrooms from {classrooms_file}")
            return classrooms
        
        except Exception as e:
            print(f"Error loading classrooms: {e}, using defaults")
            return self._load_classrooms()  # Return defaults
    
    def _get_auditorium(self):
        """Get the largest auditorium (highest capacity)"""
        if not self.classrooms:
            return 'C004'
        
        # Find classroom with highest capacity
        auditorium = max(self.classrooms.items(), key=lambda x: x[1]['capacity'])
        print(f"   Primary Auditorium: {auditorium[0]} (Capacity: {auditorium[1]['capacity']})")
        return auditorium[0]
    
    def _get_large_classrooms(self):
        """Get large classrooms (capacity >= 90, excluding auditorium)"""
        if not self.classrooms:
            return ['C101', 'C102', 'C103', 'C202', 'C203', 'C204', 'C205']
        
        large_rooms = [
            room for room, info in self.classrooms.items()
            if info['capacity'] >= 90 and room != self.large_auditorium
            and 'lab' not in info['type'].lower()
        ]
        
        # Sort by capacity (largest first)
        large_rooms.sort(key=lambda x: self.classrooms[x]['capacity'], reverse=True)
        print(f"   Large Classrooms ({len(large_rooms)}): {', '.join(large_rooms)}")
        return large_rooms
    
    def _get_lab_rooms(self):
        """Get lab rooms"""
        if not self.classrooms:
            return ['Lab-1', 'Lab-2', 'Lab-3', 'Lab-4', 'Lab-5']
        
        lab_rooms = [
            room for room, info in self.classrooms.items()
            if 'lab' in info['type'].lower()
        ]
        
        print(f"   Lab Rooms ({len(lab_rooms)}): {', '.join(lab_rooms)}")
        return lab_rooms
    
    def _get_regular_classrooms(self):
        """Get regular classrooms (not auditorium, not large, not lab)"""
        if not self.classrooms:
            return ['C101', 'C102', 'C103', 'C104', 'C202', 'C203', 'C204', 'C205']
        
        regular_rooms = [
            room for room, info in self.classrooms.items()
            if room != self.large_auditorium
            and room not in self.backup_large_classrooms
            and room not in self.lab_rooms
        ]
        
        print(f"   Regular Classrooms ({len(regular_rooms)}): {', '.join(regular_rooms)}")
        return regular_rooms
        
    def load_department_data(self, department):
        """Load CSV data for a specific department"""
        csv_file = os.path.join(self.csv_folder, f'{department}.csv')
        if not os.path.exists(csv_file):
            print(f"Warning: {csv_file} not found")
            return None
        
        df = pd.read_csv(csv_file)
        # Clean column names
        df.columns = df.columns.str.strip()
        return df
    
    def load_electives_data(self):
        """Load electives CSV file if it exists"""
        csv_file = os.path.join(self.csv_folder, 'electives.csv')
        if not os.path.exists(csv_file):
            print(f"   >> No electives.csv found - skipping elective scheduling")
            return None
        
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.strip()
        print(f"   >> Loaded {len(df)} elective courses from electives.csv")
        return df
    
    def group_electives_into_baskets(self, electives_df, semester, department):
        """
        Group elective courses into baskets based on:
        1. Branch/Department specificity (from Branch column)
        2. Duration (Full semester vs Till-midsem vs After-midsem)
        3. HSS vs non-HSS
        
        Branch column logic:
        - Empty = GLOBAL - Common to ALL branches (same time for CSE, DSAI, ECE)
        - "Cse" = BRANCH-SPECIFIC - Only for CSE
        - "Dsai" = BRANCH-SPECIFIC - Only for DSAI
        - "Cse+Dsai" = Common for CSE and DSAI only
        
        Returns: {'global': {baskets...}, 'branch_specific': {baskets...}}
        """
        if electives_df is None or electives_df.empty:
            return {'global': {}, 'branch_specific': {}}
        
        # Filter electives for this semester
        sem_electives = electives_df[electives_df['Semester'] == semester].copy()
        if sem_electives.empty:
            return {'global': {}, 'branch_specific': {}}
        
        # Separate global and branch-specific courses
        global_courses = []
        branch_specific_courses = []
        
        for _, row in sem_electives.iterrows():
            branch_val = row.get('Branch', '')
            # Handle NaN values from pandas
            if pd.isna(branch_val):
                branch_val = ''
            else:
                branch_val = str(branch_val).strip()
            
            if not branch_val:
                # Empty branch = global (common to all)
                global_courses.append(row)
            else:
                # Has branch value = check if it matches this department
                if branch_val.lower() == department.lower() or \
                   department.lower() in branch_val.lower():
                    branch_specific_courses.append(row)
        
        print(f"   >> Found {len(global_courses)} global courses, {len(branch_specific_courses)} {department}-specific courses")
        
        # Create baskets for global courses
        global_baskets = self._create_baskets_from_courses(global_courses, 'Global')
        
        # Create baskets for branch-specific courses
        branch_baskets = self._create_baskets_from_courses(branch_specific_courses, department)
        
        return {'global': global_baskets, 'branch_specific': branch_baskets}
    
    def _create_baskets_from_courses(self, courses, prefix):
        """
        Helper to create baskets from course list
        
        Basket formation rules:
        - HSS Basket: All HSS courses (separate basket as before)
        - Elective A (Till Mid-Semester): 1-2 credit NON-HSS courses running till midsem
        - Elective B (After Mid-Semester): 1-2 credit NON-HSS courses starting after midsem
        - Elective C (Whole Semester): 3-4 credit NON-HSS courses running full semester
        """
        baskets = {
            'HSS': {
                'ltpsc': 'varies', 'duration': 'full_sem', 'courses': [], 'has_tutorials': False, 'is_hss': True, 'prefix': prefix
            },
            'Elective A': {
                'ltpsc': 'varies', 'duration': 'till_midsem', 'courses': [], 'has_tutorials': False, 'is_hss': False, 'prefix': prefix
            },
            'Elective B': {
                'ltpsc': 'varies', 'duration': 'after_midsem', 'courses': [], 'has_tutorials': False, 'is_hss': False, 'prefix': prefix
            },
            'Elective C': {
                'ltpsc': 'varies', 'duration': 'full_sem', 'courses': [], 'has_tutorials': False, 'is_hss': False, 'prefix': prefix
            }
        }
        
        # Separate HSS and non-HSS courses
        hss_courses = []
        short_non_hss_courses = []  # 1-2 credits
        long_non_hss_courses = []   # 3-4 credits
        
        for row in courses:
            credits = int(row.get('Credits', 0))
            course_code = str(row['Course Code']).strip()
            hss_value = str(row.get('HSS', '')).strip().upper()
            
            # Check if HSS course using HSS column ONLY
            is_hss = hss_value == 'Y'
            
            if is_hss:
                hss_courses.append(row)
            elif credits <= 2:
                short_non_hss_courses.append(row)
            else:  # 3-4 credits
                long_non_hss_courses.append(row)
        
        # Debug output for basket formation
        if len(courses) > 0:
            print(f"   >> {prefix} basket formation: {len(hss_courses)} HSS, {len(short_non_hss_courses)} short NON-HSS (1-2cr), {len(long_non_hss_courses)} long NON-HSS (3-4cr)")
        
        # Process HSS courses
        basket_key = 'HSS'
        for row in hss_courses:
            course_code = str(row['Course Code']).strip()
            L = int(row.get('Lectures', 0))
            T = int(row.get('Tutorials', 0))
            P = int(row.get('Practicals', 0))
            credits = int(row.get('Credits', 0))
            
            if T > 0:
                baskets[basket_key]['has_tutorials'] = True
            
            baskets[basket_key]['courses'].append({
                'code': course_code,
                'title': row['Course Title'],
                'faculty': row['Faculty'],
                'L': L,
                'T': T,
                'P': P,
                'credits': credits,
                'branch': row.get('Branch', '')
            })
        
        # Distribute short NON-HSS courses: half to Till-Midsem (A), half to After-Midsem (B)
        # Sort by course code to ensure consistent distribution across all branches
        short_non_hss_courses = sorted(short_non_hss_courses, key=lambda x: x['Course Code'])
        mid_point = len(short_non_hss_courses) // 2
        
        till_midsem_courses = short_non_hss_courses[:mid_point]
        after_midsem_courses = short_non_hss_courses[mid_point:]
        
        # Process Till-Midsem NON-HSS courses (Elective A)
        basket_key = 'Elective A'
        for row in till_midsem_courses:
            course_code = str(row['Course Code']).strip()
            L = int(row.get('Lectures', 0))
            T = int(row.get('Tutorials', 0))
            P = int(row.get('Practicals', 0))
            credits = int(row.get('Credits', 0))
            
            if T > 0:
                baskets[basket_key]['has_tutorials'] = True
            
            baskets[basket_key]['courses'].append({
                'code': course_code,
                'title': row['Course Title'],
                'faculty': row['Faculty'],
                'L': L,
                'T': T,
                'P': P,
                'credits': credits,
                'branch': row.get('Branch', '')
            })
        
        # Process After-Midsem NON-HSS courses (Elective B)
        basket_key = 'Elective B'
        for row in after_midsem_courses:
            course_code = str(row['Course Code']).strip()
            L = int(row.get('Lectures', 0))
            T = int(row.get('Tutorials', 0))
            P = int(row.get('Practicals', 0))
            credits = int(row.get('Credits', 0))
            
            if T > 0:
                baskets[basket_key]['has_tutorials'] = True
            
            baskets[basket_key]['courses'].append({
                'code': course_code,
                'title': row['Course Title'],
                'faculty': row['Faculty'],
                'L': L,
                'T': T,
                'P': P,
                'credits': credits,
                'branch': row.get('Branch', '')
            })
        
        # Process Whole Semester NON-HSS courses (Elective C)
        basket_key = 'Elective C'
        for row in long_non_hss_courses:
            course_code = str(row['Course Code']).strip()
            L = int(row.get('Lectures', 0))
            T = int(row.get('Tutorials', 0))
            P = int(row.get('Practicals', 0))
            credits = int(row.get('Credits', 0))
            
            if T > 0:
                baskets[basket_key]['has_tutorials'] = True
            
            baskets[basket_key]['courses'].append({
                'code': course_code,
                'title': row['Course Title'],
                'faculty': row['Faculty'],
                'L': L,
                'T': T,
                'P': P,
                'credits': credits,
                'branch': row.get('Branch', '')
            })
        
        # Remove empty baskets
        baskets = {name: info for name, info in baskets.items() if info['courses']}
        return baskets
    
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
    
    def schedule_elective_baskets(self, timetable, used_slots, basket_groups, semester, section, department):
        """
        Schedule elective baskets into the timetable.
        
        Two types of baskets:
        1. GLOBAL baskets (empty branch) - Same time for ALL branches (CSE, DSAI, ECE)
        2. BRANCH-SPECIFIC baskets - Same time within branch sections only (CSE A & B)
        
        Args:
            basket_groups: {'global': {...}, 'branch_specific': {...}}
        """
        basket_assignments = {}
        
        # Initialize global schedule if not exists
        if 'global' not in self.elective_basket_schedule:
            self.elective_basket_schedule['global'] = {}
        
        # Initialize branch schedule if not exists
        if department not in self.elective_basket_schedule:
            self.elective_basket_schedule[department] = {}
        
        # STEP 1: Schedule GLOBAL baskets (or reuse if already scheduled)
        global_baskets = basket_groups.get('global', {})
        if global_baskets:
            if semester in self.elective_basket_schedule['global']:
                # Reuse global schedule
                print(f"\n   >> Reusing GLOBAL elective baskets (common to ALL branches)")
                for basket_name, slots in self.elective_basket_schedule['global'][semester].items():
                    basket_assignments[basket_name] = slots
                    # Find basket courses from global_baskets
                    basket_courses = None
                    for bname, basket_data in global_baskets.items():
                        if bname == basket_name:
                            basket_courses = basket_data.get('courses', [])
                            break
                    self._apply_basket_schedule_to_timetable(timetable, used_slots, basket_name, slots, basket_courses)
                
                # Also restore Elective B courses (which aren't scheduled but need to be in JSON)
                for bname, basket_data in global_baskets.items():
                    if basket_data.get('duration') == 'after_midsem':  # Elective B
                        # Add to elective_courses for JSON export
                        basket_courses = basket_data.get('courses', [])
                        if basket_courses and bname not in self.elective_courses:
                            self.elective_courses[bname] = []
                            classrooms = self._assign_classrooms_to_basket(basket_courses)
                            for course in basket_courses:
                                self.elective_courses[bname].append({
                                    'code': course['code'],
                                    'title': course['title'],
                                    'classroom': classrooms.get(course['code'], 'TBD'),
                                    'faculty': course['faculty'],
                                    'credits': course['credits'],
                                    'L': course['L'],
                                    'T': course['T'],
                                    'P': course['P']
                                })
            else:
                # First branch - create global schedule
                print(f"\n   >> Scheduling GLOBAL elective baskets (common to ALL branches)")
                self.elective_basket_schedule['global'][semester] = {}
                global_assignments = self._schedule_baskets(timetable, used_slots, global_baskets, semester, department)
                basket_assignments.update(global_assignments)
                self.elective_basket_schedule['global'][semester].update(global_assignments)
        
        # STEP 2: Schedule BRANCH-SPECIFIC baskets (or reuse within same branch)
        branch_baskets = basket_groups.get('branch_specific', {})
        if branch_baskets:
            if semester in self.elective_basket_schedule[department]:
                # Reuse branch schedule from first section
                print(f"\n   >> Reusing {department} branch-specific baskets (within branch sections)")
                for basket_name, slots in self.elective_basket_schedule[department][semester].items():
                    basket_assignments[basket_name] = slots
                    # Find basket courses from branch_baskets
                    basket_courses = None
                    for bname, basket_data in branch_baskets.items():
                        if bname == basket_name:
                            basket_courses = basket_data.get('courses', [])
                            break
                    self._apply_basket_schedule_to_timetable(timetable, used_slots, basket_name, slots, basket_courses)
                
                # Also restore Elective B courses (which aren't scheduled but need to be in JSON)
                for bname, basket_data in branch_baskets.items():
                    if basket_data.get('duration') == 'after_midsem':  # Elective B
                        # Add to elective_courses for JSON export
                        basket_courses = basket_data.get('courses', [])
                        if basket_courses and bname not in self.elective_courses:
                            self.elective_courses[bname] = []
                            classrooms = self._assign_classrooms_to_basket(basket_courses)
                            for course in basket_courses:
                                self.elective_courses[bname].append({
                                    'code': course['code'],
                                    'title': course['title'],
                                    'classroom': classrooms.get(course['code'], 'TBD'),
                                    'faculty': course['faculty'],
                                    'credits': course['credits'],
                                    'L': course['L'],
                                    'T': course['T'],
                                    'P': course['P']
                                })
            else:
                # First section of branch - create branch schedule
                print(f"\n   >> Scheduling {department} branch-specific baskets")
                self.elective_basket_schedule[department][semester] = {}
                branch_assignments = self._schedule_baskets(timetable, used_slots, branch_baskets, semester, department)
                basket_assignments.update(branch_assignments)
                self.elective_basket_schedule[department][semester].update(branch_assignments)
        
        print(f"   >> Successfully scheduled {len(basket_assignments)} total elective baskets")
        return basket_assignments
    
    def _apply_basket_schedule_to_timetable(self, timetable, used_slots, basket_name, slots, courses=None):
        """Apply pre-existing basket schedule to current timetable
        
        Args:
            courses: List of courses in the basket (for populating elective_courses)
        """
        for day, time_str, classrooms in slots:
            basket_label = basket_name
            if '[' in basket_name:
                basket_label = basket_name.split('[')[0].strip()
            if day in timetable and time_str in timetable[day]:
                timetable[day][time_str] = basket_label
            if time_str not in used_slots[day]:
                used_slots[day][time_str] = {}
            used_slots[day][time_str][basket_label] = classrooms
            print(f"      {basket_name}: {day} {time_str}")
        
        # Also populate elective_courses for display (if courses provided)
        if courses and classrooms:
            if basket_name not in self.elective_courses:
                self.elective_courses[basket_name] = []
            for course in courses:
                self.elective_courses[basket_name].append({
                    'code': course['code'],
                    'title': course['title'],
                    'classroom': classrooms.get(course['code'], 'TBD'),
                    'faculty': course['faculty'],
                    'credits': course['credits'],
                    'L': course['L'],
                    'T': course['T'],
                    'P': course['P']
                })
    
    def _schedule_baskets(self, timetable, used_slots, baskets, semester, department):
        """Schedule a set of baskets and return assignments"""
        basket_assignments = {}
        
        for basket_name, basket_info in baskets.items():
            duration = basket_info['duration']
            courses = basket_info['courses']
            
            if not courses:
                continue
            
            # Skip after-midsem baskets (Elective B) - they don't get scheduled in main timetable
            if duration == 'after_midsem':
                print(f"   >> Skipping {basket_name} (After-Midsem) - will list below timetable")
                # Store for later display (both in rotated_out AND in elective_courses for JSON export)
                if basket_name not in self.rotated_out_electives:
                    self.rotated_out_electives[basket_name] = []
                if basket_name not in self.elective_courses:
                    self.elective_courses[basket_name] = []
                    
                # Assign classrooms for display purposes
                classrooms = self._assign_classrooms_to_basket(courses)
                for course in courses:
                    course_info = {
                        'code': course['code'],
                        'title': course['title'],
                        'classroom': classrooms.get(course['code'], 'TBD'),
                        'faculty': course['faculty'],
                        'credits': course['credits'],
                        'L': course['L'],
                        'T': course['T'],
                        'P': course['P']
                    }
                    self.rotated_out_electives[basket_name].append(course_info)
                    # Also add to elective_courses so it's saved in JSON
                    self.elective_courses[basket_name].append(course_info)
                continue
            
            # Schedule Elective A (Till Mid-Sem) and Elective C (Whole Semester)
            print(f"   >> Scheduling {basket_name} ({duration})")
            
            # Calculate slots needed based on LTPSC (using first course as reference)
            sample_course = courses[0]
            L, T, P = sample_course['L'], sample_course['T'], sample_course['P']
            
            # LTPSC rules: Round UP to nearest multiple of 1.5
            # L=1 → 1.5 → 1 slot, L=2 → 3.0 → 2 slots, L=3 → 3.0 → 2 slots
            # L=4 → 4.5 → 3 slots, L=5 → 6.0 → 4 slots
            import math
            if L > 0:
                adjusted_hours = math.ceil(L / 1.5) * 1.5  # Round UP to nearest multiple of 1.5
                num_lectures = int(adjusted_hours / 1.5)
            else:
                num_lectures = 0
            num_tutorials = T
            num_practicals = P // 2
            
            print(f"      {basket_name}: {num_lectures}L + {num_tutorials}T + {num_practicals}P sessions")
            print(f"        Courses: {len(courses)}")
            
            basket_slots = []
            used_days_for_basket = set()  # Track which days we've used for this basket
            
            # Schedule lecture sessions
            for i in range(num_lectures):
                slot = self._find_free_slot_for_basket(timetable, used_slots, basket_name, 90, semester, False, used_days_for_basket)
                if slot:
                    day, time_str = slot
                    used_days_for_basket.add(day)  # Mark this day as used for this basket
                    classrooms = self._assign_classrooms_to_basket(courses)
                    basket_slots.append((day, time_str, classrooms))
                    self._mark_basket_slot_used(timetable, used_slots, day, time_str, basket_name, classrooms)
                    print(f"        Lecture {i+1}: {day} {time_str}")
                    for course_code, classroom in classrooms.items():
                        print(f"          {course_code}: {classroom}")
            
            # Schedule tutorial sessions if basket has tutorials (T > 0)
            if basket_info.get('has_tutorials', False) and num_tutorials > 0:
                print(f"      >> Scheduling {num_tutorials} tutorial session(s) for {basket_name}")
                for i in range(num_tutorials):
                    slot = self._find_free_slot_for_basket(timetable, used_slots, f"{basket_name}-T", 60, semester, False, used_days_for_basket)
                    if slot:
                        day, time_str = slot
                        used_days_for_basket.add(day)
                        classrooms = self._assign_classrooms_to_basket(courses)
                        basket_slots.append((day, time_str, classrooms))
                        self._mark_basket_slot_used(timetable, used_slots, day, time_str, f"{basket_name}-T", classrooms)
                        print(f"        Tutorial {i+1}: {day} {time_str}")
                        for course_code, classroom in classrooms.items():
                            print(f"          {course_code}: {classroom}")
            
            # Store courses for display - all scheduled baskets go to elective_courses
            # This includes: HSS (whole_semester), Elective A (till_midsem), Elective C (whole_semester)
            if basket_name not in self.elective_courses:
                self.elective_courses[basket_name] = []
            for course in courses:
                classrooms = basket_slots[0][2] if basket_slots else {}
                self.elective_courses[basket_name].append({
                    'code': course['code'],
                    'title': course['title'],
                    'classroom': classrooms.get(course['code'], 'TBD'),
                    'faculty': course['faculty'],
                    'credits': course['credits'],
                    'L': course['L'],
                    'T': course['T'],
                    'P': course['P']
                })
            
            if basket_slots:
                basket_assignments[basket_name] = basket_slots
        
        return basket_assignments
    
    def _find_free_slot_for_basket(self, timetable, used_slots, basket_name, duration_minutes, semester, is_hss=False, used_days=None):
        """Find a free slot for an elective basket
        
        Args:
            used_days: Set of days already used for this basket (to prevent same-day scheduling)
        """
        if used_days is None:
            used_days = set()
            
        for day in self.days:
            # Skip days already used for this basket
            if day in used_days:
                continue
                
            for time_slot in self.time_slots:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                
                # Skip lunch slot
                if time_slot == self.lunch_slot:
                    continue
                
                # Check slot duration matches what we need
                slot_duration = self._get_slot_duration(time_slot)
                if duration_minutes == 90 and slot_duration < 90:
                    continue
                if duration_minutes == 120 and slot_duration < 120:
                    continue
                
                # Check if slot is free
                if timetable[day].get(time_str, 'Free') == 'Free':
                    # Check global usage to avoid conflicts
                    if not self._is_slot_globally_used(day, time_str):
                        return (day, time_str)
        
        return None
    
    def _assign_classrooms_to_basket(self, courses):
        """Assign different classroom to each course in an elective basket"""
        classrooms = {}
        # Use backup large classrooms for electives (not C004 auditorium)
        available_classrooms = self.backup_large_classrooms.copy() if self.backup_large_classrooms else []
        
        # Fallback to regular classrooms if available
        if not available_classrooms and self.regular_classrooms:
            available_classrooms = self.regular_classrooms.copy()
        
        # Final fallback: use all non-auditorium classrooms
        if not available_classrooms:
            available_classrooms = [
                room for room in self.classrooms.keys()
                if room != self.large_auditorium and 'lab' not in self.classrooms[room]['type'].lower()
            ]
        
        if not available_classrooms:
            print("      Warning: No classrooms available for electives!")
            return {}
        
        for idx, course in enumerate(courses):
            if idx < len(available_classrooms):
                classroom = available_classrooms[idx]
            else:
                classroom = available_classrooms[idx % len(available_classrooms)]
            
            classrooms[course['code']] = classroom
            # Track for global usage
            self.elective_classroom_assignments[course['code']] = classroom
        
        return classrooms
    
    def _assign_lab_rooms_to_basket(self, courses):
        """Assign lab rooms to elective basket practicals"""
        lab_rooms = {}
        available_labs = list(self.lab_rooms.keys())
        
        for idx, course in enumerate(courses):
            if idx < len(available_labs):
                lab = available_labs[idx]
            else:
                lab = available_labs[idx % len(available_labs)]
            
            lab_rooms[course['code']] = lab
        
        return lab_rooms
    
    def _mark_basket_slot_used(self, timetable, used_slots, day, time_str, basket_label, classrooms):
        """Mark a slot as used by an elective basket"""
        # Update timetable with basket label
        timetable[day][time_str] = basket_label
        
        # Mark slot as used
        if day not in used_slots:
            used_slots[day] = {}
        used_slots[day][time_str] = {
            'type': 'elective_basket',
            'basket': basket_label,
            'classrooms': classrooms
        }
        
        # Mark each classroom as globally used
        for course_code, classroom in classrooms.items():
            # Track global classroom usage
            if day not in self.global_classroom_usage:
                self.global_classroom_usage[day] = {}
            if time_str not in self.global_classroom_usage[day]:
                self.global_classroom_usage[day][time_str] = {}
            
            self.global_classroom_usage[day][time_str][classroom] = {
                'dept': self.current_department,
                'semester': self.current_semester,
                'section': self.current_section,
                'course': f"{basket_label} - {course_code}"
            }
    
    def _get_course_classroom_from_assignments(self, course_code, lecture_slots):
        """Get classroom assigned to a course from lecture slot assignments"""
        if course_code in self.elective_classroom_assignments:
            return self.elective_classroom_assignments[course_code]
        
        # Fallback to first available classroom
        if self.regular_classrooms:
            return self.regular_classrooms[0]
        return "TBD"
    
    def _assign_elective_classroom(self, course_code, all_courses):
        """Assign a classroom to an elective course for display"""
        if course_code in self.elective_classroom_assignments:
            return self.elective_classroom_assignments[course_code]
        
        # Use backup large classrooms for electives
        available = self.backup_large_classrooms.copy() if self.backup_large_classrooms else []
        if not available and self.regular_classrooms:
            available = self.regular_classrooms.copy()
        if not available:
            available = [room for room in self.classrooms.keys() if room != self.large_auditorium]
        
        if not available:
            return "TBD"
        
        # Assign new classroom
        idx = len(self.elective_classroom_assignments) % len(available)
        classroom = available[idx]
        self.elective_classroom_assignments[course_code] = classroom
        return classroom
    
    def _get_slot_duration(self, time_slot):
        """Calculate duration of a time slot in minutes"""
        from datetime import datetime
        start = datetime.strptime(time_slot[0], '%H:%M')
        end = datetime.strptime(time_slot[1], '%H:%M')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    
    def _is_slot_globally_used(self, day, time_str):
        """Check if a slot is used globally across all departments/sections"""
        if day in self.global_classroom_usage:
            if time_str in self.global_classroom_usage[day]:
                # Slot is used if any classroom is occupied
                return len(self.global_classroom_usage[day][time_str]) > 0
        return False
    
    def is_common_course(self, row):
        """Check if course is common across sections
        
        A course is common if:
        1. Section column is empty (NaN or empty string) - means it's taught to both sections together
        2. NOT an elective (if Electives column exists and is 'T')
        """
        import pandas as pd
        section = row.get('Section', '')
        
        # Section is empty if it's NaN, None, or empty string
        section_empty = pd.isna(section) or str(section).strip() == ''
        
        # Check if it's an elective (Type elective = 'T')
        # If there's no Electives column, default to empty (not elective)
        elective_type = str(row.get('Electives', '')).strip().upper()
        is_type_elective = elective_type == 'T'
        
        # Common course: empty section AND not a type elective
        return section_empty and not is_type_elective
    
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
        import math
        import pandas as pd
        
        # Handle NaN values by converting to 0
        lecture_hours = row.get('Lectures', 0)
        if pd.isna(lecture_hours):
            lecture_hours = 0
        else:
            lecture_hours = int(lecture_hours)
            
        tutorial_hours = row.get('Tutorials', 0)
        if pd.isna(tutorial_hours):
            tutorial_hours = 0
        else:
            tutorial_hours = int(tutorial_hours)
            
        practical_hours = row.get('Practicals', 0)
        if pd.isna(practical_hours):
            practical_hours = 0
        else:
            practical_hours = int(practical_hours)
        
        # Convert hours to number of sessions
        # Round UP to nearest multiple of 1.5:
        # L=1 → 1.5 → 1 slot, L=2 → 3.0 → 2 slots, L=3 → 3.0 → 2 slots
        # L=4 → 4.5 → 3 slots, L=5 → 6.0 → 4 slots
        if lecture_hours > 0:
            adjusted_hours = math.ceil(lecture_hours / 1.5) * 1.5  # Round UP to nearest multiple of 1.5
            num_lecture_sessions = int(adjusted_hours / 1.5)
        else:
            num_lecture_sessions = 0
        
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
    
    def _find_available_large_classroom(self, day, time_str, is_elective=False, required_capacity=None):
        """Find an available large classroom for common courses or electives.
        
        Args:
            day: Day of the week
            time_str: Time slot string
            is_elective: If True, skip auditorium and only use backup classrooms
            required_capacity: Minimum capacity needed (optional)
        
        Returns:
            Classroom name or None if no classroom available
        """
        # Get available classrooms based on context
        if is_elective:
            # Electives: Use backup large classrooms only (not the main auditorium)
            candidate_classrooms = self.backup_large_classrooms
        else:
            # Common courses: Try auditorium first, then backups
            candidate_classrooms = [self.large_auditorium] + self.backup_large_classrooms
        
        # Filter by capacity if specified
        if required_capacity:
            candidate_classrooms = [
                room for room in candidate_classrooms
                if room in self.classrooms and self.classrooms[room]['capacity'] >= required_capacity
            ]
        
        # Check for conflicts
        if day not in self.global_classroom_usage or time_str not in self.global_classroom_usage[day]:
            # No conflicts, return first suitable classroom
            return candidate_classrooms[0] if candidate_classrooms else None
        
        # Find first available classroom
        for classroom in candidate_classrooms:
            if classroom not in self.global_classroom_usage[day][time_str]:
                return classroom
        
        # All classrooms taken
        return None
    
    def _find_best_classroom_by_capacity(self, day, time_str, required_capacity, is_common_course=False):
        """Find the best classroom for a given capacity requirement.
        
        For common courses: MUST use C004 (compulsory)
        For large capacity (>110): Prefer C004 auditorium
        Otherwise: Prefer smallest classroom that can accommodate the required capacity.
        
        Args:
            day: Day of the week
            time_str: Time slot string
            required_capacity: Number of students
            is_common_course: If True, MUST assign C004 (compulsory)
        
        Returns:
            Classroom name or None
        """
        # For common courses: C004 is COMPULSORY (not just preferred)
        if is_common_course:
            # Check if C004 exists
            if self.large_auditorium not in self.classrooms:
                print(f"      ERROR: C004 auditorium not found in classrooms!")
                return None
            
            # Check if C004 is available in this slot
            if day in self.global_classroom_usage and time_str in self.global_classroom_usage[day]:
                if self.large_auditorium in self.global_classroom_usage[day][time_str]:
                    # C004 is already occupied - common courses MUST use C004, so return None
                    print(f"      WARNING: C004 required for common course but occupied at {day} {time_str}")
                    return None
            
            # C004 is available - return it (compulsory for common courses)
            print(f"      Assigning C004 (compulsory for common course)")
            return self.large_auditorium
        
        # Get all suitable classrooms (capacity >= required)
        suitable_classrooms = [
            (room, info['capacity'])
            for room, info in self.classrooms.items()
            if info['capacity'] >= required_capacity and 'lab' not in info['type'].lower()
        ]
        
        if not suitable_classrooms:
            return None
        
        # For large capacity requirements (>110), prefer C004 auditorium (but not compulsory)
        if required_capacity > 110:
            # Try C004 first for large courses
            if day not in self.global_classroom_usage or time_str not in self.global_classroom_usage[day]:
                if self.large_auditorium in [room for room, _ in suitable_classrooms]:
                    return self.large_auditorium
            elif self.large_auditorium not in self.global_classroom_usage[day][time_str]:
                if self.large_auditorium in [room for room, _ in suitable_classrooms]:
                    return self.large_auditorium
        
        # For regular capacity or if C004 unavailable: Sort by capacity (smallest first for efficient allocation)
        suitable_classrooms.sort(key=lambda x: x[1])
        
        # Check for conflicts
        if day not in self.global_classroom_usage or time_str not in self.global_classroom_usage[day]:
            return suitable_classrooms[0][0]  # Return smallest suitable classroom
        
        # Find first available classroom
        for classroom, _ in suitable_classrooms:
            if classroom not in self.global_classroom_usage[day][time_str]:
                return classroom
        
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
            print(f"⚠️  No courses found for Semester {semester} in {department} department")
            print(f"   Creating empty timetable for {department} Sem {semester} Section {section}")
            print(f"   Note: Add semester {semester} course data to CSV file to populate timetable")
            # Return empty timetable instead of None
            timetable = self._initialize_timetable()
            return (timetable, {}, {})  # Empty timetable, no electives, no rotated out
        
        # Initialize timetable
        timetable = self._initialize_timetable()
        
        # Track used slots and available lab rooms per slot
        used_slots = {}  # {day: {time_slot: {'room': room, 'course': course}}}
        
        # Track session types separately for each course
        lecture_schedule = {}  # {course_code: {day: count}}
        tutorial_schedule = {}  # {course_code: {day: count}}
        lab_schedule = {}  # {course_code: {day: count}}
        lab_usage = {}  # {day: {time_slot: [used_labs]}}
        total_labs_per_day = {}  # Track TOTAL number of labs per day (constraint: max 1 per day)
        
        # Reset elective tracking
        self.elective_courses = {}
        self.rotated_out_electives = {}  # Track electives rotated out for "After Midsems"
        
        for day in self.days:
            used_slots[day] = {}
            lab_usage[day] = {}
            total_labs_per_day[day] = 0  # Initialize total lab count per day
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
            
            # Check if 'Electives' column exists (optional column)
            if 'Electives' in section_courses.columns:
                section_courses = section_courses[
                    (section_courses['Section'].str.strip() == section_letter) |
                    ((section_courses['Section'].str.strip() == '') & (section_courses['Electives'].str.strip().str.upper() == 'T')) |
                    (section_courses['Section'].isna() & (section_courses['Electives'].str.strip().str.upper() == 'T'))
                ]
            else:
                # If no 'Electives' column, just filter by section
                section_courses = section_courses[
                    (section_courses['Section'].str.strip() == section_letter) |
                    (section_courses['Section'].str.strip() == '') |
                    (section_courses['Section'].isna())
                ]
        
        print(f"\nTotal courses to schedule:")
        print(f"   Cross-department shared (DSAI+ECE): {len(cross_dept_courses)}")
        print(f"   Common courses (within dept): {len(common_courses)}")
        print(f"   Section-specific courses: {len(section_courses)}")
        
        # PRIORITY 1: Schedule cross-department shared courses (DSAI + ECE together)
        if not cross_dept_courses.empty:
            self._schedule_cross_dept_courses(cross_dept_courses, timetable, used_slots, 
                                             lecture_schedule, tutorial_schedule, lab_schedule,
                                             lab_usage, total_labs_per_day, section, semester, department)
        
        # PRIORITY 2: Schedule common courses (within department, both sections together)
        # For DSAI/ECE (no sections), don't mark as "common" - they're just regular courses
        is_truly_common = True if department not in ['DSAI', 'ECE'] else False
        
        if is_truly_common and not common_courses.empty:
            # Check if common courses are already scheduled (for Section B, copy from Section A)
            if section == 'B' and department in self.common_course_schedule and semester in self.common_course_schedule[department]:
                # Copy Section A's common course schedule to Section B (excluding labs)
                print(f"   >> Reusing common course schedule from Section A (same times + classrooms, labs excluded)")
                self._copy_common_course_schedule(timetable, used_slots, department, semester)
                # Now schedule Section B's own lab sessions for common courses (lectures/tutorials already copied)
                self._schedule_courses(common_courses, timetable, used_slots, 
                                      lecture_schedule, tutorial_schedule, lab_schedule,
                                      lab_usage, total_labs_per_day, section, semester, is_common=True, labs_only=True)
            elif section == 'A':
                # For Section A, schedule common courses and save the schedule
                self._schedule_courses(common_courses, timetable, used_slots, 
                                      lecture_schedule, tutorial_schedule, lab_schedule,
                                      lab_usage, total_labs_per_day, section, semester, is_common=True)
                # Save the scheduled common courses for Section B to reuse
                self._save_common_course_schedule(timetable, common_courses, department, semester)
        else:
            # For DSAI/ECE or non-common courses, schedule normally
            self._schedule_courses(common_courses, timetable, used_slots, 
                                  lecture_schedule, tutorial_schedule, lab_schedule,
                                  lab_usage, total_labs_per_day, section, semester, is_common=False)
        
        # PRIORITY 3: Schedule section-specific courses
        self._schedule_courses(section_courses, timetable, used_slots,
                              lecture_schedule, tutorial_schedule, lab_schedule,
                              lab_usage, total_labs_per_day, section, semester, is_common=False)
        
        # PRIORITY 4: Schedule elective baskets
        print(f"\n{'='*60}")
        print(f"ELECTIVE SCHEDULING - {department} Sem{semester} Section{section}")
        print(f"{'='*60}")
        
        # Load and group electives
        electives_df = self.load_electives_data()
        if electives_df is not None:
            elective_baskets = self.group_electives_into_baskets(electives_df, semester, department)
            if elective_baskets:
                basket_assignments = self.schedule_elective_baskets(
                    timetable, used_slots, elective_baskets, semester, section, department
                )
                print(f"   >> Successfully scheduled {len(basket_assignments)} elective baskets")
            else:
                print(f"   >> No electives found for Semester {semester}")
        else:
            print(f"   >> No electives.csv file found - skipping elective scheduling")
        
        # Report unscheduled courses
        if self.unscheduled_courses:
            print(f"\nWARNING: {len(self.unscheduled_courses)} sessions could not be scheduled:")
            for item in self.unscheduled_courses:
                print(f"   - {item}")
        else:
            print(f"\nAll courses scheduled successfully!")
        
        # Validate constraints
        self._validate_constraints(timetable, department, semester, section)
        
        # Return timetable with elective information and rotated-out courses
        return timetable, self.elective_courses, self.rotated_out_electives
    
    def _validate_constraints(self, timetable, department, semester, section):
        """Validate that all scheduling constraints are satisfied.
        
        Checks:
        1. Classroom capacity constraints
        2. Common courses use large classrooms
        3. Labs use lab rooms
        4. No double-booking of classrooms
        5. Cross-department shared courses use same time slots
        """
        print(f"\n{'='*60}")
        print(f"CONSTRAINT VALIDATION - {department} Sem{semester} Section{section}")
        print(f"{'='*60}")
        
        issues = []
        
        # Check 1: Classroom allocation from CSV
        classrooms_used = set()
        for day in timetable:
            for time_str, entry in timetable[day].items():
                if entry not in ['Free', 'LUNCH BREAK']:
                    # Extract classroom from entry (format: "Course\n(Type)\nClassroom\n...")
                    parts = entry.split('\n')
                    if len(parts) >= 3:
                        classroom = parts[2].strip()
                        classrooms_used.add(classroom)
                        
                        # Verify classroom exists in loaded CSV
                        if classroom not in self.classrooms and not classroom.startswith('Lab-'):
                            # For backward compatibility, allow hard-coded labs
                            if 'Lab' not in classroom:
                                issues.append(f"  [!] Classroom '{classroom}' not found in classrooms.csv")
        
        # Check 2: Common courses constraint
        common_large_count = 0
        for day in timetable:
            for time_str, entry in timetable[day].items():
                if 'Common' in entry or 'Shared' in entry:
                    common_large_count += 1
                    parts = entry.split('\n')
                    if len(parts) >= 3:
                        classroom = parts[2].strip()
                        # Verify it's a large classroom
                        if classroom in self.classrooms:
                            capacity = self.classrooms[classroom]['capacity']
                            if capacity < 90:  # Should be large classroom
                                issues.append(f"  [!] Common course using small classroom: {classroom} (capacity {capacity})")
        
        # Check 3: Lab courses use lab rooms
        lab_allocation_ok = True
        for day in timetable:
            for time_str, entry in timetable[day].items():
                if '-Lab' in entry or 'Lab (' in entry:
                    parts = entry.split('|')
                    if len(parts) >= 2:
                        classroom = parts[1].strip()
                        if classroom not in self.lab_rooms:
                            issues.append(f"  [!] Lab session not in lab room: {classroom}")
                            lab_allocation_ok = False
        
        # Check 4: No double-booking - verify no classroom is used by multiple courses at same time
        classroom_conflicts = []
        for day in self.global_classroom_usage:
            for time_str in self.global_classroom_usage[day]:
                classroom_usage = {}  # classroom -> [(dept, sem, sec, course), ...]
                
                for classroom in self.global_classroom_usage[day][time_str]:
                    if classroom not in classroom_usage:
                        classroom_usage[classroom] = []
                    
                    usage_info = self.global_classroom_usage[day][time_str][classroom]
                    if isinstance(usage_info, dict):
                        dept = usage_info.get('dept', 'Unknown')
                        sem = usage_info.get('semester', 'Unknown')
                        sec = usage_info.get('section', 'Unknown')
                        course = usage_info.get('course', 'Unknown')
                        classroom_usage[classroom].append(f"{dept}-Sem{sem}-{sec}: {course}")
                
                # Check for conflicts (same classroom, multiple entries)
                for classroom, usages in classroom_usage.items():
                    if len(usages) > 1:
                        classroom_conflicts.append(f"  [CONFLICT] {day} {time_str} - {classroom}: {' AND '.join(usages)}")
        
        if classroom_conflicts:
            issues.extend(classroom_conflicts)
            print(f"\n[ERROR] CLASSROOM CONFLICTS DETECTED ({len(classroom_conflicts)}):")
            for conflict in classroom_conflicts:
                print(conflict)
        
        # Print results
        print(f"\n[OK] Classrooms loaded from CSV: {len(self.classrooms)}")
        print(f"[OK] Classrooms used in timetable: {len(classrooms_used)}")
        print(f"[OK] Common/Shared courses: {common_large_count}")
        print(f"[OK] Lab rooms available: {len(self.lab_rooms)}")
        
        if issues:
            print(f"\n[WARNING] CONSTRAINT VIOLATIONS DETECTED ({len(issues)}):")
            for issue in issues:
                print(issue)
        else:
            print(f"\n[SUCCESS] ALL CONSTRAINTS SATISFIED!")
        
        print(f"{'='*60}\n")
    
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
                                     lab_usage, total_labs_per_day, section, semester, department):
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
                                 lab_usage, total_labs_per_day, section, semester, is_common=True)
            
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
        NOTE: Lab sessions are NOT copied - each section gets separate lab times.
        """
        if department not in self.common_course_schedule or semester not in self.common_course_schedule[department]:
            return
        
        saved_schedule = self.common_course_schedule[department][semester]
        
        for course_code, course_slots in saved_schedule.items():
            copied_count = 0
            for slot_info in course_slots:
                day = slot_info['day']
                time_str = slot_info['time_str']
                classroom = slot_info['classroom']
                entry = slot_info['entry']
                
                # Skip lab sessions - each section needs separate lab times
                if '-Lab' in entry or 'Lab-' in entry:
                    continue
                
                # Copy to timetable
                timetable[day][time_str] = entry
                copied_count += 1
                
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
            
            if copied_count > 0:
                print(f"   [COPIED] {course_code} - {copied_count} slots copied from Section A (labs excluded)")
    
    def _schedule_courses(self, courses_df, timetable, used_slots,
                         lecture_schedule, tutorial_schedule, lab_schedule,
                         lab_usage, total_labs_per_day, section, semester, is_common=False, labs_only=False):
        """Schedule courses into timetable
        
        Args:
            labs_only: If True, only schedule lab sessions (skip lectures and tutorials)
        """
        
        # Track which baskets we've already scheduled
        scheduled_baskets = set()
        
        for _, course in courses_df.iterrows():
            course_code = course['Course Code'].strip()
            course_title = course['Course Title'].strip()
            classroom = str(course.get('Classroom', '')).strip()
            
            # Convert empty classroom string to None for dynamic allocation
            if not classroom or classroom.lower() in ['nan', 'none', '']:
                classroom = None
            
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
            
            # Calculate required capacity
            required_capacity = None
            if is_common:
                # Common courses: Both sections A+B together OR DSAI+ECE together
                # Both need C004 auditorium (240 capacity)
                if self.current_department == 'CSE':
                    # CSE A + B together = 120 students → needs C004
                    required_capacity = 120
                else:
                    # DSAI + ECE sharing course = ~180 students → needs C004
                    required_capacity = 180
            
            # Schedule lectures (1.5 hours each)
            if not labs_only:
                for lec_num in range(lectures):
                    success = self._schedule_session(
                        timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                        lab_usage, course_code, course_title, classroom,
                        'Lecture', section, is_common, is_elective, basket,
                        required_capacity=required_capacity, department=self.current_department
                    )
                    if not success:
                        self.unscheduled_courses.append(f"{course_code} - Lecture {lec_num+1}")
            
            # Schedule tutorials (1 hour - use 1 slot)
            if not labs_only:
                for tut_num in range(tutorials):
                    success = self._schedule_session(
                        timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                        lab_usage, course_code, course_title, classroom,
                        'Tutorial', section, is_common, is_elective, basket, duration_hours=1,
                        required_capacity=required_capacity, department=self.current_department
                    )
                    if not success:
                        self.unscheduled_courses.append(f"{course_code} - Tutorial {tut_num+1}")
            
            # Schedule practicals/labs (2 hours per lab session)
            # Note: 'practicals' is already converted to number of sessions in parse_ltpsc()
            # Extract lab type from course row: 'H' for Hardware, 'S' for Software
            lab_type = str(course.get('Lab', '')).strip().upper() if not pd.isna(course.get('Lab', '')) else None
            
            # IMPORTANT: Labs are NOT treated as common even if lectures are common
            # Each section needs separate lab slots (especially for hardware labs with limited rooms)
            is_common_lab = False
            
            for prac_num in range(practicals):
                success = self._schedule_lab_session(
                    timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                    lab_usage, total_labs_per_day, course_code, course_title, classroom,
                    section, is_common_lab, is_elective, basket, lab_type_preference=lab_type
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
                         session_type, section, is_common, is_elective, basket, duration_hours=1.5,
                         required_capacity=None, department=None):
        """Schedule a single session (Lecture or Tutorial) - can use regular or flexible afternoon slots
        
        Args:
            required_capacity: Number of students (for common courses: Section A + Section B)
            department: Department name for capacity calculation
        """
        
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
                
                # For electives: Use regular classrooms (~40 students)
                # For common courses: Find classroom based on required capacity (needs C004 for 120-180)
                # For regular courses: Use specified classroom or find based on single section capacity
                actual_classroom = classroom
                if is_elective and basket:
                    # Electives use regular classrooms (not auditoriums) - ~40 students
                    actual_classroom = self._find_best_classroom_by_capacity(day, time_str, required_capacity=40)
                    if actual_classroom is None:
                        continue  # No suitable classroom available in this slot
                elif classroom is None:
                    # Need to find classroom dynamically
                    if is_common and required_capacity:
                        # Common courses: MUST use C004 (compulsory)
                        actual_classroom = self._find_best_classroom_by_capacity(day, time_str, required_capacity, is_common_course=True)
                    elif department and not is_common:
                        # Section-specific: Use single section capacity
                        section_capacity = self.section_size.get(department, 50)  # Default 50
                        actual_classroom = self._find_best_classroom_by_capacity(day, time_str, section_capacity)
                    else:
                        # Fallback to large classroom finder
                        actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=False)
                    
                    if actual_classroom is None:
                        continue  # No suitable classroom available in this slot
                
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
                
                # For electives: Use regular classrooms (~40 students)
                # For common courses: Find classroom based on required capacity (needs C004 for 120-180)
                # For regular courses: Use specified classroom or find based on single section capacity
                actual_classroom = classroom
                if is_elective and basket:
                    # Electives use regular classrooms (not auditoriums) - ~40 students
                    actual_classroom = self._find_best_classroom_by_capacity(day, time_str, required_capacity=40)
                    if actual_classroom is None:
                        continue  # No suitable classroom available in this slot
                elif classroom is None:
                    # Need to find classroom dynamically
                    if is_common and required_capacity:
                        # Common courses: Use capacity-based allocation (needs C004 for 120-180 students)
                        actual_classroom = self._find_best_classroom_by_capacity(day, time_str, required_capacity)
                    elif department and not is_common:
                        # Section-specific: Use single section capacity
                        section_capacity = self.section_size.get(department, 50)  # Default 50
                        actual_classroom = self._find_best_classroom_by_capacity(day, time_str, section_capacity)
                    else:
                        # Fallback to large classroom finder
                        actual_classroom = self._find_available_large_classroom(day, time_str, is_elective=False)
                    
                    if actual_classroom is None:
                        continue  # No suitable classroom available in this slot
                
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
    
    def _find_two_available_labs(self, day, time_str, lab_usage, lab_type_preference=None):
        """Find 2 available lab rooms for a session to accommodate 80 students
        
        Args:
            day: Day of the week
            time_str: Time slot string
            lab_usage: Lab usage tracking dictionary
            lab_type_preference: 'S' for Software, 'H' for Hardware, or None
        
        Returns:
            Tuple of (lab1, lab2) if available, else (None, None)
        """
        used_labs = lab_usage[day].get(time_str, [])
        available_labs = []
        
        # Filter labs by type if specified
        if lab_type_preference:
            candidate_labs = []
            for lab in self.lab_rooms:
                if lab in self.classrooms:
                    # Check both 'type' and 'description' keys (fallback to 'type')
                    lab_desc = self.classrooms[lab].get('type', self.classrooms[lab].get('description', '')).lower()
                    if lab_type_preference == 'S' and 'software' in lab_desc:
                        candidate_labs.append(lab)
                    elif lab_type_preference == 'H' and 'hardware' in lab_desc:
                        candidate_labs.append(lab)
                    elif lab_type_preference not in ['S', 'H']:
                        candidate_labs.append(lab)
            
            if not candidate_labs:
                candidate_labs = self.lab_rooms  # Fallback to all labs
        else:
            candidate_labs = self.lab_rooms
        
        # Find available labs
        for lab in candidate_labs:
            if lab not in used_labs:
                # Check GLOBAL usage
                global_conflict = False
                if day in self.global_classroom_usage and time_str in self.global_classroom_usage[day]:
                    if lab in self.global_classroom_usage[day][time_str]:
                        global_conflict = True
                
                if not global_conflict:
                    available_labs.append(lab)
        
        # Return 2 labs if available
        if len(available_labs) >= 2:
            return (available_labs[0], available_labs[1])
        else:
            return (None, None)
    
    def _schedule_lab_session(self, timetable, used_slots, lecture_schedule, tutorial_schedule,
                             lab_schedule, lab_usage, total_labs_per_day, course_code, course_title, classroom,
                             section, is_common, is_elective, basket, lab_type_preference=None):
        """Schedule a 2-hour lab session in dedicated afternoon flexible slots
        
        For lab sessions, we assign 2 lab rooms together to accommodate ~80 students
        CONSTRAINT: Maximum 1 lab per day across all courses
        
        Args:
            lab_type_preference: 'S' for Software Lab, 'H' for Hardware Lab, None for any
        """
        
        # Lab type preference is now passed as parameter from course data
        # 'S' = Software Lab, 'H' = Hardware Lab, None = any available
        
        # Labs are 2 hours and should use the afternoon 2-hour flexible slots
        # This gives priority to labs for these slots
        
        # Get day priority order (prioritize underutilized days like Friday)
        day_priority = self._get_day_priority_order(timetable)
        
        # Try each day in priority order
        for day in day_priority:
            # CONSTRAINT: Maximum 1 lab per day across all courses (prevent 2 labs on same day)
            if total_labs_per_day[day] >= 1:
                continue
            
            # Enforce: Max 1 lab session per course per day
            if lab_schedule[course_code][day] >= self.max_labs_per_day:
                continue
            
            # Try afternoon flexible slots (perfect for 2-hour labs)
            for time_slot in self.afternoon_flex_slots:
                time_str = f"{time_slot[0]}-{time_slot[1]}"
                
                # Check if slot is free
                if timetable[day][time_str] != 'Free':
                    continue
                
                # Find 2 available lab rooms (to accommodate 80 students)
                lab1, lab2 = self._find_two_available_labs(day, time_str, lab_usage, lab_type_preference)
                
                if not lab1 or not lab2:
                    continue
                
                # Create combined lab room label
                combined_labs = f"{lab1} & {lab2}"
                
                # Create label for lab session
                if is_elective and basket:
                    label = f"Elective Lab ({basket})"
                elif is_common:
                    label = f"{course_code}-Lab (Common)"
                else:
                    label = f"{course_code}-Lab-{section}"
                
                # Schedule the lab (full 2 hours) with both rooms
                timetable[day][time_str] = f"{label} [120min] | {combined_labs}"
                
                # Mark both labs as used
                if time_str not in lab_usage[day]:
                    lab_usage[day][time_str] = []
                lab_usage[day][time_str].append(lab1)
                lab_usage[day][time_str].append(lab2)
                
                # Mark in used_slots with duration info
                if day not in used_slots:
                    used_slots[day] = {}
                if time_str not in used_slots[day]:
                    used_slots[day][time_str] = {}
                
                used_slots[day][time_str][course_code] = {
                    'room': combined_labs,
                    'course': course_code,
                    'type': 'Lab',
                    'duration_minutes': 120,  # Full 2 hours
                    'slot_capacity_minutes': 120,  # Afternoon slots are 2 hours
                    'is_elective': is_elective,
                    'basket': basket
                }
                
                # Record GLOBAL classroom usage for both labs
                self._record_global_classroom_usage(
                    day, time_str, lab1,
                    self.current_department, self.current_semester, self.current_section, course_code
                )
                self._record_global_classroom_usage(
                    day, time_str, lab2,
                    self.current_department, self.current_semester, self.current_section, course_code
                )
                
                # Update lab schedule counters
                lab_schedule[course_code][day] += 1
                total_labs_per_day[day] += 1  # Track total labs per day (constraint: max 1 per day)
                
                return True
        
        print(f"      WARNING: Could not schedule lab for {course_code} (need 2 available labs)")
        return False
    
    def export_to_csv(self, timetable, filename, electives=None, rotated_out=None, output_dir='timetable_outputs'):
        """Export timetable to CSV and elective basket data to JSON"""
        if timetable is None:
            return False
        
        # Convert to DataFrame
        df = pd.DataFrame(timetable).T
        
        os.makedirs(output_dir, exist_ok=True)

        filepath = os.path.join(output_dir, filename)
        
        # Export timetable to CSV (clean, without elective info in CSV)
        df.to_csv(filepath, index=True, encoding='utf-8')
        
        # Export elective basket data to JSON file
        if electives and len(electives) > 0:
            json_filepath = filepath.replace('.csv', '_Electives.json')
            import json
            
            # Build elective data with classroom assignments
            elective_data = {}
            available_classrooms = self.backup_large_classrooms.copy()
            
            for basket_name, courses in electives.items():
                elective_data[basket_name] = []
                has_tutorials = False
                for idx, course in enumerate(courses):
                    # Assign different classroom to each course in basket
                    if idx < len(available_classrooms):
                        assigned_classroom = available_classrooms[idx]
                    else:
                        assigned_classroom = available_classrooms[idx % len(available_classrooms)]
                    
                    tutorial_count = course.get('T', 0)
                    if tutorial_count > 0:
                        has_tutorials = True
                    
                    elective_data[basket_name].append({
                        'code': course['code'],
                        'title': course['title'],
                        'classroom': assigned_classroom,
                        'tutorials': tutorial_count,
                        'credits': course.get('credits', 0)
                    })
                
                # Add metadata about tutorials
                elective_data[basket_name + '_meta'] = {
                    'has_tutorials': has_tutorials,
                    'tutorial_courses': [c['code'] for c in courses if c.get('T', 0) > 0]
                }
            
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(elective_data, f, indent=2, ensure_ascii=False)
            
            print(f"Elective baskets saved: {json_filepath}")
        
        print(f"Timetable saved: {filepath}")
        return True
    
    def print_timetable(self, timetable):
        """Print timetable to console"""
        if timetable is None:
            return
        
        df = pd.DataFrame(timetable).T
        print("\n" + str(df))
        
        # Determine which baskets are used in THIS timetable (check if courses exist, not just timetable content)
        baskets_in_timetable = set()
        
        # Check timetable content for basket labels
        for day, slots in timetable.items():
            for time, content in slots.items():
                if isinstance(content, str):
                    content_lower = content.lower()
                    if 'hss' in content_lower:
                        baskets_in_timetable.add('HSS')
                    if 'elective a' in content_lower or 'elective_a' in content_lower:
                        baskets_in_timetable.add('Elective A')
                    if 'elective c' in content_lower or 'elective_c' in content_lower:
                        baskets_in_timetable.add('Elective C')
        
        # Also check if we have any elective courses stored - if yes, show them
        if self.elective_courses:
            for basket in self.elective_courses.keys():
                if basket == 'HSS':
                    baskets_in_timetable.add('HSS')
                elif basket == 'Elective A':
                    baskets_in_timetable.add('Elective A')
                elif basket == 'Elective C':
                    baskets_in_timetable.add('Elective C')
        
        # Only print elective details if baskets are used
        if baskets_in_timetable:
            print("\n" + "-"*80)
            print("ELECTIVE BASKET DETAILS:")
            print("-"*80)
            
            available_classrooms = self.backup_large_classrooms.copy()
            
            # Collect courses by basket type (merge all instances)
            all_hss_courses = []
            all_elective_a_courses = []
            all_elective_b_courses = []
            all_elective_c_courses = []
            
            for basket, courses in self.elective_courses.items():
                if basket == 'HSS':
                    all_hss_courses.extend(courses)
                elif basket == 'Elective A':
                    all_elective_a_courses.extend(courses)
                elif basket == 'Elective B':
                    all_elective_b_courses.extend(courses)
                elif basket == 'Elective C':
                    all_elective_c_courses.extend(courses)
            
            # Collect Elective B from rotated_out
            for basket, courses in self.rotated_out_electives.items():
                if basket == 'Elective B':
                    all_elective_b_courses.extend(courses)
            
            # Print only baskets that appear in timetable (plus Elective B if Elective A exists)
            
            # HSS Electives
            if 'HSS' in baskets_in_timetable and all_hss_courses:
                print("\n==> HSS ELECTIVES (Whole Semester)")
                print("-" * 80)
                print("Scheduled in timetable above. Courses in this basket:")
                has_tutorials = any(c.get('T', 0) > 0 for c in all_hss_courses)
                for idx, course in enumerate(all_hss_courses):
                    if idx < len(available_classrooms):
                        assigned_classroom = available_classrooms[idx]
                    else:
                        assigned_classroom = available_classrooms[idx % len(available_classrooms)]
                    tutorial_info = f" [Tutorial: {course.get('T', 0)}T]" if course.get('T', 0) > 0 else ""
                    print(f"   {course['code']}: {course['title']} - {assigned_classroom}{tutorial_info}")
                if has_tutorials:
                    print(f"   NOTE: Tutorial sessions scheduled separately in the timetable")
            
            # Elective C (Whole Semester)
            if 'Elective C' in baskets_in_timetable and all_elective_c_courses:
                print("\n==> ELECTIVE C (Whole Semester - 3-4 Credits)")
                print("-" * 80)
                print("Scheduled in timetable above. Runs throughout the semester:")
                has_tutorials = any(c.get('T', 0) > 0 for c in all_elective_c_courses)
                for idx, course in enumerate(all_elective_c_courses):
                    if idx < len(available_classrooms):
                        assigned_classroom = available_classrooms[idx]
                    else:
                        assigned_classroom = available_classrooms[idx % len(available_classrooms)]
                    tutorial_info = f" [Tutorial: {course.get('T', 0)}T]" if course.get('T', 0) > 0 else ""
                    print(f"   {course['code']}: {course['title']} - {assigned_classroom}{tutorial_info}")
                if has_tutorials:
                    print(f"   NOTE: Tutorial sessions scheduled separately in the timetable")
            
            # Elective A (Till Mid-Semester)
            if 'Elective A' in baskets_in_timetable and all_elective_a_courses:
                print("\n==> ELECTIVE A (Till Mid-Semester - 1-2 Credits)")
                print("-" * 80)
                print("Scheduled in timetable above. Runs ONLY till mid-semester exams.")
                print("After mid-semester, these slots will be used by Elective B courses.")
                print("\nCourses in Elective A:")
                has_tutorials = any(c.get('T', 0) > 0 for c in all_elective_a_courses)
                for idx, course in enumerate(all_elective_a_courses):
                    if idx < len(available_classrooms):
                        assigned_classroom = available_classrooms[idx]
                    else:
                        assigned_classroom = available_classrooms[idx % len(available_classrooms)]
                    tutorial_info = f" [Tutorial: {course.get('T', 0)}T]" if course.get('T', 0) > 0 else ""
                    print(f"   {course['code']}: {course['title']} - {assigned_classroom}{tutorial_info}")
                if has_tutorials:
                    print(f"   NOTE: Tutorial sessions scheduled separately in the timetable")
                
                # Always show Elective B if it exists
                if all_elective_b_courses:
                    print("\n==> ELECTIVE B (After Mid-Semester - 1-2 Credits)")
                    print("-" * 80)
                    print("These courses START AFTER mid-semester exams.")
                    print("They will use the SAME time slots as Elective A courses shown above.")
                    print("\nCourses in Elective B (replacing Elective A after mid-semester):")
                    has_tutorials_b = any(c.get('T', 0) > 0 for c in all_elective_b_courses)
                    for idx, course in enumerate(all_elective_b_courses):
                        if idx < len(available_classrooms):
                            assigned_classroom = available_classrooms[idx]
                        else:
                            assigned_classroom = available_classrooms[idx % len(available_classrooms)]
                        tutorial_info = f" [Tutorial: {course.get('T', 0)}T]" if course.get('T', 0) > 0 else ""
                        print(f"   {course['code']}: {course['title']} - {assigned_classroom}{tutorial_info}")
                    if has_tutorials_b:
                        print(f"   NOTE: Tutorial sessions will use same tutorial slots as Elective A")
        
        print("\n" + "="*80)

def main():
    """Main function to generate all timetables"""
    # Allow overriding input/output directories via environment variables
    csv_input_folder = os.environ.get('CSV_INPUT_FOLDER', 'input_files/sdtt_inputs')
    output_csv_dir = os.environ.get('OUTPUT_CSV_DIR', 'timetable_outputs')
    output_html_dir = os.environ.get('OUTPUT_HTML_DIR', 'timetable_html')
    semester_type = os.environ.get('SEMESTER_TYPE', 'even')  # 'even' or 'odd'

    generator = TimetableGenerator(csv_input_folder)
    
    departments = ['CSE', 'DSAI', 'ECE']
    
    # Set semesters based on semester type
    if semester_type == 'odd':
        semesters = [1, 3, 5, 7]
        print("\n📅 SEMESTER TYPE: ODD (Sem 1, 3, 5, 7)")
        print("⚠️  Note: Ensure your CSV files contain data for odd semesters")
    else:
        semesters = [2, 4, 6, 8]
        print("\n📅 SEMESTER TYPE: EVEN (Sem 2, 4, 6, 8)")
        print("⚠️  Note: Semester 8 requires data in your CSV files")
    
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
                
                if result:  # Result will always exist now (even if empty)
                    timetable, electives, rotated_out = result
                    generator.print_timetable(timetable)
                    filename = f"{dept}_Sem{sem}_SectionA_Timetable.csv"
                    generator.export_to_csv(timetable, filename, electives, rotated_out, output_dir=output_csv_dir)
            else:
                # CSE has sections A and B
                for sec in sections:
                    result = generator.generate_timetable(dept, sem, sec)
                    
                    if result:  # Result will always exist now (even if empty)
                        timetable, electives, rotated_out = result
                        generator.print_timetable(timetable)
                        filename = f"{dept}_Sem{sem}_Section{sec}_Timetable.csv"
                        generator.export_to_csv(timetable, filename, electives, rotated_out, output_dir=output_csv_dir)
    
    print("\n" + "="*80)
    print(">> Timetable generation completed!")
    print(f"CSV Output location: {output_csv_dir}/")
    print(f"HTML Output location: {output_html_dir}/")
    print("\nℹ️  If some semesters were skipped, add course data to your CSV files")
    print("="*80)
    
    # Return success code
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main() or 0)
