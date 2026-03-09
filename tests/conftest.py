import os
from datetime import datetime
from core.logger import logger

def pytest_configure(config):
    """
    Dynamically configures the Allure report directory to keep an archive of all test runs.
    Creates a folder structure based on the current date and time:
    Example: reports/YYYY-MM-DD/HH-MM-SS_results
    """
    # 1. Get current date and time
    now = datetime.now()
    date_folder = now.strftime("%Y-%m-%d")
    time_folder = now.strftime("%H-%M-%S_results")
    
    # 2. Build the dynamic path
    dynamic_report_path = os.path.join("reports", date_folder, time_folder)
    
    # 3. Inject this path into Pytest's Allure plugin configuration
    config.option.allure_report_dir = dynamic_report_path
    
    # Optional: Log the directory creation so we can see it in automation.log
    logger.info(f"Test Execution Archive initialized at: {dynamic_report_path}")