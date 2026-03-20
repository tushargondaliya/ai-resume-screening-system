import time
import re
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from services.skill_extractor import extract_skills
from utils.skill_database import get_all_skills

def benchmark():
    print("--- Skill Extraction Performance Benchmark ---")
    
    # Sample resume text (mimicking a real resume)
    sample_text = """
    John Doe
    Full Stack Developer
    
    Experience:
    - Built web applications using Python, Django, and React.
    - Managed databases with PostgreSQL and Redis.
    - Deployed services on AWS using Docker and Kubernetes.
    - Implemented CI/CD pipelines with Jenkins and GitHub Actions.
    
    Skills:
    Programming: Python, Java, JavaScript, C++, Go, Rust.
    Web: React, Node.js, Express, Flask, HTML, CSS, Tailwind.
    Databases: MySQL, MongoDB, Redis, GraphQL.
    DevOps: Docker, Kubernetes, Terraform, AWS, Azure, GCP.
    Soft Skills: Communication, Leadership, Problem Solving.
    """
    
    # Warm up (compiles the regex)
    extract_skills("warmup")
    
    # Measure time
    start_time = time.time()
    iterations = 100
    for _ in range(iterations):
        extract_skills(sample_text)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / iterations
    print(f"\nAverage time per extraction: {avg_time*1000:.4f} ms")
    print(f"Total time for {iterations} iterations: {end_time - start_time:.4f} seconds")
    
    # Verify results
    skills = extract_skills(sample_text)
    print(f"\nSkills found ({len(skills)}): {', '.join(skills)}")
    
    # Check for specific skills to ensure accuracy
    expected_skills = ['Python', 'Django', 'React', 'Postgresql', 'Redis', 'Aws', 'Docker', 'Kubernetes', 'Jenkins', 'Github', 'Java', 'Javascript', 'C++', 'Go', 'Rust', 'Node.Js', 'Express', 'Flask', 'Html', 'Css', 'Tailwind', 'Mysql', 'Mongodb', 'Graphql', 'Terraform', 'Azure', 'Gcp', 'Communication', 'Leadership', 'Problem Solving']
    
    missing = [s for s in expected_skills if s.title() not in [found.title() for found in skills]]
    if not missing:
        print("\nPASS: All expected skills found.")
    else:
        print(f"\nNOTE: Some skills were not found (Expected match might differ): {', '.join(missing)}")

if __name__ == "__main__":
    benchmark()
