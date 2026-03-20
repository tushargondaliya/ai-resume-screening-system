/* ---- Script.js - AI Resume Screening System ---- */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initDragDrop();
    initAlertDismiss();
    initAnimations();
    initTooltips();
});


/* ==================================================
   DRAG & DROP FILE UPLOAD
   ================================================== */
let selectedFiles = [];

function initDragDrop() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('resume-files');
    const fileList = document.getElementById('file-list');
    
    if (!uploadArea || !fileInput) return;
    
    // Click to open file dialog
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Drag events
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        handleFiles(e.dataTransfer.files);
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
    
    function handleFiles(files) {
        // Add new files to the list (avoid duplicates if possible, or just append)
        for (let i = 0; i < files.length; i++) {
            selectedFiles.push(files[i]);
        }
        syncFiles();
        displayFiles();
    }
}

function displayFiles() {
    const fileList = document.getElementById('file-list');
    if (!fileList) return;
    fileList.innerHTML = '';
    
    if (selectedFiles.length === 0) {
        document.getElementById('upload-btn').style.display = 'none';
        return;
    }
    
    selectedFiles.forEach((file, index) => {
        const ext = file.name.split('.').pop().toLowerCase();
        const icon = ext === 'pdf' ? '📄' : '📝';
        const size = formatFileSize(file.size);
        
        const item = document.createElement('div');
        item.className = 'file-item fade-in';
        item.style.display = 'flex';
        item.style.justifyContent = 'space-between';
        item.style.alignItems = 'center';
        
        item.innerHTML = `
            <div class="d-flex align-items-center gap-2">
                <span style="font-size: 1.3rem;">${icon}</span>
                <span class="file-name text-truncate" style="max-width: 200px;">${file.name}</span>
                <span class="text-muted" style="font-size: 0.8rem;">(${size})</span>
            </div>
            <div class="d-flex align-items-center gap-3">
                <span class="file-status d-none d-sm-inline">✓ Ready</span>
                <button type="button" class="btn-remove-file" onclick="removeFile(${index})" title="Remove file">
                    <i class="bi bi-x-circle"></i>
                </button>
            </div>
        `;
        fileList.appendChild(item);
    });
    
    // Show the upload button
    const uploadBtn = document.getElementById('upload-btn');
    if (uploadBtn) {
        uploadBtn.style.display = 'inline-flex';
    }
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    syncFiles();
    displayFiles();
}

function syncFiles() {
    const fileInput = document.getElementById('resume-files');
    if (!fileInput) return;
    
    // Use DataTransfer to update file input's files
    const dataTransfer = new DataTransfer();
    selectedFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}


/* ==================================================
   ALERT AUTO-DISMISS
   ================================================== */
function initAlertDismiss() {
    const alerts = document.querySelectorAll('.alert-custom');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}


/* ==================================================
   SCROLL ANIMATIONS
   ================================================== */
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}


/* ==================================================
   TOOLTIPS (simple)
   ================================================== */
function initTooltips() {
    // Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
    }
}


/* ==================================================
   CHART INITIALIZATION
   ================================================== */
function initSkillsChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: data,
                backgroundColor: [
                    'rgba(99, 102, 241, 0.7)',
                    'rgba(34, 211, 238, 0.7)',
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(245, 158, 11, 0.7)',
                    'rgba(244, 114, 182, 0.7)',
                    'rgba(96, 165, 250, 0.7)',
                    'rgba(168, 85, 247, 0.7)',
                    'rgba(239, 68, 68, 0.7)',
                    'rgba(52, 211, 153, 0.7)',
                    'rgba(251, 191, 36, 0.7)'
                ],
                borderColor: [
                    'rgba(99, 102, 241, 1)',
                    'rgba(34, 211, 238, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(244, 114, 182, 1)',
                    'rgba(96, 165, 250, 1)',
                    'rgba(168, 85, 247, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(52, 211, 153, 1)',
                    'rgba(251, 191, 36, 1)'
                ],
                borderWidth: 1,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8', maxRotation: 45 }
                }
            }
        }
    });
}


function initDoughnutChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(99, 102, 241, 0.8)',
                    'rgba(34, 211, 238, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(244, 114, 182, 0.8)',
                    'rgba(96, 165, 250, 0.8)',
                    'rgba(168, 85, 247, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: 'rgba(10, 14, 26, 1)',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        padding: 15,
                        font: { size: 12, family: 'Inter' }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12
                }
            }
        }
    });
}


function initScoresChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Match Score %',
                data: data,
                backgroundColor: data.map(score => {
                    if (score >= 70) return 'rgba(16, 185, 129, 0.7)';
                    if (score >= 40) return 'rgba(245, 158, 11, 0.7)';
                    return 'rgba(239, 68, 68, 0.7)';
                }),
                borderColor: data.map(score => {
                    if (score >= 70) return 'rgba(16, 185, 129, 1)';
                    if (score >= 40) return 'rgba(245, 158, 11, 1)';
                    return 'rgba(239, 68, 68, 1)';
                }),
                borderWidth: 1,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    callbacks: {
                        label: function(context) {
                            return `Score: ${context.parsed.x}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8', callback: v => v + '%' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}


/* ==================================================
   CONFIRMATION DIALOGS
   ================================================== */
function confirmDelete(url, itemName) {
    if (confirm(`Are you sure you want to delete "${itemName}"? This action cannot be undone.`)) {
        window.location.href = url;
    }
}


/* ==================================================
   LOADING STATE
   ================================================== */
function handleUpload(event) {
    event.preventDefault();
    const form = event.target;
    const btn = document.getElementById('upload-btn');
    
    if (!form.checkValidity()) return;
    
    // Disable UI
    btn.disabled = true;
    showLoading(btn);

    const formData = new FormData(form);
    
    // Use Fetch for AJAX upload
    fetch(window.location.href, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.text().then(html => {
                // If not redirected, we might have stayed on the same page (errors/messages)
                document.documentElement.innerHTML = html;
                // Re-initialize relevant parts if needed, but usually redirect is expected
            });
        }
    })
    .catch(error => {
        console.error('Upload failed:', error);
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-cpu"></i> Upload & Analyze with AI';
        alert('Upload failed. Please check your connection and try again.');
    });
}


function showLoading(btn) {
    
    // Show progress bar if it exists
    const progressContainer = document.getElementById('upload-progress-container');
    const progressBar = document.getElementById('upload-progress-bar');
    const progressText = document.getElementById('analysis-step-text');
    const progressPercent = document.getElementById('progress-percent');
    
    if (progressContainer && progressBar) {
        progressContainer.style.display = 'block';
        let width = 0;
        
        const messages = [
            { threshold: 10, text: "Uploading resumes to secure storage..." },
            { threshold: 35, text: "Extracting text content from files..." },
            { threshold: 65, text: "AI identifying technical skills & experience..." },
            { threshold: 85, text: "Matching candidates with job requirements..." },
            { threshold: 95, text: "Finalizing score calculations..." },
            { threshold: 100, text: "Almost there! Preparing your dashboard..." }
        ];

        const interval = setInterval(() => {
            if (width >= 99.5) {
                clearInterval(interval);
            } else {
                // Determine step size
                let step = (98 - width) * 0.15; 
                if (width >= 95) {
                    step = 0.6; // Faster finish after 95%
                }
                
                width += step;
                progressBar.style.width = width + '%';
                if (progressPercent) progressPercent.innerText = Math.floor(width) + '%';
                
                // Update text message
                if (progressText) {
                    const msg = messages.find(m => width < m.threshold) || messages[messages.length-1];
                    progressText.innerText = msg.text;
                }
            }
        }, 150); // Faster refresh (150ms instead of 400ms)
    }
}
