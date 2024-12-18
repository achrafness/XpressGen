def generate_index_js(
    middleware_imports: list = [],
    middleware_uses: list = [],
    use_db: bool = True,
    db_type: str = "mongodb"
) -> str:
    """Generate index.js content with database support (MongoDB or PostgreSQL)."""
    
    # Default DB connection variables
    db_import = ""
    db_connection = ""

    # Add database connection logic
    if use_db:
        if db_type.lower() == "mongodb":
            db_import = 'const connectDB = require("./db/connect");'
            db_connection = "await connectDB(process.env.MONGO_URL);"
        elif db_type.lower() == "postgresql":
            db_import = 'const sequelize = require("./db/connect");'
            db_connection = """\
await sequelize.authenticate();
await sequelize.sync();
"""
        else:
            raise ValueError("Invalid db_type. Choose 'mongodb' or 'postgres'.")

    # Generate the final index.js content
    return f"""require('dotenv').config();
require("express-async-errors");

// middleware 
{chr(10).join(middleware_imports)}

const express = require("express");
const app = express();

{db_import}

// start route import



// Middleware uses
{chr(10).join(middleware_uses)}

app.use(express.json());

// routes 



// Basic route
app.get("/", (req, res) => {{
  res.json({{
    "message": "Welcome to the Express API",
    "timestamp": new Date().toISOString()
  }});
}});



// Not Found Middleware
const notFound = require("./middleware/not-found");
app.use(notFound);

// Error Handler Middleware
const errorHandler = require("./middleware/error-handler");
app.use(errorHandler);

const port = process.env.PORT || 5000;

const start = async () => {{
  try {{
    console.log("Connecting to the database...")
    {db_connection}
    console.log("{db_type.capitalize()} connection established.");
    app.listen(port, () => {{
      console.log(`Server is listening on port ${{port}}...`);
      console.log(`Environment: ${{process.env.NODE_ENV || 'development'}}`);
    }});
  }} catch (error) {{
    console.error("Failed to start server:", error);
    process.exit(1);
  }}
}};

start();
"""
