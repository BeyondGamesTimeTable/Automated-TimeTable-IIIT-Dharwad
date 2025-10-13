"""
Exam Timetable Generator
Main system to generate exam schedules and seating arrangements
"""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from student_generator import StudentDataGenerator
from course_generator import CourseDataGenerator
from seating_arrangement import SeatingArrangement

class ExamTimetableGenerator:
    def __init__(self):
        self.seating = SeatingArrangement()
        self.exam_sessions = {
            'FN': {'start': '10:00', 'end': '13:00', 'name': 'Forenoon Session'},
            'AN': {'start': '14:00', 'end': '17:00', 'name': 'Afternoon Session'}
        }
        
        # Exam period configuration - max 1 week (7 days) + max 2 extra days
        self.exam_start_date = datetime(2025, 4, 15)  # Tuesday
        self.max_exam_days = 9  # 1 week + 2 extra days max
        self.exclude_sundays = True
        
    def load_data(self):
        """Load all required data"""
        try:
            # Load students
            students_df = pd.read_csv('inputs/students.csv')
            self.students = students_df.to_dict('records')
            
            # Load courses
            courses_df = pd.read_csv('inputs/courses.csv')
            self.courses = courses_df.to_dict('records')
            
            # Load classrooms
            classrooms_df = pd.read_csv('inputs/classroom.csv')
            self.classrooms = classrooms_df.to_dict('records')
            
            print("✅ Data loaded successfully!")
            print(f"   📊 Students: {len(self.students)}")
            print(f"   📚 Courses: {len(self.courses)}")
            print(f"   🏛️ Classrooms: {len(self.classrooms)}")
            
        except FileNotFoundError as e:
            print(f"❌ Error loading data: {e}")
            print("🔧 Generating sample data...")
            self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate sample data if files don't exist"""
        # Generate students
        student_gen = StudentDataGenerator()
        self.students = student_gen.save_student_data()
        
        # Generate courses  
        course_gen = CourseDataGenerator()
        self.courses = course_gen.save_course_data()
        
        # Load classrooms (should exist)
        classrooms_df = pd.read_csv('inputs/classroom.csv')
        self.classrooms = classrooms_df.to_dict('records')
    
    def group_courses_by_semester(self):
        """Group courses by department and semester for scheduling"""
        course_groups = {}
        
        for course in self.courses:
            dept = course['department']
            sem = course['semester']
            key = f"{dept}_{sem}"
            
            if key not in course_groups:
                course_groups[key] = []
            course_groups[key].append(course)
        
        return course_groups
    
    def get_students_for_course_group(self, dept, semester):
        """Get students enrolled in specific department/semester"""
        students = []
        for student in self.students:
            if student['department'] == dept and student['semester'] == semester:
                students.append(student)
        return students
    
    def assign_classrooms(self, student_count):
        """Assign appropriate classrooms based on student count"""
        # Sort classrooms by capacity
        available_classrooms = []
        for classroom in self.classrooms:
            if classroom['Seating Capacity'] and str(classroom['Seating Capacity']).strip():  # Skip empty capacity entries
                try:
                    capacity = int(float(classroom['Seating Capacity']))  # Handle both int and float
                    available_classrooms.append({
                        'id': classroom['ID'],
                        'capacity': capacity
                    })
                except (ValueError, TypeError):
                    print(f"⚠️ Warning: Invalid capacity for {classroom['ID']}, skipping")
        
        available_classrooms.sort(key=lambda x: x['capacity'], reverse=True)
        
        # USE ALL CLASSROOMS to maximize distribution and spacing
        # This ensures we utilize the full infrastructure and spread students across all rooms
        assigned_rooms = available_classrooms
        
        return assigned_rooms
    
    def create_exam_schedule(self):
        """Create the main exam schedule - each course gets individual exam slot"""
        course_groups = self.group_courses_by_semester()
        
        # Create individual exam for each course
        all_individual_exams = []
        for group_key, courses in course_groups.items():
            dept, sem = group_key.split('_')
            students = self.get_students_for_course_group(dept, sem)
            
            if not students:
                continue
            
            # Create individual exam for each course
            for course in courses:
                exam = {
                    'course_code': course['course_code'],
                    'course_name': course['course_name'],
                    'department': dept,
                    'semester': sem,
                    'student_count': len(students),
                    'students': students
                }
                all_individual_exams.append(exam)
        
        # Calculate available slots within time limit
        available_slots = self._calculate_available_slots()
        total_exams = len(all_individual_exams)
        
        print(f"📊 Scheduling {total_exams} individual exams in {len(available_slots)} available slots")
        
        if total_exams > len(available_slots):
            print(f"⚠️ Warning: {total_exams} exams need {len(available_slots)} slots - some exams will share slots")
            # Allow multiple exams per slot by mixing different departments/semesters
            schedule = self._create_mixed_schedule(all_individual_exams, available_slots)
        else:
            # Simple 1:1 mapping when slots are sufficient
            schedule = []
            for i, exam in enumerate(all_individual_exams):
                if i >= len(available_slots):
                    print(f"❌ Cannot schedule {exam['course_code']} - exceeded time limit")
                    break
                    
                slot = available_slots[i]
                
                # Assign classrooms
                assigned_rooms = self.assign_classrooms(exam['student_count'])
                
                exam_entry = {
                    'date': slot['date'].strftime('%d/%m/%Y'),
                    'day': slot['date'].strftime('%A'),
                    'session': slot['session'],
                    'time': f"{self.exam_sessions[slot['session']]['start']} - {self.exam_sessions[slot['session']]['end']}",
                    'course_code': exam['course_code'],
                    'course_name': exam['course_name'],
                    'department': exam['department'],
                    'semester': exam['semester'],
                    'student_count': exam['student_count'],
                    'classrooms': [room['id'] for room in assigned_rooms],
                    'students': exam['students']
                }
                
                schedule.append(exam_entry)
        
        # Count total scheduled exams
        total_scheduled = sum(len(exam.get('individual_courses', [exam])) for exam in schedule)
        print(f"✅ Scheduled {len(schedule)} exam sessions covering {total_scheduled}/{total_exams} courses within {self.max_exam_days} days")
        return schedule
    
    def _create_mixed_schedule(self, all_exams, available_slots):
        """Create schedule allowing different dept/semester students in same session"""
        schedule = []
        remaining_exams = all_exams.copy()
        
        print(f"📊 Distributing {len(all_exams)} exams across {len(available_slots)} slots...")
        
        for slot_index, slot in enumerate(available_slots):
            if not remaining_exams:
                break
            
            # Calculate how many exams per slot we need on average
            remaining_slots = len(available_slots) - slot_index
            avg_exams_per_slot = max(1, len(remaining_exams) // remaining_slots)
            
            # Maximize classroom usage: fill every slot until all seats are filled
            session_exams = []
            total_students = 0
            used_dept_sems = set()
            max_capacity = sum(sorted([c['Seating Capacity'] for c in self.classrooms], reverse=True)[:6])
            exams_to_remove = []
            for i, exam in enumerate(remaining_exams):
                dept_sem_key = f"{exam['department']}_{exam['semester']}"
                # Allow mixing as long as capacity permits and not same dept-sem
                if total_students + exam['student_count'] <= max_capacity and dept_sem_key not in used_dept_sems:
                    session_exams.append(exam)
                    used_dept_sems.add(dept_sem_key)
                    total_students += exam['student_count']
                    exams_to_remove.append(i)
                # Stop only when all classroom seats are filled
                if total_students >= max_capacity:
                    break
            # Remove scheduled exams from remaining list
            for i in reversed(exams_to_remove):
                remaining_exams.pop(i)
            # If there is still space, add more exams regardless of dept-sem
            while remaining_exams and total_students + remaining_exams[0]['student_count'] <= max_capacity:
                exam = remaining_exams.pop(0)
                session_exams.append(exam)
                total_students += exam['student_count']
            
            # Create exam entry for this mixed session
            if session_exams:
                # Combine course information
                course_codes = [e['course_code'] for e in session_exams]
                course_names = [e['course_name'] for e in session_exams]
                
                # Get all students (mix of different departments) and tag with course_code
                # Interleave students round-robin across courses to avoid per-room clustering
                per_course_queues = []
                total_count = 0
                dept_sems = set()
                for ex in session_exams:
                    q = []
                    for s in ex['students']:
                        s_clone = dict(s)
                        s_clone['course_code'] = ex['course_code']
                        q.append(s_clone)
                    per_course_queues.append(q)
                    total_count += ex['student_count']
                    dept_sems.add(f"{ex['department']} {ex['semester']}")

                all_students = []
                exhausted = False
                while not exhausted:
                    exhausted = True
                    for q in per_course_queues:
                        if q:
                            all_students.append(q.pop(0))
                            exhausted = False
                
                # Assign classrooms based on total students
                assigned_rooms = self.assign_classrooms(total_count)
                
                exam_entry = {
                    'date': slot['date'].strftime('%d/%m/%Y'),
                    'day': slot['date'].strftime('%A'),
                    'session': slot['session'],
                    'time': f"{self.exam_sessions[slot['session']]['start']} - {self.exam_sessions[slot['session']]['end']}",
                    'course_code': ' + '.join(course_codes),
                    'course_name': ' + '.join(course_names[:3]) + ('...' if len(course_names) > 3 else ''),  # Truncate long names
                    'department': '/'.join(sorted(set(e['department'] for e in session_exams))),
                    'semester': '/'.join(sorted(set(e['semester'] for e in session_exams))),
                    'student_count': total_count,
                    'classrooms': [room['id'] for room in assigned_rooms],
                    'students': all_students,
                    'individual_courses': [{'course_code': e['course_code']} for e in session_exams],
                    'exam_count': len(session_exams)
                }
                
                schedule.append(exam_entry)
                print(f"   Slot {slot_index + 1}: {len(session_exams)} exams ({', '.join(course_codes)})")
        
        # Handle any remaining exams by adding them to the last few slots
        if remaining_exams:
            print(f"⚠️  {len(remaining_exams)} exams still need scheduling...")
            for i, remaining_exam in enumerate(remaining_exams):
                if i < len(schedule):
                    # Add to existing sessions
                    schedule[-(i+1)]['course_code'] += f" + {remaining_exam['course_code']}"
                    schedule[-(i+1)]['individual_courses'].append({'course_code': remaining_exam['course_code']})
                    print(f"   Added {remaining_exam['course_code']} to existing session")
                else:
                    print(f"   ❌ Could not schedule {remaining_exam['course_code']}")
        
        print(f"✅ Final distribution: {sum(len(s.get('individual_courses', [])) for s in schedule)} exams scheduled")
        return schedule
    
    def _calculate_available_slots(self):
        """Calculate all available exam slots within the time limit"""
        slots = []
        current_date = self.exam_start_date
        days_used = 0
        
        while days_used < self.max_exam_days:
            # Skip Sundays if configured
            if self.exclude_sundays and current_date.weekday() == 6:  # Sunday = 6
                current_date += timedelta(days=1)
                continue
            
            # Skip Saturdays (weekends)
            if current_date.weekday() == 5:  # Saturday = 5
                current_date += timedelta(days=1)
                continue
            
            # Add FN session
            slots.append({
                'date': current_date,
                'session': 'FN'
            })
            
            # Add AN session  
            slots.append({
                'date': current_date,
                'session': 'AN'
            })
            
            current_date += timedelta(days=1)
            days_used += 1
        
        return slots
    
    def generate_seating_arrangements(self, schedule):
        """Generate seating arrangements for all exams"""
        seating_plans = []
        
        for exam in schedule:
            for classroom_id in exam['classrooms']:
                # Get classroom capacity
                classroom_capacity = next(
                    (int(c['Seating Capacity']) for c in self.classrooms 
                     if c['ID'] == classroom_id and c['Seating Capacity']), 
                    96  # Default capacity
                )
                
                # Determine students for this classroom
                students_per_room = len(exam['students']) // len(exam['classrooms'])
                start_idx = exam['classrooms'].index(classroom_id) * students_per_room
                end_idx = start_idx + min(students_per_room, classroom_capacity)
                
                if classroom_id == exam['classrooms'][-1]:  # Last classroom gets remaining
                    end_idx = len(exam['students'])
                
                room_students = exam['students'][start_idx:end_idx]
                
                if room_students:  # Only create seating if there are students
                    # Create seating matrix
                    seating_matrix, assigned_students = self.seating.create_seating_matrix(
                        classroom_id, room_students
                    )
                    
                    # Prepare exam info for seating chart
                    courses_list = exam.get('individual_courses', [{'course_code': exam['course_code']}])
                    course_codes = [c['course_code'] for c in courses_list]
                    
                    exam_info = {
                        'date': exam['date'],
                        'time_slot': f"{exam['session']} ({exam['time']})",
                        'courses': course_codes,
                        'student_count': len(assigned_students)
                    }
                    
                    # Generate HTML seating chart
                    output_file = f"outputs/seating_charts/{exam['date'].replace('/', '_')}_{exam['session']}_{classroom_id}_{exam['course_code']}.html"
                    self.seating.generate_seating_chart_html(
                        classroom_id, seating_matrix, exam_info, output_file
                    )
                    
                    seating_plan = {
                        'exam_date': exam['date'],
                        'session': exam['session'],
                        'course_code': exam['course_code'],
                        'classroom': classroom_id,
                        'seating_matrix': seating_matrix,
                        'assigned_students': assigned_students,
                        'html_file': output_file
                    }
                    
                    seating_plans.append(seating_plan)
        
        return seating_plans
    
    def save_exam_schedule(self, schedule, output_file='outputs/exam_schedule.csv'):
        """Save exam schedule to CSV"""
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Flatten schedule for CSV
        csv_schedule = []
        for exam in schedule:
            csv_schedule.append({
                'Date': exam['date'],
                'Day': exam['day'],
                'Session': exam['session'],
                'Time': exam['time'],
                'Course_Code': exam['course_code'],
                'Course_Name': exam['course_name'],
                'Department': exam['department'],
                'Semester': exam['semester'],
                'Student_Count': exam['student_count']
            })
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Date', 'Day', 'Session', 'Time', 'Course_Code', 'Course_Name', 
                         'Department', 'Semester', 'Student_Count']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_schedule)
        
        print(f"✅ Exam schedule saved: {output_file}")
    
    def save_seating_summary(self, seating_plans, output_file='outputs/seating_summary.csv'):
        """Save seating arrangement summary"""
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        summary = []
        for plan in seating_plans:
            summary.append({
                'Exam_Date': plan['exam_date'],
                'Session': plan['session'],
                'Course_Code': plan['course_code'],
                'Classroom': plan['classroom'],
                'Students_Assigned': len(plan['assigned_students']),
                'HTML_Chart': plan['html_file']
            })
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Exam_Date', 'Session', 'Course_Code', 'Classroom', 
                         'Students_Assigned', 'HTML_Chart']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(summary)
        
        print(f"✅ Seating summary saved: {output_file}")
    
    def generate_exam_timetable_html(self, schedule, output_file='outputs/exam_timetable.html'):
        """Generate comprehensive HTML exam timetable"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 Exam Timetable - IIIT Dharwad</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        .stats {{
            display: flex;
            justify-content: space-around;
            background: #f8f9fa;
            padding: 20px;
        }}
        
        .stat {{
            text-align: center;
            background: white;
            padding: 15px 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .exam-table {{
            padding: 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: center;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
            text-align: center;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tbody tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.3s ease;
        }}
        
        .dept-cse {{ color: #1e40af; font-weight: bold; }}
        .dept-dsai {{ color: #92400e; font-weight: bold; }}
        .dept-ece {{ color: #6b21a8; font-weight: bold; }}
        
        .session-fn {{ 
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 5px 10px;
            border-radius: 15px;
            color: #92400e;
            font-weight: bold;
        }}
        
        .session-an {{ 
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            padding: 5px 10px;
            border-radius: 15px;
            color: #1e40af;
            font-weight: bold;
        }}
        
        .seating-link {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            text-decoration: none;
            font-size: 12px;
            display: inline-block;
            margin: 2px;
        }}
        
        .seating-link:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .navigation {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
            border-bottom: 3px solid #dee2e6;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .nav-button {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 14px 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.05em;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
            position: relative;
            overflow: hidden;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }}
        
        .nav-button::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .nav-button:hover {{
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
            border-color: rgba(255, 255, 255, 0.4);
        }}
        
        .nav-button:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .nav-button:active {{
            transform: translateY(-1px) scale(0.98);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .nav-button.seating {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 50%, #c44569 100%);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.35);
        }}
        
        .nav-button.seating:hover {{
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.5);
        }}
        
        .nav-button.home {{
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            box-shadow: 0 6px 20px rgba(86, 171, 47, 0.35);
        }}
        
        .nav-button.home:hover {{
            box-shadow: 0 10px 30px rgba(86, 171, 47, 0.5);
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                flex-direction: column;
                gap: 15px;
            }}
            
            table {{
                font-size: 12px;
            }}
            
            th, td {{
                padding: 8px 4px;
            }}
            
            .navigation {{
                flex-direction: column;
            }}
            
            .nav-button {{
                width: 100%;
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Exam Timetable</h1>
            <h2>Indian Institute of Information Technology Dharwad</h2>
            <p>Mid/End Semester Examinations 2025</p>
        </div>
        
        <div class="navigation">
            <a href="../../index.html" class="nav-button home">🏠 Back to Main Menu</a>
            <a href="seating_charts_viewer.html" class="nav-button seating">🪑 View Seating Arrangements</a>
            <a href="exam_schedule.csv" class="nav-button" download>📊 Download CSV</a>
        </div>
        
        <div class="exam-table">
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Day</th>
                        <th>Session</th>
                        <th>Time</th>
                        <th>Courses</th>
                    </tr>
                </thead>
                <tbody>"""
        
        for exam in schedule:
            dept_class = f"dept-{exam['department'].lower()}"
            session_class = f"session-{exam['session'].lower()}"
            
            # Generate seating chart links
            seating_links = ""
            for classroom in exam['classrooms']:
                link_file = f"seating_charts/{exam['date'].replace('/', '_')}_{exam['session']}_{classroom}_{exam['course_code']}.html"
                seating_links += f'<a href="{link_file}" class="seating-link" target="_blank">{classroom}</a> '
            
            html_content += f"""
                    <tr>
                        <td>{exam['date']}</td>
                        <td>{exam['day']}</td>
                        <td><span class="{session_class}">{exam['session']}</span></td>
                        <td>{exam['time']}</td>
                        <td>
                            <strong>{exam['course_code']}</strong><br>
                            <small>{exam['course_name']}</small>
                        </td>
                    </tr>"""
        
        html_content += """
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print(f"✅ HTML exam timetable saved: {output_file}")
    
    def run_complete_generation(self):
        """Run the complete exam timetable generation process"""
        print("🚀 Starting Exam Timetable Generation...")
        print("=" * 60)
        
        # Step 1: Load data
        print("\n📊 Step 1: Loading Data...")
        self.load_data()
        
        # Step 2: Create exam schedule
        print("\n📅 Step 2: Creating Exam Schedule...")
        schedule = self.create_exam_schedule()
        print(f"✅ Generated {len(schedule)} exam sessions")
        
        # Step 3: Generate seating arrangements
        print("\n🪑 Step 3: Generating Seating Arrangements...")
        seating_plans = self.generate_seating_arrangements(schedule)
        print(f"✅ Generated {len(seating_plans)} seating charts")
        
        # Step 4: Save outputs
        print("\n💾 Step 4: Saving Outputs...")
        self.save_exam_schedule(schedule)
        self.save_seating_summary(seating_plans)
        self.generate_exam_timetable_html(schedule)
        
        print("\n🎉 Exam Timetable Generation Complete!")
        print("=" * 60)
        print(f"📁 Outputs saved in: outputs/")
        print(f"🌐 Main timetable: outputs/exam_timetable.html")
        print(f"🪑 Seating charts: outputs/seating_charts/")
        
        return schedule, seating_plans

if __name__ == "__main__":
    generator = ExamTimetableGenerator()
    schedule, seating_plans = generator.run_complete_generation()