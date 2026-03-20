"""
Skill Extractor - AI module to extract skills from resume text.
Uses keyword matching against the skill database.
"""
import re
from utils.skill_database import get_all_skills, find_skill_category, SKILL_DATABASE


# Pre-compiled combined regex for all skills
_COMBINED_SKILLS_PATTERN = None

def get_combined_skills_pattern():
    """Get or create a combined regex pattern for all skills."""
    global _COMBINED_SKILLS_PATTERN
    if _COMBINED_SKILLS_PATTERN is None:
        all_skills = get_all_skills()
        # Sort skills by length (longest first) to ensure 'c++' matches before 'c'
        all_skills.sort(key=len, reverse=True)
        
        # Create a pattern that matches any of the skills
        # Rules:
        # 1. Must be preceded by start of string or a non-word/separator char
        # 2. Must be followed by end of string or a non-word/separator char
        escaped_skills = [re.escape(s) for s in all_skills]
        pattern_str = r'(?:^|[\s,;|\(\)\[\]\{\}/\\])(' + '|'.join(escaped_skills) + r')(?:$|[\s,;|\(\)\[\]\{\}/\\])'
        _COMBINED_SKILLS_PATTERN = re.compile(pattern_str, re.IGNORECASE)
    
    return _COMBINED_SKILLS_PATTERN

def extract_skills(text):
    """Extract skills from resume text using optimized keyword matching."""
    if not text:
        return []
    
    found_skills = set()
    pattern = get_combined_skills_pattern()
    
    # Use finditer to find all matches in one pass
    for match in pattern.finditer(text):
        skill_match = match.group(1).lower()
        # Map back to the original title case from SKILL_DATABASE if needed
        # but the set will handle duplicates. title() is a good default.
        found_skills.add(skill_match.title())
    
    # Also try to find skills mentioned in a "Skills" section for better coverage
    skills_section = extract_skills_section(text)
    if skills_section:
        all_skills = get_all_skills()
        skills_section_lower = skills_section.lower()
        for skill in all_skills:
            if skill.lower() in skills_section_lower:
                found_skills.add(skill.title())
    
    return sorted(list(found_skills))


def extract_skills_section(text):
    """Extract the skills section from resume text."""
    if not text:
        return ''
    
    text_lower = text.lower()
    
    # Look for a "Skills" section header
    section_headers = [
        'technical skills', 'skills', 'core competencies', 'technologies',
        'technical proficiency', 'programming skills', 'tools & technologies',
        'tools and technologies', 'competencies', 'expertise'
    ]
    
    # Find section ending keywords
    end_headers = [
        'experience', 'education', 'projects', 'certifications', 'awards',
        'achievements', 'interests', 'hobbies', 'references', 'publications',
        'work history', 'professional experience', 'employment'
    ]
    
    for header in section_headers:
        pattern = re.compile(r'(?:^|\n)\s*' + re.escape(header) + r'\s*[:\-]?\s*\n', re.IGNORECASE)
        match = pattern.search(text_lower)
        
        if match:
            start = match.end()
            # Find the end of the section
            end = len(text_lower)
            for end_header in end_headers:
                end_pattern = re.compile(r'(?:^|\n)\s*' + re.escape(end_header) + r'\s*[:\-]?\s*\n', re.IGNORECASE)
                end_match = end_pattern.search(text_lower, start)
                if end_match and end_match.start() < end:
                    end = end_match.start()
            
            return text[start:end].strip()
    
    return ''


def categorize_skills(skills):
    """Categorize extracted skills by their category."""
    categorized = {}
    for skill in skills:
        category = find_skill_category(skill)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(skill)
    return categorized


def calculate_resume_score(skills, experience_text, education_text):
    """Calculate a resume quality score (0-100)."""
    score = 0
    
    # Skills score (max 50 points)
    num_skills = len(skills) if isinstance(skills, list) else len(skills.split(','))
    skills_score = min(num_skills * 5, 50)
    score += skills_score
    
    # Experience score (max 30 points)
    if experience_text:
        # Try to extract years
        years_match = re.search(r'(\d+)', str(experience_text))
        if years_match:
            years = int(years_match.group(1))
            exp_score = min(years * 6, 30)
            score += exp_score
        else:
            score += 10  # Some experience mentioned
    
    # Education score (max 20 points)
    if education_text:
        edu_lower = education_text.lower()
        if any(k in edu_lower for k in ['phd', 'ph.d', 'doctorate']):
            score += 20
        elif any(k in edu_lower for k in ['master', 'm.tech', 'mtech', 'm.sc', 'mca', 'mba']):
            score += 17
        elif any(k in edu_lower for k in ['bachelor', 'b.tech', 'btech', 'b.e.', 'b.sc', 'bca']):
            score += 14
        elif any(k in edu_lower for k in ['diploma', 'associate']):
            score += 10
        else:
            score += 8
    
    return min(score, 100)
