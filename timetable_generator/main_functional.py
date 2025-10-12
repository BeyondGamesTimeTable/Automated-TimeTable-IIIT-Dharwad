"""
BeyondGames Automated Timetable Generator - Functional Version
============================================================

This is the functional (procedural) version of the timetable generation system for IIIT Dharwad.
It reads course data from CSV files and generates optimized weekly schedules.

Author: BeyondGames Team
Version: 2.0.0 (Functional Approach)
"""
import pandas as pd
import os
from datetime import datetime, timedelta
import random

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Morning/Regular time slots (1.5 hours each) for lectures and tutorials
REGULAR_SLOTS = [
    ('08:00', '09:30'),  # 1.5 hours - Early morning slot
    ('09:45', '11:15'),  # 1.5 hours
    ('11:30', '13:00'),  # 1.5 hours
]

# Lunch break
LUNCH_SLOT = ('13:00', '14:30')

# Afternoon 2-hour FLEXIBLE slots - can be used for:
# - Labs (full 2 hours)
# - Lectures (1.5 hours of the 2-hour slot)
# - Tutorials (1 hour of the 2-hour slot)
AFTERNOON_FLEX_SLOTS = [
    ('14:30', '16:30'),  # 2 hours - Flexible slot 1
    ('16:30', '18:30'),  # 2 hours - Flexible slot 2
]

# Evening slot (1.5 hours) - for overflow classes
EVENING_SLOT = [
    ('18:30', '20:00'),  # 1.5 hours - Evening slot
]

# Combined time slots for timetable display
TIME_SLOTS = REGULAR_SLOTS + [LUNCH_SLOT] + AFTERNOON_FLEX_SLOTS + EVENING_SLOT
LARGE_AUDITORIUM = 'C004'  # 240-seater for common courses
LAB_ROOMS = ['Lab-1', 'Lab-2', 'Lab-3', 'Lab-4', 'Lab-5']

# Backup large classrooms (if C004 is unavailable)
BACKUP_LARGE_CLASSROOMS = ['C001', 'C002', 'C003', 'C101', 'C102', 'C103', 'C104']

# Strict scheduling rules
MAX_LECTURES_PER_DAY = 1
MAX_TUTORIALS_PER_DAY = 1
MAX_LABS_PER_DAY = 1

# ============================================================================
# GLOBAL CLASSROOM TRACKING (Prevents double-booking across all timetables)
# ============================================================================
GLOBAL_CLASSROOM_USAGE = {}


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_department_data(department, csv_folder='input_files/sdtt_inputs'):
    """Load CSV data for a specific department"""
    csv_file = os.path.join(csv_folder, f'Even {department}.csv')
    if not os.path.exists(csv_file):
        print(f"Warning: {csv_file} not found")
        return None
    
    df = pd.read_csv(csv_file)
    # Clean column names
    df.columns = df.columns.str.strip()
    return df


def get_courses_by_semester(df, semester):
    """Filter courses for a specific semester"""
    return df[df['Semester'] == semester].copy()


def get_day_priority_order(timetable):
    """
    Calculate priority order for days based on current usage.
    Returns days sorted by number of free slots (most free first).
    This helps fill underutilized days like Friday.
    """
    day_free_count = {}
    
    for day in DAYS:
        free_count = 0
        for time_slot in TIME_SLOTS:
            time_str = f"{time_slot[0]}-{time_slot[1]}"
            if time_slot != LUNCH_SLOT and timetable[day][time_str] == 'Free':
                free_count += 1
        day_free_count[day] = free_count
    
    # Sort days by free slots (descending) - prioritize days with most free slots
    sorted_days = sorted(DAYS, key=lambda d: day_free_count[d], reverse=True)
    return sorted_days


