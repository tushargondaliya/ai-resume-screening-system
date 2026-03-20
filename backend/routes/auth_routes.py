"""
Authentication Routes - Login, Register, Logout
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import verify_login, create_user, get_user_by_email
from services.backup_service import BackupService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        
        user = verify_login(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and handler."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        role = request.form.get('role', 'recruiter')
        
        if not name or not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if get_user_by_email(email):
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        if create_user(name, email, password, role):
            # Auto-save backup
            BackupService.create_backup()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """Logout handler."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
def dashboard():
    """Main dashboard page."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    from models.resume_model import count_resumes, get_top_resumes
    from models.job_model import count_jobs, get_all_jobs
    from models.match_model import count_matches, get_average_match_score
    
    stats = {
        'total_resumes': count_resumes(),
        'total_jobs': count_jobs(),
        'total_matches': count_matches(),
        'avg_match_score': get_average_match_score()
    }
    
    recent_jobs = get_all_jobs()[:5]
    top_resumes = get_top_resumes(5)
    
    return render_template('dashboard.html', stats=stats, recent_jobs=recent_jobs, top_resumes=top_resumes)
