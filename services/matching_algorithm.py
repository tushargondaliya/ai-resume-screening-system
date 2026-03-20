"""
Matching Algorithm - Compare candidate skills with job requirements.
Calculates match score and identifies skill gaps.
"""


def calculate_match_score(candidate_skills, required_skills):
    """
    Calculate matching score between candidate and job.
    Formula: (Matched Skills / Required Skills) × 100
    
    Args:
        candidate_skills: list or comma-separated string of candidate skills
        required_skills: list or comma-separated string of required job skills
    
    Returns:
        dict with match_score, matched_skills, missing_skills
    """
    # Normalize inputs
    if isinstance(candidate_skills, str):
        candidate_skills = [s.strip().lower() for s in candidate_skills.split(',') if s.strip()]
    else:
        candidate_skills = [s.strip().lower() for s in candidate_skills if s.strip()]
    
    if isinstance(required_skills, str):
        required_skills = [s.strip().lower() for s in required_skills.split(',') if s.strip()]
    else:
        required_skills = [s.strip().lower() for s in required_skills if s.strip()]
    
    if not required_skills:
        return {
            'match_score': 0,
            'matched_skills': '',
            'missing_skills': '',
            'candidate_extra_skills': ', '.join([s.title() for s in candidate_skills])
        }
    
    # Find matches
    matched = set()
    missing = set()
    
    for req_skill in required_skills:
        found = False
        for cand_skill in candidate_skills:
            if req_skill in cand_skill or cand_skill in req_skill:
                matched.add(req_skill)
                found = True
                break
        if not found:
            missing.add(req_skill)
            
    # Extra skills the candidate has
    extra_skills = set()
    for cand_skill in candidate_skills:
        is_matched = False
        for req_skill in required_skills:
            if req_skill in cand_skill or cand_skill in req_skill:
                is_matched = True
                break
        if not is_matched:
            extra_skills.add(cand_skill)
    
    # Calculate score
    fraction = len(matched) / len(required_skills)
    match_score = float(round(fraction * 100, 1))
    
    return {
        'match_score': match_score,
        'matched_skills': ', '.join([s.title() for s in matched]),
        'missing_skills': ', '.join([s.title() for s in missing]),
        'candidate_extra_skills': ', '.join([s.title() for s in extra_skills])
    }


def rank_candidates(candidates_data, job_skills):
    """
    Rank multiple candidates against a job's required skills.
    
    Args:
        candidates_data: list of dicts with 'id', 'name', 'skills'
        job_skills: comma-separated string or list of required skills
    
    Returns:
        sorted list of candidate results with scores and ranks
    """
    results = []
    
    for candidate in candidates_data:
        match_result = calculate_match_score(
            candidate.get('skills', ''),
            job_skills
        )
        results.append({
            'candidate_id': candidate.get('id'),
            'candidate_name': candidate.get('name', 'Unknown'),
            'match_score': match_result['match_score'],
            'matched_skills': match_result['matched_skills'],
            'missing_skills': match_result['missing_skills'],
            'extra_skills': match_result['candidate_extra_skills']
        })
    
    # Sort by match score (descending)
    results.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Assign ranks
    for i, result in enumerate(results):
        result['rank'] = i + 1
    
    return results


def get_job_recommendations(candidate_skills, jobs_data):
    """
    Recommend best matching jobs for a candidate.
    
    Args:
        candidate_skills: comma-separated string or list of skills
        jobs_data: list of job dicts with 'id', 'title', 'skills_required'
    
    Returns:
        sorted list of job recommendations with scores
    """
    recommendations = []
    
    for job in jobs_data:
        match_result = calculate_match_score(
            candidate_skills,
            job.get('skills_required', '')
        )
        recommendations.append({
            'job_id': job.get('id'),
            'job_title': job.get('title', job.get('job_title', 'Unknown')),
            'match_score': match_result['match_score'],
            'matched_skills': match_result['matched_skills'],
            'missing_skills': match_result['missing_skills']
        })
    
    # Sort by match score descending
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    return recommendations
