"""Tools for computer interaction - execute commands, work with files."""

import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any


class ComputerTools:
    """Tools for interacting with the computer system."""
    
    @staticmethod
    def execute_command(command: str, cwd: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
        """Execute a shell command and return the result.
        
        Args:
            command: Shell command to execute
            cwd: Working directory (None for current)
            timeout: Command timeout in seconds
            
        Returns:
            Dict with 'stdout', 'stderr', 'returncode', 'success'
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "returncode": -1,
                "success": False
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "success": False
            }
    
    @staticmethod
    def read_file(path: str, max_lines: Optional[int] = None) -> Dict[str, Any]:
        """Read file content.
        
        Args:
            path: Path to file
            max_lines: Maximum lines to read (None for all)
            
        Returns:
            Dict with 'content', 'success', 'error'
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if max_lines:
                    lines = [f.readline() for _ in range(max_lines)]
                    content = ''.join(lines)
                else:
                    content = f.read()
            
            return {
                "content": content,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "content": "",
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def write_file(path: str, content: str, append: bool = False) -> Dict[str, Any]:
        """Write content to file.
        
        Args:
            path: Path to file
            content: Content to write
            append: Append instead of overwrite
            
        Returns:
            Dict with 'success', 'error'
        """
        try:
            mode = 'a' if append else 'w'
            with open(path, mode, encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def list_directory(path: str = ".") -> Dict[str, Any]:
        """List directory contents.
        
        Args:
            path: Directory path
            
        Returns:
            Dict with 'files', 'dirs', 'success', 'error'
        """
        try:
            p = Path(path)
            files = []
            dirs = []
            
            for item in p.iterdir():
                if item.is_file():
                    files.append(str(item))
                elif item.is_dir():
                    dirs.append(str(item))
            
            return {
                "files": files,
                "dirs": dirs,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "files": [],
                "dirs": [],
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Get system information.
        
        Returns:
            Dict with system info
        """
        import platform
        
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }
