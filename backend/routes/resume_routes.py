import os
import concurrent.futures
import sys

# Resolve local module imports for linters
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Standard and Local Imports (ignored for linters missing environment context)
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app # type: ignore
from werkzeug.utils import secure_filename # type: ignore
from models.resume_model import save_resume, get_all_resumes, get_resume_by_id, delete_resume # type: ignore
from models.job_model import get_all_jobs # type: ignore
from services.resume_parser import parse_resume # type: ignore
from services.skill_extractor import extract_skills, calculate_resume_score # type: ignore
from services.backup_service import BackupService # type: ignore
import config # type: ignore

resume_bp = Blueprint('resumes', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@resume_bp.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        candidate_name = request.form.get('candidate_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        experience = request.form.get('experience', '').strip()
        education = request.form.get('education', '').strip()
        job_id = request.form.get('job_id')
        
        if 'resume' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
            
        files = request.files.getlist('resume')
        if not files or files[0].filename == '':
            flash('No selected files', 'error')
            return redirect(request.url)
            
        processed_count = 0
        
        # Capture context data before threading to avoid RuntimeError: Working outside of application context
        upload_folder = current_app.config['UPLOAD_FOLDER']
        user_id = session.get('user_id')
        
        def process_single_file(file):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                
                # Parse resume
                raw_text = parse_resume(file_path)
                
                # Extract skills and score
                skills_list = extract_skills(raw_text)
                skills = ', '.join(skills_list)
                
                score = calculate_resume_score(skills_list, experience, education)
                
                save_resume(
                    candidate_name=candidate_name if len(files) == 1 else filename.split('.')[0],
                    email=email if len(files) == 1 else '',
                    phone=phone if len(files) == 1 else '',
                    skills=skills,
                    experience=experience,
                    education=education,
                    resume_file=filename,
                    raw_text=raw_text,
                    resume_score=score,
                    uploaded_by=user_id,
                    job_id=job_id
                )
                return True
            return False

        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(process_single_file, files))
            processed_count = sum(1 for r in results if r)
        
        if processed_count > 0:
            # Auto-save backup once after all files are processed
            BackupService.create_backup()
            flash(f'Successfully uploaded and analyzed {processed_count} resume(s)!', 'success')
        
        return redirect(url_for('resumes.upload_resume'))
            
    jobs = get_all_jobs()
    resumes = get_all_resumes()
    return render_template('upload_resume.html', jobs=jobs, resumes=resumes)

@resume_bp.route('/resumes')
def list_resumes():
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
        
    resumes = get_all_resumes()
    return render_template('resumes_list.html', resumes=resumes)

@resume_bp.route('/resume/<int:resume_id>')
def view_resume(resume_id):
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
        
    resume = get_resume_by_id(resume_id)
    if not resume:
        flash('Resume not found.', 'error')
        return redirect(url_for('resumes.list_resumes'))
        
    return render_template('resume_analysis.html', resume=resume)

@resume_bp.route('/delete_resume/<int:resume_id>')
def delete_resume_route(resume_id):
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
        
    delete_resume(resume_id)
    # Auto-save backup
    BackupService.create_backup()
    flash('Resume deleted successfully.', 'success')
    return redirect(request.referrer or url_for('resumes.list_resumes'))
