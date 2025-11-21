"""AI Agent with tool support.

Author: sqrilizz
GitHub: https://github.com/Sqrilizz/auryx-agent
"""

import json
from typing import Dict, Any, List, Optional
from auryx_agent.core.yellowfire_client import YellowFireClient
from auryx_agent.core.memory import MemorySystem
from auryx_agent.tools.computer_tools import ComputerTools
from auryx_agent.tools.network_tools import NetworkTools
from auryx_agent.tools.code_tools import CodeTools
from auryx_agent.tools.web_tools import WebTools
from auryx_agent.tools.advanced_computer_tools import AdvancedComputerTools


class Agent:
    """AI Agent that can use tools to interact with the system."""
    
    SYSTEM_PROMPT = """You are Auryx, an advanced AI assistant with extensive capabilities.

🎯 Core Capabilities:
- Code generation, review, refactoring, and debugging
- File operations (read, write, search, compress)
- Web search and internet access
- Network diagnostics and monitoring
- System monitoring and process management
- Long-term memory (remembers user preferences and context)

💻 Code Tools:
- generate_code(description, language, filename): Generate code
- review_code(filepath): Review and analyze code
- refactor_code(filepath, operation): Refactor code
- find_bugs(filepath): Find potential bugs
- generate_docs(filepath): Generate documentation
- git_status(repo_path): Get git status
- git_diff(repo_path, file): Get git diff
- create_template(template_type, name, output_dir): Create project templates

🌐 Web Tools:
- web_search(query, num_results): Search the web
- fetch_url(url, timeout): Fetch webpage content
- download_file(url, output_path): Download files
- check_website(url): Check website status
- get_weather(location): Get weather information
- extract_links(url): Extract links from webpage

🖥️ Advanced Computer Tools:
- list_processes(filter_name): List running processes
- kill_process(pid): Terminate a process
- get_disk_usage(path): Get disk usage
- get_memory_info(): Get RAM/swap info
- get_cpu_info(): Get CPU information
- get_network_connections(): List network connections
- find_files(pattern, directory): Find files
- compress_files(files, output, format): Create archives
- extract_archive(archive, output_dir): Extract archives
- monitor_system(duration): Monitor system resources

🧠 Memory System:
- memory_add(content, category, importance, tags): Store memory
- memory_search(query): Search memories
- memory_get_context(): Get relevant context

📡 Network Tools:
- ping(host): Ping a host
- dns_lookup(host): DNS lookup
- scan_ports(host): Scan ports
- traceroute(host): Traceroute

To use a tool, respond with JSON:
{"tool": "tool_name", "args": {"arg1": "value1"}}

After using a tool, explain the results naturally."""
    
    def __init__(self, client: YellowFireClient, enable_memory: bool = True):
        """Initialize agent.
        
        Args:
            client: YellowFire client instance
            enable_memory: Enable long-term memory system
        """
        self.client = client
        self.computer = ComputerTools()
        self.network = NetworkTools()
        self.code = CodeTools()
        self.web = WebTools()
        self.advanced = AdvancedComputerTools()
        self.memory = MemorySystem() if enable_memory else None
        
        # Register all tools
        self.tools = {
            # Basic computer tools
            "execute_command": self.computer.execute_command,
            "read_file": self.computer.read_file,
            "write_file": self.computer.write_file,
            "list_directory": self.computer.list_directory,
            "get_system_info": self.computer.get_system_info,
            
            # Network tools
            "ping": self.network.ping,
            "dns_lookup": self.network.dns_lookup,
            "scan_ports": self.network.scan_ports,
            "traceroute": self.network.traceroute,
            
            # Code tools
            "generate_code": self.code.generate_code,
            "review_code": self.code.review_code,
            "refactor_code": self.code.refactor_code,
            "find_bugs": self.code.find_bugs,
            "generate_docs": self.code.generate_docs,
            "git_status": self.code.git_status,
            "git_diff": self.code.git_diff,
            "create_template": self.code.create_template,
            
            # Web tools
            "web_search": self.web.web_search,
            "fetch_url": self.web.fetch_url,
            "download_file": self.web.download_file,
            "check_website": self.web.check_website,
            "get_weather": self.web.get_weather,
            "extract_links": self.web.extract_links,
            
            # Advanced computer tools
            "list_processes": self.advanced.list_processes,
            "kill_process": self.advanced.kill_process,
            "get_disk_usage": self.advanced.get_disk_usage,
            "get_memory_info": self.advanced.get_memory_info,
            "get_cpu_info": self.advanced.get_cpu_info,
            "get_network_connections": self.advanced.get_network_connections,
            "find_files": self.advanced.find_files,
            "compress_files": self.advanced.compress_files,
            "extract_archive": self.advanced.extract_archive,
            "monitor_system": self.advanced.monitor_system,
        }
        
        # Add memory tools if enabled
        if self.memory:
            self.tools.update({
                "memory_add": self._memory_add,
                "memory_search": self._memory_search,
                "memory_get_context": self._memory_get_context,
            })
    
    def _memory_add(self, content: str, category: str = "fact", 
                    importance: int = 5, tags: List[str] = None) -> Dict[str, Any]:
        """Add memory wrapper."""
        memory_id = self.memory.add(content, category, importance, tags or [])
        return {"success": True, "memory_id": memory_id, "content": content}
    
    def _memory_search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Search memory wrapper."""
        results = self.memory.search(query, limit)
        return {
            "success": True,
            "query": query,
            "results": [{"content": m.content, "category": m.category, "importance": m.importance} 
                       for m in results]
        }
    
    def _memory_get_context(self) -> Dict[str, Any]:
        """Get memory context wrapper."""
        context = self.memory.get_context_summary()
        return {"success": True, "context": context}
    
    def process(self, user_input: str, max_iterations: int = 5) -> str:
        """Process user input with tool support.
        
        Args:
            user_input: User's message
            max_iterations: Maximum tool call iterations
            
        Returns:
            Final response to user
        """
        # Add system prompt to history if empty
        if not self.client.chat_history:
            from auryx_agent.core.yellowfire_client import ChatMessage
            system_prompt = self.SYSTEM_PROMPT
            
            # Add memory context if available
            if self.memory:
                memory_context = self.memory.get_context_summary()
                if memory_context and memory_context != "No memories stored yet.":
                    system_prompt += f"\n\n📝 Remembered Context:\n{memory_context}"
            
            self.client.chat_history.append(
                ChatMessage(role="system", content=system_prompt)
            )
        
        conversation = f"User: {user_input}\n\n"
        
        for iteration in range(max_iterations):
            # Get AI response
            response = self.client.generate(user_input if iteration == 0 else conversation, use_history=True)
            
            # Check if response contains tool call
            tool_call = self._extract_tool_call(response)
            
            if not tool_call:
                # No tool call, return response
                return response
            
            # Execute tool
            tool_name = tool_call.get("tool")
            tool_args = tool_call.get("args", {})
            
            if tool_name not in self.tools:
                return f"Error: Unknown tool '{tool_name}'"
            
            try:
                result = self.tools[tool_name](**tool_args)
                conversation += f"Tool: {tool_name}\nArgs: {json.dumps(tool_args)}\nResult: {json.dumps(result, indent=2)}\n\n"
                
                # Continue conversation with tool result
                user_input = f"Tool result: {json.dumps(result)}\nPlease explain this to the user."
            except Exception as e:
                return f"Error executing tool: {str(e)}"
        
        return "Maximum iterations reached. Please try again."
    
    def _extract_tool_call(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract tool call from AI response.
        
        Args:
            response: AI response text
            
        Returns:
            Tool call dict or None
        """
        try:
            # Look for JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                
                if "tool" in data:
                    return data
        except:
            pass
        
        return None
