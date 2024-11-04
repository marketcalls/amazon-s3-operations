document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.querySelector('.upload-form');
    const progressBar = document.querySelector('.progress');
    const progressBarInner = document.querySelector('.progress-bar');

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = document.querySelector('#file');
            if (fileInput.files.length > 0) {
                progressBar.classList.remove('d-none');
                progressBarInner.style.width = '0%';
                progressBarInner.textContent = '0%';
            }
        });
    }
});

function deleteFile(filename, form) {
    if (confirm('Are you sure you want to delete this file?')) {
        const csrfToken = form.querySelector('input[name="csrf_token"]').value;
        fetch(`/delete/${filename}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert('Error deleting file: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting file');
        });
    }
}
