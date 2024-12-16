from typing import List, Tuple
from dataclasses import dataclass

from InquirerPy import inquirer

@dataclass
class MiddlewareOption:
    package: str
    import_code: str
    use_code: str = None
    description: str = ""

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
                package='validator',
                import_code="const validator = require('express-validator');",
                use_code="app.use(validator());",
                description="For data validation in middleware"
            ),
            MiddlewareOption(
                package='multer',
                import_code="const multer = require('multer');",
                use_code="app.use(multer({ dest: 'uploads/' }).single('file'));",
                description="Middleware for handling `multipart/form-data`"
            ),
            MiddlewareOption(
                package='swagger-ui-express',
                import_code="const swaggerUi = require('swagger-ui-express');",
                use_code="app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));",
                description="For serving Swagger API documentation"
            ),
        ]

    def select_middleware(self) -> Tuple[List[str], List[str]]:
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
        
        imports = [mw.import_code for mw in selected_middleware if mw.import_code]
        uses = [mw.use_code for mw in selected_middleware if mw.use_code]
        
        return imports, uses
