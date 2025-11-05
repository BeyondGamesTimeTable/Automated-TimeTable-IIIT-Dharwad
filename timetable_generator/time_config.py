"""
Time Configuration for Timetable Generator
===========================================

This file contains all time slot configurations for the timetable generator.
You can easily modify time slots here without changing the main code.

Author: BeyondGames Team
Version: 1.0.0
"""

# ============================================================================
# TIME SLOT CONFIGURATIONS
# ============================================================================

# Working days configuration
WORKING_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# You can add Saturday if needed:
# WORKING_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Special configuration: Enable Saturday for specific departments/semesters
SATURDAY_ENABLED_FOR = {
    # Format: (department, semester): True/False
    ('ECE', 4): True,  # ECE Semester 4 has Saturday classes
    # Add more if needed:
    # ('CSE', 6): True,
    # ('DSAI', 4): True,
}

# ============================================================================
# MORNING/REGULAR TIME SLOTS (90-minute slots for lectures)
# ============================================================================
# These are used for regular lectures and can accommodate tutorials
REGULAR_SLOTS = [
    ('08:00', '09:30'),  # 90 minutes - Slot 1
    ('09:45', '11:15'),  # 90 minutes - Slot 2 (15 min break after Slot 1)
    ('11:30', '13:00'),  # 90 minutes - Slot 3 (15 min break after Slot 2)
]

# ============================================================================
# LUNCH BREAK
# ============================================================================
LUNCH_SLOT = ('13:00', '14:30')  # 90 minutes lunch break

# ============================================================================
# AFTERNOON FLEXIBLE SLOTS (120-minute slots)
# ============================================================================
# These longer slots can accommodate:
# - Full 2-hour labs
# - 90-minute lectures
# - 60-minute tutorials
AFTERNOON_FLEX_SLOTS = [
    ('14:30', '16:30'),  # 120 minutes - Flexible Slot 1
    ('16:30', '18:30'),  # 120 minutes - Flexible Slot 2
]

# ============================================================================
# OPTIONAL: EVENING SLOTS (if needed)
# ============================================================================
# Uncomment these if you want to add evening slots
# EVENING_SLOTS = [
#     ('18:30', '20:00'),  # 90 minutes - Evening Slot 1
#     ('20:00', '21:30'),  # 90 minutes - Evening Slot 2
# ]

# To enable evening slots, add them to AFTERNOON_FLEX_SLOTS:
# AFTERNOON_FLEX_SLOTS = AFTERNOON_FLEX_SLOTS + EVENING_SLOTS

# ============================================================================
# BREAK DURATIONS (in minutes)
# ============================================================================
# These are used for display purposes and documentation
SHORT_BREAK = 15  # Between regular morning slots
LUNCH_BREAK = 90  # Lunch duration
EVENING_BREAK = 0  # Break before evening slots (if any)

# ============================================================================
# CUSTOM TIME SLOT CONFIGURATIONS
# ============================================================================

# Example: Different timing for different days
CUSTOM_DAY_TIMINGS = {
    # 'Monday': {
    #     'regular_slots': [('08:00', '09:30'), ('09:45', '11:15')],
    #     'afternoon_slots': [('14:30', '16:30')],
    # },
    # 'Friday': {
    #     'regular_slots': [('08:00', '09:30'), ('09:45', '11:15'), ('11:30', '13:00')],
    #     'afternoon_slots': [('14:00', '16:00')],  # End early on Friday
    # },
}

# ============================================================================
# PRESET TIME CONFIGURATIONS
# ============================================================================
# You can define multiple preset configurations and switch between them

