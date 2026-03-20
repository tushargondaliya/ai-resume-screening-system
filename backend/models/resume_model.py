from models import get_db


def save_resume(candidate_name, email, phone, skills, experience, education, resume_file, raw_text, resume_score=0.0, uploaded_by=None, job_id=None):
    """Save parsed resume data."""
    db = get_db()
    cursor = db.execute(
        '''INSERT INTO resumes (candidate_name, email, phone, skills, experience, education, 
           resume_file, raw_text, resume_score, uploaded_by, job_id) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (candidate_name, email, phone, skills, experience, education, resume_file, raw_text, resume_score, uploaded_by, job_id)
    )
    resume_id = cursor.lastrowid
    db.commit()
    db.close()
    return resume_id


def get_all_resumes():
    """Get all resumes."""
    db = get_db()
    resumes = db.execute('SELECT * FROM resumes ORDER BY uploaded_at DESC').fetchall()
    db.close()
    return resumes


def get_resume_by_id(resume_id):
    """Get resume by ID."""
    db = get_db()
    resume = db.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,)).fetchone()
    db.close()
    return resume


def delete_resume(resume_id):
    """Delete a resume."""
    db = get_db()
    db.execute('DELETE FROM match_results WHERE resume_id = ?', (resume_id,))
    db.execute('DELETE FROM resumes WHERE id = ?', (resume_id,))
    db.commit()
    db.close()


def count_resumes():
    """Count total resumes."""
    db = get_db()
    count = db.execute('SELECT COUNT(*) as count FROM resumes').fetchone()['count']
    db.close()
    return count


def get_top_resumes(limit=10):
    """Get top resumes by score."""
    db = get_db()
    resumes = db.execute('SELECT * FROM resumes ORDER BY resume_score DESC LIMIT ?', (limit,)).fetchall()
    db.close()
    return resumes


def get_all_skills_distribution():
    """Get skill distribution across all resumes."""
    db = get_db()
    resumes = db.execute('SELECT skills FROM resumes').fetchall()
    db.close()
    
    skill_count = {}
    for resume in resumes:
        if resume['skills']:
            for skill in resume['skills'].split(','):
                skill = skill.strip().title()
                if skill:
                    skill_count[skill] = skill_count.get(skill, 0) + 1
    
    # Sort by count descending
    sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_skills[:20]  # Top 20 skills
