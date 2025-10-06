"""Convert Excel timetables to HTML format with interactive viewer"""
import pandas as pd
import os
from pathlib import Path

class TimetableHTMLConverter:
    def __init__(self, input_dir='timetable_outputs', output_dir='timetable_html'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def csv_to_html(self, csv_file, html_file):
        """Convert CSV timetable to beautiful HTML"""
        try:
            df = pd.read_csv(csv_file, index_col=0)
            
            # Get timetable info from filename
            filename = Path(csv_file).stem
            parts = filename.replace('_Timetable', '').split('_')
            dept = parts[0]
            semester = parts[1]
            section = parts[2]
            
            # Load elective information if available
            elective_file = csv_file.replace('.csv', '_Electives.txt')
            electives_html = self._load_electives(elective_file)
            
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{dept} - {semester} - {section} Timetable</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
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
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .back-button {{
            display: inline-block;
            margin: 20px;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .back-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        .timetable-wrapper {{
            padding: 30px;
            overflow-x: auto;
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
            font-size: 1em;
            letter-spacing: 1px;
        }}
        
        th.time-slot {{
            font-weight: 700;
            font-size: 1.1em;
            background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            border-right: 2px solid rgba(255,255,255,0.2);
        }}
        
        th.time-slot:last-child {{
            border-right: none;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            border-right: 1px solid #e0e0e0;
            vertical-align: top;
        }}
        
        td:last-child {{
            border-right: none;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        tbody tr:hover {{
            background-color: #f5f5f5;
            transition: background-color 0.3s ease;
        }}
        
        .day-column {{
            font-weight: bold;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            text-align: center;
            font-size: 1.1em;
        }}
        
        .lunch-break {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: #333;
            font-weight: bold;
            text-align: center;
            padding: 15px;
        }}
        
        .free-slot {{
            background-color: #f0f4f8;
            color: #64748b;
            text-align: center;
            font-style: italic;
            font-weight: 500;
        }}
        
        .course-slot {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 6px solid #3b82f6;
            font-weight: 600;
            color: #1e40af;
            padding: 18px 15px;
        }}
        
        .common-course {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 6px solid #f59e0b;
            font-weight: 600;
            color: #92400e;
            padding: 18px 15px;
        }}
        
        .lab-slot {{
            background: linear-gradient(135deg, #fae8ff 0%, #f3e8ff 100%);
            border-left: 6px solid #a855f7;
            font-weight: 600;
            color: #6b21a8;
            padding: 18px 15px;
        }}
        
        .tutorial-slot {{
            background: linear-gradient(135deg, #ccfbf1 0%, #a7f3d0 100%);
            border-left: 6px solid #14b8a6;
            font-weight: 600;
            color: #115e59;
            padding: 18px 15px;
        }}
        
        .legend {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 10px;
            margin: 20px;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .legend-color {{
            width: 30px;
            height: 20px;
            border-radius: 4px;
        }}
        
        .electives-section {{
            padding: 30px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            margin: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .electives-section h2 {{
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }}
        
        .elective-note {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        
        .electives-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .basket-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .basket-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        
        .basket-card h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
        }}
        
        .course-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .course-list li {{
            padding: 12px;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            border-radius: 8px;
            border-left: 3px solid #764ba2;
            transition: background 0.2s ease;
        }}
        
        .course-list li:hover {{
            background: linear-gradient(135deg, #e3f2fd 0%, #f8f9fa 100%);
        }}
        
        .classroom-info {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
            display: inline-block;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            
            .back-button, .legend {{
                display: none;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            th, td {{
                padding: 10px;
                font-size: 0.85em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 {dept} Timetable</h1>
            <div class="subtitle">{semester} - {section}</div>
        </div>
        
        <a href="index.html" class="back-button">← Back to Selection</a>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-left: 6px solid #3b82f6;"></div>
                <span><strong>Lecture</strong> - Regular Course</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 6px solid #f59e0b;"></div>
                <span><strong>Lecture</strong> - Common Course</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #fae8ff 0%, #f3e8ff 100%); border-left: 6px solid #a855f7;"></div>
                <span><strong>Practical/Lab</strong></span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #ccfbf1 0%, #a7f3d0 100%); border-left: 6px solid #14b8a6;"></div>
                <span><strong>Tutorial</strong></span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #f0f4f8;"></div>
                <span>Free Slot</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);"></div>
                <span>🍽️ Lunch Break</span>
            </div>
        </div>
        
        <div class="timetable-wrapper">
            {self._generate_table(df)}
        </div>
        
        {electives_html}
    </div>
</body>
</html>
"""
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
        except Exception as e:
            print(f"Error converting {csv_file}: {e}")
            return False
    
    def _load_electives(self, elective_file):
        """Load elective information from text file and format as HTML"""
        if not os.path.exists(elective_file):
            return ""  # No electives for this timetable
        
        try:
            with open(elective_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the elective file
            html = """
        <div class="electives-section">
            <h2>📚 Elective Courses</h2>
            <p class="elective-note">Students must choose <strong>ONE course</strong> from each basket below:</p>
            <div class="electives-container">
"""
            
            # Split by basket
            baskets = content.split('Basket ')[1:]  # Skip header
            
            for basket_content in baskets:
                lines = basket_content.strip().split('\n')
                basket_name = lines[0].replace(':', '').strip()
                
                html += f"""
                <div class="basket-card">
                    <h3>Basket {basket_name}</h3>
                    <ul class="course-list">
"""
                
                # Parse courses
                i = 2  # Skip basket name and separator
                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith('•'):
                        course_info = line.replace('•', '').strip()
                        html += f'                        <li><strong>{course_info}</strong>'
                        # Check if next line has classroom
                        if i + 1 < len(lines) and 'Classroom:' in lines[i + 1]:
                            classroom = lines[i + 1].split('Classroom:')[1].strip()
                            html += f'<br><span class="classroom-info">📍 {classroom}</span>'
                            i += 1
                        html += '</li>\n'
                    i += 1
                
                html += """
                    </ul>
                </div>
"""
            
            html += """
            </div>
        </div>
"""
            return html
            
        except Exception as e:
            print(f"Warning: Could not load electives from {elective_file}: {e}")
            return ""
    
    def _generate_table(self, df):
        """Generate HTML table from DataFrame"""
        html = '<table>\n<thead>\n<tr>\n'
        
        # Header row
        html += '<th style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">Day/Time</th>\n'
        for col in df.columns:
            html += f'<th class="time-slot">⏰ {col}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        
        # Data rows
        for day in df.index:
            html += '<tr>\n'
            html += f'<td class="day-column">{day}</td>\n'
            
            for col in df.columns:
                cell_value = str(df.loc[day, col])
                cell_class = self._get_cell_class(cell_value)
                html += f'<td class="{cell_class}">{cell_value}</td>\n'
            
            html += '</tr>\n'
        
        html += '</tbody>\n</table>'
        return html
    
    def _get_cell_class(self, value):
        """Determine CSS class based on cell content"""
        value_lower = value.lower()
        
        if 'lunch break' in value_lower:
            return 'lunch-break'
        elif value_lower == 'free':
            return 'free-slot'
        elif 'elective' in value_lower:
            return 'common-course'  # Use same styling as common courses (yellow/amber)
        elif 'common' in value_lower:
            return 'common-course'
        elif 'lab' in value_lower:
            return 'lab-slot'
        elif '-t-' in value_lower:
            return 'tutorial-slot'
        else:
            return 'course-slot'
    
    def create_index_page(self, timetables):
        """Create main index page for timetable selection"""
        
        # Organize timetables by department
        dept_data = {}
        for tt in timetables:
            filename = Path(tt).stem
            parts = filename.replace('_Timetable', '').split('_')
            dept = parts[0]
            semester = parts[1]
            section = parts[2]
            
            if dept not in dept_data:
                dept_data[dept] = {}
            if semester not in dept_data[dept]:
                dept_data[dept][semester] = []
            
            dept_data[dept][semester].append({
                'section': section,
                'file': Path(tt).stem + '.html'
            })
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BeyondGames Timetable Viewer</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            padding: 40px 20px;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .departments {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}
        
        .department-card {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .department-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 30px 80px rgba(0,0,0,0.4);
        }}
        
        .dept-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .dept-header h2 {{
            font-size: 2em;
            margin-bottom: 5px;
        }}
        
        .dept-header p {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        
        .semester-group {{
            margin-bottom: 20px;
        }}
        
        .semester-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 2px solid #667eea;
        }}
        
        .section-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .timetable-link {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            flex: 1;
            text-align: center;
            min-width: 120px;
        }}
        
        .timetable-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }}
        
        .footer {{
            text-align: center;
            color: white;
            padding: 20px;
            margin-top: 40px;
        }}
        
        .footer p {{
            font-size: 1.1em;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .departments {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 BeyondGames Timetable Viewer</h1>
            <p>Select your department, semester, and section to view timetable</p>
        </div>
        
        <div class="departments">
"""
        
        # Department mapping
        dept_names = {
            'CSE': 'Computer Science & Engineering',
            'DSAI': 'Data Science & AI',
            'ECE': 'Electronics & Communication'
        }
        
        dept_emojis = {
            'CSE': '💻',
            'DSAI': '📊',
            'ECE': '⚡'
        }
        
        for dept in sorted(dept_data.keys()):
            html_content += f"""
            <div class="department-card">
                <div class="dept-header">
                    <h2>{dept_emojis.get(dept, '🎓')} {dept}</h2>
                    <p>{dept_names.get(dept, dept)}</p>
                </div>
"""
            
            for semester in sorted(dept_data[dept].keys()):
                html_content += f"""
                <div class="semester-group">
                    <div class="semester-title">📚 {semester}</div>
                    <div class="section-buttons">
"""
                
                for section_info in dept_data[dept][semester]:
                    section = section_info['section']
                    file = section_info['file']
                    html_content += f"""
                        <a href="{file}" class="timetable-link">Section {section}</a>
"""
                
                html_content += """
                    </div>
                </div>
"""
            
            html_content += """
            </div>
"""
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>✨ Made with ❤️ by BeyondGames Team</p>
            <p>Automated Timetable Generation System</p>
        </div>
    </div>
</body>
</html>
"""
        
        index_file = os.path.join(self.output_dir, 'index.html')
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created index page: {index_file}")
        return index_file
    
    def convert_all(self):
        """Convert all CSV timetables to HTML"""
        csv_files = []
        
        # Find all CSV files
        for file in os.listdir(self.input_dir):
            if file.endswith('.csv') and 'Timetable' in file:
                csv_files.append(os.path.join(self.input_dir, file))
        
        if not csv_files:
            print("No timetable CSV files found!")
            return False
        
        print(f"\nConverting {len(csv_files)} timetables to HTML...")
        
        converted = 0
        for csv_file in csv_files:
            filename = Path(csv_file).stem
            html_file = os.path.join(self.output_dir, filename + '.html')
            
            if self.csv_to_html(csv_file, html_file):
                print(f"Converted: {filename}")
                converted += 1
        
        # Create index page
        self.create_index_page(csv_files)
        
        print(f"\nSuccessfully converted {converted}/{len(csv_files)} timetables!")
        print(f"HTML files location: {self.output_dir}/")
        print(f"Open index.html to view all timetables")
        
        return True

def main():
    """Main function"""
    print("\nBeyondGames Timetable HTML Converter")
    print("="*80)
    
    converter = TimetableHTMLConverter()
    converter.convert_all()
    
    print("\n" + "="*80)
    print("HTML conversion complete!")
    print(f"Open: timetable_html/index.html in your browser")
    print("="*80)

if __name__ == "__main__":
    main()
