# File Upload System with AWS S3

A modern Flask-based web application for secure file uploads to AWS S3 with CSRF protection and Tailwind CSS styling.

## Features

- Secure file upload to AWS S3
- File listing and management
- Download functionality
- Secure deletion with CSRF protection
- Progress bar for uploads
- Support for multiple file types
- File size validation
- Modern UI with Tailwind CSS
- Responsive design

## Prerequisites

- Python 3.8+
- AWS Account with S3 bucket
- AWS Access Key and Secret Key
- Flask and its dependencies

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install flask flask-wtf python-dotenv boto3
```

4. Create .env file:
```bash
cp .env.sample .env
```

5. Update the .env file with your AWS credentials and other configurations.

## Configuration

The following environment variables need to be set in your .env file:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: AWS region (e.g., us-east-1)
- `AWS_BUCKET_NAME`: Your S3 bucket name
- `SECRET_KEY`: Flask secret key for session security
- `MAX_CONTENT_LENGTH`: Maximum file size in bytes
- `ALLOWED_FILE_EXTENSIONS`: Comma-separated list of allowed file extensions
- `FLASK_DEBUG`: Set to 1 for development, 0 for production

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open a web browser and navigate to:
```
http://localhost:5000
```

3. Use the interface to:
   - Upload files
   - View uploaded files
   - Download files
   - Delete files

## Security Features

- CSRF Protection
- Secure file handling
- File type validation
- Size restrictions
- AWS S3 security

## Project Structure

```
.
├── app.py              # Main application file
├── static/            
│   ├── css/           # Custom CSS styles
│   │   └── style.css
│   └── js/            # JavaScript files
│       └── script.js
├── templates/          # HTML templates with Tailwind CSS
│   ├── base.html      # Base template with common layout
│   ├── index.html     # Upload form page
│   └── uploads.html   # File management page
├── .env               # Environment variables
├── .env.sample        # Environment variables template
├── .gitignore        # Git ignore rules
├── LICENSE           # MIT License
└── README.md         # This file
```

## Styling

This project uses Tailwind CSS for styling, providing:
- Modern, utility-first CSS framework
- Responsive design out of the box
- Custom components and utilities
- No need for separate CSS framework
- Fast development and easy maintenance

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask framework
- AWS S3 service
- Tailwind CSS
- Flask-WTF for CSRF protection