PRESET_CONFIGURATIONS = {
    'standard': {
        'working_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'regular_slots': [
            ('08:00', '09:30'),
            ('09:45', '11:15'),
            ('11:30', '13:00'),
        ],
        'lunch_slot': ('13:00', '14:30'),
        'afternoon_slots': [
            ('14:30', '16:30'),
            ('16:30', '18:30'),
        ],
    },
    
    'extended': {
        'working_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        'regular_slots': [
            ('08:00', '09:30'),
            ('09:45', '11:15'),
            ('11:30', '13:00'),
        ],
        'lunch_slot': ('13:00', '14:00'),  # Shorter lunch
        'afternoon_slots': [
            ('14:00', '16:00'),
            ('16:00', '18:00'),
            ('18:00', '20:00'),  # Evening slot
        ],
    },
    
    'compact': {
        'working_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'regular_slots': [
            ('09:00', '10:30'),
            ('10:45', '12:15'),
        ],
        'lunch_slot': ('12:15', '13:15'),
        'afternoon_slots': [
            ('13:15', '15:15'),
            ('15:30', '17:30'),
        ],
    },
    
    'morning_heavy': {
        'working_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'regular_slots': [
            ('07:30', '09:00'),  # Early start
            ('09:15', '10:45'),
            ('11:00', '12:30'),
            ('12:45', '14:15'),
        ],
        'lunch_slot': ('14:15', '15:15'),
        'afternoon_slots': [
            ('15:15', '17:15'),
        ],
    },
}

# ============================================================================
# ACTIVE CONFIGURATION
# ============================================================================
# Change this to switch between preset configurations
ACTIVE_PRESET = 'standard'  # Options: 'standard', 'extended', 'compact', 'morning_heavy'

# ============================================================================
# COURSE-SPECIFIC TIME SLOT PINNING
# ============================================================================
"""
Pin specific courses to specific time slots.
This allows you to force a course to be scheduled at a particular day/time.

Format:
COURSE_TIME_PINNING = {
    'CourseCode': {
        'day': 'DayName',           # Monday, Tuesday, etc.
        'slot': ('HH:MM', 'HH:MM'), # Time slot tuple
        'type': 'Lecture' or 'Tutorial' or 'Lab',  # Session type (optional)
        'classroom': 'RoomCode',    # Specific classroom (optional)
    }
}

Examples below show different use cases:
"""

COURSE_TIME_PINNING = {
    # Example 1: Pin CS165 (Common course) to Monday 8:00-9:30
    # 'CS165': {
    #     'day': 'Monday',
    #     'slot': ('08:00', '09:30'),
    #     'type': 'Lecture',
    #     'classroom': 'C004',  # Optional: specify classroom
    # },
    
    # Example 2: Pin HS205 lectures to specific slots
    # 'HS205': {
    #     'day': 'Tuesday',
    #     'slot': ('09:45', '11:15'),
    #     'type': 'Lecture',
    # },
    
    # Example 3: Pin a lab to afternoon slot
    # 'CS163': {
    #     'day': 'Wednesday',
    #     'slot': ('14:30', '16:30'),
    #     'type': 'Lab',
    #     'classroom': 'Lab-1',
    # },
    
    # Example 4: Pin multiple sessions of same course (use course-type key)
    # 'MA163-Lecture-1': {
    #     'course_code': 'MA163',
    #     'day': 'Monday',
    #     'slot': ('08:00', '09:30'),
    #     'type': 'Lecture',
    # },
    # 'MA163-Lecture-2': {
    #     'course_code': 'MA163',
    #     'day': 'Tuesday',
    #     'slot': ('08:00', '09:30'),
    #     'type': 'Lecture',
    # },
    # 'MA163-Tutorial': {
    #     'course_code': 'MA163',
    #     'day': 'Friday',
    #     'slot': ('09:45', '11:15'),
    #     'type': 'Tutorial',
    # },
}

# ============================================================================
# DEPARTMENT/SEMESTER SPECIFIC COURSE PINNING
# ============================================================================
"""
Pin courses for specific departments and semesters.
This is useful when you want different pinning rules for different sections.

Format:
DEPT_COURSE_PINNING = {
    ('Department', Semester, 'Section'): {
        'CourseCode': {...pinning config...}
    }
}
"""

