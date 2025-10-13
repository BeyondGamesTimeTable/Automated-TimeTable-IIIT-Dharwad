"""
Course Data for Exam Timetable System
Based on the provided exam timetable image
"""

import csv
from pathlib import Path

class CourseDataGenerator:
    def __init__(self):
        self.courses_data = {
            # CSE Courses
            'CSE': {
                'Sem2': [
                    {'code': 'CS163', 'name': 'Concurrency and Computation', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS162', 'name': 'Optimization', 'credits': 3, 'exam_type': 'END SEM'},
                    {'code': 'CS161', 'name': 'Data Structures and Algorithms', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'MA163', 'name': 'Foundations of Mathematics', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS165', 'name': 'Mathematical Foundations of Computing', 'credits': 3, 'exam_type': 'END SEM'},
                    {'code': 'CS164', 'name': 'Operating Systems', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS206', 'name': 'Theory of Computing', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS471', 'name': 'Security, Governance, Risk and Policy Management', 'credits': 2, 'exam_type': 'END SEM'}
                ],
                'Sem4': [
                    {'code': 'CS301', 'name': 'Software Engineering', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS302', 'name': 'Machine Learning', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS310', 'name': 'Database Management System', 'credits': 5, 'exam_type': 'END SEM'},
                    {'code': 'CS495', 'name': 'Data Processing', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS455', 'name': 'Blockchain Technology', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS458', 'name': 'Natural Language Processing', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS462', 'name': 'Computer Graphics', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS464', 'name': 'Deep Learning for Computer Vision', 'credits': 4, 'exam_type': 'END SEM'}
                ],
                'Sem6': [
                    {'code': 'CS469', 'name': 'Virtualization and Cloud Computing', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'CS472', 'name': 'Bioinformatics', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS162', 'name': 'Computer Interface Statistical Methods', 'credits': 2, 'exam_type': 'END SEM'},
                    {'code': 'DS163', 'name': 'Data Curation Techniques', 'credits': 3, 'exam_type': 'END SEM'}
                ]
            },
            
            # DSAI Courses  
            'DSAI': {
                'Sem2': [
                    {'code': 'DS504', 'name': 'Software Engineering and Services', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS505', 'name': 'Game Business Perspectives', 'credits': 3, 'exam_type': 'END SEM'},
                    {'code': 'DS506', 'name': 'Financial Data Analytics', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS508', 'name': 'Data Security and Privacy', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS509', 'name': 'Cloud Computing', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS551', 'name': 'Statistics for Health Technology', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS554', 'name': 'Data Analytics and Visualization', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS556', 'name': 'Medical Image Analysis', 'credits': 4, 'exam_type': 'END SEM'}
                ],
                'Sem4': [
                    {'code': 'DS357', 'name': 'Large Language Models', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS358', 'name': 'Deep Speech Processing', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'DS359', 'name': 'Computational Internet of Things', 'credits': 2, 'exam_type': 'END SEM'},
                    {'code': 'EC162', 'name': 'Network Analysis', 'credits': 3, 'exam_type': 'END SEM'},
                    {'code': 'EC364', 'name': 'Analog & Digital Communication', 'credits': 6, 'exam_type': 'END SEM'},
                    {'code': 'EC305', 'name': 'Control Systems', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC372', 'name': 'VLSI Physical Design', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC207', 'name': 'Wireless Communication', 'credits': 4, 'exam_type': 'END SEM'}
                ],
                'Sem6': [
                    {'code': 'EC310', 'name': 'Embedded Systems Design', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC361', 'name': 'Introduction to 5G Networks', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC363', 'name': 'CMOS RF Circuit Design', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'HS161', 'name': 'Introduction to Personal Finance', 'credits': 2, 'exam_type': 'END SEM'},
                    {'code': 'HS162', 'name': 'Economics', 'credits': 3, 'exam_type': 'END SEM'},
                    {'code': 'HS161', 'name': 'English Language and Communication', 'credits': 3, 'exam_type': 'END SEM'},
                    {'code': 'HS204', 'name': 'Economics', 'credits': 3, 'exam_type': 'END SEM'},
                    {'code': 'HS205', 'name': 'Sociology', 'credits': 4, 'exam_type': 'END SEM'}
                ]
            },
            
            # ECE Courses
            'ECE': {
                'Sem2': [
                    {'code': 'HS808', 'name': 'Industrial Social Psychology', 'credits': 3, 'exam_type': 'END SEM'},
                    {'code': 'EC279', 'name': 'Literature Review and Seminar', 'credits': 2, 'exam_type': 'END SEM'},
                    {'code': 'MA163', 'name': 'Linear Algebra', 'credits': 4, 'exam_type': 'END SEM'}
                ],
                'Sem4': [
                    {'code': 'EC301', 'name': 'Digital Signal Processing', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC302', 'name': 'Communication Systems', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC303', 'name': 'Microprocessors and Microcontrollers', 'credits': 5, 'exam_type': 'END SEM'},
                    {'code': 'EC304', 'name': 'Electromagnetic Fields', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC305', 'name': 'Control Systems', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC306', 'name': 'VLSI Design', 'credits': 4, 'exam_type': 'END SEM'}
                ],
                'Sem6': [
                    {'code': 'EC401', 'name': 'Antenna Theory and Design', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC402', 'name': 'Digital Communication', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC403', 'name': 'Embedded Systems', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC404', 'name': 'RF and Microwave Engineering', 'credits': 4, 'exam_type': 'END SEM'},
                    {'code': 'EC405', 'name': 'Image Processing', 'credits': 4, 'exam_type': 'END SEM'}
                ]
            }
        }
    
    def save_course_data(self, output_file='inputs/courses.csv'):
        """Save course data to CSV file"""
        courses = []
        
        for dept in self.courses_data:
            for sem in self.courses_data[dept]:
                for course in self.courses_data[dept][sem]:
                    courses.append({
                        'department': dept,
                        'semester': sem,
                        'course_code': course['code'],
                        'course_name': course['name'],
                        'credits': course['credits'],
                        'exam_type': course['exam_type'],
                        'exam_duration': '3_hours'  # Standard 3-hour exams
                    })
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['department', 'semester', 'course_code', 'course_name', 'credits', 'exam_type', 'exam_duration']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(courses)
        
        print(f"✅ Generated {len(courses)} course records")
        print(f"📁 Saved to: {output_file}")
        
        # Print summary
        dept_summary = {}
        for course in courses:
            dept = course['department']
            sem = course['semester']
            key = f"{dept} {sem}"
            dept_summary[key] = dept_summary.get(key, 0) + 1
        
        print("\n📊 Course Distribution:")
        for key, count in sorted(dept_summary.items()):
            print(f"   {key}: {count} courses")
        
        return courses

if __name__ == "__main__":
    generator = CourseDataGenerator()
    courses = generator.save_course_data()
    
    # Show sample courses
    print("\n📋 Sample Courses:")
    for dept in ['CSE', 'DSAI', 'ECE']:
        for sem in ['Sem2', 'Sem4', 'Sem6']:
            if dept in generator.courses_data and sem in generator.courses_data[dept]:
                sample = generator.courses_data[dept][sem][0]
                print(f"   {dept} {sem}: {sample['code']} - {sample['name']}")