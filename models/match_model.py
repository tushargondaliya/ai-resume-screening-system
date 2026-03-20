from models import get_db


def save_match_result(resume_id, job_id, match_score, matched_skills, missing_skills, rank=0):
    """Save a match result."""
    db = get_db()
    # Delete existing match for this resume-job pair
    db.execute('DELETE FROM match_results WHERE resume_id = ? AND job_id = ?', (resume_id, job_id))
    db.execute(
        '''INSERT INTO match_results (resume_id, job_id, match_score, matched_skills, missing_skills, rank) 
           VALUES (?, ?, ?, ?, ?, ?)''',
        (resume_id, job_id, match_score, matched_skills, missing_skills, rank)
    )
    db.commit()
    db.close()


def get_rankings_for_job(job_id):
    """Get ranked candidates for a job."""
    db = get_db()
    rankings = db.execute(
        '''SELECT mr.*, r.candidate_name, r.email as candidate_email, r.skills as candidate_skills,
                  r.experience, r.education, r.resume_score
           FROM match_results mr
           JOIN resumes r ON mr.resume_id = r.id
           WHERE mr.job_id = ?
           ORDER BY mr.match_score DESC''',
        (job_id,)
    ).fetchall()
    db.close()
    return rankings


def get_skill_gap(resume_id, job_id):
    """Get skill gap for a specific resume-job match."""
    db = get_db()
    match = db.execute(
        '''SELECT mr.*, r.candidate_name, r.skills as candidate_skills, j.job_title, j.skills_required
           FROM match_results mr
           JOIN resumes r ON mr.resume_id = r.id
           JOIN jobs j ON mr.job_id = j.id
           WHERE mr.resume_id = ? AND mr.job_id = ?''',
        (resume_id, job_id)
    ).fetchone()
    db.close()
    return match


def count_matches():
    """Count total matches."""
    db = get_db()
    count = db.execute('SELECT COUNT(*) as count FROM match_results').fetchone()['count']
    db.close()
    return count


def get_average_match_score():
    """Get average match score across all results."""
    db = get_db()
    result = db.execute('SELECT AVG(match_score) as avg_score FROM match_results').fetchone()
    db.close()
    return round(result['avg_score'], 1) if result['avg_score'] else 0


def get_top_candidates(limit=10):
    """Get overall top candidates based on average match scores."""
    db = get_db()
    candidates = db.execute(
        '''SELECT r.id, r.candidate_name, r.email, r.skills, r.resume_score,
                  AVG(mr.match_score) as avg_match_score,
                  COUNT(mr.id) as total_matches
           FROM resumes r
           LEFT JOIN match_results mr ON r.id = mr.resume_id
           GROUP BY r.id
           ORDER BY avg_match_score DESC
           LIMIT ?''',
        (limit,)
    ).fetchall()
    db.close()
    return candidates
