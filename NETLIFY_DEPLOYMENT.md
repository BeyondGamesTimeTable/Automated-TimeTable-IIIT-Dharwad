# 🌐 Connecting Netlify Frontend with Backend

## ✅ Current Setup

**Frontend (Netlify)**: https://beyondgamesclasssync.netlify.app/
**Backend**: Needs to be deployed

## 🚀 Quick Deploy Backend to Render

### **Step 1: Deploy Backend to Render (FREE)**

1. **Go to Render**: https://render.com
2. **Sign up** with GitHub
3. **New → Web Service**
4. **Connect Repository**: `BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad`
5. **Configure**:
   - **Name**: `iiit-timetable-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn upload_server:app`
   - **Plan**: `Free`
6. **Create Web Service**

Your backend URL will be: `https://iiit-timetable-backend.onrender.com`

---

### **Step 2: Update Frontend to Use Backend**

Update `upload.html` line 536 and 552:

**Change from:**
```javascript
const response = await fetch('http://localhost:5000/api/upload', {
```

**Change to:**
```javascript
const response = await fetch('https://iiit-timetable-backend.onrender.com/api/upload', {
```

And line 552:
```javascript
const response = await fetch('https://iiit-timetable-backend.onrender.com/api/health');
```

---

### **Step 3: Update Backend CORS**

Your `upload_server.py` already has CORS enabled, but make sure it allows your Netlify domain:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://beyondgamesclasssync.netlify.app'])
```

---

### **Step 4: Push Changes**

```powershell
cd "c:\Users\goura\OneDrive\Documents\Third semester\Software Design Tools and Techniques\Automatic Timetable Final\Automated-Time-Table-IIIT-DHARWAD"

git add .
git commit -m "Updated for production deployment with Render backend"
git push origin main
```

---

## 🔧 Alternative: Deploy to Railway

1. **Go to Railway**: https://railway.app
2. **Sign in with GitHub**
3. **New Project → Deploy from GitHub**
4. **Select**: `Automated-TimeTable-IIIT-Dharwad`
5. **Add Variables**:
   - `PYTHON_VERSION`: `3.12`
6. **Deploy!**

Backend URL: `https://your-app.up.railway.app`

---

## 🎯 Simplified Deployment (Both Options Work!)

### **For Render:**

```powershell
# 1. Create account at render.com
# 2. Connect GitHub repo
# 3. Deploy with auto-detected settings
# 4. Copy backend URL
# 5. Update upload.html with backend URL
# 6. Push to GitHub → Netlify auto-updates
```

### **For Railway:**

```powershell
# 1. Create account at railway.app
# 2. New project from GitHub
# 3. Auto-detects Python/Flask
# 4. Copy backend URL
# 5. Update upload.html with backend URL
# 6. Push to GitHub → Netlify auto-updates
```

---

## 📝 Environment Variables (If Needed)

For production backend, set these in Render/Railway:

```
FLASK_ENV=production
MAX_FILE_SIZE=16777216
UPLOAD_FOLDER=/app/uploads
```

---

## 🔒 Security Note

For production, add authentication:

```python
# In upload_server.py, add basic auth
from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != 'your-secret-key-here':
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/upload', methods=['POST'])
@require_api_key
def upload_files():
    # ... existing code
```

---

## ✅ Complete Deployment Checklist

- [x] Frontend deployed to Netlify: https://beyondgamesclasssync.netlify.app/
- [ ] Backend deployed to Render/Railway
- [ ] Updated upload.html with backend URL
- [ ] Updated CORS settings in backend
- [ ] Pushed changes to GitHub
- [ ] Tested upload functionality
- [ ] Verified files are saved

---

## 🧪 Testing After Deployment

1. Go to: https://beyondgamesclasssync.netlify.app/upload.html
2. Check for "Server Connected!" green banner
3. Upload a CSV file
4. Verify success message
5. Check backend logs on Render/Railway

---

## 📊 Your Final Architecture

```
[User Browser]
     ↓
[Netlify - Static Frontend]
  https://beyondgamesclasssync.netlify.app/
     ↓ (API Calls)
[Render/Railway - Backend]
  https://iiit-timetable-backend.onrender.com/
     ↓
[File Storage]
  Backend server storage
```

---

## 🆘 Quick Fix Commands

```powershell
# Update backend URL in frontend
# Edit upload.html lines 536, 552
# Replace: http://localhost:5000
# With: https://your-backend-url.onrender.com

# Commit and push
git add upload.html
git commit -m "Updated backend URL for production"
git push origin main

# Netlify auto-deploys in 2 minutes
```

---

**Which backend platform would you like to use? Render or Railway?**
Both are free and work great! Let me know and I'll guide you through the setup.
