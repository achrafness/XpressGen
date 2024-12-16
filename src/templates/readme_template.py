def generate_readme_template() -> str:
    """Generate .env file content"""
    return """# Express.js Project Setup
    ## Project Structure
    ```
    project-root/
    │
    ├── controllers/       # Business logic
    ├── models/            # Mongoose models
    ├── middleware/        # Custom middleware
    ├── routes/            # API route definitions
    ├── .env               # Environment variables
    ├── index.js           # Main application entry point
    └── README.md          # Project documentation
    ```

    ## Prerequisites
    - Node.js (v14+ recommended)
    - MongoDB

    ## Installation
    1. Clone the repository
    2. Install dependencies
    ```
    npm install
    ```

    ## Environment Variables
    Create a `.env` file with the following variables:
    - `PORT`: Server port (default: 5000)
    - `MONGO_URL`: MongoDB connection string
    - `JWT_SECRET`: Secret for JWT authentication

    ## Running the Application
    - Development mode: 
    ```
    npm run dev
    ```
    - Production mode:
    ```
    npm start
    ```

    ## API Endpoints
    Check individual route files for specific endpoint details.

    ## Middleware
    Includes security middleware:
    - Helmet
    - CORS
    - Rate Limiting
    - XSS Protection

    ## Contributing
    1. Fork the repository
    2. Create your feature branch
    3. Commit your changes
    4. Push to the branch
    5. Create a Pull Request
    """