DEPT_COURSE_PINNING = {
    # Example: CSE Semester 2, Section A
    # ('CSE', 2, 'A'): {
    #     'CS165': {
    #         'day': 'Monday',
    #         'slot': ('08:00', '09:30'),
    #         'type': 'Lecture',
    #         'classroom': 'C004',
    #     },
    #     'MA163': {
    #         'day': 'Tuesday',
    #         'slot': ('09:45', '11:15'),
    #         'type': 'Lecture',
    #     },
    # },
    
    # Example: ECE Semester 4, Section A
    # ('ECE', 4, 'A'): {
    #     'HS205': {
    #         'day': 'Thursday',
    #         'slot': ('14:30', '16:30'),
    #         'type': 'Lecture',
    #     },
    # },
}

# ============================================================================
# AVOID SPECIFIC TIME SLOTS FOR COURSES
# ============================================================================
"""
Specify time slots that should be avoided for specific courses.
This is useful when you want to ensure a course is NOT scheduled at certain times.

Format:
COURSE_AVOID_SLOTS = {
    'CourseCode': [
        {'day': 'DayName', 'slot': ('HH:MM', 'HH:MM')},
        ...
    ]
}
"""

COURSE_AVOID_SLOTS = {
    # Example: Don't schedule CS307 on Monday mornings
    # 'CS307': [
    #     {'day': 'Monday', 'slot': ('08:00', '09:30')},
    #     {'day': 'Monday', 'slot': ('09:45', '11:15')},
    # ],
    
    # Example: Avoid Friday afternoon for DS309
    # 'DS309': [
    #     {'day': 'Friday', 'slot': ('14:30', '16:30')},
    #     {'day': 'Friday', 'slot': ('16:30', '18:30')},
    # ],
}

# ============================================================================
# PREFERRED TIME SLOTS FOR COURSE TYPES
# ============================================================================
"""
Specify preferred time slots for different types of courses.
The scheduler will try to use these slots first (but not force them).
"""

PREFERRED_SLOTS = {
    'Lab': [
        ('14:30', '16:30'),  # Prefer afternoon slots for labs
        ('16:30', '18:30'),
    ],
    'Tutorial': [
        ('09:45', '11:15'),  # Prefer mid-morning for tutorials
        ('11:30', '13:00'),
    ],
    'Lecture': [
        ('08:00', '09:30'),  # Prefer early morning for lectures
        ('09:45', '11:15'),
    ],
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_active_config():
    """
    Returns the currently active time configuration.
    Modify ACTIVE_PRESET above to switch configurations.
    """
    if ACTIVE_PRESET in PRESET_CONFIGURATIONS:
        return PRESET_CONFIGURATIONS[ACTIVE_PRESET]
    else:
        # Default to custom configuration
        return {
            'working_days': WORKING_DAYS,
            'regular_slots': REGULAR_SLOTS,
            'lunch_slot': LUNCH_SLOT,
            'afternoon_slots': AFTERNOON_FLEX_SLOTS,
        }

def get_all_time_slots():
    """Returns all time slots combined (for timetable display)"""
    config = get_active_config()
    return config['regular_slots'] + [config['lunch_slot']] + config['afternoon_slots']

def get_time_slot_duration(start_time, end_time):
    """Calculate duration in minutes between two time strings"""
    from datetime import datetime
    fmt = '%H:%M'
    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)
    duration = (end - start).total_seconds() / 60
    return int(duration)

def validate_time_config():
    """Validate that time configuration is correct"""
    config = get_active_config()
    errors = []
    
    # Check if working days is not empty
    if not config['working_days']:
        errors.append("ERROR: No working days configured!")
    
    # Check if regular slots exist
    if not config['regular_slots']:
        errors.append("ERROR: No regular slots configured!")
    
    # Check for time overlaps
    all_slots = config['regular_slots'] + config['afternoon_slots']
    for i, (start1, end1) in enumerate(all_slots):
        for j, (start2, end2) in enumerate(all_slots):
            if i != j:
                if start2 < end1 and start1 < end2:
                    errors.append(f"WARNING: Time overlap detected: {start1}-{end1} and {start2}-{end2}")
    
    if errors:
        for error in errors:
            print(error)
        return False
    else:
        print("✓ Time configuration is valid!")
        return True

