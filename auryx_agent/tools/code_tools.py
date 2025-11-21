"""Code generation and manipulation tools.

Author: sqrilizz
GitHub: https://github.com/Sqrilizz/auryx-agent
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional


class CodeTools:
    """Tools for code generation, review, and manipulation."""
    
    def generate_code(self, description: str, language: str = "python", 
                     filename: Optional[str] = None) -> Dict[str, Any]:
        """Generate code based on description.
        
        Args:
            description: What the code should do
            language: Programming language
            filename: Optional filename to save to
            
        Returns:
            Dict with code and metadata
        """
        # This will be enhanced by AI in agent.py
        return {
            "success": True,
            "description": description,
            "language": language,
            "filename": filename,
            "message": "Code generation requested"
        }
    
    def review_code(self, filepath: str) -> Dict[str, Any]:
        """Review code for issues and improvements.
        
        Args:
            filepath: Path to code file
            
        Returns:
            Dict with review results
        """
        try:
            path = Path(filepath).expanduser()
            if not path.exists():
                return {"success": False, "error": f"File not found: {filepath}"}
            
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Basic analysis
            lines = code.split('\n')
            issues = []
            
            # Check for common issues
            if len(lines) > 1000:
                issues.append("File is very long (>1000 lines), consider splitting")
            
            # Count TODO/FIXME comments
            todos = sum(1 for line in lines if 'TODO' in line or 'FIXME' in line)
            if todos > 0:
                issues.append(f"Found {todos} TODO/FIXME comments")
            
            return {
                "success": True,
                "filepath": str(path),
                "lines": len(lines),
                "size": len(code),
                "issues": issues,
                "code_preview": code[:500] if len(code) > 500 else code
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def refactor_code(self, filepath: str, operation: str) -> Dict[str, Any]:
        """Refactor code (extract function, rename, etc).
        
        Args:
            filepath: Path to code file
            operation: Refactoring operation description
            
        Returns:
            Dict with refactoring results
        """
        return {
            "success": True,
            "filepath": filepath,
            "operation": operation,
            "message": "Refactoring requested - AI will handle this"
        }
    
    def find_bugs(self, filepath: str) -> Dict[str, Any]:
        """Find potential bugs in code.
        
        Args:
            filepath: Path to code file
            
        Returns:
            Dict with potential bugs
        """
        try:
            path = Path(filepath).expanduser()
            if not path.exists():
                return {"success": False, "error": f"File not found: {filepath}"}
            
            # Try to run linters if available
            bugs = []
            
            # Python: try pylint or flake8
            if filepath.endswith('.py'):
                try:
                    result = subprocess.run(
                        ['python', '-m', 'py_compile', str(path)],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode != 0:
                        bugs.append(f"Syntax error: {result.stderr}")
                except:
                    pass
            
            return {
                "success": True,
                "filepath": str(path),
                "bugs": bugs,
                "message": "Basic bug check completed"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_docs(self, filepath: str) -> Dict[str, Any]:
        """Generate documentation for code.
        
        Args:
            filepath: Path to code file
            
        Returns:
            Dict with documentation
        """
        try:
            path = Path(filepath).expanduser()
            if not path.exists():
                return {"success": False, "error": f"File not found: {filepath}"}
            
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            return {
                "success": True,
                "filepath": str(path),
                "code": code[:1000],
                "message": "Documentation generation requested - AI will create docs"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def git_status(self, repo_path: str = ".") -> Dict[str, Any]:
        """Get git repository status.
        
        Args:
            repo_path: Path to git repository
            
        Returns:
            Dict with git status
        """
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {"success": False, "error": "Not a git repository"}
            
            return {
                "success": True,
                "status": result.stdout,
                "clean": len(result.stdout.strip()) == 0
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def git_diff(self, repo_path: str = ".", file: Optional[str] = None) -> Dict[str, Any]:
        """Get git diff.
        
        Args:
            repo_path: Path to git repository
            file: Optional specific file to diff
            
        Returns:
            Dict with diff
        """
        try:
            cmd = ['git', 'diff']
            if file:
                cmd.append(file)
            
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return {
                "success": True,
                "diff": result.stdout,
                "has_changes": len(result.stdout) > 0
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_template(self, template_type: str, name: str, 
                       output_dir: str = ".") -> Dict[str, Any]:
        """Create code template.
        
        Args:
            template_type: Type of template (python_script, flask_app, etc)
            name: Name for the project/file
            output_dir: Where to create the template
            
        Returns:
            Dict with created files
        """
        templates = {
            "python_script": self._template_python_script,
            "flask_app": self._template_flask_app,
            "fastapi_app": self._template_fastapi_app,
            "cli_tool": self._template_cli_tool,
        }
        
        if template_type not in templates:
            return {
                "success": False,
                "error": f"Unknown template: {template_type}",
                "available": list(templates.keys())
            }
        
        try:
            files = templates[template_type](name, output_dir)
            return {
                "success": True,
                "template": template_type,
                "files": files
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _template_python_script(self, name: str, output_dir: str) -> List[str]:
        """Create Python script template."""
        path = Path(output_dir) / f"{name}.py"
        content = f'''#!/usr/bin/env python3
"""
{name} - Description here
"""

def main():
    """Main function."""
    print("Hello from {name}!")

if __name__ == "__main__":
    main()
'''
        path.write_text(content)
        path.chmod(0o755)
        return [str(path)]
    
    def _template_flask_app(self, name: str, output_dir: str) -> List[str]:
        """Create Flask app template."""
        base = Path(output_dir) / name
        base.mkdir(exist_ok=True)
        
        files = []
        
        # app.py
        app_py = base / "app.py"
        app_py.write_text('''from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Hello World!"})

if __name__ == '__main__':
    app.run(debug=True)
''')
        files.append(str(app_py))
        
        # requirements.txt
        req = base / "requirements.txt"
        req.write_text('flask>=2.0.0\n')
        files.append(str(req))
        
        return files
    
    def _template_fastapi_app(self, name: str, output_dir: str) -> List[str]:
        """Create FastAPI app template."""
        base = Path(output_dir) / name
        base.mkdir(exist_ok=True)
        
        files = []
        
        # main.py
        main_py = base / "main.py"
        main_py.write_text('''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')
        files.append(str(main_py))
        
        # requirements.txt
        req = base / "requirements.txt"
        req.write_text('fastapi>=0.100.0\nuvicorn[standard]>=0.23.0\n')
        files.append(str(req))
        
        return files
    
    def _template_cli_tool(self, name: str, output_dir: str) -> List[str]:
        """Create CLI tool template."""
        base = Path(output_dir) / name
        base.mkdir(exist_ok=True)
        
        files = []
        
        # cli.py
        cli_py = base / "cli.py"
        cli_py.write_text('''import argparse

def main():
    parser = argparse.ArgumentParser(description='CLI Tool')
    parser.add_argument('command', help='Command to execute')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Executing: {args.command}")
    
    print(f"Command: {args.command}")

if __name__ == '__main__':
    main()
''')
        files.append(str(cli_py))
        
        return files
