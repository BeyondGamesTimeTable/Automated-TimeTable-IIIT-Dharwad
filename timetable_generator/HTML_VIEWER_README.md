# 🌐 BeyondGames Timetable HTML Viewer

## 🎉 Beautiful Interactive Timetable Viewer

Your timetables are now available as beautiful, interactive HTML pages!

---

## 🚀 **How to Use**

### **Option 1: Direct Browser Access**
1. Navigate to `timetable_html/` folder
2. Open `index.html` in any web browser
3. Select your department, semester, and section
4. View your beautiful timetable!

### **Option 2: Quick Launch**
```bash
cd timetable_generator
start timetable_html\index.html
```

---

## 📁 **Generated Files**

### **Main Index Page**
- **`index.html`** - Main selection page with all timetables

### **Individual Timetable Pages** (18 HTML files)
```
CSE_Sem2_SectionA_Timetable.html
CSE_Sem2_SectionB_Timetable.html
CSE_Sem4_SectionA_Timetable.html
CSE_Sem4_SectionB_Timetable.html
CSE_Sem6_SectionA_Timetable.html
CSE_Sem6_SectionB_Timetable.html
DSAI_Sem2_SectionA_Timetable.html
DSAI_Sem2_SectionB_Timetable.html
DSAI_Sem4_SectionA_Timetable.html
DSAI_Sem4_SectionB_Timetable.html
DSAI_Sem6_SectionA_Timetable.html
DSAI_Sem6_SectionB_Timetable.html
ECE_Sem2_SectionA_Timetable.html
ECE_Sem2_SectionB_Timetable.html
ECE_Sem4_SectionA_Timetable.html
ECE_Sem4_SectionB_Timetable.html
ECE_Sem6_SectionA_Timetable.html
ECE_Sem6_SectionB_Timetable.html
```

---

## ✨ **Features**

### **🎨 Beautiful Design**
- ✅ Modern gradient backgrounds
- ✅ Card-based layout
- ✅ Smooth hover animations
- ✅ Color-coded course types
- ✅ Responsive design for all devices

### **📊 Smart Color Coding**
- 🔵 **Blue** - Regular courses
- 🟠 **Orange** - Common courses (both sections)
- 🟣 **Purple** - Lab sessions
- 🟢 **Teal** - Tutorial sessions
- 🟢 **Light Green** - Free slots
- 🌈 **Gradient** - Lunch break

### **🎯 Easy Navigation**
- ✅ Department-wise organization (CSE, DSAI, ECE)
- ✅ Semester-wise grouping (Sem2, Sem4, Sem6)
- ✅ Section-wise buttons (A, B)
- ✅ Back button on each timetable
- ✅ Color legend on each page

### **📱 Responsive**
- ✅ Works on desktop
- ✅ Works on tablets
- ✅ Works on mobile phones
- ✅ Print-friendly

---

## 🎨 **Interface Preview**

### **Main Selection Page**
```
┌─────────────────────────────────────────────┐
│   🎓 BeyondGames Timetable Viewer          │
│   Select your department, semester & section│
└─────────────────────────────────────────────┘

┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  💻 CSE     │  │  📊 DSAI    │  │  ⚡ ECE      │
│             │  │             │  │             │
│ 📚 Sem2     │  │ 📚 Sem2     │  │ 📚 Sem2     │
│ [A] [B]     │  │ [A] [B]     │  │ [A] [B]     │
│             │  │             │  │             │
│ 📚 Sem4     │  │ 📚 Sem4     │  │ 📚 Sem4     │
│ [A] [B]     │  │ [A] [B]     │  │ [A] [B]     │
│             │  │             │  │             │
│ 📚 Sem6     │  │ 📚 Sem6     │  │ 📚 Sem6     │
│ [A] [B]     │  │ [A] [B]     │  │ [A] [B]     │
└─────────────┘  └─────────────┘  └─────────────┘
```