def print_time_config():
    """Print the current time configuration in a readable format"""
    config = get_active_config()
    
    print("\n" + "="*80)
    print(f"ACTIVE TIME CONFIGURATION: {ACTIVE_PRESET}")
    print("="*80)
    
    print(f"\nWorking Days: {', '.join(config['working_days'])}")
    
    print("\nRegular Slots (90-minute):")
    for i, (start, end) in enumerate(config['regular_slots'], 1):
        duration = get_time_slot_duration(start, end)
        print(f"  Slot {i}: {start} - {end} ({duration} minutes)")
    
    print(f"\nLunch Break: {config['lunch_slot'][0]} - {config['lunch_slot'][1]}")
    
    print("\nAfternoon Flexible Slots (120-minute):")
    for i, (start, end) in enumerate(config['afternoon_slots'], 1):
        duration = get_time_slot_duration(start, end)
        print(f"  Slot {i}: {start} - {end} ({duration} minutes)")
    
    print("\n" + "="*80)

def get_course_pinning(course_code, department=None, semester=None, section=None):
    """
    Get pinning configuration for a specific course.
    
    Args:
        course_code: The course code to look up
        department: Department name (optional, for dept-specific pinning)
        semester: Semester number (optional, for dept-specific pinning)
        section: Section name (optional, for dept-specific pinning)
    
    Returns:
        dict: Pinning configuration if found, None otherwise
    """
    # First check department-specific pinning
    if department and semester and section:
        dept_key = (department, semester, section)
        if dept_key in DEPT_COURSE_PINNING:
            if course_code in DEPT_COURSE_PINNING[dept_key]:
                return DEPT_COURSE_PINNING[dept_key][course_code]
    
    # Then check global course pinning
    if course_code in COURSE_TIME_PINNING:
        return COURSE_TIME_PINNING[course_code]
    
    # Check with course_code key in case of multi-session pinning
    for key, config in COURSE_TIME_PINNING.items():
        if 'course_code' in config and config['course_code'] == course_code:
            return config
    
    return None

def should_avoid_slot(course_code, day, slot):
    """
    Check if a course should avoid a specific time slot.
    
    Args:
        course_code: The course code to check
        day: Day name (e.g., 'Monday')
        slot: Time slot tuple (e.g., ('08:00', '09:30'))
    
    Returns:
        bool: True if this slot should be avoided, False otherwise
    """
    if course_code not in COURSE_AVOID_SLOTS:
        return False
    
    avoid_list = COURSE_AVOID_SLOTS[course_code]
    for avoid_config in avoid_list:
        if avoid_config['day'] == day and avoid_config['slot'] == slot:
            return True
    
    return False

def get_preferred_slots(session_type):
    """
    Get preferred time slots for a specific session type.
    
    Args:
        session_type: 'Lecture', 'Tutorial', or 'Lab'
    
    Returns:
        list: List of preferred time slot tuples, or None if no preference
    """
    return PREFERRED_SLOTS.get(session_type, None)

