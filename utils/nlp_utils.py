import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_match_score(resume_text, job_description):
    # Very basic TF-IDF based cosine similarity match
    cleaned_resume = clean_text(resume_text)
    cleaned_job = clean_text(job_description)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cleaned_resume, cleaned_job])
    
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return float(similarity * 100) # Returns percentage