def find_available_large_classroom(day, time_str, global_classroom_usage):
    """
    Find an available large classroom for common courses.
    Tries C004 first, then backup large classrooms.
    
    Args:
        day: Day of the week
        time_str: Time slot string (e.g., "08:00-09:30")
        global_classroom_usage: Global tracking dictionary
        
    Returns:
        Available classroom code or None if all occupied
    """
    # Try primary large auditorium first
    classrooms_to_try = [LARGE_AUDITORIUM] + BACKUP_LARGE_CLASSROOMS
    
    for classroom in classrooms_to_try:
        # Check if this classroom is free in global usage
        is_free = True
        if day in global_classroom_usage:
            if time_str in global_classroom_usage[day]:
                if classroom in global_classroom_usage[day][time_str]:
                    is_free = False
        
        if is_free:
            return classroom
    
    return None


def record_global_classroom_usage(global_dict, day, time_str, classroom, department, semester, section, course_code):
    """
    Record classroom usage in the global tracking dictionary.
    Prevents double-booking of classrooms across different timetables.
    
    Args:
        global_dict: The GLOBAL_CLASSROOM_USAGE dictionary
        day: Day of the week
        time_str: Time slot string
        classroom: Classroom code
        department: Department name (CSE, ECE, DSAI)
        semester: Semester number
        section: Section (A, B, ...)
        course_code: Course code
    """
    if day not in global_dict:
        global_dict[day] = {}
    if time_str not in global_dict[day]:
        global_dict[day][time_str] = {}
    
    # Record which dept/sem/sec is using this classroom
    global_dict[day][time_str][classroom] = {
        'department': department,
        'semester': semester,
        'section': section,
        'course': course_code
    }


def create_session_label(course_code, session_type, section, is_common, is_elective, basket):
    """
    Create consistent session label for timetable display.
    
    Returns:
        Formatted label string
    """
    if is_elective and basket:
        return f"Elective ({basket})"
    elif is_common:
        return f"{course_code} (Common)"
    else:
        if session_type == 'Tutorial':
            return f"{course_code}-T-{section}"
        else:
            return f"{course_code}-{section}"


def has_classroom_conflict(day, time_str, classroom, used_slots, global_classroom_usage):
    """
    Check if classroom is already in use at this day/time.
    Checks both local (current timetable) and global (across all timetables) usage.
    
    Returns:
        True if there's a conflict, False if classroom is available
    """
    # Check local conflict
    if day in used_slots and time_str in used_slots[day]:
        for existing_slot in used_slots[day][time_str].values():
            if existing_slot.get('room') == classroom:
                return True
    
    # Check global conflict
    if day in global_classroom_usage:
        if time_str in global_classroom_usage[day]:
            if classroom in global_classroom_usage[day][time_str]:
                return True
    
    return False


def mark_slot_used(used_slots, day, time_str, course_code, classroom, session_type, duration_minutes, slot_duration_minutes, is_elective, basket):
    """
    Mark a time slot as used in the local tracking dictionary.
    
    Args:
        used_slots: Local tracking dictionary for current timetable
        day: Day of the week
        time_str: Time slot string
        course_code: Course code
        classroom: Classroom code
        session_type: 'Lecture', 'Tutorial', or 'Lab'
        duration_minutes: Actual duration of session
        slot_duration_minutes: Duration of the time slot
        is_elective: Boolean indicating if this is an elective
        basket: Basket name for electives
    """
    if day not in used_slots:
        used_slots[day] = {}
    if time_str not in used_slots[day]:
        used_slots[day][time_str] = {}
    
    used_slots[day][time_str][course_code] = {
        'room': classroom,
        'course': course_code,
        'type': session_type,
        'duration_minutes': duration_minutes,
        'slot_duration_minutes': slot_duration_minutes,
        'is_elective': is_elective,
        'basket': basket
    }


# ============================================================================
# COURSE CLASSIFICATION FUNCTIONS
# ============================================================================

def is_common_course(row):
    """Check if course is common across sections"""
    elective = str(row.get('Electives', '')).strip().upper()
    section = str(row.get('Section', '')).strip()
    
    # Common if it's a foundation course (F) without specific section
    return elective == 'F' and section == ''


def is_elective_course(row):
    """Check if course is an elective (Type elective)"""
    elective = str(row.get('Electives', '')).strip().upper()
    return elective == 'T'


