"""AI Agent with tool support."""

import json
from typing import Dict, Any, List, Optional
from auryx_agent.core.yellowfire_client import YellowFireClient
from auryx_agent.tools.computer_tools import ComputerTools
from auryx_agent.tools.network_tools import NetworkTools


class Agent:
    """AI Agent that can use tools to interact with the system."""
    
    SYSTEM_PROMPT = """You are Auryx, an AI assistant with access to computer tools.

You can help users by:
- Executing shell commands
- Reading and writing files
- Network diagnostics (ping, DNS, port scan, traceroute)
- Listing directories
- Getting system information

When a user asks you to do something, use the appropriate tool and explain the results.

Available tools:
- execute_command(command, cwd=None): Execute shell command
- read_file(path): Read file content
- write_file(path, content, append=False): Write to file
- list_directory(path="."): List directory contents
- ping(host): Ping a host
- dns_lookup(host): DNS lookup
- scan_ports(host): Scan common ports
- traceroute(host): Traceroute to host
- get_system_info(): Get system information

To use a tool, respond with JSON:
{"tool": "tool_name", "args": {"arg1": "value1"}}

After using a tool, explain the results to the user in natural language."""
    
    def __init__(self, client: YellowFireClient):
        """Initialize agent.
        
        Args:
            client: YellowFire client instance
        """
        self.client = client
        self.computer = ComputerTools()
        self.network = NetworkTools()
        self.tools = {
            "execute_command": self.computer.execute_command,
            "read_file": self.computer.read_file,
            "write_file": self.computer.write_file,
            "list_directory": self.computer.list_directory,
            "get_system_info": self.computer.get_system_info,
            "ping": self.network.ping,
            "dns_lookup": self.network.dns_lookup,
            "scan_ports": self.network.scan_ports,
            "traceroute": self.network.traceroute,
        }
    
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
            self.client.chat_history.append(
                ChatMessage(role="system", content=self.SYSTEM_PROMPT)
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
