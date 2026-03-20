from models import get_db


def create_job(job_title, skills_required, experience_required='', education_required='', description='', company_name='', created_by=None):
    """Create a new job posting."""
    db = get_db()
    cursor = db.execute(
        '''INSERT INTO jobs (job_title, company_name, skills_required, experience_required, 
           education_required, description, created_by) 
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (job_title, company_name, skills_required, experience_required, education_required, description, created_by)
    )
    job_id = cursor.lastrowid
    db.commit()
    db.close()
    return job_id


def get_all_jobs():
    """Get all jobs."""
    db = get_db()
    jobs = db.execute('SELECT * FROM jobs ORDER BY created_at DESC').fetchall()
    db.close()
    return jobs


def get_job_by_id(job_id):
    """Get job by ID."""
    db = get_db()
    job = db.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    db.close()
    return job


def delete_job(job_id):
    """Delete a job posting."""
    db = get_db()
    db.execute('DELETE FROM match_results WHERE job_id = ?', (job_id,))
    db.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
    db.commit()
    db.close()


def get_jobs_by_user(user_id):
    """Get jobs created by a specific user."""
    db = get_db()
    jobs = db.execute('SELECT * FROM jobs WHERE created_by = ? ORDER BY created_at DESC', (user_id,)).fetchall()
    db.close()
    return jobs


def count_jobs():
    """Count total jobs."""
    db = get_db()
    count = db.execute('SELECT COUNT(*) as count FROM jobs').fetchone()['count']
    db.close()
    return count
