"""
Test Suite for Sankalp Timetable Generator
Tests various functions of main.py

Run with: python test_main.py
"""

import unittest
import os
import sys
import pandas as pd
from datetime import datetime
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import TimetableGenerator


class TestTimetableGeneratorInit(unittest.TestCase):
    """Test initialization and setup"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_initialization(self):
        """Test that generator initializes correctly"""
        self.assertIsNotNone(self.generator)
        self.assertTrue(hasattr(self.generator, 'days'))
        self.assertTrue(hasattr(self.generator, 'time_slots'))
        self.assertTrue(hasattr(self.generator, 'lunch_slot'))
        
    def test_days_configuration(self):
        """Test days are properly configured"""
        # Days can be 5 or 6 depending on configuration
        self.assertIsInstance(self.generator.days, list)
        self.assertGreater(len(self.generator.days), 0)
        self.assertIn('Monday', self.generator.days)
        self.assertIn('Friday', self.generator.days)
        
    def test_time_slots_exist(self):
        """Test that time slots are defined"""
        self.assertIsInstance(self.generator.time_slots, list)
        self.assertGreater(len(self.generator.time_slots), 0)
        
    def test_lunch_slot_defined(self):
        """Test that lunch slot is defined"""
        self.assertIsNotNone(self.generator.lunch_slot)
        
    def test_minor_slot_configuration(self):
        """Test minor slot configuration"""
        self.assertIsInstance(self.generator.minor_slot_enabled, bool)
        if self.generator.minor_slot_enabled:
            self.assertIsNotNone(self.generator.minor_slot_time)
            self.assertIsNotNone(self.generator.minor_slot_days)


class TestDataLoading(unittest.TestCase):
    """Test CSV data loading functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_load_cse_data(self):
        """Test loading CSE department data"""
        df = self.generator.load_department_data('CSE')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        
    def test_load_dsai_data(self):
        """Test loading DSAI department data"""
        df = self.generator.load_department_data('DSAI')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        
    def test_load_ece_data(self):
        """Test loading ECE department data"""
        df = self.generator.load_department_data('ECE')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        
    def test_load_invalid_department(self):
        """Test loading invalid department returns None"""
        df = self.generator.load_department_data('INVALID')
        self.assertIsNone(df)
        
    def test_load_electives_data(self):
        """Test loading electives data"""
        df = self.generator.load_electives_data()
        # Electives might be optional
        if df is not None:
            self.assertIsInstance(df, pd.DataFrame)
            
    def test_load_minors_data(self):
        """Test loading minors data"""
        df = self.generator.load_minors_data()
        # Minors might be optional
        if df is not None:
            self.assertIsInstance(df, pd.DataFrame)
            # Check for required columns
            required_cols = ['Course Code', 'Course Title', 'Semester']
            for col in required_cols:
                self.assertIn(col, df.columns)


class TestClassroomManagement(unittest.TestCase):
    """Test classroom loading and allocation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_load_classrooms(self):
        """Test classroom loading"""
        self.generator._load_classrooms()
        # Classrooms are stored in various lists, not a single df
        self.assertIsNotNone(self.generator.classrooms)
        
    def test_get_auditorium(self):
        """Test auditorium retrieval"""
        auditorium = self.generator._get_auditorium()
        # Returns a string (single auditorium) or None
        self.assertTrue(auditorium is None or isinstance(auditorium, str))
        
    def test_get_large_classrooms(self):
        """Test large classroom retrieval"""
        large_classrooms = self.generator._get_large_classrooms()
        self.assertIsInstance(large_classrooms, list)
        self.assertGreater(len(large_classrooms), 0)
        
    def test_get_lab_rooms(self):
        """Test lab room retrieval"""
        lab_rooms = self.generator._get_lab_rooms()
        self.assertIsInstance(lab_rooms, list)
        self.assertGreater(len(lab_rooms), 0)
        
    def test_get_regular_classrooms(self):
        """Test regular classroom retrieval"""
        regular = self.generator._get_regular_classrooms()
        self.assertIsInstance(regular, list)


class TestCourseFiltering(unittest.TestCase):
    """Test course filtering and parsing functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
        self.cse_df = self.generator.load_department_data('CSE')
    
    def test_get_courses_by_semester(self):
        """Test filtering courses by semester"""
        if self.cse_df is not None:
            sem2_courses = self.generator.get_courses_by_semester(self.cse_df, 2)
            self.assertIsInstance(sem2_courses, pd.DataFrame)
            # Check all courses are from semester 2
            if len(sem2_courses) > 0:
                for _, row in sem2_courses.iterrows():
                    self.assertEqual(row['Semester'], 2)
    
    def test_parse_ltpsc(self):
        """Test LTPSC parsing"""
        if self.cse_df is not None and len(self.cse_df) > 0:
            test_row = self.cse_df.iloc[0]
            ltpsc = self.generator.parse_ltpsc(test_row)
            # Returns a tuple (lectures, tutorials, practicals)
            self.assertIsInstance(ltpsc, tuple)
            self.assertEqual(len(ltpsc), 3)
            for value in ltpsc:
                self.assertIsInstance(value, (int, float))
    
    def test_is_common_course(self):
        """Test common course detection"""
        if self.cse_df is not None and len(self.cse_df) > 0:
            for _, row in self.cse_df.iterrows():
                result = self.generator.is_common_course(row)
                self.assertIsInstance(result, bool)
                break  # Test just one row


