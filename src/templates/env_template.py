def generate_env_template(
    use_db=False,
    db_type="mongodb",
    port=5000,
    jwt_secret="your_jwt_secret_here",
    jwt_lifetime="1d",
) -> str:
    """
    Generate .env file content with optional database configurations.

    Parameters:
    - use_db (bool): Whether to include database configuration.
    - db_type (str): Type of database ('mongodb' or 'postgres').
    - port (int): Port for the server.
    - jwt_secret (str): Secret key for JWT.
    - jwt_lifetime (str): Lifetime of the JWT.

    Returns:
    - str: The generated .env file content.
    """
    env_content = f"""# Server Configuration
PORT={port}

# Security Configuration
JWT_SECRET={jwt_secret}
JWT_LIFETIME={jwt_lifetime}
"""

    if use_db:
        if db_type.lower() == "mongodb":
            env_content += "\n# MongoDB Configuration\nMONGO_URL=mongodb://localhost:27017/myapp\n"
        elif db_type.lower() == "postgresql":
            env_content += "\n# PostgreSQL Configuration\nPOSTGRES_URL=postgresql://user:password@localhost:5432/myapp\n"
        else:
            raise ValueError("Invalid db_type. Choose 'mongodb' or 'postgres'.")

    return env_content
