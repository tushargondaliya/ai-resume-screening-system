import threading

class BackupService:
    """Service to handle automatic database backups (Auto-Save)."""
    
    @staticmethod
    def create_backup(as_thread=True):
        """Create a backup of the current database file."""
        if as_thread:
            thread = threading.Thread(target=BackupService._run_backup)
            thread.daemon = True # Ensure it doesn't block app exit
            thread.start()
            return True
        else:
            return BackupService._run_backup()

    @staticmethod
    def _run_backup():
        """The actual backup logic."""
        try:
            import os
            import shutil
            import datetime
            import config
            
            db_path = config.DATABASE
            if not os.path.exists(db_path):
                print(f"Backup failed: Database file not found at {db_path}")
                return False
                
            # Create backups directory
            backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Create backup filename with timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"resume_screening_auto_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Copy the database file
            shutil.copy2(db_path, backup_path)
            print(f"Auto-save completed: Backup created at {backup_path}")
            
            # Clean up old backups (keep last 10)
            BackupService._cleanup_old_backups(backup_dir)
            return True
        except Exception as e:
            print(f"Error during auto-save (backup): {str(e)}")
            return False

    @staticmethod
    def _cleanup_old_backups(backup_dir, keep_limit=10):
        """Keep only the most recent N backups."""
        try:
            backups = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) 
                       if f.startswith('resume_screening_auto_')]
            # Sort by modified time (newest first)
            backups.sort(key=os.path.getmtime, reverse=True)
            
            # Remove older backups
            if len(backups) > keep_limit:
                for old_backup in backups[keep_limit:]:
                    os.remove(old_backup)
                    print(f"Removed old backup: {old_backup}")
        except Exception as e:
            print(f"Error during backup cleanup: {str(e)}")
