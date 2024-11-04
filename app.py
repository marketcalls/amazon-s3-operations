import os
from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# AWS Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure allowed extensions
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_FILE_EXTENSIONS', 'txt,pdf,png,jpg,jpeg,gif,doc,docx').split(','))

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Create a simple form for CSRF protection
class UploadForm(FlaskForm):
    pass

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size_str(size_in_bytes):
    """Convert file size to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f} TB"

@app.route('/')
def index():
    """Render the upload form"""
    form = UploadForm()
    return render_template('index.html', form=form, allowed_extensions=ALLOWED_EXTENSIONS)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and store in S3"""
    form = UploadForm()
    if not form.validate_on_submit():
        flash('Form validation failed.', 'danger')
        return redirect(url_for('index'))

    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            
            # Upload file to S3
            s3_client.upload_fileobj(
                file,
                AWS_BUCKET_NAME,
                filename,
                ExtraArgs={
                    'ContentType': file.content_type
                }
            )
            
            # Generate a presigned URL (optional)
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': AWS_BUCKET_NAME,
                    'Key': filename
                },
                ExpiresIn=3600  # URL expires in 1 hour
            )
            
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('uploads'))
            
        except ClientError as e:
            flash(f'Error uploading file: {str(e)}', 'danger')
            return redirect(url_for('index'))
    
    flash('File type not allowed', 'danger')
    return redirect(url_for('index'))

@app.route('/uploads')
def uploads():
    """List all uploaded files"""
    try:
        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                # Get file metadata
                file_info = {
                    'filename': obj['Key'],
                    'last_modified': obj['LastModified'],
                    'size': obj['Size'],
                    'size_str': get_file_size_str(obj['Size'])
                }
                files.append(file_info)
        
        # Sort files by last modified date (newest first)
        files.sort(key=lambda x: x['last_modified'], reverse=True)
        
        form = UploadForm()  # Create form instance for CSRF token
        return render_template('uploads.html', files=files, form=form)
    
    except ClientError as e:
        flash(f'Error retrieving files: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Download a file from S3"""
    try:
        # Get file from S3
        file_obj = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=filename)
        
        # Create a BytesIO object
        file_data = BytesIO(file_obj['Body'].read())
        
        # Send file to user
        return send_file(
            file_data,
            download_name=filename,
            as_attachment=True,
            mimetype=file_obj['ContentType']
        )
        
    except ClientError as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('uploads'))

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a file from S3"""
    try:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=filename)
        return jsonify({'success': True})
    
    except ClientError as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    max_size_mb = app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
    flash(f'File is too large. Maximum size is {max_size_mb:.1f}MB', 'danger')
    return redirect(url_for('index'))

@app.context_processor
def utility_processor():
    """Add utility functions to template context"""
    def format_datetime(dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    def format_size(size):
        return get_file_size_str(size)
    
    return dict(format_datetime=format_datetime, format_size=format_size)

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', '0') == '1')
