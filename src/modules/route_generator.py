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
        """Update index.js to include new route"""
        try:
            # Read current index.js
            with open('index.js', 'r') as f:
                content = f.read()
            
            # Add route import if not exists
            if f"const {model_var}Routes = require('./routes/{model_var}.routes')" not in content:
                # Find the last import statement
                import_line_index = content.rfind('require(')
                last_import_end = content.find('\n', import_line_index)
                
                # Insert new import
                content = (
                    content[:last_import_end+1] + 
                    f"const {model_var}Routes = require('./routes/{model_var}.routes');\n" + 
                    content[last_import_end+1:]
                )
            
            # Add route use if not exists
            if f"app.use('/{model_var}s', {model_var}Routes)" not in content:
                # Find the basic route
                basic_route_index = content.find("app.use(\"/\", (req, res) => {")
                
                # Insert new route use
                content = (
                    content[:basic_route_index] + 
                    f"// {model_name} Routes\n" +
                    f"app.use('/{model_var}s', {model_var}Routes);\n\n" + 
                    content[basic_route_index:]
                )
            
            # Write updated content
            with open('index.js', 'w') as f:
                f.write(content)
            
            print(f"✅ Updated index.js to include {model_name} routes")
        except Exception as e:
            print(f"Failed to update index.js: {e}")