class TestTimetableInitialization(unittest.TestCase):
    """Test timetable initialization"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_initialize_timetable_basic(self):
        """Test basic timetable initialization"""
        timetable = self.generator._initialize_timetable()
        self.assertIsInstance(timetable, dict)
        # Check all days are present
        for day in self.generator.days:
            self.assertIn(day, timetable)
            self.assertIsInstance(timetable[day], dict)
    
    def test_initialize_timetable_semester_3(self):
        """Test timetable initialization for semester 3 (with minor slot)"""
        timetable = self.generator._initialize_timetable(semester=3)
        self.assertIsInstance(timetable, dict)
        # Check if minor slot exists on configured days
        if self.generator.minor_slot_enabled:
            time_str = f"{self.generator.minor_slot_time[0]}-{self.generator.minor_slot_time[1]}"
            for day in self.generator.minor_slot_days:
                if day in timetable:
                    self.assertIn(time_str, timetable[day])
    
    def test_initialize_timetable_semester_1(self):
        """Test timetable initialization for semester 1 (no minor slot)"""
        timetable = self.generator._initialize_timetable(semester=1)
        self.assertIsInstance(timetable, dict)
        # Minor slot should not be present for semester 1
        if self.generator.minor_slot_enabled:
            time_str = f"{self.generator.minor_slot_time[0]}-{self.generator.minor_slot_time[1]}"
            for day in self.generator.days:
                if day in timetable and time_str in timetable[day]:
                    # Should be 'Free' not 'Minor'
                    self.assertEqual(timetable[day][time_str], 'Free')
    
    def test_lunch_break_in_timetable(self):
        """Test that lunch break is properly set"""
        timetable = self.generator._initialize_timetable()
        lunch_time_str = f"{self.generator.lunch_slot[0]}-{self.generator.lunch_slot[1]}"
        for day in self.generator.days:
            self.assertIn(lunch_time_str, timetable[day])
            self.assertEqual(timetable[day][lunch_time_str], 'LUNCH BREAK')


class TestSlotDuration(unittest.TestCase):
    """Test time slot duration calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_get_slot_duration(self):
        """Test slot duration calculation"""
        # Test standard 60-minute slot
        duration = self.generator._get_slot_duration(('09:00', '10:00'))
        self.assertEqual(duration, 60)
        
        # Test 90-minute slot
        duration = self.generator._get_slot_duration(('18:30', '20:00'))
        self.assertEqual(duration, 90)
        
        # Test lunch slot
        duration = self.generator._get_slot_duration(self.generator.lunch_slot)
        self.assertEqual(duration, 60)


