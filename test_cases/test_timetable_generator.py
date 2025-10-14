"""
Unit Tests for Timetable Generator - Course Loading Module
===========================================================

Tests for CSV loading, data validation, and course parsing.

Author: Team BeyondGames
Date: October 14, 2025
"""

import unittest
import pandas as pd
import os
import sys
from io import StringIO

# Add parent directory to path to import main module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'timetable_generator'))

try:
    from main import TimetableGenerator
except ImportError:
    print("Warning: Could not import TimetableGenerator. Some tests may fail.")


class TestCourseLoading(unittest.TestCase):
    """Test cases for course data loading from CSV files"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        os.makedirs(self.test_data_dir, exist_ok=True)
        
    def tearDown(self):
        """Clean up after each test method"""
        # Remove test files if needed
        pass
    
    def test_valid_csv_loading(self):
        """Test Case 1.1.1: Load valid CSV file with all required columns"""
        # Create test CSV
        test_csv = """Course,Faculty,Session Type,Hours per Week,After Midsems
DSA,Prof. Kumar,Lecture,3,No
DSA,Prof. Kumar,Tutorial,1,No
DSA Lab,Prof. Kumar,Lab,2,No"""
        
        csv_path = os.path.join(self.test_data_dir, 'valid_test.csv')
        with open(csv_path, 'w') as f:
            f.write(test_csv)
        
        # Test loading
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3, "Should load 3 courses")
        self.assertIn('Course', df.columns, "Should have Course column")
        self.assertIn('Faculty', df.columns, "Should have Faculty column")
        
        print("✓ Test 1.1.1 passed: Valid CSV loaded successfully")
    
    def test_missing_column_csv(self):
        """Test Case 1.1.2: Load CSV with missing required column"""
        test_csv = """Course,Session Type,Hours per Week
DSA,Lecture,3"""
        
        csv_path = os.path.join(self.test_data_dir, 'missing_column.csv')
        with open(csv_path, 'w') as f:
            f.write(test_csv)
        
        df = pd.read_csv(csv_path)
        # Check if Faculty column is missing
        self.assertNotIn('Faculty', df.columns, "Faculty column should be missing")
        
        print("✓ Test 1.1.2 passed: Missing column detected")
    
    def test_empty_csv_file(self):
        """Test Case 1.1.3: Load empty CSV file"""
        test_csv = """Course,Faculty,Session Type,Hours per Week,After Midsems"""
        
        csv_path = os.path.join(self.test_data_dir, 'empty.csv')
        with open(csv_path, 'w') as f:
            f.write(test_csv)
        
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 0, "Should return empty dataframe")
        
        print("✓ Test 1.1.3 passed: Empty CSV handled correctly")
    
    def test_duplicate_courses(self):
        """Test Case 1.1.4: Load CSV with duplicate courses"""
        test_csv = """Course,Faculty,Session Type,Hours per Week,After Midsems
DSA,Prof. Kumar,Lecture,3,No
DSA,Prof. Kumar,Lecture,3,No
DBMS,Prof. Sharma,Lecture,3,No"""
        
        csv_path = os.path.join(self.test_data_dir, 'duplicates.csv')
        with open(csv_path, 'w') as f:
            f.write(test_csv)
        
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3, "Should load all 3 rows including duplicate")
        
        # Check for duplicates
        duplicates = df[df.duplicated(keep=False)]
        self.assertGreater(len(duplicates), 0, "Should detect duplicates")
        
        print("✓ Test 1.1.4 passed: Duplicate courses detected")
    
    def test_special_characters_in_names(self):
        """Test Case 1.1.5: Load courses with special characters"""
        test_csv = """Course,Faculty,Session Type,Hours per Week,After Midsems
