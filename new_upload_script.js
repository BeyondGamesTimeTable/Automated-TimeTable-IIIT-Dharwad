// Path-based Upload Flow JavaScript

let currentStep = 0;
let selectedFiles = {
    CSE: null,
    ECE: null,
    DSAI: null,
    Classroom: null,
    Electives: null,
    Minors: null
};
let currentVersion = null;
let semesterType = 'even';

// API base auto-detection
const REMOTE_API = 'https://automated-timetable-iiit-dharwad.onrender.com';
let API_BASE;
if (location.hostname === 'localhost' || location.hostname === '127.0.0.1' || location.protocol === 'file:') {
    API_BASE = 'http://localhost:5000';
} else {
    API_BASE = REMOTE_API;
}

// Path coordinates (random/curved path)
const pathCoordinates = [
    { x: 15, y: 8 },    // Step 0: Select Semester (top left)
    { x: 35, y: 18 },   // Step 1: CSE 
    { x: 65, y: 12 },   // Step 2: ECE
    { x: 80, y: 28 },   // Step 3: DSAI
    { x: 70, y: 48 },   // Step 4: Classroom
    { x: 45, y: 60 },   // Step 5: Electives (optional)
    { x: 25, y: 75 },   // Step 6: Minors (optional)
    { x: 50, y: 90 }    // Step 7: Generate
];

// Initialize page
window.addEventListener('DOMContentLoaded', () => {
    drawPath();
    positionPoints();
    updateChakraPosition(0);
    activateStep(0);
    checkServerStatus();
});

function drawPath() {
    const svg = document.getElementById('pathSvg');
    const path = document.getElementById('curvePath');
    
    // Create a smooth curve through all points
    let pathData = `M ${pathCoordinates[0].x}% ${pathCoordinates[0].y}%`;
    
    for (let i = 1; i < pathCoordinates.length; i++) {
        const curr = pathCoordinates[i];
        const prev = pathCoordinates[i - 1];
        
        // Calculate control points for smooth curve
        const cpx = (prev.x + curr.x) / 2;
        const cpy = (prev.y + curr.y) / 2;
        
        pathData += ` Q ${cpx}% ${cpy}%, ${curr.x}% ${curr.y}%`;
    }
    
    path.setAttribute('d', pathData);
}

function positionPoints() {
    pathCoordinates.forEach((coord, index) => {
        const point = document.getElementById(`point-${index}`);
        if (point) {
            point.style.left = `${coord.x}%`;
            point.style.top = `${coord.y}%`;
            point.style.transform = 'translate(-50%, -50%)';
            
            // Position labels alternately
            const label = point.querySelector('.point-label');
            if (label) {
                if (index % 2 === 0) {
                    label.style.left = '40px';
                    label.style.top = '50%';
                    label.style.transform = 'translateY(-50%)';
                } else {
                    label.style.right = '40px';
                    label.style.top = '50%';
                    label.style.transform = 'translateY(-50%)';
                }
            }
            
            // Add click handler
            point.addEventListener('click', () => {
                if (index === currentStep) {
                    showPanel(index);
                }
            });
        }
    });
}

function updateChakraPosition(step) {
    const chakra = document.getElementById('movingChakra');
    const coord = pathCoordinates[step];
    
    chakra.style.left = `${coord.x}%`;
    chakra.style.top = `${coord.y}%`;
}

function activateStep(step) {
    // Deactivate all
    for (let i = 0; i < pathCoordinates.length; i++) {
        const point = document.getElementById(`point-${i}`);
        if (point) {
            point.classList.remove('active');
            if (i < step) {
                point.classList.add('completed');
            } else {
                point.classList.remove('completed');
            }
        }
    }
    
    // Activate current
    const currentPoint = document.getElementById(`point-${step}`);
    if (currentPoint) {
        currentPoint.classList.add('active');
    }
    
    currentStep = step;
    updateChakraPosition(step);
}

