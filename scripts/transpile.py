#!/usr/bin/env python3
"""
371 OS Core Engine Transpiler
Converts Python agent logic to TypeScript modules
"""

import os
import ast
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any

class OSEngineTranspiler:
    def __init__(self):
        self.source_dir = Path(".")
        self.output_dir = Path("dist")
        self.type_mappings = {
            'str': 'string',
            'int': 'number',
            'float': 'number',
            'bool': 'boolean',
            'list': 'Array',
            'dict': 'Record<string, any>',
            'Any': 'any'
        }
        
    def setup_output_structure(self):
        """Create the output directory structure"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
            
        # Create the folder structure we defined
        folders = [
            "agents",
            "core", 
            "data",
            "api",
            "utils",
            "types"
        ]
        
        for folder in folders:
            (self.output_dir / folder).mkdir(parents=True, exist_ok=True)
            
        print(f"✅ Created output structure in {self.output_dir}")

    def transpile_python_file(self, py_file: Path) -> Dict[str, Any]:
        """Transpile a single Python file to TypeScript"""
        print(f"🔄 Transpiling {py_file}")
        
        with open(py_file, 'r') as f:
            source_code = f.read()
            
        # Parse the Python AST
        tree = ast.parse(source_code)
        
        # Extract classes, functions, and metadata
        metadata = {
            'classes': [],
            'functions': [],
            'imports': [],
            'exports': []
        }
        
        ts_code = self.generate_typescript_header(py_file)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                ts_code += self.transpile_class(node)
                metadata['classes'].append(node.name)
                metadata['exports'].append(node.name)
                
            elif isinstance(node, ast.FunctionDef) and not self.is_method(node, tree):
                ts_code += self.transpile_function(node)
                metadata['functions'].append(node.name)
                metadata['exports'].append(node.name)
                
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                metadata['imports'].append(self.extract_import_info(node))
        
        ts_code += self.generate_typescript_exports(metadata['exports'])
        
        return {
            'typescript': ts_code,
            'metadata': metadata
        }

    def generate_typescript_header(self, py_file: Path) -> str:
        """Generate TypeScript file header with imports"""
        header = f"""/**
 * 371 OS Engine - {py_file.stem}
 * Auto-generated from Python source
 * DO NOT EDIT MANUALLY
 */

"""
        return header

    def transpile_class(self, node: ast.ClassDef) -> str:
        """Convert Python class to TypeScript class"""
        ts_class = f"\nexport class {node.name} {{\n"
        
        # Extract constructor and methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if item.name == '__init__':
                    ts_class += self.transpile_constructor(item)
                else:
                    ts_class += self.transpile_method(item)
                    
        ts_class += "}\n\n"
        return ts_class

    def transpile_function(self, node: ast.FunctionDef) -> str:
        """Convert Python function to TypeScript function"""
        args = [arg.arg for arg in node.args.args]
        args_str = ', '.join(f"{arg}: any" for arg in args)
        
        return f"""
export function {node.name}({args_str}): any {{
    // TODO: Implement {node.name} logic
    throw new Error('Function {node.name} not yet implemented');
}}

"""

    def transpile_constructor(self, node: ast.FunctionDef) -> str:
        """Convert Python __init__ to TypeScript constructor"""
        args = [arg.arg for arg in node.args.args if arg.arg != 'self']
        args_str = ', '.join(f"{arg}: any" for arg in args)
        
        return f"""    constructor({args_str}) {{
        // TODO: Implement constructor logic
    }}

"""

    def transpile_method(self, node: ast.FunctionDef) -> str:
        """Convert Python method to TypeScript method"""
        args = [arg.arg for arg in node.args.args if arg.arg != 'self']
        args_str = ', '.join(f"{arg}: any" for arg in args)
        
        return f"""    {node.name}({args_str}): any {{
        // TODO: Implement {node.name} logic
        throw new Error('Method {node.name} not yet implemented');
    }}

