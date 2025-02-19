// script.js

// Elements
const dragDropArea = document.getElementById('dragDropArea');
const fileInput = document.getElementById('fileInput');
const videoPreview = document.getElementById('videoPreview');
const videoUrlInput = document.getElementById('videoUrl');
const summarizeBtn = document.getElementById('summarizeBtn');
const summaryContent = document.getElementById('summaryContent');
const uploadForm = document.getElementById('uploadForm');
const summarySection = document.getElementById('summarySection');

// Handle Drag-and-Drop Functionality
dragDropArea.addEventListener('click', () => {
    fileInput.click();
});

dragDropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dragDropArea.style.backgroundColor = '#3C3C4E'; // Highlight on drag over
});

dragDropArea.addEventListener('dragleave', () => {
    dragDropArea.style.backgroundColor = '#2C2C3E'; // Reset background on drag leave
});

dragDropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dragDropArea.style.backgroundColor = '#2C2C3E'; // Reset background on drop
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
        // Clear video URL input
        videoUrlInput.value = '';
    }
});

// Handle File Input Change
fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
        // Clear video URL input
        videoUrlInput.value = '';
    }
});

// Function to Handle File Upload
function handleFileUpload(file) {
    if (file.type.startsWith('video/')) {
        // Display video preview
        const videoURL = URL.createObjectURL(file);
        videoPreview.src = videoURL;
        videoPreview.style.display = 'block';

        // Remove any existing summary
        summarySection.style.display = 'none';
        summaryContent.textContent = '';
    } else {
        alert('Please upload a valid video file.');
    }
}

// Handle Form Submission
uploadForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(uploadForm);

    if (fileInput.files.length === 0 && videoUrlInput.value.trim() === '') {
        alert('Please upload a video file or enter a video URL.');
        return;
    }

    // Disable the button to prevent multiple submissions
    summarizeBtn.disabled = true;
    summarizeBtn.textContent = 'Summarizing...';

    // Send POST request to Flask backend
    fetch('/summarize', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        summarizeBtn.disabled = false;
        summarizeBtn.textContent = 'Summarize';

        if (data.error) {
            alert(data.error);
        } else {
            // Display the summary
            summaryContent.textContent = data.summary;
            summarySection.style.display = 'block';
            summarySection.scrollIntoView({ behavior: 'smooth' });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        summarizeBtn.disabled = false;
        summarizeBtn.textContent = 'Summarize';
        alert('An error occurred while processing your request.');
    });
});

// Optional: Function to Extract YouTube Video ID (if handling YouTube URLs)
function extractYouTubeId(url) {
    const regExp = /^(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:youtube\.com|youtu\.be)(\/(?:watch\?v=|embed\/|v\/)?)([\w-]+)(\S+)?$/;
    const match = url.match(regExp);
    return match && match[2] ? match[2] : null;
}

