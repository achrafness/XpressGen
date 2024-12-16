import os
from typing import List, Dict, Any
from InquirerPy import inquirer

class ModelGenerator:
    def __init__(self):
        self.MONGOOSE_TYPES = [
            'String', 'Number', 'Date', 'Boolean', 'ObjectId', 
            'Mixed', 'Array', 'Buffer', 'Decimal128'
        ]

    def create_schema(self) -> Dict[str, Any]:
        """Interactive schema creation"""
        # Get model name
        model_name = inquirer.text(
            message="Enter the name of the model (singular, PascalCase):"
        ).execute()

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
                choices=self.MONGOOSE_TYPES
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
            'attributes': attributes
        }

    def generate_model(self, model_info: Dict[str, Any]) -> str:
        """Generate Mongoose model"""
        # Ensure models directory exists
        os.makedirs('models', exist_ok=True)
        
        model_name = model_info['name']
        
        # Construct schema
        schema_content = f"""const mongoose = require('mongoose');

const {model_name}Schema = new mongoose.Schema({{
"""
        for attr in model_info['attributes']:
            # Construct type definition
            type_def = f"    {attr['name']}: {{\n"
            type_def += f"        type: {attr['type']},\n"
            
            if attr['required']:
                type_def += "        required: true,\n"
            
            if attr['unique']:
                type_def += "        unique: true,\n"
            
            if attr['default'] is not None:
                # Handle different types of defaults
                if attr['type'] == 'String':
                    type_def += f"        default: '{attr['default']}',\n"
                elif attr['type'] in ['Number', 'Boolean']:
                    type_def += f"        default: {attr['default']},\n"
                else:
                    type_def += f"        default: {attr['default']},\n"
            
            type_def += "    },\n"
            schema_content += type_def

        schema_content += f"""    {{
    timestamps: true
}});

module.exports = mongoose.model('{model_name}', {model_name}Schema);
"""

        # Write model file
        model_filename = f"models/{model_name.lower()}.model.js"
        with open(model_filename, 'w') as f:
            f.write(schema_content)
        
        print(f"✅ Model {model_name} created successfully")
        return model_filename