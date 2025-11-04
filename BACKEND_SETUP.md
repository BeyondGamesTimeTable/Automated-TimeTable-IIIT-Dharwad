# 🚀 Backend Server Setup & Usage Guide

## ✅ What Was Added

I've created a complete Flask backend server for file uploads with:

### **Backend Features:**
- ✅ File upload API (`/api/upload`)
- ✅ File listing API (`/api/list-files`)
- ✅ File deletion API (`/api/delete-file`)
- ✅ Health check endpoint (`/api/health`)
- ✅ CORS enabled for cross-origin requests
- ✅ File validation (CSV only)
- ✅ Secure filename handling
- ✅ Error handling & logging

### **Frontend Updates:**
- ✅ Real API integration (no more simulation)
- ✅ Server status checking
- ✅ Real-time upload progress
- ✅ Success/error notifications
- ✅ Automatic file management

---

## 📋 Installation Steps

### **1. Install Required Packages**

```powershell
# Navigate to project directory
cd "c:\Users\goura\OneDrive\Documents\Third semester\Software Design Tools and Techniques\Automatic Timetable Final\Automated-Time-Table-IIIT-DHARWAD"

# Install Flask and dependencies
pip install -r requirements.txt
```

Or install manually:
```powershell
pip install Flask flask-cors Werkzeug
```

---

## 🚀 Starting the Server

### **Method 1: Run Directly**

```powershell
# Start the upload server
py upload_server.py
```

### **Method 2: PowerShell Script**

Create `start_server.ps1`:
```powershell
Write-Host "Starting Timetable Upload Server..." -ForegroundColor Green
py upload_server.py
```

Run it:
```powershell
.\start_server.ps1
```

---

## 📤 Using the Upload Feature

### **Step 1: Start the Server**
```powershell
py upload_server.py
```

You should see:
```
🚀 Timetable Upload Server Starting...
================================================================================
📁 Upload folder: timetable_generator\input_files\sdtt_inputs
✅ Allowed file types: csv
📊 Max file size: 16.0MB

🌐 Server running at: http://localhost:5000
📤 Upload page: http://localhost:5000/upload.html

Press Ctrl+C to stop the server
================================================================================
```

### **Step 2: Open Upload Page**

Open your browser and go to:
```
http://localhost:5000/upload.html
```

Or open the local file directly:
```
file:///c:/Users/goura/.../upload.html
```

### **Step 3: Upload Files**

1. **Drag & Drop**: Drag CSV files into the drop zone
2. **Browse**: Click "Browse Files" to select files
3. **Review**: Check selected files
4. **Upload**: Click "🚀 Upload Files"
5. **Success**: Files are saved to `timetable_generator/input_files/sdtt_inputs/`

---

## 🔌 API Endpoints

### **1. Upload Files**
```
POST /api/upload
Content-Type: multipart/form-data
Body: files[] = [file1.csv, file2.csv, ...]

Response:
{
  "success": true,
  "message": "Successfully uploaded 2 file(s)",
  "files": [
    {"name": "Even CSE.csv", "size": 12345, "path": "..."},
    {"name": "Even DSAI.csv", "size": 12345, "path": "..."}
  ]
}
```

### **2. List Files**
```
GET /api/list-files

Response:
{
  "success": true,
  "files": [
    {"name": "Even CSE.csv", "size": 12345, "modified": 1234567890},
    {"name": "Even DSAI.csv", "size": 12345, "modified": 1234567890}
  ]
}
```

### **3. Delete File**
```
DELETE /api/delete-file
Content-Type: application/json
Body: {"filename": "Even CSE.csv"}

Response:
{
  "success": true,
  "message": "File Even CSE.csv deleted successfully"
}
```

### **4. Health Check**
```
GET /api/health

Response:
{
  "status": "healthy",
  "upload_folder": "...",
  "folder_exists": true
}
```

---

## 🔒 Security Features

- ✅ **Secure Filenames**: Using `secure_filename()` to prevent directory traversal
- ✅ **File Type Validation**: Only CSV files allowed
- ✅ **Size Limits**: 16MB maximum file size
- ✅ **CORS Protection**: Configurable cross-origin access
- ✅ **Error Handling**: Proper error messages and status codes

---

## 🌐 For Web Deployment (GitHub Pages + Backend)

Since GitHub Pages only serves static files, you have two options:

### **Option 1: Separate Backend (Recommended)**

1. **Deploy Backend to Heroku/Railway/Render**:
   - Push `upload_server.py` to a separate repo
   - Deploy as Python Flask app
   - Get backend URL: `https://your-backend.herokuapp.com`

2. **Update Frontend**:
   - Change `http://localhost:5000` to your backend URL in `upload.html`

3. **Deploy Frontend to GitHub Pages**:
   - Push to GitHub
   - Enable GitHub Pages
   - Frontend: `https://beyondgamestimetable.github.io/...`
   - Backend: `https://your-backend.herokuapp.com`

### **Option 2: Full Stack Hosting**

Deploy everything together on:
- **Heroku**: Free tier (with limits)
- **Railway**: Free tier (with limits)
- **Render**: Free tier
- **PythonAnywhere**: Free tier

---

## 📝 Configuration

Edit `upload_server.py` to customize:

```python
# Upload folder location
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'timetable_generator', 'input_files', 'sdtt_inputs')

# Allowed file types
ALLOWED_EXTENSIONS = {'csv'}

# Maximum file size (16MB)
MAX_FILE_SIZE = 16 * 1024 * 1024

# Server port
port=5000

# Allow external connections
host='0.0.0.0'  # or '127.0.0.1' for local only
```

---

## 🐛 Troubleshooting

### **Server won't start**
```powershell
# Check if Flask is installed
pip list | Select-String flask

# Install if missing
pip install Flask flask-cors
```

### **Upload fails**
1. Check if server is running: `http://localhost:5000/api/health`
2. Check upload folder exists: `timetable_generator/input_files/sdtt_inputs/`
3. Check file is CSV format
4. Check file size < 16MB

### **CORS errors**
- Make sure `flask-cors` is installed
- Check CORS is enabled in `upload_server.py`

### **Permission errors**
- Run as administrator (if folder is protected)
- Check folder write permissions

---

## 🎯 Quick Start Commands

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start server
py upload_server.py

# 3. Open browser
Start-Process http://localhost:5000/upload.html

# 4. Upload files via drag & drop or browse

# 5. Generate timetables
cd timetable_generator
py main.py
```

---

## ✅ Complete Workflow

1. **Start backend**: `py upload_server.py`
2. **Upload CSV files**: Go to `http://localhost:5000/upload.html`
3. **Generate timetables**: `cd timetable_generator && py main.py`
4. **Convert to HTML**: `py timetable_to_html.py`
5. **View results**: Open `timetable_html/index.html`

---

## 📦 Files Added

- `upload_server.py` - Flask backend server
- `requirements.txt` - Python dependencies
- `upload.html` - Updated with backend integration
- `BACKEND_SETUP.md` - This documentation

---

## 🚀 Production Deployment

For production, use a proper WSGI server:

```powershell
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 upload_server:app
```

---

## 💡 Tips

- Keep server running while uploading files
- Files are automatically saved to correct folder
- No need to manually copy files anymore
- Server creates upload folder if it doesn't exist
- Check server logs for debugging

---

**Your backend is ready! Start the server and try uploading files!** 🎉
