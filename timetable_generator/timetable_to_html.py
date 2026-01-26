"""Convert Excel timetables to HTML format with interactive viewer"""
import pandas as pd
import os
from pathlib import Path

class TimetableHTMLConverter:
    def __init__(self, input_dir='timetable_outputs', output_dir='timetable_html'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.till_midsem_courses = {}  # Store 2-credit courses
        self.course_colors = {}  # Cache for course code colors
    
    def _get_course_color(self, course_code):
        """Generate a consistent color for a course code using hash"""
        if course_code in self.course_colors:
            return self.course_colors[course_code]
        
        # Hash the course code to generate consistent colors
        hash_value = hash(course_code)
        
        # Generate pastel colors with good contrast
        hue = (hash_value % 360)
        saturation = 45 + (hash_value % 25)  # 45-70%
        lightness = 75 + (hash_value % 15)   # 75-90%
        
        bg_color = f"hsl({hue}, {saturation}%, {lightness}%)"
        border_hue = (hue + 180) % 360  # Complementary color for border
        border_color = f"hsl({border_hue}, 70%, 45%)"
        text_color = f"hsl({hue}, 60%, 25%)"  # Dark version for text
        
        colors = {
            'background': bg_color,
            'border': border_color,
            'text': text_color
        }
        
        self.course_colors[course_code] = colors
        return colors
        
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
            
            # Load 2-credit courses (till midsem) information
            till_midsem_html = self._load_till_midsem_courses(csv_file, dept, semester, section)
            
            # Load elective basket information from CSV (scheduled baskets only)
            electives_html = self._load_elective_baskets_from_csv(csv_file, dept, semester, section)
            
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
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin: 20px;
            padding: 14px 32px;
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.05em;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 6px 20px rgba(86, 171, 47, 0.35);
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
        
        .download-section {{
            text-align: center;
            margin: 20px;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .download-section h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .download-buttons {{
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .download-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            font-weight: bold;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            font-size: 14px;
        }}
        
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        .csv-btn {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }}
        
        .image-btn {{
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
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
        
        /* Individual section classes - Blue */
        .course-slot {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 6px solid #3b82f6;
            font-weight: 600;
            color: #1e40af;
            padding: 18px 15px;
        }}
        
        /* Common classes (CSE A+B or DSAI+ECE) - Yellow/Amber */
        .common-course {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 6px solid #f59e0b;
            font-weight: 600;
            color: #92400e;
            padding: 18px 15px;
        }}
        
        /* 2-hour Labs - Purple */
        .lab-slot {{
            background: linear-gradient(135deg, #fae8ff 0%, #f3e8ff 100%);
            border-left: 6px solid #a855f7;
            font-weight: 600;
            color: #6b21a8;
            padding: 18px 15px;
        }}
        
        /* 1-hour Tutorials - Green */
        .tutorial-slot {{
            background: linear-gradient(135deg, #ccfbf1 0%, #a7f3d0 100%);
            border-left: 6px solid #14b8a6;
            font-weight: 600;
            color: #115e59;
            padding: 18px 15px;
        }}
        
        /* Electives - Orange */
        .elective-slot {{
            background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
            border-left: 6px solid #ea580c;
            font-weight: 600;
            color: #7c2d12;
            padding: 18px 15px;
        }}
        
        /* Till Midsem Courses - Red background (entire cell) */
        .till-midsem-cell {{
            background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%) !important;
            border-left: 6px solid #dc2626 !important;
            font-weight: 600;
            color: #7f1d1d !important;
            padding: 18px 15px;
        }}
        
        /* Till Midsem Badge (deprecated - using red cell instead) */
        .till-midsem-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
            color: #7f1d1d;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 700;
            margin-left: 8px;
            border: 1px solid #dc2626;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Till Midsem Section */
        .till-midsem-section {{
            padding: 25px;
            margin: 20px;
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-radius: 15px;
            border: 3px solid #dc2626;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.2);
        }}
        
        .till-midsem-section h2 {{
            color: #991b1b;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }}
        
        .till-midsem-note {{
            text-align: center;
            color: #7f1d1d;
            margin-bottom: 20px;
            font-size: 1.1em;
            font-weight: 600;
        }}
        
        .till-midsem-courses {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .till-midsem-course-card {{
            background: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 5px solid #dc2626;
            transition: transform 0.2s ease;
        }}
        
        .till-midsem-course-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .till-midsem-course-card .course-code {{
            color: #dc2626;
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 5px;
        }}
        
        .till-midsem-course-card .course-title {{
            color: #4b5563;
            font-size: 0.95em;
            margin-bottom: 8px;
        }}
        
        .till-midsem-course-card .course-credits {{
            color: #991b1b;
            font-size: 0.85em;
            font-weight: 600;
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
        
        .basket-classroom {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            color: #1565c0;
            padding: 8px 16px;
            border-radius: 8px;
            margin: 10px 0 15px 0;
            font-size: 1em;
            text-align: center;
            border-left: 4px solid #1976d2;
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
            
            .download-buttons {{
                flex-direction: column;
                align-items: center;
            }}
            
            .download-btn {{
                width: 80%;
                max-width: 300px;
                justify-content: center;
            }}
        }}
        
        /* ============================================ */
        /* FLEXIBLE AFTERNOON SLOT DURATION BARS */
        /* ============================================ */
        
        .afternoon-flex-slot {{
            position: relative;
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px;
            overflow: hidden;
            min-height: 85px;
        }}
        
        .session-container {{
            display: flex;
            flex-direction: column;
            height: 100%;
        }}
        
        .duration-bar-wrapper {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 100%;
        }}
        
        .duration-bar {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 16px 12px;
            font-weight: 600;
            color: white;
            text-align: center;
            position: relative;
            transition: all 0.2s ease;
            border-radius: 6px;
            width: 100%;
            gap: 6px;
        }}
        /* Cell inner wrapper for regular slots to show fractional duration */
        .cell-inner {{
            position: relative;
            width: 100%;
            height: 100%;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .duration-segment {{
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            border-radius: 4px 0 0 4px;
            opacity: 0.95;
            z-index: 1;
        }}

        .tutorial-seg {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border-left: 4px solid #047857;
        }}

        .cell-text {{
            position: relative;
            z-index: 2;
            padding: 6px 8px;
            font-weight: 600;
            color: #0f172a; /* dark text over colored background */
            text-align: center;
        }}
        
        /* Lab - Full 2 hours (100%) */
        .lab-duration {{
            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
            border-left: 4px solid #6d28d9;
        }}
        
        /* Lecture - 1.5 hours (75% of 2 hours) */
        .lecture-duration {{
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            border-left: 4px solid #1d4ed8;
        }}
        
        /* Tutorial - 1 hour (50% of 2 hours) */
        .tutorial-duration {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border-left: 4px solid #047857;
        }}
        
        .duration-tag {{
            background: rgba(255, 255, 255, 0.25);
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.75em;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        
        .course-info {{
            font-size: 0.95em;
            line-height: 1.4;
        }}
        
        /* Hover effects for afternoon slots */
        .afternoon-flex-slot:hover {{
            border-color: #cbd5e1;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transform: translateY(-2px);
            transition: all 0.2s ease;
        }}
        
        .duration-bar:hover {{
            filter: brightness(1.05);
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
        function downloadAsImage() {{
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = '⏳ Generating...';
            button.disabled = true;
            
            // Get the timetable container
            const timetableContainer = document.querySelector('.container');
            
            // Configure html2canvas options
            const options = {{
                scale: 2, // Higher quality
                useCORS: true,
                allowTaint: true,
                backgroundColor: '#ffffff',
                width: timetableContainer.scrollWidth,
                height: timetableContainer.scrollHeight,
                scrollX: 0,
                scrollY: 0
            }};
            
            html2canvas(timetableContainer, options).then(canvas => {{
                // Create download link
                const link = document.createElement('a');
                link.download = '{filename}_timetable.png';
                link.href = canvas.toDataURL('image/png');
                
                // Trigger download
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                // Reset button
                button.innerHTML = originalText;
                button.disabled = false;
            }}).catch(error => {{
                console.error('Error generating image:', error);
                alert('Error generating image. Please try again.');
                button.innerHTML = originalText;
                button.disabled = false;
            }});
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 {dept} Timetable</h1>
            <div class="subtitle">{semester} - {section}</div>
        </div>
        
        <div style="display: flex; gap: 15px; margin: 20px; flex-wrap: wrap;">
            <a href="index.html" class="back-button">← Back to Timetable Menu</a>
        </div>
        
        <div class="download-section"
            <h3>📥 Download Timetable</h3>
            <div class="download-buttons">
                <a href="../timetable_outputs/{filename}.csv" class="download-btn csv-btn" download="{filename}.csv">
                    📊 Download CSV
                </a>
                <button class="download-btn image-btn" onclick="downloadAsImage()">
                    🖼️ Download as Image
                </button>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-left: 4px solid #3b82f6;"></div>
                <span><strong>Individual Section Classes</strong></span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #ccfbf1 0%, #a7f3d0 100%); border-left: 4px solid #14b8a6;"></div>
                <span><strong>1-Hour Tutorials</strong></span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #fae8ff 0%, #f3e8ff 100%); border-left: 4px solid #a855f7;"></div>
                <span><strong>2-Hour Labs</strong></span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 4px solid #f59e0b;"></div>
                <span><strong>Common Classes (A+B / DSAI+ECE)</strong></span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); border-left: 4px solid #ea580c;"></div>
                <span><strong>Electives</strong></span>
            </div>
        </div>
        
        <div class="timetable-wrapper">
            {self._generate_table(df)}
        </div>
        
        {till_midsem_html}
        
        {electives_html}
    </div>
</body>
</html>
"""
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
        except Exception as e:
            import traceback
            print(f"Error converting {csv_file}: {e}")
            traceback.print_exc()
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
                
                # Parse courses with their classrooms
                # Format is:
                #   • COURSE_CODE: Course Title
                #     Classroom: C101
                i = 2  # Skip basket name and separator line
                while i < len(lines):
                    line = lines[i].strip()
                    
                    # Check if this is a course line (starts with bullet)
                    if line.startswith('•') or line.startswith('â€¢'):
                        course_info = line.replace('•', '').replace('â€¢', '').strip()
                        
                        # Check if next line has classroom info
                        classroom = None
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if next_line.startswith('Classroom:'):
                                classroom = next_line.split('Classroom:')[1].strip()
                                i += 1  # Skip the classroom line in next iteration
                        
                        # Render course with classroom
                        if course_info and not course_info.startswith('-'):
                            if classroom and classroom not in ['nan', 'None', 'TBD', '']:
                                html += f'                        <li><strong>{course_info}</strong><br><span style="color: #3b82f6; font-size: 0.9em;">📍 {classroom}</span></li>\n'
                            else:
                                html += f'                        <li><strong>{course_info}</strong></li>\n'
                    
                    i += 1
                
                html += """
                    </ul>
                </div>
"""
            
            html += """
            </div>
        </div>
"""
            
            # Check if there are "After Midsems" electives
            if 'AFTER MIDSEMS' in content:
                html += """
        <div class="after-midsems-section" style="margin-top: 30px; padding: 25px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 15px; border: 3px solid #f59e0b;">
            <h2 style="color: #92400e; margin-bottom: 15px;">🔄 After Midsems - Second Half Electives</h2>
            <p style="color: #78350f; font-weight: 600; margin-bottom: 20px;">These elective baskets will be offered <strong>after mid-semester exams</strong> in the same time slots:</p>
            <div class="electives-container">
"""
                # Parse After Midsems section
                after_midsems_section = content.split('AFTER MIDSEMS')[1] if 'AFTER MIDSEMS' in content else ""
                after_baskets = after_midsems_section.split('Basket ')[1:] if after_midsems_section else []
                
                for basket_content in after_baskets:
                    lines = basket_content.strip().split('\n')
                    basket_name = lines[0].replace(':', '').replace('(After Midsems)', '').strip()
                    
                    html += f"""
                <div class="basket-card" style="border: 2px solid #f59e0b; background: white;">
                    <h3 style="color: #92400e;">Basket {basket_name} <span style="font-size: 0.8em; color: #f59e0b;">(After Midsems)</span></h3>
                    <ul class="course-list">
"""
                    
                    # Parse courses
                    i = 2  # Skip basket name and separator
                    while i < len(lines):
                        line = lines[i].strip()
                        if line.startswith('•'):
                            course_info = line.replace('•', '').strip()
                            classroom = None
                            # Check if next line has classroom
                            if i + 1 < len(lines) and 'Classroom:' in lines[i + 1]:
                                classroom = lines[i + 1].split('Classroom:')[1].strip()
                                i += 1
                            
                            html += f'                        <li><strong>{course_info}</strong>'
                            if classroom and classroom not in ['nan', '-', '']:
                                html += f'<br><span class="classroom-info">📍 {classroom}</span>'
                            html += '</li>\n'
                        i += 1
                    
                    html += """
                    </ul>
                </div>
"""
                
                html += """
            </div>
            <p style="margin-top: 20px; color: #78350f; font-style: italic; font-size: 0.95em;">
                💡 <strong>Note:</strong> These courses will replace the current electives in the timetable after midsem exams, using the same classroom and time slots.
            </p>
        </div>
"""
            
            return html
            
        except Exception as e:
            print(f"Warning: Could not load electives from {elective_file}: {e}")
            return ""
    
    def _load_till_midsem_courses(self, timetable_file, dept, semester, section):
        """Load and display 1-credit and 2-credit courses (till midsem) from the original CSV"""
        try:
            # Find the original CSV file with course information
            # The timetable_file path: timetable_outputs/TIMESTAMP/DEPT_SemX_SectionY_Timetable.csv
            # We need: input_files/versions/TIMESTAMP/DEPT.csv
            
            # Get base directory (timetable_generator folder - 3 levels up from the CSV file)
            base_dir = Path(timetable_file).parent.parent.parent  # Go up from timetable_outputs/TIMESTAMP/ to timetable_generator
            
            # Get the timestamp from the timetable file path
            timestamp = Path(timetable_file).parent.name
            course_csv = base_dir / 'input_files' / 'versions' / timestamp / f"{dept}.csv"
            
            print(f"Looking for course CSV: {course_csv}")
            print(f"   Timetable file: {timetable_file}")
            print(f"   Base dir: {base_dir}")
            print(f"   Timestamp: {timestamp}")
            print(f"   Course CSV exists: {course_csv.exists()}")
            
            if not course_csv.exists():
                print(f"   Course CSV not found!")
                return ""
            
            # Read the course CSV
            df_courses = pd.read_csv(course_csv)
            print(f"   Loaded {len(df_courses)} courses from CSV")
            
            # Filter 1 and 2-credit courses for this semester and section (Till Midsem)
            two_credit_courses = df_courses[
                (df_courses['Credits'].isin([1, 2])) & 
                (df_courses['Semester'] == int(semester.replace('Sem', '')))
            ]
            
            print(f"   Found {len(two_credit_courses)} till-midsem courses for {semester}")
            
            # Further filter by section if specified (only if Section column exists)
            if 'Section' in df_courses.columns:
                if section != 'SectionA' and section != 'SectionB':
                    # Common courses
                    two_credit_courses = two_credit_courses[
                        (two_credit_courses['Section'].isna()) | 
                        (two_credit_courses['Section'] == '')
                    ]
                else:
                    # Section-specific or common courses
                    section_num = section.replace('Section', '')
                    two_credit_courses = two_credit_courses[
                        (two_credit_courses['Section'].isna()) | 
                        (two_credit_courses['Section'] == '') |
                        (two_credit_courses['Section'].str.contains(section_num, na=False))
                    ]
            else:
                # No Section column - all courses are common
                print(f"   No Section column in CSV - treating all courses as common")
            
            print(f"   Final count after section filter ({section}): {len(two_credit_courses)} courses")
            
            if len(two_credit_courses) == 0:
                print(f"   No till-midsem courses to display")
                return ""
            
            # Store for later use (to add badges in cells)
            self.till_midsem_courses = set(two_credit_courses['Course Code'].tolist())
            print(f"   Till-midsem courses: {self.till_midsem_courses}")
            
            # Generate HTML for till midsem section
            html = """
        <div class="till-midsem-section">
            <h2>⏰ Till Midsem Courses (1-2 Credits)</h2>
            <p class="till-midsem-note">⚠️ These courses are scheduled only until the midsemester examinations</p>
            <div class="till-midsem-courses">
"""
            
            for _, course in two_credit_courses.iterrows():
                course_code = course['Course Code']
                course_title = course['Course Title']
                faculty = course.get('Faculty', 'TBA')
                credits = course['Credits']
                
                html += f"""
                <div class="till-midsem-course-card">
                    <div class="course-code">{course_code}</div>
                    <div class="course-title">{course_title}</div>
                    <div class="course-credits">👨‍🏫 {faculty} | 📊 {credits} Credit{'s' if credits > 1 else ''}</div>
                </div>
"""
            
            html += """
            </div>
            <p style="margin-top: 20px; color: #7f1d1d; font-style: italic; text-align: center; font-size: 0.95em;">
                💡 <strong>Note:</strong> After midsem exams, these time slots will be used for other courses or activities.
            </p>
        </div>
"""
            
            return html
            
        except Exception as e:
            print(f"Warning: Could not load 2-credit courses: {e}")
            return ""
    
    def _generate_table(self, df):
        """Generate HTML table from DataFrame with duration bar support"""
        html = '<table>\n<thead>\n<tr>\n'
        
        # Header row
        html += '<th style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">Day/Time</th>\n'
        for col in df.columns:
            # Check if this is an afternoon flexible slot
            if self._is_afternoon_flex_slot(col):
                html += f'<th class="time-slot" style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);">⏰ {col} <br><small style="font-size:0.8em;opacity:0.9">📦 2-Hour Flexible</small></th>\n'
            else:
                html += f'<th class="time-slot">⏰ {col}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        
        # Data rows
        for day in df.index:
            html += '<tr>\n'
            html += f'<td class="day-column">{day}</td>\n'
            
            for col in df.columns:
                cell_value = str(df.loc[day, col])
                
                # Check if this is an afternoon flexible slot
                if self._is_afternoon_flex_slot(col):
                    html += self._render_flex_slot_cell(cell_value, col)
                else:
                    # Check if this cell contains a till midsem course (1-2 credits)
                    is_till_midsem = self._is_till_midsem_course(cell_value)
                    
                    # Extract course code and get course-specific color
                    course_code = self._extract_course_code(cell_value)
                    cell_style = ""
                    
                    # Get cell class, override with red if till midsem
                    if is_till_midsem:
                        cell_class = 'till-midsem-cell'
                        # Till midsem cells get red background, no custom color
                    elif course_code and cell_value.lower() != 'free' and 'lunch' not in cell_value.lower():
                        # Use course-specific color
                        colors = self._get_course_color(course_code)
                        cell_class = 'course-slot'
                        cell_style = f"background: {colors['background']}; border-left: 6px solid {colors['border']}; color: {colors['text']};"
                    else:
                        cell_class = self._get_cell_class(cell_value)
                    
                    # Clean display value (remove [EVENING] label)
                    display_value = cell_value.replace('[EVENING]', '').strip()
                    # For regular slots (non-flex), show tutorials with fractional colored bar
                    # Clean display value (remove duration markers and EVENING label)
                    display_clean = display_value.replace('[120min]', '').replace('[90min]', '').replace('[60min]', '').replace('[EVENING]', '').strip()

                    # Robust tutorial detection (case-insensitive) for regular slots
                    val_lower = cell_value.lower()
                    is_tutorial = ('[60min]' in val_lower) or ('-t-' in val_lower) or ('tutorial' in val_lower)

                    if is_tutorial:
                        # Regular slot capacity is 90 minutes
                        slot_capacity = 90
                        dur = 60

                        width_pct = round((dur / slot_capacity) * 100, 2)

                        # Build a clean display label: show course and explicit "Tutorial (1 hour)"
                        # Remove any bracketed duration markers and tutorial markers from the raw text
                        cleaned = display_clean.replace('[60min]', '').replace('[90min]', '').replace('[120min]', '')
                        cleaned = cleaned.replace('-T-', '').replace('-t-', '').replace('  ', ' ').strip()

                        # If classroom info is present around a pipe '|' keep it
                        display_label = f"{cleaned} \u2014 Tutorial (1 hour)"

                        html += (
                            f'<td class="{cell_class}" style="{cell_style}">'
                            f'<div class="cell-inner">'
                            f'<div class="duration-segment tutorial-seg" style="width:{width_pct}%;"></div>'
                            f'<div class="cell-text">{display_label}</div>'
                            f'</div></td>\n'
                        )
                    else:
                        html += f'<td class="{cell_class}" style="{cell_style}">{display_clean}</td>\n'
            
            html += '</tr>\n'
        
        html += '</tbody>\n</table>'
        return html
    
    def _is_afternoon_flex_slot(self, time_slot):
        """Check if a time slot is an afternoon flexible slot (2 hours)"""
        # Afternoon flexible slots: 14:30-16:30 and 16:30-18:30
        flex_patterns = ['14:30-16:30', '16:30-18:30']
        return any(pattern in time_slot for pattern in flex_patterns)
    
    def _render_flex_slot_cell(self, cell_value, time_slot):
        """Render a flexible afternoon slot cell with duration bar"""
        # Check for free slot or lunch
        if cell_value.lower() == 'free':
            return '<td class="free-slot">Free</td>\n'
        elif 'lunch' in cell_value.lower():
            return '<td class="lunch-break">🍽️ LUNCH BREAK</td>\n'
        
        # Check if this is a till midsem course
        is_till_midsem = self._is_till_midsem_course(cell_value)
        
        # Extract course code and get course-specific color
        course_code = self._extract_course_code(cell_value)
        cell_style = ""
        
        # Parse duration from cell value (e.g., "[120min]", "[90min]", "[60min]")
        duration_minutes = 120  # Default to full slot
        duration_class = 'lab-duration'  # Default
        duration_label = '2 Hours'
        
        if '[120min]' in cell_value:
            duration_minutes = 120
            duration_class = 'lab-duration'
            duration_label = '2 Hours'
        elif '[90min]' in cell_value:
            duration_minutes = 90
            duration_class = 'lecture-duration'
            duration_label = '1.5 Hours'
        elif '[60min]' in cell_value:
            duration_minutes = 60
            duration_class = 'tutorial-duration'
            duration_label = '1 Hour'
        elif 'Lab' in cell_value or 'lab' in cell_value:
            duration_class = 'lab-duration'
            duration_label = '2 Hours'
        elif '-T-' in cell_value or 'Tutorial' in cell_value:
            duration_class = 'tutorial-duration'
            duration_minutes = 60
            duration_label = '1 Hour'
        else:
            duration_class = 'lecture-duration'
            duration_minutes = 90
            duration_label = '1.5 Hours'
        
        # Clean cell value for display (remove duration markers and EVENING label)
        display_value = cell_value.replace('[120min]', '').replace('[90min]', '').replace('[60min]', '').replace('[EVENING]', '').strip()
        
        # Override with till midsem class if needed
        if is_till_midsem:
            cell_class = 'till-midsem-cell'
        elif course_code:
            # Use course-specific color
            colors = self._get_course_color(course_code)
            cell_class = 'afternoon-flex-slot'
            cell_style = f"background: {colors['background']}; border-left: 6px solid {colors['border']}; color: {colors['text']};"
        else:
            cell_class = 'afternoon-flex-slot'
        
        # Generate cell HTML with duration bar
        cell_html = f'''<td class="{cell_class}" style="{cell_style}">
    <div class="session-container">
        <div class="duration-bar-wrapper">
            <div class="duration-bar {duration_class}">
                <div class="course-info">{display_value}</div>
                <div class="duration-tag">{duration_label}</div>
            </div>
        </div>
    </div>
</td>
'''
        return cell_html
    
    def _is_till_midsem_course(self, cell_value):
        """Check if cell contains a till midsem course (1-2 credits)"""
        if not hasattr(self, 'till_midsem_courses') or not self.till_midsem_courses:
            return False
        
        # Extract course code from cell value (format: "CSXXX - Title" or "CSXXX")
        for course_code in self.till_midsem_courses:
            if course_code in cell_value:
                return True
        
        return False
    
    def _extract_course_code(self, cell_value):
        """Extract course code from cell value (e.g., CS101, MA102, etc.)"""
        import re
        # Match patterns like CS101, MA102, EC201, etc.
        match = re.search(r'[A-Z]{2,4}\d{3}', cell_value)
        if match:
            return match.group(0)
        return None
    
    def _get_cell_class(self, value):
        """Determine CSS class based on cell content"""
        value_lower = value.lower()
        
        if 'lunch break' in value_lower:
            return 'lunch-break'
        elif value_lower == 'free':
            return 'free-slot'
        elif 'elective' in value_lower:
            return 'elective-slot'  # Orange color for electives
        elif 'common' in value_lower:
            return 'common-course'  # Yellow/amber for common classes
        elif 'lab' in value_lower or '[120min]' in value:
            return 'lab-slot'  # Purple for 2-hour labs
        elif '-t-' in value_lower or '[60min]' in value or 'tutorial' in value_lower:
            return 'tutorial-slot'  # Green for 1-hour tutorials
        else:
            return 'course-slot'  # Blue for individual section classes
    
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
        
        @keyframes gradient {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}
        
        @keyframes float {{
            0%, 100% {{
                transform: translateY(0px);
            }}
            50% {{
                transform: translateY(-20px);
            }}
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe, #43e97b, #fa709a);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: float 20s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
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
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3),
                         0 0 20px rgba(255,255,255,0.5),
                         0 0 40px rgba(255,255,255,0.3);
            animation: float 3s ease-in-out infinite;
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
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3),
                        0 0 30px rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .department-card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 30px 80px rgba(0,0,0,0.4),
                        0 0 50px rgba(102, 126, 234, 0.5);
        }}
        
        .dept-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            position: relative;
            overflow: hidden;
        }}
        
        .dept-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }}
        
        @keyframes shine {{
            0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
            100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            flex: 1;
            text-align: center;
            min-width: 120px;
            border: 2px solid rgba(255,255,255,0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .timetable-link::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .timetable-link:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .timetable-link:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6),
                        0 0 20px rgba(240, 147, 251, 0.4);
            background: linear-gradient(135deg, #f093fb 0%, #764ba2 50%, #667eea 100%);
            border-color: rgba(255,255,255,0.5);
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
        
        .back-to-main {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin: 20px;
            padding: 12px 28px;
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.05em;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(86, 171, 47, 0.35);
        }}
        
        .back-to-main:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(86, 171, 47, 0.5);
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
        <a href="/upload.html" class="back-to-main">🏠 Back to Main Menu</a>
        
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
"""
                
                # Check if DSAI or ECE (they don't have sections)
                if dept in ['DSAI', 'ECE'] and len(dept_data[dept][semester]) == 1:
                    html_content += """
                    <div class="section-buttons">
"""
                    section_info = dept_data[dept][semester][0]
                    file = section_info['file']
                    html_content += f"""
                        <a href="{file}" class="timetable-link">View Timetable</a>
"""
                else:
                    # CSE has sections
                    html_content += """
                    <div class="section-buttons">
"""
                    for section_info in dept_data[dept][semester]:
                        section = section_info['section']
                        file = section_info['file']
                        # Extract just the letter from 'SectionA' -> 'A'
                        section_letter = section.replace('Section', '')
                        html_content += f"""
                        <a href="{file}" class="timetable-link">Section {section_letter}</a>
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
        
        <!-- Editor Panel (loads selected timetable into iframe for viewing/editing) -->
        <div id="editorPanel" style="margin-top:40px; display:none; gap:20px; align-items:flex-start;">
            <div style="flex:1;">
                <div style="display:flex; gap:10px; align-items:center; margin-bottom:10px;">
                    <button id="closeEditor" class="timetable-link" style="background:#ef4444;">Close Editor</button>
                    <label style="color:#fff; font-weight:600;">Editor Mode:</label>
                    <button id="toggleEdit" class="timetable-link" style="background:#10b981;">Enable Edit</button>
                    <button id="undoBtn" class="timetable-link" style="background:#f59e0b;" disabled>Undo</button>
                    <button id="redoBtn" class="timetable-link" style="background:#f97316;" disabled>Redo</button>
                    <button id="saveCsv" class="timetable-link" style="background:#06b6d4;">Save CSV</button>
                    <span id="editorStatus" style="color:#fff; margin-left:10px; font-weight:600; opacity:0.95;"></span>
                    <button id="viewFullBtn" class="timetable-link" style="background:#8b5cf6; display:none; margin-left:10px;">🔍 View as Full</button>
                </div>
                <iframe id="timetableFrame" src="" style="width:100%; height:720px; border-radius:12px; border:4px solid rgba(255,255,255,0.08); background:white;"></iframe>
            </div>
        </div>
    </div>
</body>
<script>
// Timetable Viewer Editor - parent-page based iframe editor
(() => {
    const links = document.querySelectorAll('.timetable-link');
    const editorPanel = document.getElementById('editorPanel');
    const frame = document.getElementById('timetableFrame');
    const toggleEditBtn = document.getElementById('toggleEdit');
    const saveCsvBtn = document.getElementById('saveCsv');
    const closeBtn = document.getElementById('closeEditor');
    const status = document.getElementById('editorStatus');
    const viewFullBtn = document.getElementById('viewFullBtn');
    let editEnabled = false;
    let currentHref = null;
    // Undo/Redo history stacks (store table.outerHTML snapshots)
    const MAX_HISTORY = 60;
    let historyStack = [];
    let redoStack = [];
    const undoBtn = document.getElementById('undoBtn');
    const redoBtn = document.getElementById('redoBtn');

    // Intercept timetable links to open in iframe editor
    links.forEach(a => {
        a.addEventListener('click', (e) => {
            const href = a.getAttribute('href');
            if (!href) return;
            e.preventDefault();
            currentHref = href;
            
            // Show loading state
            status.textContent = 'Loading: ' + href.split('/').pop();
            status.style.color = '#fbbf24'; // yellow
            viewFullBtn.style.display = 'none';
            editEnabled = false;
            toggleEditBtn.textContent = 'Enable Edit';
            toggleEditBtn.disabled = true;
            
            // reset history for new file
            historyStack = [];
            redoStack = [];
            updateHistoryButtons();
            
            // Load iframe
            frame.src = href;
            editorPanel.style.display = 'flex';
            
            // Wait for iframe to load
            const loadTimeout = setTimeout(() => {
                status.textContent = 'Load timeout - try refreshing';
                status.style.color = '#ef4444'; // red
            }, 10000);
            
            frame.onload = () => {
                clearTimeout(loadTimeout);
                try {
                    const doc = frame.contentDocument || frame.contentWindow.document;
                    if (!doc || !doc.querySelector('table')) {
                        status.textContent = 'Error: No table found or cross-origin blocked';
                        status.style.color = '#ef4444';
                        return;
                    }
                    status.textContent = 'Ready: ' + href.split('/').pop();
                    status.style.color = '#10b981'; // green
                    viewFullBtn.style.display = 'inline-block';
                    toggleEditBtn.disabled = false;
                } catch (err) {
                    console.error('Iframe load error:', err);
                    status.textContent = 'Error: Cannot access iframe (cross-origin?)';
                    status.style.color = '#ef4444';
                }
            };
            
            frame.onerror = () => {
                clearTimeout(loadTimeout);
                status.textContent = 'Failed to load timetable';
                status.style.color = '#ef4444';
            };
        });
    });

    // Close editor
    closeBtn.addEventListener('click', () => {
        frame.src = '';
        frame.onload = null;
        frame.onerror = null;
        editorPanel.style.display = 'none';
        status.textContent = '';
        status.style.color = '#fff';
        viewFullBtn.style.display = 'none';
        toggleEditBtn.disabled = false;
        // clear history when closing
        historyStack = [];
        redoStack = [];
        updateHistoryButtons();
    });
    
    // View Full Page button
    viewFullBtn.addEventListener('click', () => {
        if (currentHref) {
            window.open(currentHref, '_blank');
        }
    });

    // Toggle edit mode
    toggleEditBtn.addEventListener('click', () => {
        if (!frame.src) {
            alert('Open a timetable first');
            return;
        }
        
        try {
            const doc = frame.contentDocument || frame.contentWindow.document;
            if (!doc) {
                alert('Cannot access iframe content. The page may not have loaded yet or there is a cross-origin issue.');
                return;
            }
            
            const table = doc.querySelector('table');
            if (!table) {
                alert('No timetable table found in the loaded page.');
                return;
            }
            
            editEnabled = !editEnabled;
            toggleEditBtn.textContent = editEnabled ? 'Disable Edit' : 'Enable Edit';
            status.textContent = editEnabled ? 'Edit mode ON' : 'Edit mode OFF';
            status.style.color = editEnabled ? '#10b981' : '#fff';
            
            if (editEnabled) {
                enableEditing(doc);
                // initial snapshot (only if history is empty for this session)
                if (historyStack.length === 0) pushSnapshot(doc);
                attachKeyHandlers(doc);
            } else {
                disableEditing(doc);
                removeKeyHandlers(doc);
            }
        } catch (err) {
            console.error('Error toggling edit mode:', err);
            alert('Unable to toggle edit mode:\\n' + err.message + '\\n\\nThis usually happens if:\\n- The page is still loading\\n- Cross-origin restrictions apply\\n- The timetable file is missing or corrupted');
        }
    });

    // Save CSV by extracting table inside iframe
    saveCsvBtn.addEventListener('click', () => {
        if (!frame.src) return alert('Open a timetable first');
        try {
            const doc = frame.contentDocument || frame.contentWindow.document;
            const table = doc.querySelector('table');
            if (!table) return alert('No timetable table found in the page');
            const csv = tableToCSV(table);
            const filename = (currentHref || 'timetable').split('/').pop().replace('.html','.csv');
            downloadString(csv, filename);
        } catch (err) {
            console.error(err);
            alert('Error saving CSV: ' + err.message);
        }
    });

    // Undo / Redo button handlers
    undoBtn.addEventListener('click', () => { try { undo(); } catch(e){console.error(e);} });
    redoBtn.addEventListener('click', () => { try { redo(); } catch(e){console.error(e);} });


    // Helper: enable editing in iframe doc
    function enableEditing(doc) {
        const cells = doc.querySelectorAll('td');
        cells.forEach(td => {
            // Enable drag-and-drop
            td.setAttribute('draggable','true');
            td.style.cursor = 'move';
            td.addEventListener('dragstart', dragStartHandler);
            td.addEventListener('dragover', dragOverHandler);
            td.addEventListener('drop', dropHandler);
            
            // Enable direct text editing (especially for classroom names)
            td.contentEditable = 'true';
            td.addEventListener('blur', cellBlurHandler);
            td.addEventListener('keydown', cellKeydownHandler);
        });
        // Enable editing of time slot headers (except first column)
        const headers = doc.querySelectorAll('thead th');
        headers.forEach((th, idx) => {
            if (idx === 0) return; // skip Day/Time column
            th.contentEditable = 'true';
            th.style.cursor = 'text';
            th.addEventListener('blur', headerBlurHandler);
            th.addEventListener('keydown', headerKeydownHandler);
        });
    }

    function disableEditing(doc) {
        const cells = doc.querySelectorAll('td');
        cells.forEach(td => {
            td.removeAttribute('draggable');
            td.style.cursor = '';
            td.contentEditable = 'false';
            td.removeEventListener('dragstart', dragStartHandler);
            td.removeEventListener('dragover', dragOverHandler);
            td.removeEventListener('drop', dropHandler);
            td.removeEventListener('blur', cellBlurHandler);
            td.removeEventListener('keydown', cellKeydownHandler);
        });
        // Disable header editing
        const headers = doc.querySelectorAll('thead th');
        headers.forEach((th, idx) => {
            if (idx === 0) return;
            th.contentEditable = 'false';
            th.style.cursor = '';
            th.removeEventListener('blur', headerBlurHandler);
            th.removeEventListener('keydown', headerKeydownHandler);
        });
    }

    // Drag handlers (operate on iframe's document elements)
    function dragStartHandler(ev) {
        // store source element reference on the document for later swapping
        try { ev.target.ownerDocument._dragSrc = ev.target; } catch(e){}
        ev.dataTransfer.setData('text/html', ev.target.innerHTML || '');
        ev.dataTransfer.setData('text/plain', 'timetable-cell');
        ev.dataTransfer.effectAllowed = 'move';
    }

    function dragOverHandler(ev) { ev.preventDefault(); ev.dataTransfer.dropEffect = 'move'; }

    function dropHandler(ev) {
        ev.preventDefault();
        const target = ev.currentTarget;
        const html = ev.dataTransfer.getData('text/html');
        const doc = target.ownerDocument;
        if (!html) return;
        // Try to swap source and target content if source reference exists
        const src = doc._dragSrc;
        if (src && src !== target) {
            const tmp = target.innerHTML;
            target.innerHTML = src.innerHTML;
            src.innerHTML = tmp;
            // cleanup
            try { delete doc._dragSrc; } catch(e) { doc._dragSrc = null; }
            // push snapshot after a swap
            try { pushSnapshot(doc); } catch (e) { console.error('pushSnapshot error', e); }
        } else {
            // Fallback: just place dragged HTML into target
            target.innerHTML = html;
            try { pushSnapshot(doc); } catch (e) { console.error('pushSnapshot error', e); }
        }
    }

    // Convert table DOM to CSV (day in first column + text content of each cell)
    function tableToCSV(table) {
        const rows = [];
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => cleanText(th.innerText));
        rows.push(headers.join(','));
        table.querySelectorAll('tbody tr').forEach(tr => {
            const cells = Array.from(tr.children).map(td => '"' + cleanText(td.innerText).replace(/"/g,'""') + '"');
            rows.push(cells.join(','));
        });
        return rows.join('\\n');
    }

    function cleanText(s) { return (s||'').trim().replace(/\\n+/g,' ').replace(/\\s+/g,' ').replace(/,/g,';'); }

    function downloadString(text, filename) {
        const blob = new Blob([text], {type: 'text/csv;charset=utf-8;'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    }

    // History (undo/redo) helpers: snapshots store table.outerHTML
    function pushSnapshot(doc) {
        try {
            const table = doc.querySelector('table');
            if (!table) return;
            const snap = table.outerHTML;
            // avoid duplicates
            if (historyStack.length && historyStack[historyStack.length-1] === snap) return;
            historyStack.push(snap);
            if (historyStack.length > MAX_HISTORY) historyStack.shift();
            // clear redo when new action occurs
            redoStack = [];
            updateHistoryButtons();
        } catch (e) { console.error('pushSnapshot failed', e); }
    }

    function restoreSnapshot(snapshot, doc) {
        try {
            const table = doc.querySelector('table');
            if (!table) return;
            // replace table markup
            table.outerHTML = snapshot;
            // re-enable handlers on the new DOM elements if editing is active
            if (editEnabled) enableEditing(doc);
            updateHistoryButtons();
        } catch (e) { console.error('restoreSnapshot failed', e); }
    }

    function undo() {
        try {
            if (historyStack.length < 2) return;
            const doc = frame.contentDocument || frame.contentWindow.document;
            if (!doc) return;
            const last = historyStack.pop();
            redoStack.push(last);
            const prev = historyStack[historyStack.length-1];
            if (prev) restoreSnapshot(prev, doc);
        } finally { updateHistoryButtons(); }
    }

    function redo() {
        try {
            if (redoStack.length === 0) return;
            const doc = frame.contentDocument || frame.contentWindow.document;
            if (!doc) return;
            const snap = redoStack.pop();
            historyStack.push(snap);
            restoreSnapshot(snap, doc);
        } finally { updateHistoryButtons(); }
    }

    function updateHistoryButtons() {
        try {
            undoBtn.disabled = !(historyStack.length > 1);
            redoBtn.disabled = !(redoStack.length > 0);
        } catch (e) { /* ignore if buttons not present yet */ }
    }

    // Keyboard shortcuts inside iframe (when editing): Ctrl+Z / Ctrl+Y
    function attachKeyHandlers(doc) {
        try {
            const win = doc.defaultView || doc.parentWindow;
            if (!win) return;
            const handler = (ev) => {
                const key = ev.key.toLowerCase();
                const isMod = ev.ctrlKey || ev.metaKey;
                if (!isMod) return;
                if (key === 'z') { ev.preventDefault(); undo(); }
                else if (key === 'y' || (ev.shiftKey && key === 'z')) { ev.preventDefault(); redo(); }
            };
            // store reference so we can remove later
            doc._historyKeyHandler = handler;
            win.addEventListener('keydown', handler);
        } catch (e) { console.error('attachKeyHandlers failed', e); }
    }

    function removeKeyHandlers(doc) {
        try {
            const win = doc.defaultView || doc.parentWindow;
            if (!win) return;
            const handler = doc._historyKeyHandler;
            if (handler) win.removeEventListener('keydown', handler);
            doc._historyKeyHandler = null;
        } catch (e) { console.error('removeKeyHandlers failed', e); }
    }

    // Header editing handlers inside iframe
    function headerBlurHandler(ev) {
        // normalize whitespace and ensure readable format
        ev.target.innerText = ev.target.innerText.trim().replace(/\\n+/g,' ').replace(/\\s+/g,' ');
        // record header edit in history
        try { const doc = ev.target.ownerDocument; pushSnapshot(doc); } catch(e){ console.error('pushSnapshot error', e); }
    }

    function headerKeydownHandler(ev) {
        // Enter commits edit and blurs
        if (ev.key === 'Enter') {
            ev.preventDefault();
            ev.target.blur();
        }
    }

    // Cell editing handlers (for editing course names, classrooms, etc.)
    function cellBlurHandler(ev) {
        // normalize whitespace
        ev.target.innerText = ev.target.innerText.trim().replace(/\\n+/g,' ').replace(/\\s+/g,' ');
        // record cell edit in history
        try { const doc = ev.target.ownerDocument; pushSnapshot(doc); } catch(e){ console.error('pushSnapshot error', e); }
    }

    function cellKeydownHandler(ev) {
        // Enter commits edit and blurs
        if (ev.key === 'Enter') {
            ev.preventDefault();
            ev.target.blur();
        }
    }

})();
</script>
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
    
    def _load_elective_baskets_from_csv(self, csv_file, dept, semester, section):
        """Load and display elective baskets that are scheduled in this timetable"""
        try:
            # Read the CSV to find which baskets are scheduled
            df = pd.read_csv(csv_file, index_col=0)
            
            # Find all basket names in the timetable
            baskets_found = set()
            basket_time_slots = {}  # Track time slots for each basket
            
            for col in df.columns:
                for idx, val in enumerate(df[col]):
                    # Look for elective baskets (contains "Basket" or "Elective")
                    if isinstance(val, str) and ('Basket' in val or 'Elective' in val or 'HSS' in val):
                        # Extract basket name (remove any extra info like "[...]" or "-T")
                        basket_name = val.split('[')[0].strip()
                        # Remove tutorial suffix (-T)
                        if basket_name.endswith('-T'):
                            basket_name = basket_name[:-2]
                        baskets_found.add(basket_name)
                        
                        # Track the day and time slot
                        day = df.index[idx]
                        if basket_name not in basket_time_slots:
                            basket_time_slots[basket_name] = []
                        # Include tutorial indicator in time slot display
                        time_display = f"{day} {col}"
                        if val.endswith('-T'):
                            time_display += " (Tutorial)"
                        basket_time_slots[basket_name].append(time_display)
            
            # Load elective basket data from JSON file
            json_filepath = csv_file.replace('.csv', '_Electives.json')
            elective_data = {}
            
            if os.path.exists(json_filepath):
                import json
                with open(json_filepath, 'r', encoding='utf-8') as f:
                    elective_data = json.load(f)
            
            # Add all baskets from JSON to baskets_found (including Elective B which isn't in CSV)
            for key in elective_data.keys():
                if not key.endswith('_meta'):
                    baskets_found.add(key)
            
            if not baskets_found:
                return ""  # No baskets in this timetable
            
            # Create HTML display
            html = f"""
        <div class="electives-section" style="margin-top: 30px; padding: 25px; background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); border-radius: 15px; border: 3px solid #6366f1;">
            <h2 style="color: #3730a3; margin-bottom: 15px;">📚 Elective Baskets in This Timetable</h2>
            <p style="color: #4338ca; font-weight: 600; margin-bottom: 20px;">The following elective baskets are scheduled in your timetable. Choose <strong>ONE course</strong> from each basket:</p>
            <div class="electives-container">
"""
            
            for basket in sorted(baskets_found):
                # Special handling for Elective B (uses Elective A's time slots)
                time_info = ""
                special_note = ""
                
                if basket == 'Elective B':
                    # Elective B uses Elective A's time slots
                    if 'Elective A' in basket_time_slots and basket_time_slots['Elective A']:
                        time_info = f"<p style='color: #6b7280; font-size: 0.9em; margin-bottom: 15px;'><strong>⏰ Time:</strong> {', '.join(sorted(set(basket_time_slots['Elective A'])))} (Same as Elective A)</p>"
                    special_note = """
                    <div style="background: #fef3c7; padding: 12px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 15px;">
                        <strong style="color: #b45309;">⏳ After Mid-Semester Only:</strong><br>
                        <span style="color: #78350f; font-size: 0.95em;">These courses START AFTER mid-semester exams and use the SAME time slots as Elective A courses shown above.</span>
                    </div>
"""
                elif basket in basket_time_slots and basket_time_slots[basket]:
                    time_info = f"<p style='color: #6b7280; font-size: 0.9em; margin-bottom: 15px;'><strong>⏰ Time:</strong> {', '.join(sorted(set(basket_time_slots[basket])))}</p>"
                
                html += f"""
                <div class="basket-card" style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #6366f1;">
                    <h3 style="color: #3730a3; margin-bottom: 10px;">🎯 {basket}</h3>
                    {time_info}
                    {special_note}
                    <p style="color: #4338ca; font-weight: 600; margin-bottom: 10px;">Courses in this basket (all run at the same time):</p>
"""
                
                # Add course list if available
                if basket in elective_data and len(elective_data[basket]) > 0:
                    # Check if basket has tutorials
                    meta_key = basket + '_meta'
                    has_tutorials = False
                    tutorial_courses = []
                    if meta_key in elective_data:
                        has_tutorials = elective_data[meta_key].get('has_tutorials', False)
                        tutorial_courses = elective_data[meta_key].get('tutorial_courses', [])
                    
                    html += """
                    <ul style="list-style-type: none; padding-left: 0; margin: 10px 0;">
"""
                    for course in elective_data[basket]:
                        tutorial_indicator = ""
                        if course.get('tutorials', 0) > 0:
                            tutorial_indicator = f" | 📝 Tutorial: {course['tutorials']}T"
                        
                        credit_info = f" ({course.get('credits', 0)} Credits)"
                        
                        html += f"""
                        <li style="padding: 8px; margin: 5px 0; background: #f3f4f6; border-radius: 5px;">
                            <strong style="color: #3730a3;">{course['code']}</strong> - {course['title']}{credit_info}<br>
                            <span style="color: #6b7280; font-size: 0.9em;">📍 Classroom: {course['classroom']}{tutorial_indicator}</span>
                        </li>
"""
                    html += """
                    </ul>
"""
                    
                    # Add tutorial note if basket has tutorials
                    if has_tutorials:
                        html += f"""
                    <div style="background: #fef3c7; padding: 10px; border-radius: 5px; border-left: 3px solid #f59e0b; margin-top: 10px;">
                        <strong style="color: #b45309;">⚠️ Tutorial Requirement:</strong><br>
                        <span style="color: #78350f; font-size: 0.9em;">This basket includes courses with tutorial sessions. 
                        Courses with tutorials: {', '.join(tutorial_courses)}</span>
                    </div>
"""
                else:
                    html += """
                    <p style="color: #6b7280; font-size: 0.95em;">Choose one course from this basket. All courses run at the same time in different classrooms.</p>
"""
                
                html += """
                </div>
"""
            
            html += """
            </div>
            <p style="margin-top: 20px; color: #4338ca; font-style: italic; font-size: 0.95em;">
                💡 <strong>Note:</strong> Check with your department for the complete list of courses in each basket and their classrooms.
            </p>
        </div>
"""
            
            return html
            
        except Exception as e:
            print(f"Warning: Could not load elective baskets from {csv_file}: {e}")
            return ""

def main():
    """Main function"""
    print("\nBeyondGames Timetable HTML Converter")
    print("="*80)
    # Allow overriding input/output directories via environment variables
    input_dir = os.environ.get('INPUT_CSV_DIR', 'timetable_outputs')
    output_dir = os.environ.get('OUTPUT_HTML_DIR', 'timetable_html')

    converter = TimetableHTMLConverter(input_dir=input_dir, output_dir=output_dir)
    converter.convert_all()
    
    print("\n" + "="*80)
    print("HTML conversion complete!")
    print(f"Open: timetable_html/index.html in your browser")
    print("="*80)

if __name__ == "__main__":
    main()
