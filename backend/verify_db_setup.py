import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models import init_db
from services.backup_service import BackupService
import config

def verify():
    print("--- Verifying Database Setup ---")
    
    # 1. Test init_db
    print("\n1. Testing init_db()...")
    init_db()
    if os.path.exists(config.DATABASE):
        print(f"PASS: Database file exists at {config.DATABASE}")
    else:
        print(f"FAIL: Database file not found at {config.DATABASE}")

    # 2. Test BackupService
    print("\n2. Testing BackupService.create_backup()...")
    success = BackupService.create_backup()
    if success:
        backup_dir = os.path.join(os.path.dirname(config.DATABASE), 'backups')
        backups = [f for f in os.listdir(backup_dir) if f.startswith('resume_screening_auto_')]
        if backups:
            print(f"PASS: Backup created successfully. Found {len(backups)} backup(s).")
            print(f"Latest backup: {backups[-1]}")
        else:
            print("FAIL: Backup file not found in backups directory.")
    else:
        print("FAIL: BackupService.create_backup() returned False.")

if __name__ == "__main__":
    verify()
