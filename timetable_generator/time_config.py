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
    
    # Test all presets
    print("\n" + "="*80)
    print("AVAILABLE PRESET CONFIGURATIONS:")
    print("="*80)
    for preset_name in PRESET_CONFIGURATIONS.keys():
        print(f"\n✓ {preset_name}")
    
    print("\n" + "="*80)
    print("To use a different preset, change ACTIVE_PRESET in time_config.py")
    print("="*80 + "\n")
