"""
Flask Backend Server for Timetable File Upload
Handles CSV file uploads and saves them to input_files folder
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)
# Enable CORS for Netlify frontend
CORS(app, origins=[
    'https://beyondgamesclasssync.netlify.app',
    'http://localhost:5000',
    'http://127.0.0.1:5000'
])

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'timetable_generator', 'input_files', 'sdtt_inputs')
ALLOWED_EXTENSIONS = {'csv'}
# Increase request max payload to 64MB to allow larger uploads
MAX_FILE_SIZE = 64 * 1024 * 1024  # 64MB
# Per-file maximum (32MB) to prevent a single file from consuming entire request
PER_FILE_MAX = 32 * 1024 * 1024  # 32MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"✅ Upload folder ready: {UPLOAD_FOLDER}")
except Exception as e:
    print(f"⚠️ Warning: Could not create upload folder: {e}")
    # Create a temporary uploads folder as fallback
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print(f"✅ Using fallback folder: {UPLOAD_FOLDER}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main index.html"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file upload - Expects 4 required files + 2 optional files + semester type"""
    try:
        # Get semester type (default to 'even' if not provided)
        semester_type = request.form.get('semester_type', 'even')
        print(f"📅 Semester Type: {semester_type}")
        
        # Check if all required files are present
        required_files = ['cse_file', 'ece_file', 'dsai_file', 'classroom_file']
        optional_files = ['electives_file', 'minors_file']
        
        missing_files = [f for f in required_files if f not in request.files]
        
        if missing_files:
            return jsonify({
                'success': False,
                'error': f'Missing required files: {", ".join(missing_files)}'
            }), 400
        
        # Create a new versioned folder to store this upload
        versions_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetable_generator', 'input_files', 'versions')
        os.makedirs(versions_root, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        version_dir = os.path.join(versions_root, timestamp)
        os.makedirs(version_dir, exist_ok=True)
        
        # Save semester type configuration to a file
        config_file = os.path.join(version_dir, 'config.json')
        with open(config_file, 'w') as f:
            json.dump({'semester_type': semester_type}, f)
        print(f"✅ Saved config: {config_file}")
        
        uploaded_files = []
        errors = []
        
        # File mappings: form field name -> saved filename
        file_mappings = {
            'cse_file': 'CSE.csv',
            'ece_file': 'ECE.csv',
            'dsai_file': 'DSAI.csv',
            'classroom_file': 'classrooms.csv',
            'electives_file': 'electives.csv',  # Optional
            'minors_file': 'minors.csv'  # Optional
        }
        
        for field_name, save_name in file_mappings.items():
            # Skip optional files if not provided
            if field_name in optional_files and field_name not in request.files:
                continue
            
            file = request.files.get(field_name)
            
            if not file or not file.filename:
                # Skip if optional file is empty
                if field_name in optional_files:
                    continue
                else:
                    errors.append(f'{field_name} - No file provided')
                    continue
            
            if file and file.filename and allowed_file(file.filename):
                # Save with standardized name
                filepath = os.path.join(version_dir, save_name)
                file.save(filepath)

                # Get file size
                file_size = os.path.getsize(filepath)

                # Enforce per-file size limit
                if file_size > PER_FILE_MAX:
                    try:
                        os.remove(filepath)
                    except Exception:
                        pass
                    errors.append(f'{file.filename} - File too large (>{PER_FILE_MAX//(1024*1024)}MB)')
                    continue
                
                uploaded_files.append({
                    'name': save_name,
                    'original_name': file.filename,
                    'size': file_size,
                    'path': filepath
                })
            else:
                # Only error for required files
                if field_name not in optional_files:
                    errors.append(f'{field_name} - Invalid file type (only CSV allowed)')
        
        # Success if we have at least the 4 required files
        required_count = sum(1 for f in uploaded_files if f['name'] in ['CSE.csv', 'ECE.csv', 'DSAI.csv', 'classrooms.csv'])
        if required_count == 4:
            return jsonify({
                'success': True,
                'message': f'Successfully uploaded {len(uploaded_files)} files to version {timestamp}',
                'files': uploaded_files,
                'version': timestamp
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to upload all required files',
                'uploaded': uploaded_files,
                'errors': errors
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/list-files', methods=['GET'])
def list_files():
    """List all CSV files in the upload folder"""
    try:
        files = []
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if filename.endswith('.csv'):
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    files.append({
                        'name': filename,
                        'size': os.path.getsize(filepath),
                        'modified': os.path.getmtime(filepath)
                    })
        
        return jsonify({
            'success': True,
            'files': files
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error listing files: {str(e)}'
        }), 500


@app.route('/api/list-versions', methods=['GET'])
def list_versions():
    """List all uploaded versions and whether outputs exist for them"""
    try:
        versions_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetable_generator', 'input_files', 'versions')
        versions = []
        if os.path.exists(versions_root):
            for name in os.listdir(versions_root):
                vpath = os.path.join(versions_root, name)
                if os.path.isdir(vpath):
                    # Count input files
                    inputs = [f for f in os.listdir(vpath) if f.endswith('.csv')]
                    # Check for generated CSV/HTML outputs
                    csv_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetable_outputs', name)
                    html_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetable_html', name)
                    index_exists = os.path.exists(os.path.join(html_out, 'index.html'))
                    versions.append({
                        'version': name,
                        'created': os.path.getmtime(vpath),
                        'input_count': len(inputs),
                        'csv_output_exists': os.path.exists(csv_out),
                        'html_output_exists': os.path.exists(html_out),
                        'index_path': (f'timetable_html/{name}/index.html' if index_exists else None)
                    })
        # Sort by version (timestamp) desc
        versions.sort(key=lambda x: x['version'], reverse=True)
        return jsonify({'success': True, 'versions': versions}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/list-generated', methods=['GET'])
def list_generated():
    """List all generated timetable versions (with HTML output)"""
    try:
        html_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetable_generator', 'timetable_html')
        versions = []
        
        if os.path.exists(html_root):
            for name in os.listdir(html_root):
                folder_path = os.path.join(html_root, name)
                # Only include timestamped folders (format: YYYYMMDD_HHMMSS)
                if os.path.isdir(folder_path) and len(name) == 15 and '_' in name:
                    index_path = os.path.join(folder_path, 'index.html')
                    if os.path.exists(index_path):
                        # Count HTML files in the folder
                        html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
                        
                        # Check for corresponding input files
                        input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                   'timetable_generator', 'input_files', 'versions', name)
                        file_count = 0
                        if os.path.exists(input_folder):
                            file_count = len([f for f in os.listdir(input_folder) if f.endswith('.csv')])
                        
                        versions.append({
                            'timestamp': name,
                            'html_count': len(html_files) - 1,  # Exclude index.html from count
                            'file_count': file_count,
                            'created': os.path.getmtime(folder_path)
                        })
        
        return jsonify({'success': True, 'versions': versions}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/delete-file', methods=['DELETE'])
def delete_file():
    """Delete a specific CSV file"""
    try:
        data = request.get_json()
        filename = secure_filename(data.get('filename', ''))
        
        if not filename:
            return jsonify({
                'success': False,
                'error': 'No filename provided'
            }), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({
                'success': True,
                'message': f'File {filename} deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error deleting file: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'upload_folder': app.config['UPLOAD_FOLDER'],
        'folder_exists': os.path.exists(app.config['UPLOAD_FOLDER'])
    }), 200

@app.route('/api/regenerate', methods=['POST'])
def regenerate_timetables():
    """Regenerate timetables from the most recent uploaded CSV files"""
    try:
        import subprocess
        import sys
        
        print("\n" + "="*80)
        print("🔄 REGENERATE REQUEST RECEIVED")
        print("="*80)
        
        # Find the most recent version folder
        versions_root = os.path.join(BASE_DIR, 'timetable_generator', 'input_files', 'versions')
        print(f"📁 Versions root: {versions_root}")
        print(f"✓ Exists: {os.path.exists(versions_root)}")
        
        if not os.path.exists(versions_root):
            print("❌ Versions folder not found!")
            return jsonify({
                'success': False,
                'error': 'No uploaded files found. Please upload CSV files first.'
            }), 404
        
        versions = [d for d in os.listdir(versions_root) if os.path.isdir(os.path.join(versions_root, d))]
        print(f"📂 Found {len(versions)} versions: {versions}")
        
        if not versions:
            print("❌ No version folders found!")
            return jsonify({
                'success': False,
                'error': 'No uploaded files found. Please upload CSV files first.'
            }), 404
        
        # Get the latest version (sorted by timestamp)
        latest_version = sorted(versions, reverse=True)[0]
        print(f"🎯 Using latest version: {latest_version}")
        
        # Load semester type configuration
        config_file = os.path.join(versions_root, latest_version, 'config.json')
        semester_type = 'even'  # Default
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    semester_type = config.get('semester_type', 'even')
                print(f"📅 Loaded semester type: {semester_type}")
            except Exception as e:
                print(f"⚠️  Could not load config, using default: {e}")
        
        # Path to main.py
        tg_dir = os.path.join(BASE_DIR, 'timetable_generator')
        main_script = os.path.join(tg_dir, 'main.py')
        print(f"📜 Main script: {main_script}")
        print(f"✓ Exists: {os.path.exists(main_script)}")
        
        if not os.path.exists(main_script):
            print("❌ main.py not found!")
            return jsonify({
                'success': False,
                'error': 'main.py not found'
            }), 404
        
        # Set up environment variables for the timetable generator
        env = os.environ.copy()
        env['CSV_INPUT_FOLDER'] = os.path.join('input_files', 'versions', latest_version)
        env['OUTPUT_CSV_DIR'] = os.path.join('timetable_outputs', latest_version)
        env['OUTPUT_HTML_DIR'] = os.path.join('timetable_html', latest_version)
        env['SEMESTER_TYPE'] = semester_type  # Pass semester type to main.py
        
        print(f"🔧 Environment variables:")
        print(f"   CSV_INPUT_FOLDER: {env['CSV_INPUT_FOLDER']}")
        print(f"   OUTPUT_CSV_DIR: {env['OUTPUT_CSV_DIR']}")
        print(f"   OUTPUT_HTML_DIR: {env['OUTPUT_HTML_DIR']}")
        print(f"   SEMESTER_TYPE: {env['SEMESTER_TYPE']}")
        print(f"\n🚀 Running main.py...")
        
        # Run the timetable generation script with UTF-8 encoding
        result = subprocess.run(
            [sys.executable, main_script],
            cwd=tg_dir,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace encoding errors instead of failing
            env=env,
            timeout=600  # 10 minutes timeout
        )
        
        print(f"✅ Main.py exit code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Timetable generation successful!")
            print(f"\n📄 Output (first 500 chars):\n{result.stdout[:500]}")
            
            # Generate HTML from CSV outputs
            html_script = os.path.join(tg_dir, 'timetable_to_html.py')
            env2 = env.copy()
            env2['INPUT_CSV_DIR'] = env['OUTPUT_CSV_DIR']
            env2['OUTPUT_HTML_DIR'] = env['OUTPUT_HTML_DIR']
            env2['CSV_INPUT_FOLDER'] = env['CSV_INPUT_FOLDER']  # Pass original CSV folder for course data
            
            print(f"\n🎨 Running timetable_to_html.py...")
            print(f"   INPUT_CSV_DIR: {env2['INPUT_CSV_DIR']}")
            print(f"   OUTPUT_HTML_DIR: {env2['OUTPUT_HTML_DIR']}")
            print(f"   CSV_INPUT_FOLDER: {env2['CSV_INPUT_FOLDER']}")
            
            html_result = subprocess.run(
                [sys.executable, html_script],
                cwd=tg_dir,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',  # Replace encoding errors instead of failing
                env=env2,
                timeout=300
            )
            
            print(f"✅ HTML generation exit code: {html_result.returncode}")
            if html_result.stdout:
                print(f"📄 HTML Output:\n{html_result.stdout}")
            if html_result.stderr:
                print(f"⚠️  HTML Errors:\n{html_result.stderr}")
            
            # Build index URL
            web_path = f'timetable_html/{latest_version}/index.html'
            index_url = request.host_url.rstrip('/') + '/' + web_path
            
            print(f"🌐 Timetable URL: {index_url}")
            print("="*80 + "\n")
            
            return jsonify({
                'success': True,
                'message': f'Timetables generated successfully for version {latest_version}!',
                'version': latest_version,
                'index_url': index_url,
                'output': result.stdout
            }), 200
        else:
            print(f"❌ Timetable generation FAILED!")
            print(f"📄 STDOUT:\n{result.stdout}")
            print(f"⚠️  STDERR:\n{result.stderr}")
            print("="*80 + "\n")
            
            return jsonify({
                'success': False,
                'error': 'Timetable generation failed',
                'details': result.stderr,
                'stdout': result.stdout
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Timetable generation timed out (>10 minutes)'
        }), 500
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Regenerate failed: {str(e)}")
        print(error_trace)
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}',
            'traceback': error_trace
        }), 500

@app.route('/api/list-generated', methods=['GET'])
def list_generated_timetables():
    """List all generated timetable versions with their files"""
    try:
        tg_dir = os.path.join(BASE_DIR, 'timetable_generator')
        html_dir = os.path.join(BASE_DIR, 'timetable_html')
        csv_dir = os.path.join(BASE_DIR, 'timetable_outputs')
        
        versions = []
        
        # Get all HTML version folders
        if os.path.exists(html_dir):
            for version in sorted(os.listdir(html_dir), reverse=True):
                version_path = os.path.join(html_dir, version)
                if os.path.isdir(version_path):
                    # Check if index.html exists
                    index_path = os.path.join(version_path, 'index.html')
                    has_html = os.path.exists(index_path)
                    
                    # Check if CSV outputs exist
                    csv_version_path = os.path.join(csv_dir, version)
                    has_csv = os.path.exists(csv_version_path) and os.path.isdir(csv_version_path)
                    
                    # Count CSV files
                    csv_count = 0
                    if has_csv:
                        csv_count = len([f for f in os.listdir(csv_version_path) if f.endswith('.csv')])
                    
                    # Parse timestamp for display
                    try:
                        from datetime import datetime
                        dt = datetime.strptime(version, '%Y%m%d_%H%M%S')
                        display_time = dt.strftime('%B %d, %Y at %I:%M:%S %p')
                    except:
                        display_time = version
                    
                    versions.append({
                        'version': version,
                        'display_time': display_time,
                        'has_html': has_html,
                        'has_csv': has_csv,
                        'csv_count': csv_count,
                        'html_url': f'/timetable_html/{version}/index.html' if has_html else None,
                        'csv_folder': f'/timetable_outputs/{version}/' if has_csv else None
                    })
        
        return jsonify({
            'success': True,
            'versions': versions
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error listing versions: {str(e)}'
        }), 500

@app.route('/timetable_outputs/<path:path>')
def serve_csv_outputs(path):
    """Serve CSV output files with directory listing"""
    csv_dir = os.path.join(BASE_DIR, 'timetable_outputs')
    full_path = os.path.join(csv_dir, path)
    
    # If it's a directory, return a simple HTML listing
    if os.path.isdir(full_path):
        files = []
        for item in sorted(os.listdir(full_path)):
            item_path = os.path.join(full_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append({
                    'name': item,
                    'size': size,
                    'url': f'/timetable_outputs/{path}/{item}' if path else f'/timetable_outputs/{item}'
                })
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>CSV Files - {path or 'Root'}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #667eea; padding-bottom: 15px; }}
        .file-list {{ list-style: none; padding: 0; }}
        .file-item {{ padding: 15px; margin: 10px 0; background: #f8f9fa; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }}
        .file-item:hover {{ background: #e9ecef; }}
        .file-name {{ font-weight: 600; color: #495057; }}
        .file-size {{ color: #6c757d; font-size: 0.9em; }}
        .download-btn {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px 20px; border-radius: 6px; text-decoration: none; font-weight: 600; }}
        .download-btn:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 CSV Files - {path or 'All Versions'}</h1>
        <ul class="file-list">
'''
        for file in files:
            html += f'''
            <li class="file-item">
                <div>
                    <div class="file-name">📄 {file['name']}</div>
                    <div class="file-size">{file['size']:,} bytes</div>
                </div>
                <a href="{file['url']}" class="download-btn" download>⬇ Download</a>
            </li>
'''
        html += '''
        </ul>
    </div>
</body>
</html>
'''
        return html
    
    # Otherwise serve the file
    return send_from_directory(csv_dir, path)

@app.route('/timetable_html/<path:path>')
def serve_html_outputs(path):
    """Serve HTML timetable files"""
    html_dir = os.path.join(BASE_DIR, 'timetable_generator', 'timetable_html')
    return send_from_directory(html_dir, path)

@app.route('/api/download_excel/<timestamp>')
def download_excel(timestamp):
    """Generate and download Excel file with all timetables"""
    try:
        from timetable_generator.export_to_excel import TimetableExcelExporter
        from flask import send_file
        
        print(f"\n📊 Excel download requested for timestamp: {timestamp}")
        
        # Set input directory to the specific timestamp folder
        output_dir = os.path.join(BASE_DIR, 'timetable_generator', 'timetable_outputs', timestamp)
        
        if not os.path.exists(output_dir):
            print(f"❌ Output directory not found: {output_dir}")
            return jsonify({
                'success': False,
                'error': f'Timetables for {timestamp} not found'
            }), 404
        
        # Create exporter and generate Excel
        exporter = TimetableExcelExporter(input_dir=output_dir)
        excel_file = exporter.export_to_excel(output_file='All_Timetables.xlsx')
        
        if not excel_file or not os.path.exists(excel_file):
            print(f"❌ Failed to create Excel file")
            return jsonify({
                'success': False,
                'error': 'Failed to generate Excel file'
            }), 500
        
        print(f"✅ Sending Excel file: {excel_file}")
        
        # Send the file
        return send_file(
            excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'Timetables_{timestamp}.xlsx'
        )
    
    except Exception as e:
        print(f"❌ Error generating Excel: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500

@app.route('/api/download_single_excel/<timestamp>/<filename>')
def download_single_excel(timestamp, filename):
    """Download a single timetable as Excel"""
    try:
        from timetable_generator.export_to_excel import TimetableExcelExporter
        
        # Construct paths
        output_dir = os.path.join('timetable_generator', 'timetable_outputs', timestamp)
        
        if not os.path.exists(output_dir):
            return jsonify({
                'success': False,
                'error': 'Timetable folder not found'
            }), 404
        
        # Check if CSV file exists
        csv_filename = f"{filename}.csv"
        csv_path = os.path.join(output_dir, csv_filename)
        
        if not os.path.exists(csv_path):
            return jsonify({
                'success': False,
                'error': f'CSV file not found: {csv_filename}'
            }), 404
        
        # Create exporter and generate Excel for single timetable
        exporter = TimetableExcelExporter(input_dir=output_dir)
        excel_file = exporter.export_single_timetable(csv_filename, output_filename=f'{filename}.xlsx')
        
        if not excel_file or not os.path.exists(excel_file):
            return jsonify({
                'success': False,
                'error': 'Failed to generate Excel file'
            }), 500
        
        print(f"✅ Sending Excel file: {excel_file}")
        
        # Send the file
        return send_file(
            excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'{filename}.xlsx'
        )
    
    except Exception as e:
        print(f"❌ Error generating single Excel: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 Timetable Upload Server Starting...")
    print("="*80)
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"✅ Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    print(f"📊 Max file size: {MAX_FILE_SIZE / (1024*1024)}MB")
    print("\n🌐 Server running at: http://localhost:5000")
    print("📤 Upload page: http://localhost:5000/upload.html")
    print("\n⚠️  IMPORTANT: Access via http://localhost:5000/upload.html")
    print("   Do NOT open upload.html directly from file explorer!")
    print("\nPress Ctrl+C to stop the server")
    print("="*80 + "\n")
    
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=True,
        threaded=True
    )
