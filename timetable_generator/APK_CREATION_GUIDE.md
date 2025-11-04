# 📱 APK Creation Guide for Timetable App

## ✅ Your HTML Files Are Already Connected!

All timetable HTML files are connected with:
- **index.html**: Main navigation hub with all departments and semesters
- **Individual timetables**: Each has a "Back to Home" button to return to index.html
- **Responsive design**: Mobile-friendly and ready for APK conversion

## 🚀 Option 1: Website to APK (Easiest - No Coding!)

### Using **Website 2 APK Builder** (Recommended for beginners)

1. **Upload Your HTML Files**:
   - Go to: https://appsgeyser.com or https://andromo.com
   - Create a free account
   - Choose "Website/HTML" option
   - Upload the entire `timetable_html` folder

2. **Configure Your App**:
   - App Name: "IIIT Dharwad Timetable"
   - Icon: Upload a logo (512x512 PNG)
   - Start Page: `index.html`
   - Enable offline mode

3. **Build & Download APK**:
   - Click "Create App"
   - Download the generated APK
   - Install on Android device

### Using **Apache Cordova** (More control, requires Node.js)

**Prerequisites**: Install Node.js from https://nodejs.org

**Steps**:

```powershell
# 1. Install Cordova globally
npm install -g cordova

# 2. Create new Cordova project
cd "c:\Users\goura\OneDrive\Documents\Third semester\Software Design Tools and Techniques\Automatic Timetable Final\Automated-Time-Table-IIIT-DHARWAD"
cordova create TimetableApp com.iiitdharwad.timetable "IIIT Dharwad Timetable"

# 3. Navigate to project
cd TimetableApp

# 4. Add Android platform
cordova platform add android

# 5. Copy your HTML files
# Delete www folder contents and copy timetable_html contents
Remove-Item www\* -Recurse -Force
Copy-Item ..\timetable_generator\timetable_html\* www\ -Recurse

# 6. Build APK
cordova build android

# APK location: platforms\android\app\build\outputs\apk\debug\app-debug.apk
```

## 🎯 Option 2: Using Android Studio (Professional)

### Steps:

1. **Install Android Studio**: https://developer.android.com/studio

2. **Create New Project**:
   - File → New → New Project
   - Choose "Empty Activity"
   - Language: Java/Kotlin
   - Minimum SDK: API 21 (Android 5.0)

3. **Add WebView**:
   ```xml
   <!-- activity_main.xml -->
   <WebView
       android:id="@+id/webview"
       android:layout_width="match_parent"
       android:layout_height="match_parent" />
   ```

4. **Copy HTML Files**:
   - Create `app/src/main/assets` folder
   - Copy all files from `timetable_html` folder to `assets`

5. **Load HTML in MainActivity**:
   ```java
   WebView webView = findViewById(R.id.webview);
   webView.getSettings().setJavaScriptEnabled(true);
   webView.loadUrl("file:///android_asset/index.html");
   ```

6. **Build APK**:
   - Build → Build Bundle(s) / APK(s) → Build APK(s)
   - APK location: `app/build/outputs/apk/debug/app-debug.apk`

## 🔧 Option 3: Using Capacitor (Modern Alternative)

```powershell
# 1. Install Capacitor
npm install -g @capacitor/cli @capacitor/core

# 2. Initialize Capacitor
cd timetable_generator
npx cap init "IIIT Timetable" "com.iiit.timetable" --web-dir="timetable_html"

# 3. Add Android platform
npx cap add android

# 4. Open in Android Studio
npx cap open android

# 5. Build APK from Android Studio
```

## 📦 Recommended Approach for Your Project

**For Quick APK (No Coding)**:
- Use **AppsGeyser** or **Andromo**
- Just upload `timetable_html` folder
- Get APK in 5 minutes

**For Professional APK (With Control)**:
- Use **Apache Cordova** method above
- Allows customization and updates
- Can publish to Play Store

## 📝 App Configuration Checklist

Before building APK, ensure:
- ✅ All HTML files are in `timetable_html` folder
- ✅ `index.html` is the main entry point
- ✅ All links use relative paths (no absolute paths)
- ✅ All images/CSS are embedded or in same folder
- ✅ App works offline (no external dependencies)

## 🎨 App Icon

Create app icon (512x512 PNG) with:
- IIIT Dharwad logo
- Timetable/calendar symbol
- School colors

## 📲 Testing Your APK

1. **Enable Developer Options** on Android:
   - Settings → About Phone → Tap "Build Number" 7 times
   
2. **Enable USB Debugging**:
   - Settings → Developer Options → USB Debugging

3. **Install APK**:
   ```powershell
   adb install app-debug.apk
   ```

## 🚀 Next Steps

1. Choose your preferred method (Cordova recommended)
2. Follow the steps above
3. Test APK on Android device
4. Share with students!

---

**Note**: All your HTML files are already properly connected with navigation. You're ready to convert to APK immediately! 🎉