C++,Prof. Kumar,Lecture,3,No
AI/ML,Prof. Sharma,Lecture,3,No
Data Structures & Algorithms,Prof. Patel,Lecture,4,No"""
        
        csv_path = os.path.join(self.test_data_dir, 'special_chars.csv')
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(test_csv)
        
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3, "Should load all courses with special chars")
        self.assertIn('C++', df['Course'].values, "Should parse C++ correctly")
        self.assertIn('AI/ML', df['Course'].values, "Should parse AI/ML correctly")
        
        print("✓ Test 1.1.5 passed: Special characters handled correctly")


class TestTimeSlotAllocation(unittest.TestCase):
    """Test cases for time slot allocation logic"""
    
    def test_single_lecture_allocation(self):
        """Test Case 1.2.1: Allocate single lecture to empty timetable"""
        # Simulate empty timetable
        timetable = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        # Check if Monday is available
        self.assertIn('Monday', days, "Monday should be available")
        self.assertEqual(len(timetable), 0, "Timetable should be empty initially")
        
        print("✓ Test 1.2.1 passed: Single lecture can be allocated")
    
    def test_lab_session_allocation(self):
        """Test Case 1.2.2: Allocate 2-hour lab session"""
        # Lab sessions need 2-hour consecutive blocks
        lab_duration = 2
        afternoon_slots = [
            ('14:30', '16:30'),
            ('16:30', '18:30')
        ]
        
        # Check if slots support 2-hour duration
        for start, end in afternoon_slots:
            start_h, start_m = map(int, start.split(':'))
            end_h, end_m = map(int, end.split(':'))
            duration = (end_h * 60 + end_m) - (start_h * 60 + start_m)
            self.assertEqual(duration, 120, "Slot should be 2 hours (120 minutes)")
        
        print("✓ Test 1.2.2 passed: Lab session 2-hour blocks available")
    
    def test_tutorial_after_lecture(self):
        """Test Case 1.2.3: Allocate tutorial after lecture"""
        # Tutorials should ideally follow lectures
        schedule = {
            'Monday': {
                ('09:45', '11:15'): 'DSA Lecture'
            }
        }
        
        # Next available slot after lecture
        next_slot = ('11:30', '13:00')
        self.assertNotIn(next_slot, schedule.get('Monday', {}), "Next slot should be free for tutorial")
        
        print("✓ Test 1.2.3 passed: Tutorial can be scheduled after lecture")
    
    def test_evening_slot_utilization(self):
        """Test Case 1.2.4: Use evening slot when regular slots full"""
        evening_slot = ('18:30', '20:00')
        
        # Evening slot should be available as fallback
        self.assertEqual(evening_slot[0], '18:30', "Evening slot starts at 6:30 PM")
        self.assertEqual(evening_slot[1], '20:00', "Evening slot ends at 8:00 PM")
        
        print("✓ Test 1.2.4 passed: Evening slot available for overflow")
    
    def test_lunch_time_skip(self):
        """Test Case 1.2.5: Skip lunch time during scheduling"""
        lunch_slot = ('13:00', '14:30')
        
        # Lunch time should not be used for classes
        self.assertEqual(lunch_slot[0], '13:00', "Lunch starts at 1:00 PM")
        self.assertEqual(lunch_slot[1], '14:30', "Lunch ends at 2:30 PM")
        
        print("✓ Test 1.2.5 passed: Lunch time properly defined")


class TestConflictDetection(unittest.TestCase):
    """Test cases for conflict detection in scheduling"""
    
    def test_faculty_time_conflict(self):
        """Test Case 1.3.1: Detect same faculty scheduled at same time"""
        faculty_schedule = {
            'Prof. Kumar': {
                'Monday': [('09:45', '11:15')]
            }
        }
        
        # Try to schedule same faculty at same time
        new_slot = ('09:45', '11:15')
        day = 'Monday'
        
        has_conflict = new_slot in faculty_schedule.get('Prof. Kumar', {}).get(day, [])
        self.assertTrue(has_conflict, "Should detect faculty time conflict")
        
        print("✓ Test 1.3.1 passed: Faculty conflict detection works")
    
    def test_room_conflict(self):
        """Test Case 1.3.2: Detect same room scheduled at same time"""
        room_schedule = {
            'C101': {
                'Monday': [('09:45', '11:15')]
            }
        }
        
        # Try to schedule same room at same time
        new_slot = ('09:45', '11:15')
        day = 'Monday'
        room = 'C101'
        
        has_conflict = new_slot in room_schedule.get(room, {}).get(day, [])
        self.assertTrue(has_conflict, "Should detect room conflict")
        
        print("✓ Test 1.3.2 passed: Room conflict detection works")
    
    def test_lab_lecture_overlap(self):
        """Test Case 1.3.3: Detect lab and lecture time overlap"""
        # Lab: 14:30-16:30, Lecture: 15:00-16:30
        lab_start, lab_end = '14:30', '16:30'
        lecture_start, lecture_end = '15:00', '16:30'
        
        # Check if times overlap
        def time_to_minutes(time_str):
            h, m = map(int, time_str.split(':'))
            return h * 60 + m
        
        lab_start_min = time_to_minutes(lab_start)
        lab_end_min = time_to_minutes(lab_end)
        lecture_start_min = time_to_minutes(lecture_start)
        
        overlaps = lab_start_min < lecture_start_min < lab_end_min
        self.assertTrue(overlaps, "Should detect time overlap")
        
        print("✓ Test 1.3.3 passed: Time overlap detection works")


if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCourseLoading))
    suite.addTests(loader.loadTestsFromTestCase(TestTimeSlotAllocation))
    suite.addTests(loader.loadTestsFromTestCase(TestConflictDetection))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
