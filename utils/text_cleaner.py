"""
Text Cleaner - Utility functions for text preprocessing.
"""
import re


def clean_text(text):
    """Clean and normalize text from resumes."""
    if not text:
        return ''
    
    # Replace multiple newlines with single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Remove special characters but keep useful punctuation
    text = re.sub(r'[^\w\s\-\.\,\@\+\#\/\(\)]', ' ', text)
    
    # Remove extra whitespace
    text = text.strip()
    
    return text


def extract_email(text):
    """Extract email address from text."""
    if not text:
        return ''
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group() if match else ''


def extract_phone(text):
    """Extract phone number from text."""
    if not text:
        return ''
    # Match various phone formats
    pattern = r'[\+]?[\d]{1,3}[\s\-]?[\(]?[\d]{2,5}[\)]?[\s\-]?[\d]{2,5}[\s\-]?[\d]{2,5}'
    match = re.search(pattern, text)
    return match.group().strip() if match else ''


def extract_name(text):
    """Extract candidate name (first line or first two words)."""
    if not text:
        return 'Unknown'
    
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        # Skip empty lines and lines that look like headers/labels
        if not line:
            continue
        if any(keyword in line.lower() for keyword in ['resume', 'curriculum', 'cv', 'objective', 'summary']):
            continue
        
        # Clean the line - remove special chars
        name = re.sub(r'[^\w\s]', '', line).strip()
        
        # Take first 2-4 words as name
        words = name.split()
        if 1 <= len(words) <= 5:
            return ' '.join(words[:4])
        elif len(words) > 5:
            return ' '.join(words[:3])
    
    return 'Unknown'


def extract_experience(text):
    """Extract years of experience from text."""
    if not text:
        return ''
    
    text_lower = text.lower()
    
    # Pattern: X years, X+ years, X-Y years
    patterns = [
        r'(\d+[\+]?\s*[\-\–]?\s*\d*\s*(?:years?|yrs?))\s*(?:of\s+)?(?:experience|exp)',
        r'(?:experience|exp)\s*[:\-]?\s*(\d+[\+]?\s*[\-\–]?\s*\d*\s*(?:years?|yrs?))',
        r'(\d+[\+]?\s*(?:years?|yrs?))\s+(?:in|of|working)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1).strip()
    
    return ''


def extract_education(text):
    """Extract education information from text."""
    if not text:
        return ''
    
    text_lower = text.lower()
    
    education_keywords = [
        'b.tech', 'btech', 'b.e.', 'b.sc', 'bsc', 'bca', 'bba',
        'm.tech', 'mtech', 'm.e.', 'm.sc', 'msc', 'mca', 'mba',
        'phd', 'ph.d', 'bachelor', 'master', 'diploma',
        'computer science', 'information technology', 'engineering',
        'b.com', 'bcom', 'm.com'
    ]
    
    found_education = []
    lines = text_lower.split('\n')
    
    for line in lines:
        for keyword in education_keywords:
            if keyword in line:
                clean_line = line.strip()
                if clean_line and clean_line not in found_education:
                    found_education.append(clean_line[:100])  # Limit line length
                break
    
    return ', '.join(found_education[:3]) if found_education else ''
