try:
    import schedule
except ImportError:
    schedule = None

import time
import subprocess
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def run_script(script_name):
    """Run a python script and log its execution."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), script_name)

    logger.info(f"Running scheduled job: {script_name}")
    try:
        # Run script using the current Python executable
        result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        logger.info(f"Successfully completed {script_name}")
        if result.stdout:
            logger.debug(f"{script_name} output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running {script_name}. Exit code: {e.returncode}")
        logger.error(f"Error output:\n{e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error running {script_name}: {e}")

def job_email_alerts():
    run_script("email_alerts.py")

def job_snapshot_manager():
    run_script("snapshot_manager.py")

def start_scheduler():
    logger.info("Starting ChurnGuard Task Scheduler...")
    
    if schedule is None:
        logger.warning("'schedule' package not installed. Running tasks in manual trigger mode.")
        logger.info("Executing initial email alerts check...")
        job_email_alerts()
        return

    # Schedule email alerts every morning at 8 AM
    schedule.every().day.at("08:00").do(job_email_alerts)
    
    # Schedule database snapshots at midnight
    schedule.every().day.at("00:00").do(job_snapshot_manager)
    
    logger.info("Scheduler is running. Press Ctrl+C to exit.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()
