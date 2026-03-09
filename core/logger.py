import logging
import os

def setup_logger():
    """
    Creates and configures a custom logger for the automation framework.
    It writes logs to both the terminal (Console) and a permanent file (automation.log).
    """
    logger = logging.getLogger("API_Automation")
    
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_file_path = os.path.join(os.path.dirname(__file__), '..', 'automation.log')
        file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()