# Time Configuration Guide 🕒

## Overview
The timetable generator now supports **fully configurable time slots** that can be adjusted without modifying any core code! All timing configurations are managed through the `time_config.py` file.

## Quick Start - Changing Time Slots

### Option 1: Use a Preset Configuration
Simply change one line in `time_config.py`:

```python
# Change this line to switch presets:
ACTIVE_PRESET = 'standard'  # Default configuration

# Available presets:
# 'standard'       - Mon-Fri, 8 AM - 6:30 PM (current system)
# 'extended'       - Mon-Sat with evening classes until 8:30 PM
# 'compact'        - Mon-Fri, 9 AM - 5:30 PM (fewer slots)
# 'morning_heavy'  - Mon-Fri, 7:30 AM - 6:30 PM (more morning slots)
```

### Option 2: Create Your Custom Configuration
Add your own preset to the `PRESET_CONFIGURATIONS` dictionary:

```python
PRESET_CONFIGURATIONS['my_custom'] = {
    'working_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'regular_slots': [
        ('09:00', '10:30'),  # Slot 1 - 90 minutes
        ('10:45', '12:15'),  # Slot 2 - 90 minutes
    ],
    'lunch_slot': ('12:15', '13:15'),  # 60 minutes
    'afternoon_slots': [
        ('13:15', '15:15'),  # Afternoon slot 1 - 120 minutes
        ('15:30', '17:30'),  # Afternoon slot 2 - 120 minutes
    ],
}

# Then activate it:
ACTIVE_PRESET = 'my_custom'
```

## Detailed Preset Descriptions

### 1. **Standard Configuration** (Default)
```
Days: Monday - Friday
Regular Slots:
  • 08:00 - 09:30 (90 min) - Lectures
  • 09:45 - 11:15 (90 min) - Lectures
  • 11:30 - 13:00 (90 min) - Lectures
Lunch: 13:00 - 14:30
Afternoon Slots:
  • 14:30 - 16:30 (120 min) - Labs/Lectures/Tutorials
  • 16:30 - 18:30 (120 min) - Labs/Lectures
```

**Best for:** Standard academic schedules with balanced morning/afternoon sessions

---

### 2. **Extended Configuration**
```
Days: Monday - Saturday
Regular Slots:
  • 08:00 - 09:30 (90 min)
  • 09:45 - 11:15 (90 min)
  • 11:30 - 13:00 (90 min)
Lunch: 13:00 - 14:00
Afternoon Slots:
  • 14:00 - 16:00 (120 min)
  • 16:15 - 18:15 (120 min)
  • 18:30 - 20:30 (120 min) - Evening classes
```

**Best for:** Heavy course loads, institutions with Saturday classes, evening programs

---

### 3. **Compact Configuration**
```
Days: Monday - Friday
Regular Slots:
  • 09:00 - 10:30 (90 min)
  • 10:45 - 12:15 (90 min)
Lunch: 12:15 - 13:15
Afternoon Slots:
  • 13:15 - 15:15 (120 min)
  • 15:30 - 17:30 (120 min)
```

**Best for:** Lighter course loads, shorter school days, summer semesters

---

### 4. **Morning-Heavy Configuration**
```
Days: Monday - Friday
Regular Slots:
  • 07:30 - 09:00 (90 min) - Early start
  • 09:15 - 10:45 (90 min)
  • 11:00 - 12:30 (90 min)
  • 12:45 - 14:15 (90 min)
Lunch: 14:15 - 15:15
Afternoon Slots:
  • 15:15 - 17:15 (120 min)
```

**Best for:** Institutions preferring early starts, maximizing morning productivity

---

## Enabling Saturday Classes by Department

You can enable Saturday classes for specific departments and semesters:

```python
SATURDAY_ENABLED_FOR = {
    ('ECE', 4): True,   # Enable Saturday for ECE Semester 4
    ('CSE', 6): True,   # Enable Saturday for CSE Semester 6
    ('DSAI', 2): True,  # Enable Saturday for DSAI Semester 2
}
```

**Important:** Saturday classes only work if your active preset includes Saturday in `working_days`.

---

## How to Use

### Step 1: Validate Your Configuration
Before generating timetables, test your configuration:

```bash
cd timetable_generator
py time_config.py
```

This will show:
- ✓ Validation status
- Current active configuration details
- All available presets
- Any configuration errors

