"""
Job Routes - Create, List, Delete job postings
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.job_model import create_job, get_all_jobs, get_job_by_id, delete_job
from services.backup_service import BackupService

job_bp = Blueprint('jobs', __name__)


@job_bp.route('/create_job', methods=['GET', 'POST'])
def create_job_page():
    """Create job posting page."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        job_title = request.form.get('job_title', '').strip()
        company_name = request.form.get('company_name', '').strip()
        skills_required = request.form.get('skills_required', '').strip()
        experience_required = request.form.get('experience_required', '').strip()
        education_required = request.form.get('education_required', '').strip()
        description = request.form.get('description', '').strip()
        
        if not job_title or not skills_required:
            flash('Job title and required skills are mandatory.', 'error')
            return render_template('create_job.html')
        
        job_id = create_job(
            job_title=job_title,
            skills_required=skills_required,
            experience_required=experience_required,
            education_required=education_required,
            description=description,
            company_name=company_name,
            created_by=session.get('user_id')
        )
        
        # Auto-save backup
        BackupService.create_backup()
        
        flash(f'Job "{job_title}" created successfully!', 'success')
        return redirect(url_for('auth.dashboard'))
    
    jobs = get_all_jobs()
    return render_template('create_job.html', jobs=jobs)


@job_bp.route('/jobs')
def list_jobs():
    """List all job postings."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    jobs = get_all_jobs()
    return render_template('jobs_list.html', jobs=jobs)


@job_bp.route('/job/<int:job_id>')
def view_job(job_id):
    """View a specific job."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found.', 'error')
        return redirect(url_for('jobs.list_jobs'))
    
    return render_template('view_job.html', job=job)


@job_bp.route('/delete_job/<int:job_id>')
def delete_job_route(job_id):
    """Delete a job posting."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    delete_job(job_id)
    # Auto-save backup
    BackupService.create_backup()
    flash('Job deleted successfully.', 'success')
    return redirect(url_for('auth.dashboard'))
