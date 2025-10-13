"""
Generate Seating Charts Viewer HTML
This script reads the seating_summary.csv and creates a comprehensive viewer page
"""

import pandas as pd
import os
from pathlib import Path

def generate_seating_viewer():
    """Generate HTML page with all seating charts organized by date and session"""
    
    # Read the seating summary CSV
    summary_file = 'outputs/seating_summary.csv'
    
    if not os.path.exists(summary_file):
        print(f"❌ Error: {summary_file} not found!")
        print("Please run main.py first to generate the seating arrangements.")
        return
    
    df = pd.read_csv(summary_file)
    
    # Group by exam date and session
    # First, we need to aggregate data by date, session, and classroom
    summary = df.groupby(['Exam_Date', 'Session', 'Classroom']).agg({
        'Course_Code': lambda x: ' + '.join(sorted(set(x))),
        'Students_Assigned': 'sum',
        'HTML_Chart': 'first'
    }).reset_index()
    
    summary.columns = ['Date', 'Session', 'Classroom', 'Courses', 'Total_Students', 'Chart_File']
    
    # Group by date and session
    grouped = summary.groupby(['Date', 'Session'])
    
    # Start building HTML
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exam Seating Charts - IIIT Dharwad</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #667eea;
        }
        
        .header h1 {
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            color: #64748b;
        }
        
        .back-button {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            margin-bottom: 30px;
        }
        
        .back-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .session-group {
            margin-bottom: 50px;
            animation: fadeIn 0.6s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .session-header {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        }
        
        .session-header h2 {
            font-size: 1.8em;
            margin-bottom: 5px;
        }
        
        .session-header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .session-header.forenoon {
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        }
        
        .session-header.afternoon {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .chart-card {
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        
        .chart-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            border-color: #667eea;
        }
        
        .chart-classroom {
            font-size: 1.5em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .chart-courses {
            font-size: 0.95em;
            color: #64748b;
            margin-bottom: 8px;
            line-height: 1.5;
        }
        
        .chart-students {
            font-size: 0.9em;
            color: #94a3b8;
            font-weight: 500;
        }
        
        .stats {
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: 700;
            color: #0c4a6e;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 1em;
            color: #64748b;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .charts-grid {
                grid-template-columns: 1fr;
            }
        }
        
        .navigation {
            display: flex;
            gap: 20px;
            margin-bottom: 35px;
            flex-wrap: wrap;
            justify-content: center;
            padding: 15px;
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,249,250,0.9) 100%);
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .nav-button {
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
        }
        
        .nav-button::before {
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
        }
        
        .nav-button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
            border-color: rgba(255, 255, 255, 0.4);
        }
        
        .nav-button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .nav-button:active {
            transform: translateY(-1px) scale(0.98);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .nav-button.exam {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 50%, #c44569 100%);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.35);
        }
        
        .nav-button.exam:hover {
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.5);
        }
        
        .nav-button.home {
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            box-shadow: 0 6px 20px rgba(86, 171, 47, 0.35);
        }
        
        .nav-button.home:hover {
            box-shadow: 0 10px 30px rgba(86, 171, 47, 0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🪑 Exam Seating Arrangements</h1>
            <p>View all seating charts organized by date and session</p>
        </div>
        
        <div class="navigation">
            <a href="../../index.html" class="nav-button home">🏠 Main Menu</a>
            <a href="exam_timetable.html" class="nav-button exam">📋 Exam Schedule</a>
            <a href="exam_schedule.csv" class="nav-button" download>📊 Download CSV</a>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value">TOTAL_CHARTS_PLACEHOLDER</div>
                <div class="stat-label">Seating Charts</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">TOTAL_CLASSROOMS_PLACEHOLDER</div>
                <div class="stat-label">Classrooms</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">TOTAL_SESSIONS_PLACEHOLDER</div>
                <div class="stat-label">Exam Sessions</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">TOTAL_STUDENTS_PLACEHOLDER</div>
                <div class="stat-label">Total Seats</div>
            </div>
        </div>
"""
    
    # Generate content for each date and session
    for (date, session), group in grouped:
        session_class = 'forenoon' if session == 'FN' else 'afternoon'
        session_name = 'Forenoon' if session == 'FN' else 'Afternoon'
        
        html_content += f"""
        <div class="session-group">
            <div class="session-header {session_class}">
                <h2>📅 {date}</h2>
                <p>{session_name} Session ({session})</p>
            </div>
            
            <div class="charts-grid">
"""
        
        # Add each classroom card
        for _, row in group.iterrows():
            classroom = row['Classroom']
            courses = row['Courses']
            num_students = row['Total_Students']
            chart_file = row['Chart_File']
            
            # Remove 'outputs/' prefix if present (file is relative to outputs folder)
            if chart_file.startswith('outputs/'):
                chart_file = chart_file.replace('outputs/', '', 1)
            
            html_content += f"""
                <a href="{chart_file}" class="chart-card">
                    <div class="chart-classroom">🏛️ {classroom}</div>
                    <div class="chart-courses">{courses}</div>
                    <div class="chart-students">👥 {num_students} students</div>
                </a>
"""
        
        html_content += """
            </div>
        </div>
"""
    
    # Calculate statistics
    total_charts = len(summary)
    total_classrooms = summary['Classroom'].nunique()
    total_sessions = len(grouped)
    total_students = summary['Total_Students'].sum()
    
    # Replace statistics placeholders
    html_content = html_content.replace('TOTAL_CHARTS_PLACEHOLDER', str(total_charts))
    html_content = html_content.replace('TOTAL_CLASSROOMS_PLACEHOLDER', str(total_classrooms))
    html_content = html_content.replace('TOTAL_SESSIONS_PLACEHOLDER', str(total_sessions))
    html_content = html_content.replace('TOTAL_STUDENTS_PLACEHOLDER', str(total_students))
    
    # Close HTML
    html_content += """
    </div>
</body>
</html>
"""
    
    # Write to file
    output_file = 'outputs/seating_charts_viewer.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Seating charts viewer generated: {output_file}")
    print(f"📊 Total charts: {total_charts}")
    print(f"🏛️ Classrooms: {total_classrooms}")
    print(f"📅 Sessions: {total_sessions}")
    print(f"👥 Total seats: {total_students}")

if __name__ == "__main__":
    print("🎓 Generating Seating Charts Viewer...")
    print("=" * 50)
    generate_seating_viewer()
    print("=" * 50)
    print("✅ Generation complete!")
