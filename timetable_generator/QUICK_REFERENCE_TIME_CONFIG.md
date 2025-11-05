# 🕒 Quick Reference: Adjustable Time Slots

## ⚡ Quick Start (3 Steps)

### 1️⃣ Choose Your Schedule
Open `time_config.py` and change this line:
```python
ACTIVE_PRESET = 'standard'  # Change to: extended, compact, or morning_heavy
```

### 2️⃣ Validate (Optional but Recommended)
```bash
py time_config.py
```
Look for: `✓ Time configuration is valid!`

### 3️⃣ Generate Timetables
```bash
py main.py
py timetable_to_html.py
```

## 📋 Available Presets

| Preset | Best For | Days | Hours | Slots |
|--------|----------|------|-------|-------|
| `standard` | Normal schedule | Mon-Fri | 8 AM - 6:30 PM | 5 slots |
| `extended` | Heavy load + Saturday | Mon-Sat | 8 AM - 8:30 PM | 6 slots |
| `compact` | Lighter schedule | Mon-Fri | 9 AM - 5:30 PM | 4 slots |
| `morning_heavy` | Early start | Mon-Fri | 7:30 AM - 5:15 PM | 5 slots |

## 🎯 Common Tasks

### Change Start Time
```python
# In time_config.py, modify regular_slots:
'regular_slots': [
    ('09:00', '10:30'),  # Changed from 08:00
    ('10:45', '12:15'),
    ('12:00', '13:30'),
],
```

### Enable Saturday Classes
```python
# In time_config.py:
SATURDAY_ENABLED_FOR = {
    ('ECE', 4): True,   # Enable for ECE Semester 4
    ('CSE', 6): True,   # Enable for CSE Semester 6
}
```

### Create Custom Schedule
```python
# In time_config.py, add to PRESET_CONFIGURATIONS:
PRESET_CONFIGURATIONS['my_custom'] = {
    'working_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'regular_slots': [
        ('08:30', '10:00'),
        ('10:15', '11:45'),
    ],
    'lunch_slot': ('12:00', '13:00'),
    'afternoon_slots': [
        ('13:00', '15:00'),
        ('15:15', '17:15'),
    ],
}

# Activate it:
ACTIVE_PRESET = 'my_custom'
```

## ⚠️ Important Rules

✅ **DO:**
- Use 24-hour format: `'08:00'`, `'13:30'`
- Use full day names: `'Monday'`, `'Tuesday'`
- Run validation before generating: `py time_config.py`
- Keep 15-minute gaps between slots

❌ **DON'T:**
- Use 12-hour format: `'8:00 AM'` ❌
- Abbreviate days: `'Mon'`, `'Tue'` ❌
- Create overlapping time slots
- Edit `main.py` directly

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Time configuration is invalid" | Run `py time_config.py` to see errors |
| Saturday not showing | Check both `working_days` AND `SATURDAY_ENABLED_FOR` |
| Timetables look wrong | Verify time format is `'HH:MM'` |
| Config not loading | Check for syntax errors in `time_config.py` |

## 📚 Need More Help?

- 📖 **Full Guide:** `TIME_CONFIGURATION_GUIDE.md`
- 📖 **User Manual:** `USER_MANUAL.md`
- 🧪 **Test Config:** `py time_config.py`
- 💡 **Examples:** See comments in `time_config.py`

## 🎓 Example Workflow

**Scenario:** Start classes at 9 AM instead of 8 AM

1. **Edit** `time_config.py`:
   ```python
   ACTIVE_PRESET = 'compact'  # This preset starts at 9 AM
   ```

2. **Validate**:
   ```bash
   py time_config.py
   ```

3. **Generate**:
   ```bash
   py main.py
   ```

4. **Done!** All timetables now start at 9 AM 🎉

---

## 📁 Files You'll Edit

- **time_config.py** - All time slot configurations (ONLY file you need to edit!)

## 📁 Files That Update Automatically

- main.py - Uses your configuration automatically
- All CSV outputs - Generated with your times
- All HTML views - Displays your schedule

---

**Version:** 2.1.0 | **Last Updated:** December 2024