function moveToNextStep() {
    if (currentStep < pathCoordinates.length - 1) {
        activateStep(currentStep + 1);
        closePanel();
        
        // Auto-show next panel after a delay
        setTimeout(() => {
            showPanel(currentStep);
        }, 800);
    }
}

function showPanel(step) {
    const panel = document.getElementById('uploadPanel');
    const title = document.getElementById('panelTitle');
    const description = document.getElementById('panelDescription');
    const content = document.getElementById('panelContent');
    
    panel.classList.add('active');
    
    const panels = {
        0: {
            title: 'Select Semester Type',
            description: 'Choose even or odd semester',
            content: `
                <div class="semester-slider-container">
                    <div class="semester-option ${semesterType === 'even' ? 'active' : ''}" id="evenLabel">
                        <div class="semester-title">Even Semester</div>
                        <div class="semester-subtitle">Sem 2, 4, 6, 8</div>
                    </div>
                    <div class="toggle-track" onclick="toggleSemester()">
                        <div class="toggle-wheel ${semesterType === 'odd' ? 'odd' : ''}" id="toggleWheel">☸</div>
                    </div>
                    <div class="semester-option ${semesterType === 'odd' ? 'active' : ''}" id="oddLabel">
                        <div class="semester-title">Odd Semester</div>
                        <div class="semester-subtitle">Sem 1, 3, 5, 7</div>
                    </div>
                </div>
                <button class="action-button" onclick="moveToNextStep()">Continue</button>
            `
        },
        1: {
            title: 'CSE Course File',
            description: 'Upload Computer Science course data',
            content: createFileUploadPanel('CSE', 'CSE.csv or CSE_course.csv')
        },
        2: {
            title: 'ECE Course File',
            description: 'Upload Electronics & Communication course data',
            content: createFileUploadPanel('ECE', 'ECE.csv or ECE_course.csv')
        },
        3: {
            title: 'DSAI Course File',
            description: 'Upload Data Science & AI course data',
            content: createFileUploadPanel('DSAI', 'DSAI.csv or DSAI_course.csv')
        },
        4: {
            title: 'Classroom File',
            description: 'Upload available classrooms and capacities',
            content: createFileUploadPanel('Classroom', 'classrooms.csv')
        },
        5: {
            title: 'Electives File (Optional)',
            description: 'Upload elective courses or skip',
            content: createFileUploadPanel('Electives', 'electives.csv', true)
        },
        6: {
            title: 'Minors File (Optional)',
            description: 'Upload minor courses or skip',
            content: createFileUploadPanel('Minors', 'minors.csv', true)
        },
        7: {
            title: 'Generate Timetables',
            description: 'Upload and generate your timetables',
            content: `
                <div style="text-align: center; padding: 30px; background: rgba(99, 102, 241, 0.1); border-radius: 12px; margin-bottom: 20px;">
                    <div style="font-size: 4em; margin-bottom: 15px;">🏆</div>
                    <p style="color: #a5b4fc; font-size: 1.2em;">All required files ready!</p>
                </div>
                <button class="action-button generate" onclick="uploadAndGenerate()">Generate Timetables</button>
            `
        }
    };
    
    const panelData = panels[step];
    title.textContent = panelData.title;
    description.textContent = panelData.description;
    content.innerHTML = panelData.content;
}

function createFileUploadPanel(type, fileName, isOptional = false) {
    const file = selectedFiles[type];
    
    if (file) {
        return `
            <div class="upload-zone uploaded">
                <div class="zone-icon" style="color: #4ade80;">✓</div>
                <div class="zone-text" style="color: #4ade80;">File Uploaded</div>
                <div class="zone-subtext">${file.name} (${formatBytes(file.size)})</div>
            </div>
            <button class="action-button" onclick="removeFile('${type}')">Remove & Re-upload</button>
        `;
    } else {
        return `
            <div class="upload-zone" onclick="document.getElementById('file-${type}').click()">
                <div class="zone-icon">📂</div>
                <div class="zone-text">Drop file here or click to browse</div>
                <div class="zone-subtext">Accepted: ${fileName}</div>
            </div>
            <input type="file" id="file-${type}" class="file-input" accept=".csv" onchange="handleFileUpload('${type}', this.files[0])">
            ${isOptional ? '<button class="action-button skip" onclick="moveToNextStep()">Skip This Step</button>' : ''}
        `;
    }
}

