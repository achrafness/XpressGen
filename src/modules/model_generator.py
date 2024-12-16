import os
from typing import Dict, Any, List
from InquirerPy import inquirer

class ModelGenerator:
    def __init__(self):
        # Types for both databases
        self.MONGOOSE_TYPES = [
            'String', 'Number', 'Date', 'Boolean', 'ObjectId',
            'Mixed', 'Array', 'Buffer', 'Decimal128'
        ]
        
        self.POSTGRES_TYPES = [
            'String', 'Integer', 'Float', 'Boolean', 'Date', 'DateTime'
        ]

    def create_schema(self, db_type: str = 'mongodb') -> Dict[str, Any]:
        """Interactive schema creation with database-specific type selection"""
        # Get model name
        model_name = inquirer.text(
            message="Enter the name of the model (singular, PascalCase):"
        ).execute()
        
        if not model_name.strip():
            print("Finish model creation.")
            return None
        # Select appropriate types based on database
        type_choices = self.MONGOOSE_TYPES if db_type == 'mongodb' else self.POSTGRES_TYPES
        
        # Collect schema attributes
        attributes = []
        while True:
            # Attribute name
            attr_name = inquirer.text(
                message="Enter attribute name (or 'done' to finish):"
            ).execute()
            
            if attr_name.lower() == 'done':
                break
            
            # Attribute type
            attr_type = inquirer.select(
                message=f"Select type for {attr_name}:",
                choices=type_choices
            ).execute()
            
            # Additional attribute options
            required = inquirer.confirm(
                message=f"Is {attr_name} required?",
                default=False
            ).execute()
            
            unique = inquirer.confirm(
                message=f"Should {attr_name} be unique?",
                default=False
            ).execute()
            
            # Default value (optional)
            default_choice = inquirer.select(
                message=f"Add a default value for {attr_name}?",
                choices=['No Default', 'Specify Default']
            ).execute()
            
            default_value = None
            if default_choice == 'Specify Default':
                default_value = inquirer.text(
                    message="Enter default value:"
                ).execute()
            
            attributes.append({
                'name': attr_name,
                'type': attr_type,
                'required': required,
                'unique': unique,
                'default': default_value
            })
        
        return {
            'name': model_name,
            'attributes': attributes,
            'db_type': db_type
        }

    def generate_model(self, model_info: Dict[str, Any]) -> str:
        """Generate model based on database type"""
        # Ensure models directory exists
        os.makedirs('models', exist_ok=True)
        
        # Dispatch to appropriate model generator
        if model_info['db_type'] == 'mongodb':
            return self._generate_mongoose_model(model_info)
        elif model_info['db_type'] == 'postgres':
            return self._generate_postgres_model(model_info)
        else:
            raise ValueError(f"Unsupported database type: {model_info['db_type']}")

    def _generate_mongoose_model(self, model_info: Dict[str, Any]) -> str:
        """Generate Mongoose model"""
        model_name = model_info['name']
        model_var = model_name.lower()
        
        # Construct schema
        schema_content = f"""const mongoose = require('mongoose');
const {model_name}Schema = new mongoose.Schema({{
"""
        for attr in model_info['attributes']:
            # Construct type definition
            type_def = f" {attr['name']}: {{\n"
            type_def += f" type: mongoose.Schema.Types.{attr['type']},\n"
            
            if attr['required']:
                type_def += " required: true,\n"
            
            if attr['unique']:
                type_def += " unique: true,\n"
            
            if attr['default'] is not None:
                # Handle different types of defaults
                if attr['type'] == 'String':
                    type_def += f" default: '{attr['default']}',\n"
                elif attr['type'] in ['Number', 'Boolean']:
                    type_def += f" default: {attr['default']},\n"
                else:
                    type_def += f" default: {attr['default']},\n"
            
            type_def += " },\n"
            schema_content += type_def
        
        schema_content += f""" }}, {{
 timestamps: true
}});
module.exports = mongoose.model('{model_name}', {model_name}Schema);
"""
        
        # Write model file
        model_filename = f"models/{model_var}.model.js"
        with open(model_filename, 'w') as f:
            f.write(schema_content)
        
        print(f"✅ Mongoose Model {model_name} created successfully")
        return model_filename

    def _generate_postgres_model(self, model_info: Dict[str, Any]) -> str:
        """Generate SQLAlchemy PostgreSQL model"""
        model_name = model_info['name']
        model_var = model_name.lower()
        
        # Construct SQLAlchemy model
        model_content = f"""from sqlalchemy import Column, {', '.join(attr['type'] for attr in model_info['attributes'])}, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class {model_name}(Base):
    __tablename__ = '{model_var}s'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
"""
        
        # Add model attributes
        for attr in model_info['attributes']:
            column_args = []
            if attr['required']:
                column_args.append('nullable=False')
            if attr['unique']:
                column_args.append('unique=True')
            
            # Add default value if specified
            if attr['default'] is not None:
                column_args.append(f"default='{attr['default']}'" if attr['type'] == 'String' else f"default={attr['default']}")
            
            # Construct column definition
            column_def = f"    {attr['name']} = Column({attr['type']}, {', '.join(column_args)})" if column_args else f"    {attr['name']} = Column({attr['type']})"
            model_content += column_def + '\n'
        
        # Write model file
        model_filename = f"models/{model_var}_model.py"
        with open(model_filename, 'w') as f:
            f.write(model_content)
        
        print(f"✅ PostgreSQL Model {model_name} created successfully")
        return model_filename