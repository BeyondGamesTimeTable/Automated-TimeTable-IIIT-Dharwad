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
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetable_generator', 'input_files', 'sdtt_inputs')
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
    """Handle file upload - Deletes old files before uploading new ones"""
    try:
        # Check if files were sent
        if 'files[]' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided'
            }), 400
        
        files = request.files.getlist('files[]')
        
        if not files or files[0].filename == '':
            return jsonify({
                'success': False,
                'error': 'No files selected'
            }), 400
        
        # Instead of deleting old files, create a new versioned folder to store this upload
        # This preserves existing inputs and generated timetables.
        versions_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetable_generator', 'input_files', 'versions')
        os.makedirs(versions_root, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        version_dir = os.path.join(versions_root, timestamp)
        os.makedirs(version_dir, exist_ok=True)
        deleted_count = 0
        
        uploaded_files = []
        errors = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                
                # Save the file into the new version folder
                filepath = os.path.join(version_dir, filename)
                file.save(filepath)

                # Get file size
                file_size = os.path.getsize(filepath)

                # Enforce per-file size limit; if exceeded, remove saved file and record error
                if file_size > PER_FILE_MAX:
                    try:
                        os.remove(filepath)
                    except Exception:
                        pass
                    errors.append(f'{filename} - File too large (>{PER_FILE_MAX//(1024*1024)}MB)')
                    continue
                
                uploaded_files.append({
                    'name': filename,
                    'size': file_size,
                    'path': filepath
                })
            else:
                errors.append(f'{file.filename} - Invalid file type (only CSV allowed)')
        
        if uploaded_files:
            # After successful upload, trigger regeneration using the uploaded version folder.
            try:
                import subprocess, sys
                # Run main.py in timetable_generator using the uploaded CSV folder
                tg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetable_generator')
                main_script = os.path.join(tg_dir, 'main.py')

                env = os.environ.copy()
                # CSV input folder relative to timetable_generator (used by main)
                env['CSV_INPUT_FOLDER'] = os.path.join('input_files', 'versions', timestamp)
                # Output folders (place per-run outputs under timestamped dirs)
                env['OUTPUT_CSV_DIR'] = os.path.join('..', 'timetable_outputs', timestamp)
                env['OUTPUT_HTML_DIR'] = os.path.join('..', 'timetable_html', timestamp)

                # Run the timetable generator
                result = subprocess.run([
                    sys.executable, main_script
                ], cwd=tg_dir, capture_output=True, text=True, env=env, timeout=600)

                if result.returncode != 0:
                    # Generation failed; return upload success but generation error
                    return jsonify({
                        'success': True,
                        'message': f'Uploaded {len(uploaded_files)} new file(s) into version {timestamp}',
                        'files': uploaded_files,
                        'version': timestamp,
                        'regenerate': False,
                        'error': result.stderr,
                        'generator_stdout': result.stdout
                    }), 200

                # Convert CSVs to HTML using timetable_to_html.py and the output folders
                html_script = os.path.join(tg_dir, 'timetable_to_html.py')
                env2 = env.copy()
                # input csv dir for html converter is the CSV output dir we set above (relative to tg_dir)
                env2['INPUT_CSV_DIR'] = env['OUTPUT_CSV_DIR']
                env2['OUTPUT_HTML_DIR'] = env['OUTPUT_HTML_DIR']

                html_result = subprocess.run([
                    sys.executable, html_script
                ], cwd=tg_dir, capture_output=True, text=True, env=env2, timeout=300)

                if html_result.returncode != 0:
                    return jsonify({
                        'success': True,
                        'message': f'Uploaded {len(uploaded_files)} new file(s) into version {timestamp}; CSVs generated but HTML conversion failed',
                        'files': uploaded_files,
                        'version': timestamp,
                        'regenerate': True,
                        'html_error': html_result.stderr
                    }), 200

                # Success: return links to the new HTML index
                # Construct web path (remove leading .. so it's relative to repo root)
                web_path = os.path.normpath(os.path.join(env2['OUTPUT_HTML_DIR'], 'index.html'))
                # If it starts with ..\ remove the parent reference
                parent_prefix = '..' + os.sep
                if web_path.startswith(parent_prefix):
                    web_path = web_path[len(parent_prefix):]
                web_path = web_path.replace('\\', '/')

                return jsonify({
                    'success': True,
                    'message': f'Uploaded {len(uploaded_files)} new file(s) into version {timestamp}; timetables regenerated',
                    'files': uploaded_files,
                    'version': timestamp,
                    'regenerate': True,
                    'index_url': request.host_url.rstrip('/') + '/' + web_path
                }), 200
            except Exception as e:
                return jsonify({
                    'success': True,
                    'message': f'Uploaded {len(uploaded_files)} new file(s) into version {timestamp}',
                    'files': uploaded_files,
                    'version': timestamp,
                    'regenerate': False,
                    'error': str(e)
                }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No valid CSV files uploaded',
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
    """Regenerate timetables from uploaded CSV files"""
    try:
        import subprocess
        import sys
        
        # Path to main.py
        main_script = os.path.join(os.path.dirname(__file__), 'timetable_generator', 'main.py')
        
        if not os.path.exists(main_script):
            return jsonify({
                'success': False,
                'error': 'main.py not found'
            }), 404
        
        # Run the timetable generation script
        result = subprocess.run(
            [sys.executable, main_script],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Timetables regenerated successfully!',
                'output': result.stdout
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Timetable generation failed',
                'details': result.stderr
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Timetable generation timed out (>5 minutes)'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error regenerating timetables: {str(e)}'
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
    print("\nPress Ctrl+C to stop the server")
    print("="*80 + "\n")
    
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=True,
        threaded=True
    )
