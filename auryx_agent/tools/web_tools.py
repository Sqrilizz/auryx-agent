"""Web and internet access tools.

Author: sqrilizz
GitHub: https://github.com/Sqrilizz/auryx-agent
"""

import json
import subprocess
from typing import Dict, Any, Optional, List
from urllib.parse import quote_plus, urlparse
import socket


class WebTools:
    """Tools for web search, scraping, and internet access."""
    
    def web_search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Search the web using DuckDuckGo (no API key needed).
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Dict with search results
        """
        try:
            # Use curl to search DuckDuckGo's instant answer API
            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json"
            
            result = subprocess.run(
                ['curl', '-s', url],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {"success": False, "error": "Search failed"}
            
            data = json.loads(result.stdout)
            
            results = []
            
            # Abstract
            if data.get('Abstract'):
                results.append({
                    "title": data.get('Heading', 'Result'),
                    "snippet": data['Abstract'],
                    "url": data.get('AbstractURL', '')
                })
            
            # Related topics
            for topic in data.get('RelatedTopics', [])[:num_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        "title": topic.get('Text', '')[:100],
                        "snippet": topic.get('Text', ''),
                        "url": topic.get('FirstURL', '')
                    })
            
            return {
                "success": True,
                "query": query,
                "results": results[:num_results],
                "count": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fetch_url(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Fetch content from URL.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            Dict with page content
        """
        try:
            result = subprocess.run(
                ['curl', '-s', '-L', '--max-time', str(timeout), url],
                capture_output=True,
                text=True,
                timeout=timeout + 2
            )
            
            if result.returncode != 0:
                return {"success": False, "error": "Failed to fetch URL"}
            
            content = result.stdout
            
            return {
                "success": True,
                "url": url,
                "content": content[:5000],  # Limit to first 5000 chars
                "size": len(content),
                "preview": content[:500]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def download_file(self, url: str, output_path: str) -> Dict[str, Any]:
        """Download file from URL.
        
        Args:
            url: URL to download from
            output_path: Where to save the file
            
        Returns:
            Dict with download status
        """
        try:
            result = subprocess.run(
                ['curl', '-L', '-o', output_path, url],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return {"success": False, "error": "Download failed"}
            
            import os
            size = os.path.getsize(output_path)
            
            return {
                "success": True,
                "url": url,
                "output": output_path,
                "size": size
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_website(self, url: str) -> Dict[str, Any]:
        """Check if website is accessible.
        
        Args:
            url: Website URL
            
        Returns:
            Dict with website status
        """
        try:
            # Parse URL
            parsed = urlparse(url)
            host = parsed.netloc or parsed.path
            port = 443 if parsed.scheme == 'https' else 80
            
            # Try to connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            accessible = result == 0
            
            # Get HTTP status if accessible
            status_code = None
            if accessible:
                try:
                    curl_result = subprocess.run(
                        ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    status_code = int(curl_result.stdout)
                except:
                    pass
            
            return {
                "success": True,
                "url": url,
                "accessible": accessible,
                "status_code": status_code,
                "message": "Website is accessible" if accessible else "Website is not accessible"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather information using wttr.in.
        
        Args:
            location: City name or location
            
        Returns:
            Dict with weather info
        """
        try:
            url = f"https://wttr.in/{quote_plus(location)}?format=j1"
            
            result = subprocess.run(
                ['curl', '-s', url],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {"success": False, "error": "Failed to get weather"}
            
            data = json.loads(result.stdout)
            
            current = data['current_condition'][0]
            
            return {
                "success": True,
                "location": location,
                "temperature": current['temp_C'] + "°C",
                "feels_like": current['FeelsLikeC'] + "°C",
                "condition": current['weatherDesc'][0]['value'],
                "humidity": current['humidity'] + "%",
                "wind": current['windspeedKmph'] + " km/h",
                "description": f"{current['weatherDesc'][0]['value']}, {current['temp_C']}°C"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def whois_lookup(self, domain: str) -> Dict[str, Any]:
        """Perform WHOIS lookup for domain.
        
        Args:
            domain: Domain name
            
        Returns:
            Dict with WHOIS info
        """
        try:
            result = subprocess.run(
                ['whois', domain],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return {
                "success": True,
                "domain": domain,
                "info": result.stdout[:2000]  # Limit output
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_links(self, url: str) -> Dict[str, Any]:
        """Extract all links from a webpage.
        
        Args:
            url: URL to extract links from
            
        Returns:
            Dict with extracted links
        """
        try:
            # Fetch page
            result = subprocess.run(
                ['curl', '-s', '-L', url],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {"success": False, "error": "Failed to fetch page"}
            
            content = result.stdout
            
            # Simple regex to find links
            import re
            links = re.findall(r'href=[\'"]?([^\'" >]+)', content)
            
            # Filter and clean links
            clean_links = []
            for link in links:
                if link.startswith('http') or link.startswith('//'):
                    clean_links.append(link)
            
            return {
                "success": True,
                "url": url,
                "links": list(set(clean_links))[:50],  # Unique, max 50
                "count": len(clean_links)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
