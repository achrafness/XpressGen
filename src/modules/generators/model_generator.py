import os
from typing import Dict, Any, List
from InquirerPy import inquirer
import re


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
        # Ensure the first letter of model name is uppercase
        model_name = model_name.capitalize()
        
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
        elif model_info['db_type'] == 'postgresql':
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
        """Generate Sequelize PostgreSQL model in modern JavaScript format"""
        model_name = model_info['name']
        model_var = model_name.lower()

        # Begin model content
        model_content = f"""const {{ DataTypes }} = require('sequelize');
    const sequelize = require("../db/connect");
    const {model_name} = sequelize.define('{model_name}', {{
    """

        # Add model attributes
        for attr in model_info['attributes']:
            # Map type to Sequelize DataTypes
            type_mapping = {
                'VARCHAR': 'DataTypes.STRING',
                'INTEGER': 'DataTypes.INTEGER',
                'BOOLEAN': 'DataTypes.BOOLEAN',
                'TIMESTAMP': 'DataTypes.DATE',
                'UUID': 'DataTypes.UUID',
                'TEXT': 'DataTypes.TEXT'
            }
            attr_type = type_mapping.get(attr['type'], 'DataTypes.STRING')

            # Begin attribute definition
            attr_def = f"    {attr['name']}: {{\n"
            attr_def += f"        type: {attr_type},\n"

            # Add constraints and validations
            constraints = []
            
            # Required/Nullable
            if attr['required']:
                constraints.append("allowNull: false")
            else:
                constraints.append("allowNull: true")
            
            # Unique
            if attr['unique']:
                constraints.append("unique: true")
            
            # Default value
            if attr.get('default') is not None:
                default_value = f"'{attr['default']}'" if attr['type'] in ['VARCHAR', 'TEXT'] else attr['default']
                constraints.append(f"defaultValue: {default_value}")
            
            # Length validation for string types
            if attr['type'] in ['VARCHAR', 'TEXT']:
                constraints.append("validate: {\n            len: [3, 255]\n        }")

            # Add constraints to attribute definition
            if constraints:
                attr_def += "        " + ",\n        ".join(constraints) + "\n"
            
            attr_def += "    },\n"
            model_content += attr_def

        # Close model definition with additional options
        model_content += f"""}}, {{
        timestamps: true,
        paranoid: true, // Soft delete
        tableName: '{model_var}s'
    }});

    module.exports = {model_name};
    """

        # Write model file
        model_filename = f"models/{model_var}.model.js"
        with open(model_filename, 'w') as f:
            f.write(model_content)
        
        print(f"✅ PostgreSQL Model {model_name} created successfully")
        return model_filename
    
