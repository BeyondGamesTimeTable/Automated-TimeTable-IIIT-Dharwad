# 🌐 Web App Deployment Guide

## Your Timetable System is Ready for Web Deployment!

All HTML files are connected with proper navigation and can be deployed as a web app immediately.

---

## 🚀 Quick Deployment Options (FREE)

### Option 1: **GitHub Pages** (Recommended - Free & Fast)

**Perfect for:** Public websites, no server needed

**Steps:**

1. **Push to GitHub** (if not already done):
```powershell
cd "c:\Users\goura\OneDrive\Documents\Third semester\Software Design Tools and Techniques\Automatic Timetable Final\Automated-Time-Table-IIIT-DHARWAD"
git add .
git commit -m "Ready for GitHub Pages deployment"
git push origin main
```

2. **Enable GitHub Pages**:
   - Go to: https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad
   - Click **Settings** → **Pages**
   - Source: Deploy from branch
   - Branch: `main` / `root`
   - Click **Save**

3. **Your Website URL**:
   ```
   https://beyondgamestimetable.github.io/Automated-TimeTable-IIIT-Dharwad/
   ```
   - Main page: `https://beyondgamestimetable.github.io/Automated-TimeTable-IIIT-Dharwad/index.html`
   - Will be live in 2-5 minutes!

---

### Option 2: **Netlify** (Drag & Drop - Instant)

**Perfect for:** Quick deployment with custom domain support

**Steps:**

1. **Go to Netlify**: https://www.netlify.com
2. **Sign up** (free account)
3. **Drag & Drop** your entire project folder
4. **Done!** Get instant URL like: `https://iiit-dharwad-timetable.netlify.app`

**OR via CLI**:
```powershell
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd "c:\Users\goura\OneDrive\Documents\Third semester\Software Design Tools and Techniques\Automatic Timetable Final\Automated-Time-Table-IIIT-DHARWAD"
netlify deploy --prod
```

---

### Option 3: **Vercel** (GitHub Integration)

**Perfect for:** Automatic deployments on every git push

**Steps:**

1. **Go to Vercel**: https://vercel.com
2. **Sign up** with GitHub
3. **Import Repository**: `BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad`
4. **Deploy!** 
   - Auto-deploys on every push
   - Custom domain support
   - URL: `https://iiit-dharwad-timetable.vercel.app`

---

### Option 4: **Firebase Hosting** (Google)

**Perfect for:** Scalable hosting with analytics

**Steps:**

```powershell
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
cd "c:\Users\goura\OneDrive\Documents\Third semester\Software Design Tools and Techniques\Automatic Timetable Final\Automated-Time-Table-IIIT-DHARWAD"
firebase init hosting

# Deploy
firebase deploy
```

---

### Option 5: **Render** (Free Static Site)

**Steps:**

1. Go to: https://render.com
2. New → Static Site
3. Connect GitHub repo
4. Deploy!
5. URL: `https://iiit-dharwad-timetable.onrender.com`

---

## 🎯 Recommended: GitHub Pages (Easiest)

Since your code is already on GitHub, just enable GitHub Pages:

### Quick Setup:

1. **Go to your repository**:
   ```
   https://github.com/BeyondGamesTimeTable/Automated-TimeTable-IIIT-Dharwad
   ```

2. **Settings → Pages**:
   - Branch: `main`
   - Folder: `/ (root)`
   - Save

3. **Done!** Your site will be live at:
   ```
   https://beyondgamestimetable.github.io/Automated-TimeTable-IIIT-Dharwad/
   ```

---

## 📱 Custom Domain (Optional)

After deploying, you can add a custom domain:

### For GitHub Pages:
1. Buy domain (e.g., `iiitdharwad-timetable.com`)
2. Add CNAME record pointing to: `beyondgamestimetable.github.io`
3. Add custom domain in GitHub Settings → Pages

### For Netlify/Vercel:
- Free SSL certificate included
- Add custom domain in dashboard
- Automatic HTTPS

---

## 🔒 Access Control (If Needed)

If you need password protection:

### Option 1: Netlify (Free Plan)
- Supports password protection
- Settings → Access Control

### Option 2: Add Simple Auth
Create `auth.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <script>
        const password = prompt("Enter password:");
        if (password === "iiitdharwad2025") {
            window.location.href = "index.html";
        } else {
            alert("Wrong password!");
            window.location.href = "auth.html";
        }
    </script>
</body>
</html>
```

---

## ✅ Pre-Deployment Checklist

Your project is ready! ✓
- [x] All HTML files connected with navigation
- [x] Relative paths (no absolute URLs)
- [x] Mobile-responsive design
- [x] No external dependencies
- [x] Offline-capable
- [x] 12 daily timetables + exam timetable + 324 seating charts

---

## 🚀 Deploy Now (Fastest Method)

**30-Second Deployment**:

1. Open: https://app.netlify.com/drop
2. Drag your project folder
3. Done! Get instant URL
4. Share with students!

---

## 📊 After Deployment

Your web app will have:
- **Main Menu**: https://your-url.com/
- **Daily Timetables**: https://your-url.com/timetable_generator/timetable_html/
- **Exam Schedule**: https://your-url.com/exam_timetable/outputs/exam_timetable.html
- **Seating Charts**: https://your-url.com/exam_timetable/outputs/seating_charts_viewer.html

Share the main URL with students!

---

## 🎓 Usage

Students can:
1. Open URL on any device (phone, tablet, laptop)
2. Navigate between daily & exam timetables
3. Download CSV files
4. View seating arrangements
5. Bookmark their timetable page

---

## 🔄 Updates

To update content:
1. Regenerate timetables: `py main.py`
2. Convert to HTML: `py timetable_to_html.py`
3. Push to GitHub: `git push`
4. **GitHub Pages auto-updates!**

---

## 🆘 Need Help?

Choose deployment method based on:
- **Easiest**: GitHub Pages (already on GitHub)
- **Fastest**: Netlify Drop (drag & drop)
- **Most Features**: Vercel (auto-deploys + analytics)
- **Custom Domain**: Any of above (all support it)

**Recommended**: Use GitHub Pages since you're already using GitHub!
