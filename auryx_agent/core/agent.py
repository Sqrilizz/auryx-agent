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

🚨 CRITICAL RULE - NO HALLUCINATIONS:
- NEVER invent or fabricate data, system information, or command outputs
- ALWAYS use tools to get real data from the system
- If user asks for system info (neofetch, disk usage, processes, etc.) - USE THE TOOL
- If you don't have a tool for something - SAY SO, don't make up data
- Example: User asks "show neofetch" → Use execute_command tool with "neofetch"
- Example: User asks "disk usage" → Use get_disk_usage tool
- VIOLATION: Making up fake system specs, fake command outputs, fake file contents

⚠️ FORMATTING RULES:
- Use PLAIN TEXT only, NO LaTeX, NO math formulas ($$...$$)
- Use simple markdown: **bold**, *italic*, `code`, lists
- Format numbers simply: 7.98 GB, 48.1%, not $$\text{...}$$
- Use emojis for visual appeal: ✓ ✗ 💾 🔍 ⚡ 📊

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

After using a tool, explain the results naturally.

🧠 AUTOMATIC MEMORY:
You MUST automatically remember important information about the user using memory_add tool:
- User's name, location, profession, interests
- User's preferences (programming languages, tools, frameworks)
- Important facts about user's projects
- User's goals and plans
- Technical skills and experience level

When you learn something important, use memory_add and mention it briefly at the end:
"💾 Saved to memory: [brief description]"

Categories: "preference", "fact", "context", "skill", "project"
Importance: 1-10 (use 7-9 for important user info)"""
    
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
        # Check for duplicates
        existing = self.memory.search(content, limit=1)
        if existing and existing[0].content.lower() == content.lower():
            return {"success": False, "error": "Memory already exists", "content": content}
        
        memory_id = self.memory.add(content, category, importance, tags or [])
        return {"success": True, "memory_id": memory_id, "content": content, "category": category}
    
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
    
    def _detect_hallucination_risk(self, user_input: str, response: str) -> bool:
        """Detect if response might contain hallucinated data.
        
        Args:
            user_input: User's original question
            response: AI's response
            
        Returns:
            True if hallucination risk detected
        """
        # Keywords that indicate user wants real system data
        system_info_keywords = [
            'neofetch', 'system info', 'disk usage', 'disk space', 'memory', 'cpu', 'processes',
            'running', 'network', 'connections', 'files', 'directory', 'ls',
            'ps', 'top', 'df', 'free', 'ifconfig', 'ip addr', 'netstat',
            'uname', 'hostname', 'uptime', 'who', 'w', 'last', 'kernel'
        ]
        
        # Check if user is asking for system info
        user_lower = user_input.lower()
        asking_for_system_info = any(keyword in user_lower for keyword in system_info_keywords)
        
        if not asking_for_system_info:
            return False
        
        # Check if response contains data without tool call
        # If response has specific numbers/paths but no tool was used, it's likely hallucinated
        has_specific_data = any([
            'GB' in response or 'MB' in response or 'KB' in response or 'TB' in response,
            'CPU:' in response or 'Memory:' in response,
            'Kernel:' in response or 'OS:' in response,
            '/dev/' in response or '/home/' in response,
            'PID' in response and 'USER' in response,
        ])
        
        # Check if agent is making excuses instead of using tools
        excuse_phrases = [
            'слишком много данных',
            'не может быть полностью отображён',
            'ограничений',
            'обычно neofetch отображает',
            'если вам нужно что-то конкретное',
            'too much data',
            'cannot be displayed',
            'limitations',
            'usually shows',
            'if you need something specific',
        ]
        
        making_excuses = any(phrase.lower() in response.lower() for phrase in excuse_phrases)
        
        return has_specific_data or making_excuses
    
    def process(self, user_input: str, max_iterations: int = 5) -> str:
        """Process user input with tool support.
        
        Args:
            user_input: User's message
            max_iterations: Maximum tool call iterations
            
        Returns:
            Final response to user
        """
        from auryx_agent.core.yellowfire_client import ChatMessage
        
        # Build system prompt with current memory context
        system_prompt = self.SYSTEM_PROMPT
        
        # Add memory context if available
        if self.memory:
            memory_context = self.memory.get_context_summary()
            if memory_context and memory_context != "No memories stored yet.":
                system_prompt += f"\n\n📝 Remembered Context:\n{memory_context}"
        
        # Update or add system prompt
        if self.client.chat_history and self.client.chat_history[0].role == "system":
            # Update existing system prompt with fresh memory
            self.client.chat_history[0] = ChatMessage(role="system", content=system_prompt)
        else:
            # Add new system prompt
            self.client.chat_history.insert(0, ChatMessage(role="system", content=system_prompt))
        
        conversation = f"User: {user_input}\n\n"
        
        for iteration in range(max_iterations):
            # Get AI response
            response = self.client.generate(user_input if iteration == 0 else conversation, use_history=True)
            
            # Check if response contains tool call
            tool_call = self._extract_tool_call(response)
            
            if not tool_call:
                # Check for potential hallucination before returning
                if self._detect_hallucination_risk(user_input, response):
                    # Force agent to use tools
                    warning = "\n\n⚠️ WARNING: You provided specific system data without using tools. This is likely fabricated. Please use the appropriate tool to get real data."
                    conversation += f"Assistant (REJECTED): {response}\n{warning}\n\n"
                    user_input = f"You must use a tool to answer this question. Do not fabricate data. {user_input}"
                    continue
                
                # No tool call, return response
                return response
            
            # Execute tool
            tool_name = tool_call.get("tool")
            tool_args = tool_call.get("args", {})
            
            if tool_name not in self.tools:
                return f"Error: Unknown tool '{tool_name}'"
            
            try:
                result = self.tools[tool_name](**tool_args)
                
                # Limit result size to prevent context overflow
                result_str = json.dumps(result, indent=2)
                max_result_size = 5000  # characters
                if len(result_str) > max_result_size:
                    result_str = result_str[:max_result_size] + f"\n... (truncated, {len(result_str) - max_result_size} chars omitted)"
                
                conversation += f"Tool: {tool_name}\nArgs: {json.dumps(tool_args)}\nResult: {result_str}\n\n"
                
                # Continue conversation with tool result (also truncated)
                user_input = f"Tool result: {result_str}\nPlease explain this to the user."
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
