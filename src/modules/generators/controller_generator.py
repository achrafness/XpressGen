import os
from typing import Dict, Any

class ControllerGenerator:
    def generate_controller(self, model_info: Dict[str, Any]) -> str:
        """Generate CRUD controller for MongoDB or PostgreSQL with custom errors"""
        # Ensure controllers directory exists
        os.makedirs('controllers', exist_ok=True)
        
        model_name = model_info['name']
        model_var = model_name.lower()
        db_type = model_info.get('db_type', 'mongodb')
        
        # Generate attributes destructuring string
        attributes_list = model_info.get('attributes', [])
        attributes_destructure = ', '.join([attr['name'] for attr in attributes_list])
        
                # Generate required attribute validation
        required_attrs = [
            attr for attr in attributes_list 
            if attr.get('required', False)
        ]
        
        # Create required attributes validation code
        required_validation = "\n    ".join([
            f"if (!{attr['name']}) {{\n        throw new BadRequestError('{attr['name']} is required');\n    }}"
            for attr in required_attrs
        ])
        
        if db_type == 'mongodb':
            controller_content = f"""const {model_name} = require('../models/{model_var}.model');
const {{ StatusCodes }} = require('http-status-codes');
const {{ 
    BadRequestError, 
    NotFoundError, 
    CustomAPIError 
}} = require('../errors');

// Create new {model_var}
const create{model_name} = async (req, res) => {{
    const {{ {attributes_destructure} }} = req.body;
    
    // Validate required attributes
    {required_validation}
    
    const {model_var} = await {model_name}.create({{ {attributes_destructure} }});
    res.status(StatusCodes.CREATED).json({{{model_var}}});
}};

// Get all {model_var}s
const get{model_name}s = async (req, res) => {{
    const {model_var}s = await {model_name}.find({{}});
    res.status(StatusCodes.OK).json({{{model_var}s}});
}};

// Get single {model_var} by ID
const get{model_name}ById = async (req, res) => {{
    const {model_var} = await {model_name}.findById(req.params.id);
    if (!{model_var}) {{
        throw new NotFoundError('{model_name} not found');
    }}
    res.status(StatusCodes.OK).json({{{model_var}}});
}};

// Update {model_var}
const update{model_name} = async (req, res) => {{
    const {{ {attributes_destructure} }} = req.body;
    const {model_var} = await {model_name}.findByIdAndUpdate(
        req.params.id, 
        {{ {attributes_destructure} }}, 
        {{ new: true, runValidators: true }}
    );
    if (!{model_var}) {{
        throw new NotFoundError('{model_name} not found');
    }}
    res.status(StatusCodes.OK).json({{{model_var}}});
}};

// Delete {model_var}
const delete{model_name} = async (req, res) => {{
    const {model_var} = await {model_name}.findByIdAndDelete(req.params.id);
    if (!{model_var}) {{
        throw new NotFoundError('{model_name} not found');
    }}
    res.status(StatusCodes.OK).json({{ message: '{model_name} deleted successfully' }});
}};

module.exports = {{
    create{model_name},
    get{model_name}s,
    get{model_name}ById,
    update{model_name},
    delete{model_name}
}};
"""
        elif db_type == 'postgresql':
            controller_content = f"""const {model_name} = require('../models/{model_var}.model');
const {{ StatusCodes }} = require('http-status-codes');
const {{ 
    BadRequestError, 
    NotFoundError, 
    CustomAPIError 
}} = require('../errors');

// Create new {model_var}
const create{model_name} = async (req, res) => {{
    const {{ {attributes_destructure} }} = req.body;
    // Validate required attributes
    {required_validation}
    const {model_var} = await {model_name}.create({{ {attributes_destructure} }});
    res.status(StatusCodes.CREATED).json({{{model_var}}});
}};

// Get all {model_var}s
const get{model_name}s = async (req, res) => {{
    const {model_var}s = await {model_name}.findAll();
    res.status(StatusCodes.OK).json({{{model_var}s}});
}};

// Get single {model_var} by ID
const get{model_name}ById = async (req, res) => {{
    const {model_var} = await {model_name}.findByPk(req.params.id);
    if (!{model_var}) {{
        throw new NotFoundError('{model_name} not found');
    }}
    res.status(StatusCodes.OK).json({{{model_var}}});
}};

// Update {model_var}
const update{model_name} = async (req, res) => {{
    const {{ {attributes_destructure} }} = req.body;
    const [updated] = await {model_name}.update(
        {{ {attributes_destructure} }}, 
        {{
            where: {{ id: req.params.id }},
            returning: true
        }}
    );
    if (!updated) {{
        throw new NotFoundError('{model_name} not found');
    }}
    const updated{model_name} = await {model_name}.findByPk(req.params.id);
    res.status(StatusCodes.OK).json({{{model_var}: updated{model_name}}});
}};

// Delete {model_var}
const delete{model_name} = async (req, res) => {{
    const deleted = await {model_name}.destroy({{ where: {{ id: req.params.id }} }});
    if (!deleted) {{
        throw new NotFoundError('{model_name} not found');
    }}
    res.status(StatusCodes.OK).json({{ message: '{model_name} deleted successfully' }});
}};

module.exports = {{
    create{model_name},
    get{model_name}s,
    get{model_name}ById,
    update{model_name},
    delete{model_name}
}};
"""

        else:
            raise ValueError(f"Unsupported db_type: {db_type}")

        # Write controller file
        controller_filename = f"controllers/{model_var}.controller.js"
        with open(controller_filename, 'w') as f:
            f.write(controller_content)
        
        print(f"✅ Controller {model_name} created successfully")
        return controller_filename