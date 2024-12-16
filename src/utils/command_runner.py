import subprocess
import logging
from typing import List

class CommandRunner:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def run_command(self, command: List[str], error_message: str = "Command failed"):
        """Run shell command with error handling"""
        try:
            result = subprocess.run(
                command, 
                check=True, 
                capture_output=True, 
                text=True
            )
            self.logger.info(f"Executed: {' '.join(command)}")
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"{error_message}. Error: {e.stderr}")
            raise