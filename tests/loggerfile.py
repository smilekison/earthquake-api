import unittest
import logging
from io import StringIO
from app.logger import setup_logging

class TestLogger(unittest.TestCase):
    def test_setup_logging(self):
        # Set up a stream to capture log output
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.INFO)

        # Get the logger and add the stream handler
        logger = setup_logging()
        logger.handlers.clear()  # Clear any existing handlers
        logger.addHandler(handler)  # Add our custom handler

        # Log a test message
        test_message = "This is a test log message"
        logger.info(test_message)

        # Check if the log message was captured correctly
        log_output = log_stream.getvalue()
        self.assertIn(test_message, log_output, f"Expected log output to contain '{test_message}'")

        # Check if the log level is set to INFO
        self.assertEqual(logger.level, logging.INFO, "Expected logger level to be INFO")

if __name__ == "__main__":
    unittest.main()