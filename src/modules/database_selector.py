import os
from InquirerPy import inquirer
from utils.command_runner import CommandRunner

class DatabaseSelector:
    def __init__(self, command_runner: CommandRunner):
        self.command_runner = command_runner
        self.database_options = {
            'MongoDB': self._setup_mongodb,
            'PostgreSQL': self._setup_postgresql
        }

    def select_and_setup_database(self):
        """Interactive database selection and setup"""
        # First, ask if a database is needed
        use_database = inquirer.select(
            message="Do you want to use a database in your project?",
            choices=['Yes', 'No'],
            default='No'
        ).execute()

        if use_database == 'No':
            print("Skipping database setup.")
            return None

        # If database is needed, choose which one
        database_type = inquirer.select(
            message="Select the database you want to use:",
            choices=list(self.database_options.keys()),
            default='MongoDB'
        ).execute()

        # return the type and useage of database or not
        if database_type in self.database_options:
            self.database_options[database_type]()
        return database_type

    def _setup_mongodb(self):
        """Setup MongoDB with Mongoose"""
        # Install Mongoose
        self.command_runner.run_command(
            ['npm', 'install', 'mongoose'], 
            "Failed to install Mongoose"
        )
        
        # Create db directory
        os.makedirs('db', exist_ok=True)
        
        # Create connection file
        mongodb_connection_content = """const mongoose = require("mongoose");

const connectDB = async (url) => {
  try {
    await mongoose.connect(url);
    console.log("MongoDB connection successful");
  } catch (error) {
    console.error("MongoDB connection failed:", error);
    process.exit(1);
  }
};

module.exports = connectDB;
"""
        with open('db/connect.js', 'w') as file:
            file.write(mongodb_connection_content)
        
        return {
            'type': 'MongoDB',
            'connection_file': 'db/connect.js',
            'dependencies': ['mongoose']
        }

    def _setup_postgresql(self):
        """Setup PostgreSQL with Sequelize"""
        # Install Sequelize and PostgreSQL driver
        self.command_runner.run_command(
            ['npm', 'install', 'sequelize', 'pg', 'pg-hstore'], 
            "Failed to install Sequelize and PostgreSQL dependencies"
        )
        
        # Create db directory
        os.makedirs('db', exist_ok=True)
        
        # Create connection file
        postgresql_connection_content = """const { Sequelize } = require('sequelize');

const connectDB = async (dbUrl) => {
  try {
    const sequelize = new Sequelize(dbUrl, {
      dialect: 'postgres',
      logging: false,
      dialectOptions: {
        ssl: process.env.NODE_ENV === 'production' ? {
          require: true,
          rejectUnauthorized: false
        } : false
      }
    });

    await sequelize.authenticate();
    console.log('PostgreSQL connection successful');
    return sequelize;
  } catch (error) {
    console.error('PostgreSQL connection failed:', error);
    process.exit(1);
  }
};

module.exports = connectDB;
"""
        with open('db/connect.js', 'w') as file:
            file.write(postgresql_connection_content)

        return {
            'type': 'PostgreSQL',
            'connection_file': 'db/connect.js',
            'dependencies': ['sequelize', 'pg', 'pg-hstore']
        }
