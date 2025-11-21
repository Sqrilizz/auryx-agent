"""Advanced computer control tools.

Author: sqrilizz
GitHub: https://github.com/Sqrilizz/auryx-agent
"""

import os
import subprocess
import psutil
from typing import Dict, Any, List, Optional
from pathlib import Path


class AdvancedComputerTools:
    """Advanced tools for computer control and monitoring."""
    
    def list_processes(self, filter_name: Optional[str] = None) -> Dict[str, Any]:
        """List running processes.
        
        Args:
            filter_name: Optional filter by process name
            
        Returns:
            Dict with process list
        """
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    if filter_name and filter_name.lower() not in info['name'].lower():
                        continue
                    
                    processes.append({
                        "pid": info['pid'],
                        "name": info['name'],
                        "cpu": round(info['cpu_percent'], 2),
                        "memory": round(info['memory_percent'], 2)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda p: p['cpu'], reverse=True)
            
            return {
                "success": True,
                "count": len(processes),
                "processes": processes[:20]  # Top 20
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def kill_process(self, pid: int) -> Dict[str, Any]:
        """Kill a process by PID.
        
        Args:
            pid: Process ID
            
        Returns:
            Dict with result
        """
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            proc.terminate()
            
            return {
                "success": True,
                "pid": pid,
                "name": name,
                "message": f"Process {name} (PID {pid}) terminated"
            }
        except psutil.NoSuchProcess:
            return {"success": False, "error": f"Process {pid} not found"}
        except psutil.AccessDenied:
            return {"success": False, "error": f"Access denied to kill process {pid}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_disk_usage(self, path: str = "/") -> Dict[str, Any]:
        """Get disk usage information.
        
        Args:
            path: Path to check (default: root)
            
        Returns:
            Dict with disk usage
        """
        try:
            usage = psutil.disk_usage(path)
            
            return {
                "success": True,
                "path": path,
                "total": self._format_bytes(usage.total),
                "used": self._format_bytes(usage.used),
                "free": self._format_bytes(usage.free),
                "percent": usage.percent
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get system memory information.
        
        Returns:
            Dict with memory info
        """
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                "success": True,
                "ram": {
                    "total": self._format_bytes(mem.total),
                    "available": self._format_bytes(mem.available),
                    "used": self._format_bytes(mem.used),
                    "percent": mem.percent
                },
                "swap": {
                    "total": self._format_bytes(swap.total),
                    "used": self._format_bytes(swap.used),
                    "free": self._format_bytes(swap.free),
                    "percent": swap.percent
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information.
        
        Returns:
            Dict with CPU info
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq()
            
            return {
                "success": True,
                "cores": psutil.cpu_count(logical=False),
                "threads": psutil.cpu_count(logical=True),
                "usage_per_core": cpu_percent,
                "usage_total": sum(cpu_percent) / len(cpu_percent),
                "frequency": {
                    "current": cpu_freq.current if cpu_freq else None,
                    "min": cpu_freq.min if cpu_freq else None,
                    "max": cpu_freq.max if cpu_freq else None
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_network_connections(self) -> Dict[str, Any]:
        """Get active network connections.
        
        Returns:
            Dict with connections
        """
        try:
            connections = []
            
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        "local": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "remote": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        "status": conn.status,
                        "pid": conn.pid
                    })
            
            return {
                "success": True,
                "count": len(connections),
                "connections": connections[:30]  # Limit to 30
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_battery_info(self) -> Dict[str, Any]:
        """Get battery information (if available).
        
        Returns:
            Dict with battery info
        """
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                return {
                    "success": True,
                    "available": False,
                    "message": "No battery detected"
                }
            
            return {
                "success": True,
                "available": True,
                "percent": battery.percent,
                "plugged": battery.power_plugged,
                "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_files(self, pattern: str, directory: str = ".", 
                   max_results: int = 50) -> Dict[str, Any]:
        """Find files matching pattern.
        
        Args:
            pattern: File pattern (e.g., "*.py", "test*")
            directory: Directory to search in
            max_results: Maximum number of results
            
        Returns:
            Dict with found files
        """
        try:
            import glob
            
            search_path = Path(directory).expanduser() / "**" / pattern
            files = list(glob.glob(str(search_path), recursive=True))
            
            return {
                "success": True,
                "pattern": pattern,
                "directory": directory,
                "count": len(files),
                "files": files[:max_results]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def compress_files(self, files: List[str], output: str, 
                      format: str = "zip") -> Dict[str, Any]:
        """Compress files into archive.
        
        Args:
            files: List of files to compress
            output: Output archive name
            format: Archive format (zip, tar, tar.gz)
            
        Returns:
            Dict with result
        """
        try:
            if format == "zip":
                import zipfile
                with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file in files:
                        zipf.write(file, Path(file).name)
            
            elif format in ["tar", "tar.gz"]:
                import tarfile
                mode = "w:gz" if format == "tar.gz" else "w"
                with tarfile.open(output, mode) as tar:
                    for file in files:
                        tar.add(file, Path(file).name)
            
            else:
                return {"success": False, "error": f"Unsupported format: {format}"}
            
            size = os.path.getsize(output)
            
            return {
                "success": True,
                "output": output,
                "format": format,
                "files_count": len(files),
                "size": self._format_bytes(size)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_archive(self, archive: str, output_dir: str = ".") -> Dict[str, Any]:
        """Extract archive.
        
        Args:
            archive: Archive file path
            output_dir: Where to extract
            
        Returns:
            Dict with result
        """
        try:
            archive_path = Path(archive)
            
            if archive.endswith('.zip'):
                import zipfile
                with zipfile.ZipFile(archive, 'r') as zipf:
                    zipf.extractall(output_dir)
                    files = zipf.namelist()
            
            elif archive.endswith(('.tar', '.tar.gz', '.tgz')):
                import tarfile
                with tarfile.open(archive, 'r:*') as tar:
                    tar.extractall(output_dir)
                    files = tar.getnames()
            
            else:
                return {"success": False, "error": "Unsupported archive format"}
            
            return {
                "success": True,
                "archive": archive,
                "output_dir": output_dir,
                "files_extracted": len(files)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def monitor_system(self, duration: int = 5) -> Dict[str, Any]:
        """Monitor system resources for a duration.
        
        Args:
            duration: Monitoring duration in seconds
            
        Returns:
            Dict with monitoring results
        """
        try:
            import time
            
            samples = []
            for _ in range(duration):
                samples.append({
                    "cpu": psutil.cpu_percent(interval=1),
                    "memory": psutil.virtual_memory().percent,
                    "disk_io": psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else None
                })
            
            avg_cpu = sum(s['cpu'] for s in samples) / len(samples)
            avg_memory = sum(s['memory'] for s in samples) / len(samples)
            
            return {
                "success": True,
                "duration": duration,
                "avg_cpu": round(avg_cpu, 2),
                "avg_memory": round(avg_memory, 2),
                "samples": samples
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _format_bytes(self, bytes: int) -> str:
        """Format bytes to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
