import os
import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MiddlewareGenerator:
    """Class to create Not Found and Error Handler middleware files."""

    def create_middleware_directory(self):
        """Create the middleware directory if it doesn't exist."""
        os.makedirs('middleware', exist_ok=True)
        logger.info("✅ Middleware directory created successfully")

    def create_not_found_middleware(self):
        """Create the Not Found middleware file."""
        with open('middleware/not-found.js', 'w') as file:
            file.write("""const { StatusCodes } = require('http-status-codes');

const notFound = (req, res) => {
  res.status(StatusCodes.NOT_FOUND).json({
    error: 'Route Not Found',
    path: req.path
  });
};

module.exports = notFound;
""")
        logger.info("✅ Not Found middleware file created successfully")

    def create_error_handler_middleware(self):
        """Create the Error Handler middleware file."""
        with open('middleware/error-handler.js', 'w') as file:
            file.write("""const { StatusCodes } = require('http-status-codes');

const errorHandlerMiddleware = (err, req, res, next) => {
  console.error(err);  // Log the full error for server-side tracking
  
  const customError = {
    statusCode: err.statusCode || StatusCodes.INTERNAL_SERVER_ERROR,
    message: err.message || 'Something went wrong, please try again later'
  };

  // Specific error type handling
  if (err.name === 'ValidationError') {
    customError.message = Object.values(err.errors)
      .map(item => item.message)
      .join(', ');
    customError.statusCode = StatusCodes.BAD_REQUEST;
  }

  if (err.code === 11000) {
    customError.message = `Duplicate value for ${Object.keys(err.keyValue)} field`;
    customError.statusCode = StatusCodes.CONFLICT;
  }

  return res.status(customError.statusCode).json({
    error: customError.message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

module.exports = errorHandlerMiddleware;
""")
        logger.info("✅ Error Handler middleware file created successfully")

    def create_middleware_files(self):
        """Orchestrate the creation of middleware directory and files."""
        self.create_middleware_directory()
        self.create_not_found_middleware()
        self.create_error_handler_middleware()
        logger.info("✅ All middleware files created successfully")

# Example usage
if __name__ == "__main__":
    generator = MiddlewareGenerator()
    generator.create_middleware_files()
