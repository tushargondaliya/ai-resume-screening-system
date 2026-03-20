import os
import sqlite3
import sys

# Ensure config can be found even if running from different contexts
try:
    import config  # type: ignore
except ImportError:
    # Add parent directory to path if not already there
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    import config  # type: ignore


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database from schema.sql and handle migrations."""
    # Ensure database directory exists
    db_dir = os.path.dirname(os.path.abspath(config.DATABASE))
    if not os.path.exists(db_dir):
        os.makedirs(str(db_dir))
        print(f"Created database directory: {db_dir}")

    schema_path = os.path.join(config.BASE_DIR, 'database', 'schema.sql')
    
    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found at {schema_path}")
        return

    try:
        conn = get_db()
        # 1. Execute schema.sql (IF NOT EXISTS protects existing tables)
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
        
        # 2. Automated Migration: Ensure job_id exists in resumes table
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(resumes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'job_id' not in columns:
            print("Migrating database: Adding missing job_id column to resumes table...")
            try:
                cursor.execute("ALTER TABLE resumes ADD COLUMN job_id INTEGER REFERENCES jobs(id)")
                conn.commit()
                print("Migration successful: Added job_id column.")
            except Exception as migrate_err:
                print(f"Migration warning: {str(migrate_err)}")
        
        # 3. Ensure performance indexes exist
        print("Optimizing database: Creating performance indexes...")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_resumes_score ON resumes(resume_score)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_match_results_job ON match_results(job_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_match_results_resume ON match_results(resume_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_match_results_score ON match_results(match_score)")
        conn.commit()
        
        conn.close()
        print("Database structure verified and ready.")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

