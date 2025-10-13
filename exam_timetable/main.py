"""
Main Runner for Exam Timetable System
Run this file to generate complete exam timetables and seating arrangements
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

from exam_scheduler import ExamTimetableGenerator

def main():
    """Main function to run the exam timetable system"""
    
    print("🎓 IIIT Dharwad Exam Timetable System")
    print("=" * 50)
    print("📋 Features:")
    print("   ✅ Automatic student roll number generation")
    print("   ✅ Course-wise exam scheduling")
    print("   ✅ Optimal classroom assignment")
    print("   ✅ Smart seating arrangements (no same-course adjacent)")
    print("   ✅ Visual HTML seating charts")
    print("   ✅ Comprehensive exam timetable")
    print("=" * 50)
    
    try:
        # Initialize and run the exam generator
        generator = ExamTimetableGenerator()
        schedule, seating_plans = generator.run_complete_generation()
        
        print("\n🎯 Generation Summary:")
        print(f"   📚 Total Exams: {len(schedule)}")
        print(f"   🪑 Seating Charts: {len(seating_plans)}")
        print(f"   🏛️ Classrooms Used: {len(set(room for exam in schedule for room in exam['classrooms']))}")
        print(f"   👥 Total Student Seats: {sum(len(plan['assigned_students']) for plan in seating_plans)}")
        
        print("\n📂 Output Files Generated:")
        print("   📊 exam_schedule.csv - Complete exam schedule")
        print("   🪑 seating_summary.csv - Seating arrangement summary") 
        print("   🌐 exam_timetable.html - Interactive HTML timetable")
        print("   📁 seating_charts/ - Individual classroom seating charts")
        
        print("\n🌐 To View Results:")
        print("   1. Open: outputs/exam_timetable.html")
        print("   2. Click on classroom links to view seating charts")
        print("   3. Check CSV files for detailed data")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Tip: Make sure all input files are present in inputs/ directory")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Exam timetable generation completed successfully!")
    else:
        print("\n❌ Exam timetable generation failed!")
        sys.exit(1)