import os
import sys

from utils.command_runner import CommandRunner
from utils.logger import setup_logger
from modules.middleware_selector import MiddlewareSelector
from modules.database_selector import DatabaseSelector
from modules.model_generator import ModelGenerator
from modules.route_generator import RouteGenerator
from modules.controller_generator import ControllerGenerator
from modules.create_middleware_files import MiddlewareGenerator
from templates.index_js import generate_index_js
from templates.env_template import generate_env_template
from templates.readme_template import generate_readme_template

class ProjectInitializer:
    def __init__(self):
        self.logger = setup_logger()
        self.command_runner = CommandRunner(self.logger)
        self.middleware_selector = MiddlewareSelector()
        self.database_selector = DatabaseSelector(self.command_runner)
        self.model_generator = ModelGenerator()
        self.route_generator = RouteGenerator()
        self.controller_generator = ControllerGenerator()

        self.CORE_DEPENDENCIES = [
            'express', 
            'dotenv', 
            'express-async-errors', 
            'http-status-codes'
        ]

    def setup_project(self):
        """Main project setup method"""
        try:
            # Project initialization
            # self.initialize_project()
            # self.create_project_structure()
            


            # Database setup can reterun none or mongodb or postgress 
            database_config = self.database_selector.select_and_setup_database()
            self.use_db = database_config is not None
            self.db_type = database_config.lower() if self.use_db else None   
            
            # Middleware setup
            # middleware_imports, middleware_uses = self.middleware_selector.select_middleware()
            
            # Create dotenv files
            # self.create_env_file()
            
            # Create middleware files
            # self.create_middleware_files()
            
            # Create index.js file
            # self.create_index_file()
            

            # Model, route, and controller generation
            self.interactive_model_generation()

            # Git initialization
            # self.create_readme()  wait after db question
            self.initialize_git()

            self.logger.info("🎉 Express.js project setup completed successfully!")

        except Exception as e:
            self.logger.error(f"Setup failed: {e}")
            sys.exit(1)

    def initialize_project(self):
        """
        Initialize npm project and install core dependencies 
            1- npm init -y
            2- install core dependencies
            3- install dev dependencies
        """
        self.logger.info("🚀 Initializing Express.js Project Setup")
        
        # Initialize npm project
        self.command_runner.run_command(
            ['npm', 'init', '-y'], 
            "Failed to initialize npm project"
        )
        # Install core dependencies
        for dep in self.CORE_DEPENDENCIES:
            self.command_runner.run_command(
                ['npm', 'install', dep], 
                f"Failed to install {dep}"
            )
        
        
        # Install dev dependencies
        self.command_runner.run_command(
            ['npm', 'install', 'nodemon', '--save-dev'], 
            "Failed to install nodemon"
        )

    def create_project_structure(self):
        """Create basic project directories"""
        directories = [
            'controllers', 'models', 'routes', 'middleware', 'db'
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def create_env_file(self):
        """Create .env file with default configurations"""

        env_content = generate_env_template(use_db=self.use_db , db_type=self.db_type)
        try:
            with open('.env', 'w') as file:
                file.write(env_content)
            self.logger.info("✅ .env file created successfully")
        except IOError as e:
            self.logger.error(f"Failed to create .env file: {e}")
            sys.exit(1)

    def create_index_file(self):
        """Create index.js with dynamic configuration"""
        index_content = generate_index_js(use_db=self.use_db , db_type=self.db_type)
        try:
            with open('index.js', 'w') as file:
                file.write(index_content)
            self.logger.info("✅ index.js file created successfully")
        except IOError as e:
            self.logger.error(f"Failed to create index.js: {e}")
            sys.exit(1)

    def create_middleware_files(self):
        """Create Not Found and Error Handler middleware files"""
        middleware_genrator = MiddlewareGenerator()
        middleware_genrator.create_middleware_files()

    def interactive_model_generation(self):
        """Interactive model, route, and controller generation"""
        if not self.use_db:
            self.logger.info("Skipping model, route, and controller generation")
            return
        while True:
            model_info = self.model_generator.create_schema(db_type=self.db_type)
            print(model_info)
            if not model_info:
                break
            print("done")
        #     # Generate model, controller, and routes
        #     model_file = self.model_generator.generate_model(model_info)
        #     controller_file = self.controller_generator.generate_controller(model_info)
        #     route_file = self.route_generator.generate_routes(model_info)

        #     # Update index.js with new routes
        #     self.route_generator.update_index_routes(
        #         model_info['name'], 
        #         model_info['name'].lower()
        #     )

    def create_readme(self):
        """Create a comprehensive README.md for the project"""
        readme_content = generate_readme_template()
        
        with open('README.md', 'w') as f:
            f.write(readme_content)
        
        self.logger.info("✅ README.md created successfully")

    def initialize_git(self):
        """Initialize git repository"""
        try:
            self.command_runner.run_command(['git', 'init'], "Failed to initialize git")
            self.command_runner.run_command(['git', 'add', '.'], "Failed to add files to git")
            self.command_runner.run_command(
                ['git', 'commit', '-m', 'Initial project setup'], 
                "Failed to commit initial setup"
            )
        except Exception as e:
            self.logger.warning(f"Git initialization failed: {e}")