### Step 2: Generate Timetables
Once validated, generate timetables normally:

```bash
py main.py
```

The system will automatically:
- Load your time configuration
- Display which preset is active
- Generate timetables using your custom slots

### Step 3: Generate HTML Views
```bash
py timetable_to_html.py
```

---

## Configuration Rules & Guidelines

### Time Slot Rules
1. **Regular Slots:** Typically 90 minutes for lectures
2. **Afternoon Slots:** Typically 120 minutes for labs/tutorials
3. **Lunch Slot:** At least 60 minutes recommended
4. **Gaps:** 15-minute breaks between slots recommended

### Time Format
- Use 24-hour format: `'HH:MM'`
- Examples: `'08:00'`, `'13:30'`, `'18:45'`

### Working Days
- Must be full day names: `'Monday'`, `'Tuesday'`, etc.
- Case-sensitive
- Saturday is optional based on institutional needs

---

## Validation Features

The configuration system automatically checks for:
- ✓ Overlapping time slots
- ✓ Invalid time formats
- ✓ Proper time ordering
- ✓ Minimum slot durations
- ✓ Missing required fields

Run `py time_config.py` anytime to validate your configuration.

---

## Advanced Customization

### Creating Department-Specific Time Slots
While not directly supported, you can:
1. Create multiple preset configurations
2. Switch between them before generating each department's timetable
3. Regenerate timetables as needed

### Modifying Individual Slots
You can fine-tune individual slots in your preset:

```python
'regular_slots': [
    ('08:00', '09:15'),  # 75-minute slot
    ('09:30', '11:00'),  # 90-minute slot
    ('11:15', '13:00'),  # 105-minute slot
],
```

---

## Troubleshooting

### Problem: "Time configuration is invalid"
**Solution:** Run `py time_config.py` to see specific validation errors

### Problem: Timetables look wrong after changing times
**Solution:** 
1. Verify time format is correct (HH:MM)
2. Check for overlapping slots
3. Ensure lunch slot doesn't overlap with other slots
4. Run validation script

### Problem: Saturday classes not appearing
**Solution:**
1. Check that `'Saturday'` is in your preset's `working_days`
2. Verify department/semester is enabled in `SATURDAY_ENABLED_FOR`
3. Confirm both conditions are met

### Problem: "config is not defined" error
**Solution:** 
- This is fixed in the latest version
- Update `main.py` if using an older version
- The system will fall back to default configuration

---

## Example Workflow

**Scenario:** Your institution wants to start classes at 8:30 AM instead of 8:00 AM

1. **Edit time_config.py:**
   ```python
   PRESET_CONFIGURATIONS['my_schedule'] = {
       'working_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
       'regular_slots': [
           ('08:30', '10:00'),  # Changed from 08:00
           ('10:15', '11:45'),  # Adjusted accordingly
           ('12:00', '13:30'),  # Adjusted accordingly
       ],
       'lunch_slot': ('13:30', '14:30'),
       'afternoon_slots': [
           ('14:30', '16:30'),
           ('16:30', '18:30'),
       ],
   }
   
   ACTIVE_PRESET = 'my_schedule'
   ```

2. **Validate:**
   ```bash
   py time_config.py
   ```

3. **Generate:**
   ```bash
   py main.py
   py timetable_to_html.py
   ```

4. **Done!** All timetables now use 8:30 AM start time.

---

## Benefits of Configurable Time Slots

✅ **No Code Editing:** Change times without touching scheduling logic  
✅ **Multiple Presets:** Switch between different schedules easily  
✅ **Validation Built-in:** Catch errors before generating timetables  
✅ **Department Flexibility:** Enable Saturday for specific departments  
✅ **Easy Testing:** Try different configurations quickly  
✅ **Maintainable:** Clear separation of configuration and logic  

---

## Files Modified

When you change time configuration, only **one file** needs to be edited:
- `time_config.py` - All time slot definitions

No changes needed to:
- `main.py` - Core scheduling engine (automatically uses config)
- `excel_exporter.py` - Excel generation
- `schedule_generator.py` - Schedule logic
- Any other core files

---

## Support

If you need help with time configuration:
1. Run `py time_config.py` to validate
2. Check this guide for examples
3. Review the comments in `time_config.py`
4. Refer to `USER_MANUAL.md` for general usage

---

**Last Updated:** December 2024  
**Version:** 2.1.0 (Dynamic Time Configuration)