def get_elective_basket(row):
    """Get the basket name for elective course"""
    return str(row.get('Basket', '')).strip()


def parse_ltpsc(row):
    """Parse LTPSC values"""
    lectures = int(row.get('Lectures', 0))
    tutorials = int(row.get('Tutorials', 0))
    practicals = int(row.get('Practicals', 0))
    return lectures, tutorials, practicals


# ============================================================================
# TIMETABLE INITIALIZATION FUNCTIONS
# ============================================================================

def initialize_timetable():
    """Initialize empty timetable"""
    timetable = {}
    for day in DAYS:
        timetable[day] = {}
        for time_slot in TIME_SLOTS:
            time_str = f"{time_slot[0]}-{time_slot[1]}"
            if time_slot == LUNCH_SLOT:
                timetable[day][time_str] = 'LUNCH BREAK'
            else:
                timetable[day][time_str] = 'Free'
    return timetable


def initialize_tracking_structures():
    """Initialize all tracking data structures"""
    used_slots = {}
    lab_usage = {}
    lecture_schedule = {}
    tutorial_schedule = {}
    lab_schedule = {}
    
    for day in DAYS:
        used_slots[day] = {}
        lab_usage[day] = {}
        for time_slot in TIME_SLOTS:
            lab_usage[day][f"{time_slot[0]}-{time_slot[1]}"] = []
    
    return used_slots, lab_usage, lecture_schedule, tutorial_schedule, lab_schedule


def initialize_course_tracking(course_code, lecture_schedule, tutorial_schedule, lab_schedule):
    """Initialize schedule tracking for a specific course"""
    if course_code not in lecture_schedule:
        lecture_schedule[course_code] = {}
        tutorial_schedule[course_code] = {}
        lab_schedule[course_code] = {}
        for day in DAYS:
            lecture_schedule[course_code][day] = 0
            tutorial_schedule[course_code][day] = 0
            lab_schedule[course_code][day] = 0


# ============================================================================
# SCHEDULING FUNCTIONS
# ============================================================================

