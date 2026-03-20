from models import get_db


def create_user(name, email, password, role='recruiter'):
    """Create a new user."""
    db = get_db()
    try:
        db.execute(
            'INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
            (name, email, password, role)
        )
        db.commit()
        return True
    except Exception:
        return False
    finally:
        db.close()


def get_user_by_email(email):
    """Get user by email."""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    db.close()
    return user


def get_user_by_id(user_id):
    """Get user by ID."""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    db.close()
    return user


def verify_login(email, password):
    """Verify user login credentials."""
    user = get_user_by_email(email)
    if user and user['password'] == password:
        return user
    return None


def get_all_users():
    """Get all users."""
    db = get_db()
    users = db.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    db.close()
    return users