def print_course_pinning_config():
    """Print all course pinning configurations"""
    print("\n" + "="*80)
    print("COURSE-SPECIFIC TIME SLOT PINNING CONFIGURATION")
    print("="*80)
    
    if COURSE_TIME_PINNING:
        print("\nGlobal Course Pinning:")
        for course, config in COURSE_TIME_PINNING.items():
            course_code = config.get('course_code', course)
            day = config.get('day', 'Not specified')
            slot = config.get('slot', ('?', '?'))
            session_type = config.get('type', 'Any')
            classroom = config.get('classroom', 'Any')
            print(f"  • {course_code}: {day} {slot[0]}-{slot[1]} ({session_type}) in {classroom}")
    else:
        print("\n  No global course pinning configured.")
    
    if DEPT_COURSE_PINNING:
        print("\nDepartment-Specific Course Pinning:")
        for dept_key, courses in DEPT_COURSE_PINNING.items():
            dept, sem, sec = dept_key
            print(f"\n  {dept} Semester {sem}, Section {sec}:")
            for course, config in courses.items():
                day = config.get('day', 'Not specified')
                slot = config.get('slot', ('?', '?'))
                session_type = config.get('type', 'Any')
                classroom = config.get('classroom', 'Any')
                print(f"    • {course}: {day} {slot[0]}-{slot[1]} ({session_type}) in {classroom}")
    else:
        print("\n  No department-specific course pinning configured.")
    
    if COURSE_AVOID_SLOTS:
        print("\nCourses with Avoided Time Slots:")
        for course, avoid_list in COURSE_AVOID_SLOTS.items():
            print(f"  • {course}:")
            for avoid_config in avoid_list:
                day = avoid_config['day']
                slot = avoid_config['slot']
                print(f"    - Avoid: {day} {slot[0]}-{slot[1]}")
    else:
        print("\n  No avoided time slots configured.")
    
    print("\n" + "="*80)

# ============================================================================
# INSTRUCTIONS FOR CUSTOMIZATION
# ============================================================================
"""
HOW TO CUSTOMIZE TIME SLOTS:
=============================

METHOD 1: MODIFY EXISTING SLOTS
--------------------------------
Simply edit the REGULAR_SLOTS, LUNCH_SLOT, and AFTERNOON_FLEX_SLOTS above.

Example - Start 30 minutes earlier:
    REGULAR_SLOTS = [
        ('07:30', '09:00'),
        ('09:15', '10:45'),
        ('11:00', '12:30'),
    ]

METHOD 2: USE A PRESET CONFIGURATION
------------------------------------
Change the ACTIVE_PRESET variable to one of the predefined configurations:
- 'standard' - Normal 8 AM to 6:30 PM schedule
- 'extended' - Includes Saturday and evening classes
- 'compact' - Fewer slots, 9 AM start
- 'morning_heavy' - More morning slots, early start

METHOD 3: CREATE YOUR OWN PRESET
---------------------------------
Add a new preset to PRESET_CONFIGURATIONS dictionary:

    'my_custom': {
        'working_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'regular_slots': [
            ('10:00', '11:30'),
            ('11:45', '13:15'),
        ],
        'lunch_slot': ('13:15', '14:15'),
        'afternoon_slots': [
            ('14:15', '16:15'),
        ],
    }

Then set: ACTIVE_PRESET = 'my_custom'

METHOD 4: ENABLE SATURDAY FOR SPECIFIC DEPARTMENTS
--------------------------------------------------
Add entries to SATURDAY_ENABLED_FOR dictionary:

    SATURDAY_ENABLED_FOR = {
        ('ECE', 4): True,
        ('CSE', 6): True,
        ('DSAI', 4): True,
    }

TESTING YOUR CONFIGURATION:
---------------------------
Run this file directly to test:
    python time_config.py

This will validate and display your configuration.
"""

# ============================================================================
# MAIN - FOR TESTING
# ============================================================================
if __name__ == '__main__':
    print("\n" + "🕒 " * 20)
    print("TIME CONFIGURATION VALIDATOR")
    print("🕒 " * 20)
    
    # Validate configuration
    is_valid = validate_time_config()
    
    # Print configuration
    print_time_config()
    
    # Print course pinning configuration
    print_course_pinning_config()
    
    # Test all presets
    print("\n" + "="*80)
    print("AVAILABLE PRESET CONFIGURATIONS:")
    print("="*80)
    for preset_name in PRESET_CONFIGURATIONS.keys():
        print(f"\n✓ {preset_name}")
    
    print("\n" + "="*80)
    print("To use a different preset, change ACTIVE_PRESET in time_config.py")
    print("="*80 + "\n")