function handleFileUpload(type, file) {
    if (!file) return;
    
    if (!file.name.endsWith('.csv')) {
        alert('Please select CSV files only.');
        return;
    }
    
    selectedFiles[type] = file;
    showPanel(currentStep); // Refresh panel
    
    // Auto-move to next step after short delay
    setTimeout(() => {
        moveToNextStep();
    }, 800);
}

function removeFile(type) {
    selectedFiles[type] = null;
    document.getElementById(`file-${type}`).value = '';
    showPanel(currentStep); // Refresh panel
}

function closePanel() {
    document.getElementById('uploadPanel').classList.remove('active');
}

function toggleSemester() {
    semesterType = semesterType === 'even' ? 'odd' : 'even';
    showPanel(0); // Refresh the panel
}

async function uploadAndGenerate() {
    // Validate required files
    if (!selectedFiles.CSE || !selectedFiles.ECE || !selectedFiles.DSAI || !selectedFiles.Classroom) {
        alert('Please upload all required files (CSE, ECE, DSAI, Classroom)');
        return;
    }
    
    const panel = document.getElementById('uploadPanel');
    const content = document.getElementById('panelContent');
    
    content.innerHTML = '<div style="text-align: center; color: #a5b4fc; padding: 40px;">Uploading files...</div>';
    
    try {
        // Upload files
        const formData = new FormData();
        formData.append('cse_file', selectedFiles.CSE);
        formData.append('ece_file', selectedFiles.ECE);
        formData.append('dsai_file', selectedFiles.DSAI);
        formData.append('classroom_file', selectedFiles.Classroom);
        formData.append('semester_type', semesterType);
        
        if (selectedFiles.Electives) {
            formData.append('electives_file', selectedFiles.Electives);
        }
        if (selectedFiles.Minors) {
            formData.append('minors_file', selectedFiles.Minors);
        }
        
        const uploadResponse = await fetch(`${API_BASE}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        const uploadResult = await uploadResponse.json();
        console.log('Upload response:', uploadResult);
        
        if (!uploadResult.success) {
            throw new Error(uploadResult.error || 'Upload failed');
        }
        
        currentVersion = uploadResult.version;
        content.innerHTML = '<div style="text-align: center; color: #a5b4fc; padding: 40px;">Generating timetables...</div>';
        
        // Show loading overlay
        document.getElementById('loadingOverlay').classList.add('active');
        
        // Generate timetables
        const generateResponse = await fetch(`${API_BASE}/api/regenerate`, {
            method: 'POST'
        });
        
        const generateResult = await generateResponse.json();
        console.log('Generation response:', generateResult);
        
        if (generateResult.success) {
            document.getElementById('loadingOverlay').classList.remove('active');
            
            panel.classList.remove('active');
            alert('Timetables generated successfully! Opening results...');
            
            if (generateResult.index_url) {
                window.open(generateResult.index_url, '_blank');
            }
            
            // Reset after delay
            setTimeout(() => {
                if (confirm('Would you like to upload again?')) {
                    location.reload();
                }
            }, 2000);
        } else {
            throw new Error(generateResult.error || generateResult.details || 'Generation failed');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loadingOverlay').classList.remove('active');
        
        content.innerHTML = `
            <div style="text-align: center; color: #fca5a5; padding: 30px;">
                <p style="margin-bottom: 20px;">Error: ${error.message}</p>
                <button class="action-button" onclick="uploadAndGenerate()">Retry</button>
            </div>
        `;
    }
}

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

async function checkServerStatus() {
    const indicator = document.getElementById('serverStatusIndicator');
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            indicator.className = 'server-status connected';
        }
    } catch (error) {
        indicator.className = 'server-status disconnected';
    }
}
