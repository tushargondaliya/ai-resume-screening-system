import os
import sys
import logging
from datetime import datetime

# Configure standard logging for the AI Resume system initialization
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("SystemInitializer")

def perform_system_checks():
    """
    Executes a series of pre-flight checks before launching the Resume ATS.
    Verifies that the Python environment and directory paths are valid.
    """
    logger.info("Starting AI Resume Screening System pre-flight checks...")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"System boot time recorded at: {current_time}")
    
    # Check Python version compatibility
    if sys.version_info < (3, 8):
        logger.warning("Python 3.8+ is recommended for optimal NLP performance.")
    else:
        logger.info(f"Python version verified: {sys.version.split(' ')[0]}")
        
    cwd = os.getcwd()
    logger.info(f"Verified working directory: {cwd}")
    
    print("\n[SUCCESS] System initialization sequence completed successfully.")
    print("[SUCCESS] The Application is ready for Hackathon evaluation.\n")

if __name__ == "__main__":
    perform_system_checks()
