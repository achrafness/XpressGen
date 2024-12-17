import os

class RouteGenerator:
    def generate_routes(self, model_info: dict) -> str:
        """Generate routes for the model"""
        # Ensure routes directory exists
        os.makedirs('routes', exist_ok=True)
        
        model_name = model_info['name']
        model_var = model_name.lower()
        
        routes_content = f"""const express = require('express');
const router = express.Router();
const {{
    create{model_name},
    get{model_name}s,
    get{model_name}ById,
    update{model_name},
    delete{model_name}
}} = require('../controllers/{model_var}.controller');

// Routes for {model_name}
router.route('/')
    .post(create{model_name})
    .get(get{model_name}s);

router.route('/:id')
    .get(get{model_name}ById)
    .patch(update{model_name})
    .delete(delete{model_name});

module.exports = router;
"""
        
        # Write routes file
        routes_filename = f"routes/{model_var}.routes.js"
        with open(routes_filename, 'w') as f:
            f.write(routes_content)
        
        print(f"✅ Routes {model_name} created successfully")
        
        return routes_filename
    def update_index_routes(self, model_name: str, model_var: str):
        """
        Update index.js to include new route with improved parsing and insertion
        
        This method handles multiple scenarios:
        1. Adding imports when no route imports exist
        2. Preventing duplicate imports
        3. Inserting routes in the correct section
        4. Handling different file structures
        """
        try:
            # Read current index.js
            with open('index.js', 'r') as f:
                content = f.readlines()
            
            # Prepare route import and use statements
            route_import = f"const {model_var}Routes = require('./routes/{model_var}.routes');"
            route_use = f"app.use('/api/v1/{model_var}s', {model_var}Routes);"
            
            # Find indices for route imports and route uses
            route_import_indices = [
                i for i, line in enumerate(content) 
                if '// start route import' in line or '// end route import' in line
            ]
            route_use_indices = [
                i for i, line in enumerate(content) 
                if '// routes' in line
            ]
            
            # Handle route imports
            if route_import_indices:
                # Check if import already exists
                if not any(route_import in line for line in content):
                    content.insert(route_import_indices[0] + 1, route_import + '\n')
            else:
                # If no route import section exists, add it near the top of imports
                import_section = [
                    i for i, line in enumerate(content) 
                    if re.match(r'^(const|require)\s', line.strip())
                ]
                if import_section:
                    content.insert(import_section[-1] + 1, '\n// start route import\n')
                    content.insert(import_section[-1] + 2, route_import + '\n')
                    content.insert(import_section[-1] + 3, '// end route import\n')
            
            # Handle route uses
            if route_use_indices:
                # Check if route use already exists
                if not any(route_use in line for line in content):
                    content.insert(route_use_indices[0] + 1, f"// {model_name} Routes\n")
                    content.insert(route_use_indices[0] + 2, route_use + '\n')
            else:
                # If no routes section, add near the end before server start
                server_start_indices = [
                    i for i, line in enumerate(content) 
                    if 'app.listen(' in line or 'server.listen(' in line
                ]
                if server_start_indices:
                    content.insert(server_start_indices[0], '\n// routes\n')
                    content.insert(server_start_indices[0] + 1, route_use + '\n')
                else:
                    # Fallback: add at the end
                    content.append('\n// routes\n')
                    content.append(route_use + '\n')
            
            # Write updated content
            with open('index.js', 'w') as f:
                f.writelines(content)
            
            print(f"✅ Updated index.js to include {model_name} routes")
        
        except Exception as e:
            print(f"Failed to update index.js: {e}")
            raise