### **Individual Timetable Page**
```
┌────────────────────────────────────────────┐
│    🎓 CSE Timetable - Sem2 - SectionA     │
└────────────────────────────────────────────┘

[← Back to Selection]

[Legend: Regular | Common | Lab | Tutorial | Free | Lunch]

┌──────────┬──────────────┬──────────────┬─────┐
│ Day/Time │ 09:00-10:30  │ 10:45-12:15  │ ... │
├──────────┼──────────────┼──────────────┼─────┤
│ Monday   │ CS163-A      │ MA163-A      │ ... │
│ Tuesday  │ HS153-T-A    │ HS204-A      │ ... │
│ ...      │ ...          │ ...          │ ... │
└──────────┴──────────────┴──────────────┴─────┘
```

---

## 🔄 **Regenerate HTML**

If you update Excel timetables and want to regenerate HTML:

```bash
cd timetable_generator
py timetable_to_html.py
```

This will:
1. Convert all Excel timetables to HTML
2. Regenerate the index page
3. Update all individual timetable pages

---

## 🌟 **Sharing Timetables**

### **Share with Students**
1. Copy the entire `timetable_html/` folder
2. Share via Google Drive, OneDrive, or USB
3. Students open `index.html` in any browser
4. No installation required!

### **Upload to Website**
1. Upload the entire `timetable_html/` folder to your web server
2. Share the link: `https://yourwebsite.com/timetable_html/`
3. Accessible from anywhere!

### **Email Individual Timetables**
- Each HTML file is standalone
- Can be emailed or shared individually
- Opens in any email client or browser

---

## 💡 **Tips**

### **Print Timetables**
1. Open any timetable page
2. Press `Ctrl+P` (or `Cmd+P` on Mac)
3. Print preview will show clean, print-friendly version
4. Back button and legend hidden for printing

### **Bookmark Favorites**
- Bookmark your specific timetable page
- Direct access without going through index
- Quick reference for daily use

### **Mobile Access**
- Works perfectly on phones
- Add to home screen for app-like experience
- Responsive tables adjust to screen size

---

## 🎯 **Advantages of HTML Viewer**

### **vs Excel Files**
- ✅ No Excel installation required
- ✅ Works on any device with browser
- ✅ More visually appealing
- ✅ Easier to navigate
- ✅ Faster to load
- ✅ Better for sharing

### **vs PDF Files**
- ✅ Interactive navigation
- ✅ Better color coding
- ✅ Responsive design
- ✅ Smaller file size
- ✅ Easy to update

---

## 📊 **File Structure**

```
timetable_html/
├── index.html                          # Main selection page
├── CSE_Sem2_SectionA_Timetable.html   # Individual timetables
├── CSE_Sem2_SectionB_Timetable.html   # (18 files total)
├── ...
└── ECE_Sem6_SectionB_Timetable.html
```

---

## 🔧 **Technical Details**

### **Technologies Used**
- Pure HTML5
- CSS3 with gradients and animations
- No JavaScript required
- Self-contained (no external dependencies)

### **Browser Compatibility**
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ✅ Mobile browsers

### **File Size**
- Index page: ~5-10 KB
- Each timetable: ~10-15 KB
- Total: Less than 500 KB for all files
- Very fast loading!

---

## ✨ **Made with ❤️ by BeyondGames Team**

**Features:**
- 🎨 Beautiful gradient design
- 📱 Fully responsive
- 🌈 Color-coded courses
- 🚀 Lightning fast
- 🎯 Easy to use
- 💯 Production ready

**Perfect for:**
- Student access
- Faculty reference
- Administrative use
- Public display
- Mobile viewing
- Print distribution

---

## 📞 **Support**

**To regenerate:**
```bash
py timetable_to_html.py
```

**To open:**
```bash
start timetable_html\index.html
```

**Location:**
```
timetable_generator/timetable_html/
```

Enjoy your beautiful timetable viewer! 🎓✨
