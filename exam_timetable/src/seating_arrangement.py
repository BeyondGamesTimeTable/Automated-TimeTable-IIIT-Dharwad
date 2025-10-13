"""
Seating Arrangement System
Generates optimal seating plans ensuring no same-course students sit together
"""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Set random seed for reproducible results
random.seed(42)

class SeatingArrangement:
    def __init__(self):
        self.classroom_layouts = {
            'C402': {
                'capacity': 96,
                'rows': 12,
                'cols': 8,
                'layout': 'standard',
                'window_side': 'left',
                'door_side': 'bottom'
            },
            'C403': {
                'capacity': 78,
                'rows': 10,
                'cols': 8,
                'layout': 'standard',
                'window_side': 'left', 
                'door_side': 'bottom'
            },
            # Add other classrooms with standard layout
            'C101': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C102': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C104': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C201': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C202': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C203': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C204': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C205': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C302': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C303': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C304': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C305': {'capacity': 96, 'rows': 12, 'cols': 8, 'layout': 'standard'},
            'C404': {'capacity': 78, 'rows': 10, 'cols': 8, 'layout': 'standard'},
            'C405': {'capacity': 78, 'rows': 10, 'cols': 8, 'layout': 'standard'},
            'C406': {'capacity': 78, 'rows': 10, 'cols': 8, 'layout': 'standard'},
            'C407': {'capacity': 78, 'rows': 10, 'cols': 8, 'layout': 'standard'}
        }
    
    def load_students(self, file_path='inputs/students.csv'):
        """Load student data"""
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    
    def load_courses(self, file_path='inputs/courses.csv'):
        """Load course data"""
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    
    def create_seating_matrix(self, classroom_id, students_list):
        """Create seating matrix with each column filled by one course, adjacent columns different courses, repeat pattern"""
        layout = self.classroom_layouts[classroom_id]
        rows = layout['rows']
        cols = layout['cols']
        capacity = layout['capacity']

        # Group students by actual course for this session (falls back to dept_sem)
        course_groups = {}
        for student in students_list[:capacity]:
            course_key = student.get('course_code') or f"{student['department']}_{student['semester']}"
            if course_key not in course_groups:
                course_groups[course_key] = []
            course_groups[course_key].append(student)

        course_keys = list(course_groups.keys())
        num_courses = len(course_keys)

        # Initialize seating matrix
        seating_matrix = [[None for _ in range(cols)] for _ in range(rows)]
        assigned_students = []

        # Fill row-wise with strict no-adjacent-same-course horizontally
        course_pointers = {key: 0 for key in course_keys}
        for row in range(rows):
            last_course = None
            for col in range(cols):
                # pick next course different from last_course and with remaining students
                pick_key = None
                for offset in range(num_courses):
                    key = course_keys[(col + offset) % num_courses]
                    if key != last_course and course_pointers[key] < len(course_groups[key]):
                        pick_key = key
                        break
                if pick_key is None:
                    # if all remaining are same as last or empty, just take any with remaining
                    for key in course_keys:
                        if course_pointers[key] < len(course_groups[key]):
                            pick_key = key
                            break
                if pick_key is None:
                    continue
                student = course_groups[pick_key][course_pointers[pick_key]]
                course_pointers[pick_key] += 1
                last_course = pick_key
                seating_matrix[row][col] = {
                    'roll_number': student['roll_number'],
                    'department': student['department'],
                    'semester': student['semester'],
                    'section': student['section'],
                    'course_key': pick_key
                }
                assigned_students.append(student)
        return seating_matrix, assigned_students
    
    def _is_valid_position(self, matrix, row, col, course_key, total_rows, total_cols):
        """Check if position is valid - allow max 2 students from different courses adjacent"""
        # Check immediate adjacent positions (4-directional: up, down, left, right)
        adjacent_positions = [
            (-1, 0),  # up
            (1, 0),   # down  
            (0, -1),  # left
            (0, 1)    # right
        ]
        
        same_course_adjacent = 0
        
        for dr, dc in adjacent_positions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < total_rows and 0 <= new_col < total_cols):
                if matrix[new_row][new_col] is not None:
                    if matrix[new_row][new_col]['course_key'] == course_key:
                        same_course_adjacent += 1
        
        # Allow position if no same-course students are adjacent
        # This allows different-course students to sit together
        return same_course_adjacent == 0
    
    def generate_seating_chart_html(self, classroom_id, seating_matrix, exam_info, output_file):
        """Generate visual HTML seating chart"""
        layout = self.classroom_layouts[classroom_id]
        rows = layout['rows']
        cols = layout['cols']
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seating Chart - {classroom_id}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .exam-info {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 3px solid #e9ecef;
        }}
        
        .exam-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .exam-detail {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .classroom-layout {{
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .seating-grid {{
            display: grid;
            grid-template-columns: repeat({cols}, 1fr);
            gap: 5px;
            max-width: 800px;
            margin: 0 auto;
            background: #e9ecef;
            padding: 20px;
            border-radius: 15px;
        }}
        
        .seat {{
            aspect-ratio: 1;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
            text-align: center;
            padding: 2px;
            min-height: 60px;
        }}
        
        .seat.occupied {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-color: #3b82f6;
            color: #1e40af;
        }}
        
        .seat.empty {{
            background: #f8f9fa;
            border-color: #dee2e6;
            color: #6c757d;
        }}
        
        .seat.cse {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-color: #3b82f6;
            color: #1e40af;
        }}
        
        .seat.dsai {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-color: #f59e0b;
            color: #92400e;
        }}
        
        .seat.ece {{
            background: linear-gradient(135deg, #fae8ff 0%, #f3e8ff 100%);
            border-color: #a855f7;
            color: #6b21a8;
        }}
        
        .legend {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .legend-color {{
            width: 30px;
            height: 30px;
            border-radius: 6px;
            border: 2px solid;
        }}
        
        .window {{
            text-align: center;
            background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            font-weight: bold;
            color: #0277bd;
        }}
        
        .door {{
            text-align: center;
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            font-weight: bold;
            color: #ef6c00;
        }}
        
        .back-button {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 14px 32px;
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.05em;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 6px 20px rgba(86, 171, 47, 0.35);
            margin: 20px 30px;
            position: relative;
            overflow: hidden;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }}
        
        .back-button::before {{
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
        
        .back-button:hover {{
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 30px rgba(86, 171, 47, 0.5);
            border-color: rgba(255, 255, 255, 0.4);
        }}
        
        .back-button:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .back-button:active {{
            transform: translateY(-1px) scale(0.98);
            box-shadow: 0 4px 15px rgba(86, 171, 47, 0.4);
        }}
        
        @media (max-width: 768px) {{
            .seating-grid {{
                grid-template-columns: repeat({min(cols, 6)}, 1fr);
            }}
            
            .exam-details {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏛️ Seating Chart</h1>
            <h2>{classroom_id}</h2>
        </div>
        
        <a href="../seating_charts_viewer.html" class="back-button">
            ← Back to All Seating Charts
        </a>
        
        <div class="exam-info">
            <div class="exam-details">
                <div class="exam-detail">
                    <h4>📅 Exam Date</h4>
                    <p>{exam_info.get('date', 'TBD')}</p>
                </div>
                <div class="exam-detail">
                    <h4>🕒 Time Slot</h4>
                    <p>{exam_info.get('time_slot', 'TBD')}</p>
                </div>
                <div class="exam-detail">
                    <h4>📚 Courses</h4>
                    <p>{', '.join(exam_info.get('courses', []))}</p>
                </div>
                <div class="exam-detail">
                    <h4>👥 Students</h4>
                    <p>{exam_info.get('student_count', 0)} students</p>
                </div>
            </div>
            
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color cse" style="border-color: #3b82f6;"></div>
                    <span><strong>CSE</strong> - Computer Science</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color dsai" style="border-color: #f59e0b;"></div>
                    <span><strong>DSAI</strong> - Data Science & AI</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color ece" style="border-color: #a855f7;"></div>
                    <span><strong>ECE</strong> - Electronics</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color empty" style="background: #f8f9fa; border-color: #dee2e6;"></div>
                    <span>Empty Seat</span>
                </div>
            </div>
        </div>
        
        <div class="classroom-layout">
            <div class="window">🪟 WINDOW</div>
            
            <div class="seating-grid">"""
        
        # Generate seating grid
        for row in range(rows):
            for col in range(cols):
                seat_data = seating_matrix[row][col]
                if seat_data:
                    dept_class = seat_data['department'].lower()
                    html_content += f"""
                <div class="seat occupied {dept_class}">
                    <div>{seat_data['roll_number']}</div>
                    <div>{seat_data['department']}</div>
                </div>"""
                else:
                    html_content += f"""
                <div class="seat empty">
                    <div>Empty</div>
                </div>"""
        
        html_content += f"""
            </div>
            
            <div class="door">🚪 DOOR</div>
        </div>
    </div>
</body>
</html>"""
        
        # Save HTML file
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print(f"✅ Generated seating chart: {output_file}")

if __name__ == "__main__":
    seating = SeatingArrangement()
    
    # Test with sample data
    sample_students = [
        {'roll_number': '24BCS101', 'department': 'CSE', 'semester': 'Sem2', 'section': 'A'},
        {'roll_number': '24BDS102', 'department': 'DSAI', 'semester': 'Sem2', 'section': 'A'},
        {'roll_number': '24BEC103', 'department': 'ECE', 'semester': 'Sem2', 'section': 'A'},
        {'roll_number': '24BCS104', 'department': 'CSE', 'semester': 'Sem2', 'section': 'A'},
        {'roll_number': '24BDS105', 'department': 'DSAI', 'semester': 'Sem2', 'section': 'A'},
    ]
    
    matrix, assigned = seating.create_seating_matrix('C402', sample_students)
    
    exam_info = {
        'date': '2025-04-15',
        'time_slot': 'FN (10:00 AM - 1:00 PM)', 
        'courses': ['CS163', 'DS504', 'EC301'],
        'student_count': len(assigned)
    }
    
    seating.generate_seating_chart_html('C402', matrix, exam_info, 'outputs/seating_charts/test_seating.html')
    print("✅ Test seating chart generated!")