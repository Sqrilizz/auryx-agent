"""Network diagnostic tools - ping, DNS, port scan, traceroute."""

import socket
import subprocess
import platform
from typing import Dict, Any, List


class NetworkTools:
    """Network diagnostic tools."""
    
    @staticmethod
    def ping(host: str, count: int = 4) -> Dict[str, Any]:
        """Ping a host.
        
        Args:
            host: Hostname or IP to ping
            count: Number of ping packets
            
        Returns:
            Dict with ping results
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = f"ping {param} {count} {host}"
        
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "host": host,
                "output": result.stdout,
                "success": result.returncode == 0,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {
                "host": host,
                "output": "",
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def dns_lookup(host: str) -> Dict[str, Any]:
        """Perform DNS lookup.
        
        Args:
            host: Hostname to lookup
            
        Returns:
            Dict with DNS results
        """
        try:
            ip_addresses = socket.gethostbyname_ex(host)
            
            return {
                "host": host,
                "hostname": ip_addresses[0],
                "aliases": ip_addresses[1],
                "addresses": ip_addresses[2],
                "success": True,
                "error": None
            }
        except socket.gaierror as e:
            return {
                "host": host,
                "hostname": None,
                "aliases": [],
                "addresses": [],
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
        """Check if a port is open.
        
        Args:
            host: Hostname or IP
            port: Port number
            timeout: Connection timeout
            
        Returns:
            True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    @staticmethod
    def scan_ports(host: str, ports: List[int] = None) -> Dict[str, Any]:
        """Scan multiple ports.
        
        Args:
            host: Hostname or IP
            ports: List of ports to scan (default: common ports)
            
        Returns:
            Dict with scan results
        """
        if ports is None:
            # Common ports
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 5432, 8080, 8443]
        
        open_ports = []
        closed_ports = []
        
        for port in ports:
            if NetworkTools.scan_port(host, port):
                open_ports.append(port)
            else:
                closed_ports.append(port)
        
        return {
            "host": host,
            "open_ports": open_ports,
            "closed_ports": closed_ports,
            "total_scanned": len(ports),
            "success": True
        }
    
    @staticmethod
    def traceroute(host: str, max_hops: int = 30) -> Dict[str, Any]:
        """Perform traceroute to host.
        
        Args:
            host: Hostname or IP
            max_hops: Maximum number of hops
            
        Returns:
            Dict with traceroute results
        """
        system = platform.system().lower()
        
        if system == 'windows':
            command = f"tracert -h {max_hops} {host}"
        else:
            command = f"traceroute -m {max_hops} {host}"
        
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "host": host,
                "output": result.stdout,
                "success": result.returncode == 0,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {
                "host": host,
                "output": "",
                "success": False,
                "error": str(e)
            }
