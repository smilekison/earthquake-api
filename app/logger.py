# This file helps us keep track of what our application is doing

import logging

"""
    Purpose: Initializes and configures the logging system for the application
    What it does:
    - Sets up basic logging configuration with INFO level
    - Creates and returns a logger instance for the current module
    - Helps track application events, errors, and information
    Returns: A configured logger object
"""

def setup_logging():

    # 'INFO' level means we want to know about normal activities, not just problems
    logging.basicConfig(level=logging.INFO)

    # Create a log just for this part of our program (wherever it's used)
    logger = logging.getLogger(__name__)
    return logger
