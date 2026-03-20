"""
Match Routes - Matching, Ranking, Skill Gap, Analytics
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.job_model import get_job_by_id, get_all_jobs
from models.resume_model import get_all_resumes, get_resume_by_id, get_all_skills_distribution
from models.match_model import save_match_result, get_rankings_for_job, get_skill_gap, get_top_candidates
from services.matching_algorithm import calculate_match_score, rank_candidates, get_job_recommendations

match_bp = Blueprint('matching', __name__)


@match_bp.route('/match/<int:job_id>')
def run_matching(job_id):
    """Run matching algorithm for a job against all resumes."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found.', 'error')
        return redirect(url_for('auth.dashboard'))
    
    resumes = get_all_resumes()
    if not resumes:
        flash('No resumes uploaded yet. Upload resumes first.', 'warning')
        return redirect(url_for('resumes.upload_resume'))
    
    # Prepare candidate data
    candidates = []
    for resume in resumes:
        candidates.append({
            'id': resume['id'],
            'name': resume['candidate_name'],
            'skills': resume['skills']
        })
    
    # Run matching
    results = rank_candidates(candidates, job['skills_required'])
    
    # Save results to database
    for result in results:
        save_match_result(
            resume_id=result['candidate_id'],
            job_id=job_id,
            match_score=result['match_score'],
            matched_skills=', '.join(result['matched_skills']),
            missing_skills=', '.join(result['missing_skills']),
            rank=result['rank']
        )
    
    flash(f'Matching completed! {len(results)} candidates analyzed for "{job["job_title"]}".', 'success')
    return redirect(url_for('matching.ranking_page', job_id=job_id))


@match_bp.route('/ranking/<int:job_id>')
def ranking_page(job_id):
    """Show candidate ranking for a specific job."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found.', 'error')
        return redirect(url_for('auth.dashboard'))
    
    rankings = get_rankings_for_job(job_id)
    
    return render_template('ranking.html', job=job, rankings=rankings)


@match_bp.route('/skill_gap/<int:resume_id>/<int:job_id>')
def skill_gap_page(resume_id, job_id):
    """Show skill gap analysis for a candidate-job pair."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    match_data = get_skill_gap(resume_id, job_id)
    if not match_data:
        flash('Match data not found. Run matching first.', 'error')
        return redirect(url_for('auth.dashboard'))
    
    resume = get_resume_by_id(resume_id)
    job = get_job_by_id(job_id)
    
    return render_template('skill_gap.html', match_data=match_data, resume=resume, job=job)


@match_bp.route('/analytics')
def analytics_page():
    """Analytics dashboard with charts."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.login'))
    
    # Get skills distribution
    skills_dist = get_all_skills_distribution()
    
    # Get top candidates
    top_candidates = get_top_candidates(10)
    
    # Get all jobs for matching
    jobs = get_all_jobs()
    
    # Get all resumes for experience distribution
    resumes = get_all_resumes()
    
    return render_template('analytics.html', 
                          skills_dist=skills_dist,
                          top_candidates=top_candidates,
                          jobs=jobs,
                          resumes=resumes)


@match_bp.route('/api/skills_data')
def api_skills_data():
    """API endpoint for skills chart data."""
    skills_dist = get_all_skills_distribution()
    labels = [s[0] for s in skills_dist[:10]]
    values = [s[1] for s in skills_dist[:10]]
    return jsonify({'labels': labels, 'values': values})


@match_bp.route('/api/rankings_data/<int:job_id>')
def api_rankings_data(job_id):
    """API endpoint for rankings chart data."""
    rankings = get_rankings_for_job(job_id)
    labels = [r['candidate_name'] for r in rankings[:10]]
    values = [r['match_score'] for r in rankings[:10]]
    return jsonify({'labels': labels, 'values': values})
