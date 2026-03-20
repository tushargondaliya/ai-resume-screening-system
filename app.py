"""
AI Resume Screening & Candidate Matching System
Main Application - Flask Server
AU Hackathon 2.0 | Atmiya University
"""
import os
from flask import Flask, render_template, redirect, url_for, session
import config
from models import init_db

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Ensure directories exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(config.DATABASE), exist_ok=True)

# Register Blueprints
from routes.auth_routes import auth_bp
from routes.job_routes import job_bp
from routes.resume_routes import resume_bp
from routes.match_routes import match_bp

app.register_blueprint(auth_bp)
app.register_blueprint(job_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(match_bp)


@app.route('/')
def home():
    """Home page."""
    # Redirect logged-in users to dashboard
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))
    return render_template('index.html')


# Custom Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('index.html'), 500


# Initialize database on first run
with app.app_context():
    init_db()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  AI Resume Screening & Candidate Matching System")
    print("  AU Hackathon 2.0 | Atmiya University")
    print("="*60)
    print("  Server running at: http://localhost:5000")
    print("  Default Login: hr@company.com / recruiter123")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5002)
