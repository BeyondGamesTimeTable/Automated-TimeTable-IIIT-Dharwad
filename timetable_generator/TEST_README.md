# Test Suite for Sankalp Timetable Generator

Comprehensive test suite for testing the main.py timetable generation functions.

## Test Coverage

### 1. Initialization Tests (`TestTimetableGeneratorInit`)
- Generator initialization
- Days configuration
- Time slots setup
- Lunch slot validation
- Minor slot configuration

### 2. Data Loading Tests (`TestDataLoading`)
- CSE department data loading
- DSAI department data loading
- ECE department data loading
- Invalid department handling
- Electives data loading
- Minors data loading
- Column validation

### 3. Classroom Management Tests (`TestClassroomManagement`)
- Classroom loading
- Auditorium retrieval
- Large classroom retrieval
- Lab room retrieval
- Regular classroom retrieval

### 4. Course Filtering Tests (`TestCourseFiltering`)
- Semester-based filtering
- LTPSC parsing
- Common course detection

### 5. Timetable Initialization Tests (`TestTimetableInitialization`)
- Basic timetable structure
- Minor slot for Semester 3+
- No minor slot for Semester 1-2
- Lunch break placement

### 6. Slot Duration Tests (`TestSlotDuration`)
- 60-minute slot calculation
- 90-minute slot calculation
- Lunch slot duration

### 7. Cross-Department Tests (`TestCrossDepartmentCourses`)
- Shared course detection
- Cross-department course filtering

### 8. Timetable Generation Tests (`TestTimetableGeneration`)
- CSE Sem 2 Section A generation
- DSAI Sem 2 Section A generation
- ECE Sem 2 Section A generation
- Invalid department handling

### 9. CSV Export Tests (`TestCSVExport`)
- CSV file creation
- File structure validation
- Data integrity

### 10. Elective Basket Tests (`TestElectiveBaskets`)
- Basket grouping logic
- Elective course organization

### 11. Minor Courses Tests (`TestMinorCourses`)
- Minors CSV loading
- Multi-semester parsing
- Column validation

## Running the Tests

### Run All Tests
```bash
cd timetable_generator
python test_main.py
```

### Run Specific Test Class
```bash
python -m unittest test_main.TestDataLoading
```

### Run Specific Test Method
```bash
python -m unittest test_main.TestDataLoading.test_load_cse_data
```

### Run with Verbose Output
```bash
python -m unittest test_main -v
```

## Test Results

The test suite will display:
- Number of tests run
- Number of successes
- Number of failures
- Number of errors
- Overall success rate

Example output:
```
======================================================================
TEST SUMMARY
======================================================================
Tests Run: 45
Successes: 43
Failures: 1
Errors: 1
Success Rate: 95.6%
======================================================================
```

## Requirements

All tests use the same requirements as the main application:
- Python 3.12+
- pandas 2.0+
- Standard library modules (unittest, os, sys, tempfile, datetime)

## Test Data

Tests use the sample CSV files located in:
- `input_files/sdtt_inputs/CSE.csv`
- `input_files/sdtt_inputs/DSAI.csv`
- `input_files/sdtt_inputs/ECE.csv`
- `input_files/sdtt_inputs/electives.csv`
- `input_files/sdtt_inputs/minors.csv`

## Notes

- Tests create temporary files during CSV export testing
- All temporary files are automatically cleaned up
- Tests are independent and can run in any order
- Some tests may be skipped if optional files (electives, minors) are not present

## Troubleshooting

### Import Errors
Ensure you're running tests from the `timetable_generator` directory:
```bash
cd timetable_generator
python test_main.py
```

### File Not Found Errors
Verify sample CSV files exist in `input_files/sdtt_inputs/`

### Test Failures
Check that:
1. CSV files have correct format and columns
2. Python version is 3.12+
3. pandas is installed and up to date

## Adding New Tests

To add new tests:

1. Create a new test class inheriting from `unittest.TestCase`
2. Add setup/teardown methods if needed
3. Write test methods (must start with `test_`)
4. Add the test class to `run_test_suite()` function

Example:
```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_new_function(self):
        result = self.generator.new_function()
        self.assertIsNotNone(result)
```

## Contributors

Team BeyondGames - IIIT Dharwad
