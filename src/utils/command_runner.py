import subprocess
import logging
from typing import List
import os
import platform

class CommandRunner:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    def detect_os(self) -> str:
        os_name = (platform.system()).lower()
        if "windows" in os_name :
            return "Windows"
        elif  "darwin" in os_name:
            return "macOS"
        elif  "linux" in os_name:
            return "Linux"
        else:
            raise Exception(f"Unsupported operating system: {os_name}")
    def run_command(self, command: List[str], error_message: str = "Command failed"):
        """Run shell command with error handling"""
        self.os_type = self.detect_os()
        if self.os_type == "Windows":
            full_command = ["powershell"] + command
        else:
            full_command = command
        try:
            result = subprocess.run(
                full_command, 
                check=True, 
                capture_output=True, 
                text=True
            )
            self.logger.info(f"Executed: {' '.join(command)}")
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"{error_message}. Error: {e.stderr}")
            raise