def schedule_session(timetable, used_slots, lecture_schedule, tutorial_schedule,
                     lab_schedule, lab_usage, course_code, course_title, classroom,
                     session_type, section, is_common, is_elective, basket,
                     global_classroom_usage, department, semester, duration_hours=1.5):
    """
    Schedule a single session (Lecture or Tutorial) using MULTI-STAGE slot prioritization.
    
    CRITICAL: This function MUST match the OOP version in main.py exactly!
    
    Scheduling Stages (in order of priority):
        Stage 1: Try REGULAR morning slots first (08:00-13:00)
        Stage 2: Try AFTERNOON flexible slots (14:30-18:30) with duration labels
        Stage 3: Try EVENING slot (18:30-20:00) as last resort
    
    This ensures morning slots are filled first, matching the OOP implementation.
    
    Args:
        timetable: Current timetable dictionary
        used_slots: Local slot tracking
        lecture_schedule: Lecture count tracker
        tutorial_schedule: Tutorial count tracker
        lab_schedule: Lab count tracker (unused here)
        lab_usage: Lab room tracker (unused here)
        course_code: Course code
        course_title: Course title
        classroom: Assigned classroom (or None for common courses)
        session_type: 'Lecture' or 'Tutorial'
        section: Section (A, B, ...)
        is_common: Boolean - is this a common course?
        is_elective: Boolean - is this an elective?
        basket: Elective basket name
        global_classroom_usage: Global classroom tracking dict (prevents double-booking)
        department: Department name (CSE, ECE, DSAI)
        semester: Semester number
        duration_hours: Duration in hours (1.5 for lectures, 1.0 for tutorials)
        
    Returns:
        True if scheduled successfully, False otherwise
    """
    
    # Determine session-specific settings
    if session_type == 'Lecture':
        session_schedule = lecture_schedule
        max_per_day = MAX_LECTURES_PER_DAY
        duration_minutes = 90  # 1.5 hours
    elif session_type == 'Tutorial':
        session_schedule = tutorial_schedule
        max_per_day = MAX_TUTORIALS_PER_DAY
        duration_minutes = 60  # 1 hour
    else:
        session_schedule = lecture_schedule  # Fallback
        max_per_day = 1
        duration_minutes = 90
    
    # Get day priority order (prioritize underutilized days like Friday)
    day_priority = get_day_priority_order(timetable)
    
    # ========================================================================
    # STAGE 1: Try REGULAR morning slots FIRST (08:00-13:00)
    # ========================================================================
    for day in day_priority:
        # Enforce strict rule: max 1 lecture/tutorial per course per day
        if session_schedule[course_code][day] >= max_per_day:
            continue
        
        # Prevent lecture+tutorial on same day for same course
        if session_type == 'Lecture' and tutorial_schedule[course_code][day] > 0:
            continue
        elif session_type == 'Tutorial' and lecture_schedule[course_code][day] > 0:
            continue
        
        # Try each regular morning slot
        for time_slot in REGULAR_SLOTS:
            time_str = f"{time_slot[0]}-{time_slot[1]}"
            
            # Check if slot is free in timetable
            if timetable[day][time_str] != 'Free':
                continue
            
            # For common courses, dynamically find large classroom
            actual_classroom = classroom
            if is_common and classroom is None:
                actual_classroom = find_available_large_classroom(day, time_str, global_classroom_usage)
                if actual_classroom is None:
                    continue  # No large classroom available
            
            # Check classroom conflicts (local + global)
            if has_classroom_conflict(day, time_str, actual_classroom, used_slots, global_classroom_usage):
                continue
            
            # Schedule the session in regular slot
            label = create_session_label(course_code, session_type, section, is_common, is_elective, basket)
            
            if is_elective and basket:
                timetable[day][time_str] = label  # No classroom for electives in grid
            else:
                timetable[day][time_str] = f"{label} | {actual_classroom}"
            
            # Mark slot as used locally
            mark_slot_used(used_slots, day, time_str, course_code, actual_classroom, 
                          session_type, duration_minutes, 90, is_elective, basket)
            
            # Record classroom usage globally
            record_global_classroom_usage(global_classroom_usage, day, time_str, 
                                         actual_classroom, department, semester, section, course_code)
            
            # Update session count
            session_schedule[course_code][day] += 1
            
            return True
    
    # ========================================================================
    # STAGE 2: Try AFTERNOON FLEXIBLE slots (14:30-18:30)
    # ========================================================================
    # These are 2-hour slots that can fit lectures (90min) or tutorials (60min)
    # Show duration info: [90min] or [60min]
    
    for day in day_priority:
        if session_schedule[course_code][day] >= max_per_day:
            continue
        
        if session_type == 'Lecture' and tutorial_schedule[course_code][day] > 0:
            continue
        elif session_type == 'Tutorial' and lecture_schedule[course_code][day] > 0:
            continue
        
        # Try each afternoon flexible slot
        for time_slot in AFTERNOON_FLEX_SLOTS:
            time_str = f"{time_slot[0]}-{time_slot[1]}"
            
            if timetable[day][time_str] != 'Free':
                continue
            
            # For common courses, dynamically find large classroom
            actual_classroom = classroom
            if is_common and classroom is None:
                actual_classroom = find_available_large_classroom(day, time_str, global_classroom_usage)
                if actual_classroom is None:
                    continue
            
            # Check classroom conflicts
            if has_classroom_conflict(day, time_str, actual_classroom, used_slots, global_classroom_usage):
                continue
            
            # Schedule in afternoon flexible slot WITH duration display
            label = create_session_label(course_code, session_type, section, is_common, is_elective, basket)
            duration_display = f"{duration_minutes}min"
            
            if is_elective and basket:
                timetable[day][time_str] = f"{label} [{duration_display}]"
            else:
                timetable[day][time_str] = f"{label} [{duration_display}] | {actual_classroom}"
            
            # Mark slot as used (120-minute slot, but actual usage is duration_minutes)
            mark_slot_used(used_slots, day, time_str, course_code, actual_classroom,
                          session_type, duration_minutes, 120, is_elective, basket)
            
            # Record global usage
            record_global_classroom_usage(global_classroom_usage, day, time_str,
                                         actual_classroom, department, semester, section, course_code)
            
            session_schedule[course_code][day] += 1
            
            return True
    
    # ========================================================================
    # STAGE 3: Try EVENING slot (18:30-20:00) as LAST RESORT
    # ========================================================================
    
    for day in day_priority:
        if session_schedule[course_code][day] >= max_per_day:
            continue
        
        if session_type == 'Lecture' and tutorial_schedule[course_code][day] > 0:
            continue
        elif session_type == 'Tutorial' and lecture_schedule[course_code][day] > 0:
            continue
        
        # Try evening slot
        for time_slot in EVENING_SLOT:
            time_str = f"{time_slot[0]}-{time_slot[1]}"
            
            if timetable[day][time_str] != 'Free':
                continue
            
            # For common courses, dynamically find large classroom
            actual_classroom = classroom
            if is_common and classroom is None:
                actual_classroom = find_available_large_classroom(day, time_str, global_classroom_usage)
                if actual_classroom is None:
                    continue
            
            # Check classroom conflicts
            if has_classroom_conflict(day, time_str, actual_classroom, used_slots, global_classroom_usage):
                continue
            
            # Schedule in evening slot
            label = create_session_label(course_code, session_type, section, is_common, is_elective, basket)
            
            if is_elective and basket:
                timetable[day][time_str] = label
            else:
                timetable[day][time_str] = f"{label} | {actual_classroom}"
            
            # Mark slot as used
            mark_slot_used(used_slots, day, time_str, course_code, actual_classroom,
                          session_type, duration_minutes, 90, is_elective, basket)
            
            # Record global usage
            record_global_classroom_usage(global_classroom_usage, day, time_str,
                                         actual_classroom, department, semester, section, course_code)
            
            session_schedule[course_code][day] += 1
            
            return True
    
    # ========================================================================
    # All stages failed - could not schedule
    # ========================================================================
    print(f"      WARNING: Could not schedule {course_code} - {session_type}")
    return False


