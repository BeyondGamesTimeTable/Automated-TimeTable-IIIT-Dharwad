# Exam Timetable Configuration Guide

## Overview
The exam timetable system now supports **dynamic configuration** through a user-friendly web interface. You can customize exam dates, session timings, and weekend exclusions without modifying any code!

## Features
✅ **Custom Date Range** - Select any start and end dates for your exam period  
✅ **Flexible Session Times** - Configure forenoon and afternoon session timings  
✅ **Weekend Management** - Choose to include or exclude Saturdays/Sundays  
✅ **JSON Export** - Download configuration for use with Python scripts  
✅ **Validation** - Automatic checks for minimum duration and valid date ranges  

---

## Quick Start Guide

### Method 1: Using the Web Interface (Recommended)

1. **Open the Configuration Page**
   - Navigate to: `exam_timetable/exam_config.html`
   - Or access from main menu: "Configure & Generate Exam Timetable"

2. **Set Your Exam Period**
   - **Start Date**: Click the date picker and select exam start date
   - **End Date**: Click the date picker and select exam end date
   - Minimum period: 3 days
   - End date must be after start date

3. **Configure Session Times**
   - **Forenoon Start**: Default 10:00 AM
   - **Forenoon End**: Default 01:00 PM (13:00)
   - **Afternoon Start**: Default 02:00 PM (14:00)
   - **Afternoon End**: Default 05:00 PM (17:00)

4. **Choose Weekend Exclusions**
   - ☑️ **Exclude Saturdays**: Check to skip Saturdays
   - ☑️ **Exclude Sundays**: Check to skip Sundays
   - Both are enabled by default

5. **Save Configuration**
   - Click **"Save & Download Configuration"**
   - File `exam_config.json` will be downloaded
   - Configuration also saved to browser's localStorage

6. **Generate Exam Timetable**
   - Place downloaded `exam_config.json` in `exam_timetable/` folder
   - Run: `python exam_timetable/main.py`
   - Or click **"View Existing Exam Timetable"** if already generated

---

### Method 2: Directly Edit JSON File

Create or edit `exam_timetable/exam_config.json`:

```json
{
  "start_date": "2025-04-15",
  "end_date": "2025-04-25",
  "fn_start": "10:00",
  "fn_end": "13:00",
  "an_start": "14:00",
  "an_end": "17:00",
  "exclude_saturday": true,
  "exclude_sunday": true
}
```

Then run: `python exam_timetable/main.py`

---

## Configuration Parameters

| Parameter | Type | Format | Default | Description |
|-----------|------|--------|---------|-------------|
| `start_date` | String | YYYY-MM-DD | 2025-04-15 | Exam period start date |
| `end_date` | String | YYYY-MM-DD | 2025-04-25 | Exam period end date |
| `fn_start` | String | HH:MM | 10:00 | Forenoon session start time |
| `fn_end` | String | HH:MM | 13:00 | Forenoon session end time |
| `an_start` | String | HH:MM | 14:00 | Afternoon session start time |
| `an_end` | String | HH:MM | 17:00 | Afternoon session end time |
| `exclude_saturday` | Boolean | true/false | true | Skip Saturdays in scheduling |
| `exclude_sunday` | Boolean | true/false | true | Skip Sundays in scheduling |

---

## Example Configurations

### Example 1: Standard 10-Day Exam Period
```json
{
  "start_date": "2025-04-15",
  "end_date": "2025-04-25",
  "fn_start": "10:00",
  "fn_end": "13:00",
  "an_start": "14:00",
  "an_end": "17:00",
  "exclude_saturday": true,
  "exclude_sunday": true
}
```
**Result**: Exams scheduled Mon-Fri only, 2 sessions/day = ~9 exam days

---

### Example 2: Weekend-Inclusive Exam Period
```json
{
  "start_date": "2025-04-15",
  "end_date": "2025-04-22",
  "fn_start": "10:00",
  "fn_end": "13:00",
  "an_start": "14:00",
  "an_end": "17:00",
  "exclude_saturday": false,
  "exclude_sunday": false
}
```
**Result**: Exams scheduled 7 days a week including weekends

