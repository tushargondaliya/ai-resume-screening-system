import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database Settings
DATABASE = os.path.join(BASE_DIR, 'database', 'resume_screening.db')
SCHEMA_FILE = os.path.join(BASE_DIR, 'database', 'schema.sql')

# Upload folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'resumes')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Secret key for sessions
SECRET_KEY = 'au-hackathon-2025-ai-resume-screening-secret-key'

# Max file size (16 MB)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