def schedule_lab_session(timetable, used_slots, lecture_schedule, tutorial_schedule,
                         lab_schedule, lab_usage, course_code, course_title, classroom,
                         section, is_common, is_elective, basket,
                         global_classroom_usage, department, semester):
    """
    Schedule a 2-hour lab session in dedicated afternoon flexible slots.
    CRITICAL: Must match main.py's _schedule_lab_session() exactly!
    
    Labs are 2 hours and use the AFTERNOON_FLEX_SLOTS (14:30-16:30, 16:30-18:30).
    Each afternoon slot is 2 hours, perfect for labs.
    
    Args:
        (same as schedule_session plus global_classroom_usage, department, semester)
        
    Returns:
        True if lab scheduled successfully, False otherwise
    """
    
    # Get day priority order (prioritize underutilized days like Friday)
    day_priority = get_day_priority_order(timetable)
    
    # Try each day in priority order
    for day in day_priority:
        # Enforce: Max 1 lab session per course per day
        if lab_schedule[course_code][day] >= MAX_LABS_PER_DAY:
            continue
        
        # Try afternoon flexible slots (2-hour blocks - perfect for labs!)
        for time_slot in AFTERNOON_FLEX_SLOTS:
            time_str = f"{time_slot[0]}-{time_slot[1]}"
            
            # Check if slot is free
            if timetable[day][time_str] != 'Free':
                continue
            
            # Find an available lab room
            used_labs = lab_usage[day].get(time_str, [])
            available_lab = None
            
            for lab in LAB_ROOMS:
                if lab not in used_labs:
                    # Check GLOBAL usage to prevent double-booking
                    global_conflict = False
                    if day in global_classroom_usage and time_str in global_classroom_usage[day]:
                        if lab in global_classroom_usage[day][time_str]:
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
            
            # Schedule the lab (full 2 hours) with [120min] duration label
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
            record_global_classroom_usage(
                global_classroom_usage, day, time_str, available_lab,
                department, semester, section, course_code
            )
            
            # Update lab schedule
            lab_schedule[course_code][day] += 1
            
            return True
    
    print(f"      WARNING: Could not schedule lab for {course_code}")
    return False