---

### Example 3: Extended Session Timings
```json
{
  "start_date": "2025-05-01",
  "end_date": "2025-05-15",
  "fn_start": "09:00",
  "fn_end": "12:30",
  "an_start": "13:30",
  "an_end": "17:00",
  "exclude_saturday": true,
  "exclude_sunday": true
}
```
**Result**: Earlier start time with longer sessions

---

## Validation Rules

The system automatically validates your configuration:

✅ **Date Range Validation**
- End date must be after start date
- Minimum exam period: 3 days
- Both dates are required

✅ **Time Format Validation**
- Must be in HH:MM format (24-hour)
- All session times are required

✅ **Logical Checks**
- FN end time should be before AN start time
- Sufficient slots generated for all exams
- Warning if too few slots for scheduled exams

---

## How It Works

### 1. Configuration Loading
```python
# In exam_scheduler.py
def load_configuration(self, config_file):
    # Reads exam_config.json if exists
    # Falls back to default values if not found
    # Parses dates, times, and exclusion rules
```

### 2. Slot Generation
```python
def _calculate_available_slots(self):
    # Iterates from start_date to end_date
    # Skips weekends if configured
    # Creates FN and AN slots for each valid day
    # Returns list of available exam slots
```

### 3. Exam Scheduling
- System loads your configuration automatically
- Generates exam slots based on date range
- Schedules courses optimally across available slots
- Creates seating arrangements and HTML outputs

---

## Output Files Generated

After running with your configuration:

📊 **exam_schedule.csv** - Complete exam schedule with dates  
🪑 **seating_summary.csv** - All seating arrangements  
🌐 **exam_timetable.html** - Interactive HTML timetable  
📁 **seating_charts/** - Individual classroom seating charts  

---

## Troubleshooting

### Issue: Configuration not loading
**Solution**: Ensure `exam_config.json` is in `exam_timetable/` directory

### Issue: Insufficient slots warning
**Solution**: 
- Extend end date
- Include weekends (uncheck exclusions)
- Verify you have enough exam days for all courses

### Issue: Invalid date format
**Solution**: Use YYYY-MM-DD format (e.g., 2025-04-15)

### Issue: Default values used
**Solution**: Check JSON syntax - missing commas, quotes, or braces

---

## Technical Details

### File Locations
```
exam_timetable/
├── exam_config.html       # Configuration web interface
├── exam_config.json       # Your saved configuration
├── main.py                # Run this to generate timetables
├── src/
│   └── exam_scheduler.py  # Core scheduling logic
└── outputs/
    ├── exam_timetable.html
    ├── exam_schedule.csv
    └── seating_charts/
```

### Default Configuration
If no `exam_config.json` found, system uses:
- Start: 2025-04-15
- End: 2025-04-25
- FN: 10:00-13:00
- AN: 14:00-17:00
- Exclude both weekends

---

## Tips for Best Results

💡 **Exam Duration Planning**
- Count your courses (typically ~60 courses)
- Calculate needed slots: courses ÷ 2 = minimum exam days
- Add buffer days for flexibility

💡 **Avoid Tight Schedules**
- Leave 1-2 extra days beyond minimum
- Accounts for uneven course distribution
- Prevents slot shortage warnings

💡 **Weekend Considerations**
- Including weekends = more flexibility
- Excluding weekends = more days needed
- Check academic calendar for holidays

💡 **Session Timing**
- Standard 3-hour sessions work well
- Ensure break between FN and AN sessions
- Consider student/faculty preferences

---

## Support

For issues or questions:
1. Check this README first
2. Verify JSON syntax at [jsonlint.com](https://jsonlint.com)
3. Review console output for specific errors
4. Check that exam_config.json exists in correct location

---

## Version History

**v2.0** - Dynamic Configuration System
- Added web-based configuration interface
- JSON-based configuration loading
- Flexible date ranges and session times
- Weekend inclusion/exclusion options

**v1.0** - Initial Release
- Hardcoded exam dates and times
- Fixed 9-day exam period
- Manual code editing required

---

**Made with ❤️ for IIIT Dharwad**  
*Automated Exam Timetable Generation System*
