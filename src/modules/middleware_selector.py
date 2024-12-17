import os
import subprocess
import sys
from typing import List, Tuple
from dataclasses import dataclass

from InquirerPy import inquirer

@dataclass
class MiddlewareOption:
    package: str
    import_code: str
    use_code: str = None
    description: str = ""
    dev_dependency: bool = False

class MiddlewareSelector:
    def __init__(self):
        # Initialize the optional middleware with detailed information
        self.OPTIONAL_MIDDLEWARE = [
            MiddlewareOption(
                package='cors',
                import_code="const cors = require('cors');",
                use_code="app.use(cors());",
                description="Enables Cross-Origin Resource Sharing (CORS)"
            ),
            MiddlewareOption(
                package='helmet',
                import_code="const helmet = require('helmet');",
                use_code="app.use(helmet());",
                description="Sets various HTTP headers to secure the app"
            ),
            MiddlewareOption(
                package='morgan',
                import_code="const morgan = require('morgan');",
                use_code="app.use(morgan('dev'));",
                description="HTTP request logger middleware for Node.js"
            ),
            MiddlewareOption(
                package='express-rate-limit',
                import_code="const rateLimit = require('express-rate-limit');",
                use_code="app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));",
                description="To limit repeated requests to public APIs"
            ),
            MiddlewareOption(
                package='body-parser',
                import_code="const bodyParser = require('body-parser');",
                use_code="app.use(bodyParser.json());",
                description="Parse incoming request bodies in a middleware"
            ),
            MiddlewareOption(
                package='compression',
                import_code="const compression = require('compression');",
                use_code="app.use(compression());",
                description="Middleware to compress response bodies"
            ),
            MiddlewareOption(
                package='cookie-parser',
                import_code="const cookieParser = require('cookie-parser');",
                use_code="app.use(cookieParser());",
                description="Parse Cookie header and populate req.cookies"
            ),
            MiddlewareOption(
                package='express-session',
                import_code="const session = require('express-session');",
                use_code="app.use(session({ secret: 'secret', resave: false, saveUninitialized: true }));",
                description="For handling sessions in Express apps"
            ),
            MiddlewareOption(
                package='passport',
                import_code="const passport = require('passport');",
                use_code="app.use(passport.initialize());",
                description="Authentication middleware"
            ),
            MiddlewareOption(
                package='express-validator',
                import_code="const { body, validationResult } = require('express-validator');",
                use_code="// Use validator in routes, e.g., [body('email').isEmail()]",
                description="For data validation in middleware"
            ),
            MiddlewareOption(
                package='multer',
                import_code="const multer = require('multer');",
                use_code="const upload = multer({ dest: 'uploads/' });",
                description="Middleware for handling `multipart/form-data`"
            ),
            MiddlewareOption(
                package='swagger-ui-express',
                import_code="const swaggerUi = require('swagger-ui-express');",
                use_code="app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));",
                description="For serving Swagger API documentation"
            ),
        ]

    def select_middleware(self) -> Tuple[List[str], List[str], List[str]]:
        """Interactive middleware setup"""
        selected_middleware = []
        
        for middleware in self.OPTIONAL_MIDDLEWARE:
            include = inquirer.select(
                message=f"Add {middleware.package}? ({middleware.description})",
                choices=['Yes', 'No'],
                default='No'
            ).execute()
            
            if include == 'Yes':
                selected_middleware.append(middleware)
        
        return (
            [mw.import_code for mw in selected_middleware if mw.import_code],
            [mw.use_code for mw in selected_middleware if mw.use_code],
            [mw.package for mw in selected_middleware if mw.package]
        )

    def install_packages(self, packages: List[str], dev: bool = False):
        """
        Install selected packages using npm
        
        Args:
            packages (List[str]): List of packages to install
            dev (bool, optional): Install as dev dependencies. Defaults to False.
        """
        if not packages:
            print("No packages selected for installation.")
            return

        # Ensure npm is installed
        try:
            subprocess.run(['npm', '--version'], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            print("npm is not installed. Please install Node.js and npm.")
            return

        # Prepare installation command
        install_cmd = ['npm', 'install']
        if dev:
            install_cmd.append('-D')
        
        # Add packages to the command
        install_cmd.extend(packages)

        # Confirm installation
        confirm = inquirer.select(
            message=f"Install {'dev ' if dev else ''}packages: {', '.join(packages)}?",
            choices=['Yes', 'No'],
            default='Yes'
        ).execute()

        if confirm == 'Yes':
            try:
                print(f"Installing {' '.join(packages)}...")
                result = subprocess.run(install_cmd, capture_output=True, text=True, check=True)
                print("✅ Packages installed successfully!")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"❌ Error installing packages: {e}")
                print(e.stderr)

    def full_middleware_setup(self):
        """
        Complete middleware setup process:
        1. Select middleware
        2. Install packages
        3. Update index.js with imports and uses
        """
        # Select middleware
        imports, uses, packages = self.select_middleware()

        if packages:
            # Option to install as dev or production dependency
            dep_type = inquirer.select(
                message="Install packages as development or production dependencies?",
                choices=['Production', 'Development'],
                default='Production'
            ).execute()

            # Install packages
            self.install_packages(
                packages, 
                dev=(dep_type == 'Development')
            )

        return imports, uses, packages

