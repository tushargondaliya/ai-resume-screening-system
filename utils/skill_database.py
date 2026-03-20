"""
Skill Database - Master list of technical skills for matching.
Contains 100+ skills organized by category.
"""

SKILL_DATABASE = {
    'programming_languages': [
        'python', 'java', 'javascript', 'c', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
        'go', 'rust', 'typescript', 'scala', 'perl', 'r', 'matlab', 'dart', 'lua', 'shell',
        'bash', 'powershell', 'objective-c', 'assembly', 'vba', 'groovy', 'haskell', 'erlang'
    ],
    'web_frameworks': [
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'laravel', 'rails',
        'asp.net', 'nextjs', 'next.js', 'nuxt', 'svelte', 'bootstrap', 'tailwind', 'jquery',
        'node.js', 'nodejs', 'fastapi', 'gin', 'fiber'
    ],
    'databases': [
        'mysql', 'postgresql', 'mongodb', 'sqlite', 'redis', 'oracle', 'sql server',
        'dynamodb', 'cassandra', 'elasticsearch', 'firebase', 'mariadb', 'neo4j', 'couchdb',
        'sql', 'nosql', 'graphql'
    ],
    'cloud_devops': [
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins', 'terraform',
        'ansible', 'ci/cd', 'linux', 'nginx', 'apache', 'heroku', 'vercel', 'netlify',
        'git', 'github', 'gitlab', 'bitbucket', 'svn'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'data analysis', 'data science', 'artificial intelligence',
        'nlp', 'natural language processing', 'computer vision', 'tensorflow', 'pytorch', 'keras',
        'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'tableau', 'power bi',
        'statistics', 'data mining', 'big data', 'hadoop', 'spark', 'data visualization'
    ],
    'mobile': [
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
        'swift', 'kotlin', 'objective-c'
    ],
    'tools_technologies': [
        'rest api', 'api', 'microservices', 'agile', 'scrum', 'jira', 'confluence',
        'testing', 'unit testing', 'selenium', 'cypress', 'postman', 'swagger',
        'html', 'css', 'sass', 'less', 'webpack', 'babel', 'figma', 'photoshop',
        'illustrator', 'sketch', 'ui/ux', 'responsive design'
    ],
    'soft_skills': [
        'teamwork', 'leadership', 'communication', 'problem solving', 'critical thinking',
        'time management', 'project management', 'collaboration', 'presentation',
        'analytical', 'creative thinking', 'adaptability'
    ]
}


def get_all_skills():
    """Get a flat list of all skills."""
    all_skills = []
    for category_skills in SKILL_DATABASE.values():
        all_skills.extend(category_skills)
    return all_skills


def get_skills_by_category(category):
    """Get skills for a specific category."""
    return SKILL_DATABASE.get(category, [])


def get_all_categories():
    """Get all skill categories."""
    return list(SKILL_DATABASE.keys())


def find_skill_category(skill):
    """Find which category a skill belongs to."""
    skill_lower = skill.lower().strip()
    for category, skills in SKILL_DATABASE.items():
        if skill_lower in skills:
            return category
    return 'other'