class TestCrossDepartmentCourses(unittest.TestCase):
    """Test cross-department course detection"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_find_cross_dept_shared_courses(self):
        """Test finding cross-department shared courses"""
        # Test for semester 2
        shared_courses = self.generator.find_cross_dept_shared_courses(2)
        # Returns a dict of shared courses
        self.assertIsInstance(shared_courses, dict)
        
    def test_cross_dept_courses_semester_4(self):
        """Test cross-department courses for semester 4"""
        shared_courses = self.generator.find_cross_dept_shared_courses(4)
        # Returns a dict of shared courses
        self.assertIsInstance(shared_courses, dict)


class TestTimetableGeneration(unittest.TestCase):
    """Test complete timetable generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_generate_timetable_cse_sem2_a(self):
        """Test generating CSE Semester 2 Section A timetable"""
        result = self.generator.generate_timetable('CSE', 2, 'A')
        if result is not None:
            timetable, electives, rotated_out = result
            self.assertIsInstance(timetable, dict)
            self.assertIsInstance(electives, dict)
            # Check timetable has all days
            for day in self.generator.days:
                self.assertIn(day, timetable)
    
    def test_generate_timetable_dsai_sem2_a(self):
        """Test generating DSAI Semester 2 Section A timetable"""
        result = self.generator.generate_timetable('DSAI', 2, 'A')
        if result is not None:
            timetable, electives, rotated_out = result
            self.assertIsInstance(timetable, dict)
    
    def test_generate_timetable_ece_sem2_a(self):
        """Test generating ECE Semester 2 Section A timetable"""
        result = self.generator.generate_timetable('ECE', 2, 'A')
        if result is not None:
            timetable, electives, rotated_out = result
            self.assertIsInstance(timetable, dict)
    
    def test_generate_timetable_invalid_department(self):
        """Test generating timetable for invalid department"""
        result = self.generator.generate_timetable('INVALID', 2, 'A')
        self.assertIsNone(result)


class TestCSVExport(unittest.TestCase):
    """Test CSV export functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_export_to_csv(self):
        """Test exporting timetable to CSV"""
        # Create a simple timetable
        timetable = self.generator._initialize_timetable()
        filename = 'test_timetable.csv'
        
        # Export to test directory
        self.generator.export_to_csv(
            timetable, 
            filename, 
            output_dir=self.test_dir,
            semester=2
        )
        
        # Check if file was created
        csv_path = os.path.join(self.test_dir, filename)
        self.assertTrue(os.path.exists(csv_path))
        
        # Verify CSV can be read
        df = pd.read_csv(csv_path)
        self.assertIsInstance(df, pd.DataFrame)


class TestElectiveBaskets(unittest.TestCase):
    """Test elective basket grouping"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
        self.electives_df = self.generator.load_electives_data()
    
    def test_group_electives_into_baskets(self):
        """Test grouping electives into baskets"""
        if self.electives_df is not None and len(self.electives_df) > 0:
            baskets = self.generator.group_electives_into_baskets(
                self.electives_df, 
                semester=2, 
                department='CSE'
            )
            self.assertIsInstance(baskets, dict)


class TestMinorCourses(unittest.TestCase):
    """Test minor courses functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TimetableGenerator('input_files/sdtt_inputs')
    
    def test_load_minors_csv(self):
        """Test loading minors.csv file"""
        minors_df = self.generator.load_minors_data()
        if minors_df is not None:
            self.assertIsInstance(minors_df, pd.DataFrame)
            # Check required columns exist
            required_cols = ['Course Code', 'Course Title', 'Semester']
            for col in required_cols:
                self.assertIn(col, minors_df.columns)
    
    def test_minor_semester_parsing(self):
        """Test parsing multi-semester minor courses"""
        minors_df = self.generator.load_minors_data()
        if minors_df is not None and len(minors_df) > 0:
            for _, row in minors_df.iterrows():
                semester_val = str(row.get('Semester', '')).strip()
                # Should be able to parse comma-separated or single values
                semester_list = [s.strip() for s in semester_val.split(',') if s.strip()]
                self.assertIsInstance(semester_list, list)
                break  # Test just one row


def run_test_suite():
    """Run the complete test suite"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTimetableGeneratorInit))
    suite.addTests(loader.loadTestsFromTestCase(TestDataLoading))
    suite.addTests(loader.loadTestsFromTestCase(TestClassroomManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestCourseFiltering))
    suite.addTests(loader.loadTestsFromTestCase(TestTimetableInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestSlotDuration))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossDepartmentCourses))
    suite.addTests(loader.loadTestsFromTestCase(TestTimetableGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestCSVExport))
    suite.addTests(loader.loadTestsFromTestCase(TestElectiveBaskets))
    suite.addTests(loader.loadTestsFromTestCase(TestMinorCourses))
    
    # Run tests
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
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_test_suite()
    sys.exit(0 if success else 1)
