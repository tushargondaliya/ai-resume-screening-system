-- AI Resume Screening & Candidate Matching System
-- Database Schema for SQLite

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'recruiter',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title VARCHAR(200) NOT NULL,
    company_name VARCHAR(200) DEFAULT '',
    skills_required TEXT NOT NULL,
    experience_required VARCHAR(50) DEFAULT '',
    education_required VARCHAR(100) DEFAULT '',
    description TEXT DEFAULT '',
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Resumes Table
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) DEFAULT '',
    phone VARCHAR(30) DEFAULT '',
    skills TEXT DEFAULT '',
    experience VARCHAR(100) DEFAULT '',
    education VARCHAR(200) DEFAULT '',
    resume_file VARCHAR(300) NOT NULL,
    raw_text TEXT DEFAULT '',
    resume_score FLOAT DEFAULT 0.0,
    job_id INTEGER,
    uploaded_by INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

-- Skills Table
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) DEFAULT 'general'
);

-- Match Results Table
CREATE TABLE IF NOT EXISTS match_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    match_score FLOAT DEFAULT 0.0,
    matched_skills TEXT DEFAULT '',
    missing_skills TEXT DEFAULT '',
    rank INTEGER DEFAULT 0,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resumes(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

-- Insert default admin user (password: admin123)
INSERT OR IGNORE INTO users (name, email, password, role) 
VALUES ('Admin', 'admin@company.com', 'admin123', 'admin');

-- Insert default recruiter (password: recruiter123)
INSERT OR IGNORE INTO users (name, email, password, role) 
VALUES ('HR Recruiter', 'hr@company.com', 'recruiter123', 'recruiter');

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_resumes_score ON resumes(resume_score);
CREATE INDEX IF NOT EXISTS idx_match_results_job ON match_results(job_id);
CREATE INDEX IF NOT EXISTS idx_match_results_resume ON match_results(resume_id);
CREATE INDEX IF NOT EXISTS idx_match_results_score ON match_results(match_score);