def schedule_courses(courses_df, timetable, used_slots,
                     lecture_schedule, tutorial_schedule, lab_schedule,
                     lab_usage, section, semester, is_common, elective_courses, unscheduled_courses,
                     global_classroom_usage, department):
    """Schedule courses into timetable (with global classroom tracking)"""
    
    # Track which baskets we've already scheduled
    scheduled_baskets = set()
    
    for _, course in courses_df.iterrows():
        course_code = course['Course Code'].strip()
        course_title = course['Course Title'].strip()
        classroom = str(course.get('Classroom', '')).strip()
        
        # Check if this is an elective course
        is_elective = is_elective_course(course)
        basket = get_elective_basket(course) if is_elective else None
        
        # Store elective info for later display
        if is_elective and basket:
            if basket not in elective_courses:
                elective_courses[basket] = []
            elective_courses[basket].append({
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
        
        # For common courses, classroom will be dynamically assigned (pass None)
        if is_common:
            classroom = None  # Will be dynamically found by find_available_large_classroom()
        
        lectures, tutorials, practicals = parse_ltpsc(course)
        
        # For electives: Find the maximum L, T, P across all courses in the basket
        if is_elective and basket:
            basket_courses = courses_df[
                (courses_df['Electives'].str.strip().str.upper() == 'T') &
                (courses_df['Basket'].str.strip() == basket)
            ]
            max_lectures = basket_courses['Lectures'].max()
            max_tutorials = basket_courses['Tutorials'].max()
            max_practicals = basket_courses['Practicals'].max()
            
            lectures = int(max_lectures) if not pd.isna(max_lectures) else 0
            tutorials = int(max_tutorials) if not pd.isna(max_tutorials) else 0
            practicals = int(max_practicals) if not pd.isna(max_practicals) else 0
        
        # Initialize course schedule tracking
        initialize_course_tracking(course_code, lecture_schedule, tutorial_schedule, lab_schedule)
        
        print(f"\n   Scheduling: {course_code} - L:{lectures} T:{tutorials} P:{practicals}")
        
        # Schedule lectures (1.5 hours each)
        for lec_num in range(lectures):
            success = schedule_session(
                timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                lab_usage, course_code, course_title, classroom,
                'Lecture', section, is_common, is_elective, basket,
                global_classroom_usage, department, semester
            )
            if not success:
                unscheduled_courses.append(f"{course_code} - Lecture {lec_num+1}")
        
        # Schedule tutorials (1 hour - use 1 slot)
        for tut_num in range(tutorials):
            success = schedule_session(
                timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                lab_usage, course_code, course_title, classroom,
                'Tutorial', section, is_common, is_elective, basket,
                global_classroom_usage, department, semester, duration_hours=1
            )
            if not success:
                unscheduled_courses.append(f"{course_code} - Tutorial {tut_num+1}")
        
        # Schedule practicals/labs (2 hours per lab session)
        # Practicals value represents credits: 2 credits = 1 lab session (2 hours), 4 credits = 2 lab sessions
        num_lab_sessions = practicals // 2  # Each lab session is 2 hours (2 credits)
        for prac_num in range(num_lab_sessions):
            success = schedule_lab_session(
                timetable, used_slots, lecture_schedule, tutorial_schedule, lab_schedule,
                lab_usage, course_code, course_title, classroom,
                section, is_common, is_elective, basket,
                global_classroom_usage, department, semester
            )
            if not success:
                unscheduled_courses.append(f"{course_code} - Lab {prac_num+1}")


# ============================================================================
# MAIN TIMETABLE GENERATION FUNCTION
# ============================================================================

def generate_timetable(department, semester, section='A', csv_folder='input_files/sdtt_inputs'):
    """
    Generate timetable for a specific department, semester, and section.
    Uses GLOBAL_CLASSROOM_USAGE to prevent double-booking across all timetables.
    """
    print(f"\n{'='*80}")
    print(f"Generating Timetable: {department} - Semester {semester} - Section {section}")
    print(f"{'='*80}")
    
    # Dynamic Saturday scheduling for ECE Semester 4 (high course load)
    global DAYS, GLOBAL_CLASSROOM_USAGE
    if department == 'ECE' and semester == 4:
        DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        print(">> Saturday classes enabled for ECE Semester 4 (high load optimization)")
    else:
        DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # Load department data
    df = load_department_data(department, csv_folder)
    if df is None:
        return None
    
    # Get courses for specific semester
    courses_df = get_courses_by_semester(df, semester)
    if courses_df.empty:
        print(f"No courses found for Semester {semester}")
        return None
    
    # Initialize timetable and tracking structures
    timetable = initialize_timetable()
    used_slots, lab_usage, lecture_schedule, tutorial_schedule, lab_schedule = initialize_tracking_structures()
    
    # Initialize elective and unscheduled tracking
    elective_courses = {}
    unscheduled_courses = []
    
    # Separate common and section-specific courses
    common_courses = courses_df[courses_df.apply(is_common_course, axis=1)]
    section_courses = courses_df[~courses_df.apply(is_common_course, axis=1)]
    
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
    
    # Schedule common courses first (pass global_classroom_usage)
    schedule_courses(common_courses, timetable, used_slots, 
                    lecture_schedule, tutorial_schedule, lab_schedule,
                    lab_usage, section, semester, True, elective_courses, unscheduled_courses,
                    GLOBAL_CLASSROOM_USAGE, department)
    
    # Schedule section-specific courses (pass global_classroom_usage)
    schedule_courses(section_courses, timetable, used_slots,
                    lecture_schedule, tutorial_schedule, lab_schedule,
                    lab_usage, section, semester, False, elective_courses, unscheduled_courses,
                    GLOBAL_CLASSROOM_USAGE, department)
    
    # Report unscheduled courses
    if unscheduled_courses:
        print(f"\nWARNING: {len(unscheduled_courses)} sessions could not be scheduled:")
        for item in unscheduled_courses:
            print(f"   - {item}")
    else:
        print(f"\nAll courses scheduled successfully!")
    
    # Return timetable with elective information and rotated courses (for compatibility with main.py)
    # Note: rotated_out_electives would contain "After Midsems" courses if we tracked them separately
    rotated_out_electives = {}  # Placeholder for compatibility
    return timetable, elective_courses, rotated_out_electives


# ============================================================================
# OUTPUT FUNCTIONS
# ============================================================================

def export_to_csv(timetable, filename, electives=None, output_dir='timetable_outputs'):
    """Export timetable to CSV with elective information"""
    if timetable is None:
        return False
    
    # Convert to DataFrame
    df = pd.DataFrame(timetable).T
    
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
    
    print(f"Timetable saved: {filepath}")
    return True


def print_timetable(timetable):
    """Print timetable to console"""
    if timetable is None:
        return
    
    df = pd.DataFrame(timetable).T
    print("\n" + str(df))
    print("\n" + "="*80)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to generate all timetables"""
    global GLOBAL_CLASSROOM_USAGE
    
    departments = ['CSE', 'DSAI', 'ECE']
    semesters = [2, 4, 6]
    sections = ['A', 'B']
    
    print("\nBeyondGames Enhanced Timetable Generator - Functional Version")
    print("="*80)
    print("Generating timetables from CSV files...")
    print("="*80)
    
    # Reset global classroom usage at the start
    GLOBAL_CLASSROOM_USAGE = {}
    
    for dept in departments:
        for sem in semesters:
            for sec in sections:
                result = generate_timetable(dept, sem, sec)
                
                if result:
                    timetable, electives, rotated_out = result
                    print_timetable(timetable)
                    filename = f"{dept}_Sem{sem}_Section{sec}_Timetable.csv"
                    export_to_csv(timetable, filename, electives)
    
    print("\nAll timetables generated successfully!")
    print(f"CSV Output location: timetable_outputs/")
    print(f"HTML Output location: timetable_html/")


if __name__ == "__main__":
    main()
