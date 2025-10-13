"""
Student Data Generator for Exam Timetable System
Generates realistic student data with proper roll number patterns
"""

import csv
import random
from pathlib import Path

class StudentDataGenerator:
    def __init__(self):
        self.departments = {
            'CSE': 'CS',    # Computer Science
            'DSAI': 'DS',   # Data Science & AI  
            'ECE': 'EC'     # Electronics
        }
        
        self.semesters = {
            'Sem2': '24B',  # 2024 admission (2nd semester)
            'Sem4': '23B',  # 2023 admission (4th semester) 
            'Sem6': '22B'   # 2022 admission (6th semester)
        }
        
        self.sections = ['A', 'B']
        
    def generate_roll_number(self, dept, semester, section, student_num):
        """Generate roll number based on pattern: YYBDDsss"""
        year_batch = self.semesters[semester]
        dept_code = self.departments[dept]
        
        # Student number with leading zeros (3 digits)
        student_id = f"{student_num:03d}"
        
        return f"{year_batch}{dept_code}{student_id}"
    
    def generate_student_data(self):
        """Generate comprehensive student data"""
        students = []
        
        # Increased dummy student counts per section
        student_counts = {
            'CSE': {'Sem2': {'A': 120, 'B': 120}, 'Sem4': {'A': 110, 'B': 110}, 'Sem6': {'A': 100, 'B': 100}},
            'DSAI': {'Sem2': {'A': 100, 'B': 100}, 'Sem4': {'A': 90, 'B': 90}, 'Sem6': {'A': 80, 'B': 80}},
            'ECE': {'Sem2': {'A': 110, 'B': 110}, 'Sem4': {'A': 100, 'B': 100}, 'Sem6': {'A': 90, 'B': 90}}
        }
        
        for dept in self.departments:
            for sem in self.semesters:
                for section in self.sections:
                    count = student_counts[dept][sem][section]
                    
                    # Generate base roll numbers starting from different ranges
                    base_start = {'A': 101, 'B': 151}[section]
                    
                    for i in range(count):
                        student_num = base_start + i
                        roll_no = self.generate_roll_number(dept, sem, section, student_num)
                        
                        students.append({
                            'roll_number': roll_no,
                            'department': dept,
                            'semester': sem,
                            'section': section,
                            'student_name': f"Student_{roll_no}",
                            'year': self.semesters[sem][:2]
                        })
        
        return students
    
    def save_student_data(self, output_file='inputs/students.csv'):
        """Save student data to CSV file"""
        students = self.generate_student_data()
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['roll_number', 'department', 'semester', 'section', 'student_name', 'year']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(students)
        
        print(f"✅ Generated {len(students)} student records")
        print(f"📁 Saved to: {output_file}")
        
        # Print summary
        dept_summary = {}
        for student in students:
            dept = student['department']
            sem = student['semester'] 
            key = f"{dept} {sem}"
            dept_summary[key] = dept_summary.get(key, 0) + 1
        
        print("\n📊 Student Distribution:")
        for key, count in sorted(dept_summary.items()):
            print(f"   {key}: {count} students")
        
        return students

if __name__ == "__main__":
    generator = StudentDataGenerator()
    students = generator.save_student_data()
    
    # Show sample roll numbers
    print("\n📋 Sample Roll Numbers:")
    for dept in ['CSE', 'DSAI', 'ECE']:
        for sem in ['Sem2', 'Sem4', 'Sem6']:
            sample = next(s for s in students if s['department'] == dept and s['semester'] == sem)
            print(f"   {dept} {sem}: {sample['roll_number']}")