"""

    def generate_typescript_exports(self, exports: List[str]) -> str:
        """Generate export statements"""
        if not exports:
            return ""
            
        return f"\n// Exports\nexport {{ {', '.join(exports)} }};\n"

    def is_method(self, node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if function is a class method"""
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef):
                if node in parent.body:
                    return True
        return False

    def extract_import_info(self, node) -> Dict[str, Any]:
        """Extract import information for metadata"""
        if isinstance(node, ast.Import):
            return {'type': 'import', 'modules': [alias.name for alias in node.names]}
        elif isinstance(node, ast.ImportFrom):
            return {
                'type': 'from_import', 
                'module': node.module,
                'names': [alias.name for alias in node.names]
            }

    def determine_output_folder(self, py_file: Path) -> str:
        """Determine which output folder based on filename prefix"""
        name = py_file.stem
        
        if name.startswith('core_'):
            return 'core'
        elif name.startswith('agent_'):
            return 'agents'
        elif name.startswith('data_'):
            return 'data'
        elif name.startswith('api_'):
            return 'api'
        elif name.startswith('util_'):
            return 'utils'
        else:
            return 'core'  # Default fallback

    def create_package_json(self):
        """Create package.json for the transpiled engine"""
        package_json = {
            "name": "@371-minds/os-engine",
            "version": "1.0.0",
            "description": "371 OS Core Engine - Transpiled TypeScript modules",
            "main": "index.js",
            "types": "index.d.ts",
            "scripts": {
                "build": "tsc",
                "test": "jest"
            },
            "keywords": ["371-os", "ai", "agents", "typescript"],
            "author": "371 Minds",
            "license": "MIT",
            "devDependencies": {
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0"
            }
        }
        
        with open(self.output_dir / "package.json", 'w') as f:
            json.dump(package_json, f, indent=2)

    def create_index_file(self, all_metadata: Dict[str, Any]):
        """Create main index.ts file that exports everything"""
        index_content = """/**
 * 371 OS Engine - Main Entry Point
 * Auto-generated exports for all transpiled modules
 */

"""
        
        # Group exports by folder
        for folder in ['core', 'agents', 'data', 'api', 'utils']:
            folder_exports = []
            for file_name, metadata in all_metadata.items():
                if self.determine_output_folder(Path(file_name)) == folder:
                    folder_exports.extend(metadata['exports'])
            
            if folder_exports:
                index_content += f"// {folder.title()} exports\n"
                for export in folder_exports:
                    ts_file = file_name.replace('.py', '')
                    index_content += f"export {{ {export} }} from './{folder}/{ts_file}';\n"
                index_content += "\n"
        
        with open(self.output_dir / "index.ts", 'w') as f:
            f.write(index_content)

    def run(self):
        """Main transpilation process"""
        print("🚀 Starting 371 OS Engine Transpilation")
        
        # Setup output structure
        self.setup_output_structure()
        
        # Find all Python files
        py_files = list(self.source_dir.glob("**/*.py"))
        py_files = [f for f in py_files if not f.name.startswith('__') and f.name != 'transpile.py']
        
        print(f"📁 Found {len(py_files)} Python files to transpile")
        
        all_metadata = {}
        
        # Transpile each file
        for py_file in py_files:
            try:
                result = self.transpile_python_file(py_file)
                
                # Determine output folder and filename
                output_folder = self.determine_output_folder(py_file)
                ts_filename = py_file.stem + '.ts'
                output_path = self.output_dir / output_folder / ts_filename
                
                # Write TypeScript file
                with open(output_path, 'w') as f:
                    f.write(result['typescript'])
                
                # Store metadata
                all_metadata[py_file.name] = result['metadata']
                
                print(f"✅ {py_file} -> {output_path}")
                
            except Exception as e:
                print(f"❌ Error transpiling {py_file}: {e}")
        
        # Create package.json and index.ts
        self.create_package_json()
        self.create_index_file(all_metadata)
        
        # Write metadata file
        with open(self.output_dir / "transpilation-metadata.json", 'w') as f:
            json.dump(all_metadata, f, indent=2)
        
        print(f"🎉 Transpilation complete! Output in {self.output_dir}")
        print(f"📊 Transpiled {len(py_files)} files")

if __name__ == "__main__":
    transpiler = OSEngineTranspiler()
    transpiler.run()
