import os
from typing import Dict, Any

class ControllerGenerator:
    def generate_controller(self, model_info: Dict[str, Any]) -> str:
        """Generate CRUD controller for MongoDB or PostgreSQL"""
        # Ensure controllers directory exists
        os.makedirs('controllers', exist_ok=True)
        
        model_name = model_info['name']
        model_var = model_name.lower()
        db_type = model_info.get('db_type', 'mongodb')
        
        if db_type == 'mongodb':
            controller_content = f"""const {model_name} = require('../models/{model_var}.model');
const {{ StatusCodes }} = require('http-status-codes');

// Create new {model_var}
const create{model_name} = async (req, res) => {{
    try {{
        const {model_var} = await {model_name}.create(req.body);
        res.status(StatusCodes.CREATED).json({{{model_var}}});
    }} catch (error) {{
        res.status(StatusCodes.BAD_REQUEST).json({{ error: error.message }});
    }}
}};

// Get all {model_var}s
const get{model_name}s = async (req, res) => {{
    try {{
        const {model_var}s = await {model_name}.find({{}});
        res.status(StatusCodes.OK).json({{{model_var}s}});
    }} catch (error) {{
        res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({{ error: error.message }});
    }}
}};

// Get single {model_var} by ID
const get{model_name}ById = async (req, res) => {{
    try {{
        const {model_var} = await {model_name}.findById(req.params.id);
        if (!{model_var}) {{
            return res.status(StatusCodes.NOT_FOUND).json({{ message: '{model_name} not found' }});
        }}
        res.status(StatusCodes.OK).json({{{model_var}}});
    }} catch (error) {{
        res.status(StatusCodes.BAD_REQUEST).json({{ error: error.message }});
    }}
}};

// Update {model_var}
const update{model_name} = async (req, res) => {{
    try {{
        const {model_var} = await {model_name}.findByIdAndUpdate(
            req.params.id, 
            req.body, 
            {{ new: true, runValidators: true }}
        );
        if (!{model_var}) {{
            return res.status(StatusCodes.NOT_FOUND).json({{ message: '{model_name} not found' }});
        }}
        res.status(StatusCodes.OK).json({{{model_var}}});
    }} catch (error) {{
        res.status(StatusCodes.BAD_REQUEST).json({{ error: error.message }});
    }}
}};

// Delete {model_var}
const delete{model_name} = async (req, res) => {{
    try {{
        const {model_var} = await {model_name}.findByIdAndDelete(req.params.id);
        if (!{model_var}) {{
            return res.status(StatusCodes.NOT_FOUND).json({{ message: '{model_name} not found' }});
        }}
        res.status(StatusCodes.OK).json({{ message: '{model_name} deleted successfully' }});
    }} catch (error) {{
        res.status(StatusCodes.BAD_REQUEST).json({{ error: error.message }});
    }}
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
            controller_content = f"""const db = require('../models');
const { StatusCodes } = require('http-status-codes');
const { {model_name} } = db;

// Create new {model_var}
const create{model_name} = async (req, res) => {{
    try {{
        const {model_var} = await {model_name}.create(req.body);
        res.status(StatusCodes.CREATED).json({{{model_var}}});
    }} catch (error) {{
        res.status(StatusCodes.BAD_REQUEST).json({{ error: error.message }});
    }}
}};

// Get all {model_var}s
const get{model_name}s = async (req, res) => {{
    try {{
        const {model_var}s = await {model_name}.findAll();
        res.status(StatusCodes.OK).json({{{model_var}s}});
    }} catch (error) {{
        res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({{ error: error.message }});
    }}
}};

// Get single {model_var} by ID
const get{model_name}ById = async (req, res) => {{
    try {{
        const {model_var} = await {model_name}.findByPk(req.params.id);
        if (!{model_var}) {{
            return res.status(StatusCodes.NOT_FOUND).json({{ message: '{model_name} not found' }});
        }}
        res.status(StatusCodes.OK).json({{{model_var}}});
    }} catch (error) {{
        res.status(StatusCodes.BAD_REQUEST).json({{ error: error.message }});
    }}
}};

// Update {model_var}
const update{model_name} = async (req, res) => {{
    try {{
        const [updated] = await {model_name}.update(req.body, {{
            where: {{ id: req.params.id }},
            returning: true
        }});
        if (!updated) {{
            return res.status(StatusCodes.NOT_FOUND).json({{ message: '{model_name} not found' }});
        }}
        const updated{model_name} = await {model_name}.findByPk(req.params.id);
        res.status(StatusCodes.OK).json({{{model_var}: updated{model_name}}});
    }} catch (error) {{
        res.status(StatusCodes.BAD_REQUEST).json({{ error: error.message }});
    }}
}};

// Delete {model_var}
const delete{model_name} = async (req, res) => {{
    try {{
        const deleted = await {model_name}.destroy({{ where: {{ id: req.params.id }} }});
        if (!deleted) {{
            return res.status(StatusCodes.NOT_FOUND).json({{ message: '{model_name} not found' }});
        }}
        res.status(StatusCodes.OK).json({{ message: '{model_name} deleted successfully' }});
    }} catch (error) {{
        res.status(StatusCodes.BAD_REQUEST).json({{ error: error.message }});
    }}
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
