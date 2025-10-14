"""
Test Runner Script
==================

Runs all unit tests and generates a comprehensive report.

Author: Team BeyondGames
Date: October 14, 2025
"""

import unittest
import sys
import os
from datetime import datetime

# Add test directory to path
sys.path.insert(0, os.path.dirname(__file__))


def run_all_tests():
    """Run all test suites and generate report"""
    
    print("="*80)
    print(" AUTOMATED TIMETABLE GENERATOR - UNIT TEST SUITE")
    print("="*80)
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print()
    
    # Discover and load all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print detailed summary
    print("\n" + "="*80)
    print(" TEST EXECUTION SUMMARY")
    print("="*80)
    print(f" Total Tests Run:     {result.testsRun}")
    print(f" Successful:          {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" Failures:            {len(result.failures)}")
    print(f" Errors:              {len(result.errors)}")
    print(f" Skipped:             {len(result.skipped)}")
    print("="*80)
    
    # Calculate success rate
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
        print(f" Success Rate:        {success_rate:.2f}%")
    
    # Print failure details if any
    if result.failures:
        print("\n" + "="*80)
        print(" FAILURES")
        print("="*80)
        for test, traceback in result.failures:
            print(f"\n Test: {test}")
            print(f" {traceback}")
    
    # Print error details if any
    if result.errors:
        print("\n" + "="*80)
        print(" ERRORS")
        print("="*80)
        for test, traceback in result.errors:
            print(f"\n Test: {test}")
            print(f" {traceback}")
    
    # Final status
    print("\n" + "="*80)
    if result.wasSuccessful():
        print(" STATUS: ✓ ALL TESTS PASSED")
    else:
        print(" STATUS: ✗ SOME TESTS FAILED")
    print(f" Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
