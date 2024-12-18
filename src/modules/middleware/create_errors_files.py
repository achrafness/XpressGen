import os
import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ErrorClassesGenerator:
    """Class to create custom error classes for API errors."""
    
    def create_errors_directory(self):
        """Create the errors directory if it doesn't exist."""
        os.makedirs('errors', exist_ok=True)
        logger.info("✅ Errors directory created successfully")

    def create_custom_api_error(self):
        """Create the base CustomAPIError class file."""
        with open('errors/custom-api.js', 'w') as file:
            file.write("""class CustomAPIError extends Error {
  constructor(message) {
    super(message);
    this.name = 'CustomAPIError';
  }
}

module.exports = CustomAPIError;
""")
        logger.info("✅ Custom API Error base class created successfully")

    def create_not_found_error(self):
        """Create the NotFoundError class file."""
        with open('errors/not-found.js', 'w') as file:
            file.write("""const { StatusCodes } = require('http-status-codes');
const CustomAPIError = require('./custom-api');

class NotFoundError extends CustomAPIError {
  constructor(message) {
    super(message);
    this.name = 'NotFoundError';
    this.statusCode = StatusCodes.NOT_FOUND;
  }
}

module.exports = NotFoundError;
""")
        logger.info("✅ Not Found Error class created successfully")

    def create_unauthenticated_error(self):
        """Create the UnauthenticatedError class file."""
        with open('errors/unauthenticated.js', 'w') as file:
            file.write("""const { StatusCodes } = require('http-status-codes');
const CustomAPIError = require('./custom-api');

class UnauthenticatedError extends CustomAPIError {
  constructor(message) {
    super(message);
    this.name = 'UnauthenticatedError';
    this.statusCode = StatusCodes.UNAUTHORIZED;
  }
}

module.exports = UnauthenticatedError;
""")
        logger.info("✅ Unauthenticated Error class created successfully")

    def create_unauthorized_error(self):
        """Create the UnauthorizedError class file."""
        with open('errors/unauthorized.js', 'w') as file:
            file.write("""const { StatusCodes } = require('http-status-codes');
const CustomAPIError = require('./custom-api');

class UnauthorizedError extends CustomAPIError {
  constructor(message) {
    super(message);
    this.name = 'UnauthorizedError';
    this.statusCode = StatusCodes.FORBIDDEN;
  }
}

module.exports = UnauthorizedError;
""")
        logger.info("✅ Unauthorized Error class created successfully")

    def create_bad_request_error(self):
        """Create the BadRequestError class file."""
        with open('errors/bad-request.js', 'w') as file:
            file.write("""const { StatusCodes } = require('http-status-codes');
const CustomAPIError = require('./custom-api');

class BadRequestError extends CustomAPIError {
  constructor(message) {
    super(message);
    this.name = 'BadRequestError';
    this.statusCode = StatusCodes.BAD_REQUEST;
  }
}

module.exports = BadRequestError;
""")
        logger.info("✅ Bad Request Error class created successfully")

    def create_errors_index(self):
        """Create the index file for exporting all error classes."""
        with open('errors/index.js', 'w') as file:
            file.write("""const CustomAPIError = require('./custom-api');
const UnauthenticatedError = require('./unauthenticated');
const NotFoundError = require('./not-found');
const BadRequestError = require('./bad-request');
const UnauthorizedError = require('./unauthorized');

module.exports = {
  CustomAPIError,
  UnauthenticatedError,
  NotFoundError,
  BadRequestError,
  UnauthorizedError,
};
""")
        logger.info("✅ Errors index file created successfully")

    def generate_error_classes(self):
        """Orchestrate the creation of error classes and directory."""
        self.create_errors_directory()
        self.create_custom_api_error()
        self.create_not_found_error()
        self.create_unauthenticated_error()
        self.create_unauthorized_error()
        self.create_bad_request_error()
        self.create_errors_index()
        logger.info("✅ All error classes created successfully")

