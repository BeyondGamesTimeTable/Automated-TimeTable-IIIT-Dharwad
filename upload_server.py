"""
Flask Backend Server for Timetable File Upload
Handles CSV file uploads and saves them to input_files folder
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
# Enable CORS for Netlify frontend
CORS(app, origins=[
    'https://beyondgamesclasssync.netlify.app',
    'http://localhost:5000',
    'http://127.0.0.1:5000'
])

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'timetable_generator', 'input_files', 'sdtt_inputs')
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    """Handle file upload"""
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
        
        uploaded_files = []
        errors = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                
                # Save the file
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Get file size
                file_size = os.path.getsize(filepath)
                
                uploaded_files.append({
                    'name': filename,
                    'size': file_size,
                    'path': filepath
                })
            else:
                errors.append(f'{file.filename} - Invalid file type (only CSV allowed)')
        
        if uploaded_files:
            return jsonify({
                'success': True,
                'message': f'Successfully uploaded {len(uploaded_files)} file(s)',
                'files': uploaded_files,
                'errors': errors if errors else None
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
