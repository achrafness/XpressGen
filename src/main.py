#!/usr/bin/env python3
import sys
from core.project_initializer import ProjectInitializer

def main():
    """
    Entry point for the Express.js project generator.
    Initializes the project setup process.
    """
    try:
        project_setup = ProjectInitializer()
        project_setup.setup_project()
    
    except Exception as e:
        print(f"Error during project setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()