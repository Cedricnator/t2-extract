import logging
import os
from datetime import datetime

class Logger:
   _instance = None

   @classmethod
   def get_instance(cls):
      """Get or create the Logger singleton instance"""
      if cls._instance is None:
         cls._instance = Logger()
      return cls._instance

   def __init__(self):
      """Initialize the logger with file and console handlers"""
      # Create logs directory if it doesn't exist
      os.makedirs("logs", exist_ok=True)

      # Configure logger
      self.logger = logging.getLogger("github_extractor")
      self.logger.setLevel(logging.INFO)

      # Clear any existing handlers (important for singleton pattern)
      if self.logger.handlers:
         self.logger.handlers.clear()

      # Create timestamp for log file
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

      # Create and configure file handler
      file_handler = logging.FileHandler(f"logs/extract_{timestamp}.log")
      file_handler.setLevel(logging.INFO)

      # Create and configure console handler
      console_handler = logging.StreamHandler()
      console_handler.setLevel(logging.INFO)

      # Create formatter
      formatter = logging.Formatter(
         "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
      )
      file_handler.setFormatter(formatter)
      console_handler.setFormatter(formatter)

      # Add handlers to logger
      self.logger.addHandler(file_handler)
      self.logger.addHandler(console_handler)

   def log(self, message, context=None):
      """Log an info message, optionally with context"""
      msg = f"[{context}] {message}" if context else message
      self.logger.info(msg)

   def log_error(self, message, context=None):
      """Log an error message, optionally with context"""
      msg = f"[{context}] {message}" if context else message
      self.logger.error(msg)

   def log_warning(self, message, context=None):
      """Log a warning message, optionally with context"""
      msg = f"[{context}] {message}" if context else message
      self.logger.warning(msg)

   def log_debug(self, message, context=None):
      """Log a debug message, optionally with context"""
      msg = f"[{context}] {message}" if context else message
      self.logger.debug(msg)
