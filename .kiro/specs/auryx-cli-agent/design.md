# Design Document: Auryx CLI Agent

## Overview

The Auryx CLI Agent is a Python-based command-line application that bridges AI language models with network diagnostic tools. The system uses the YellowFire unified API service to access multiple AI models (GPT, Claude, Gemini, DeepSeek, etc.) through a single API key, simplifying configuration and reducing costs. The architecture follows a modular design with clear separation between the AI client layer, network tool adapters, CLI interface, and formatting/output components.

The agent operates in two primary modes:
1. **Chat Mode**: Interactive REPL where users input natural language queries that are interpreted by AI models to execute network diagnostics
2. **Command Mode**: Direct CLI invocation for scripting and automation

The design emphasizes simplicity through the unified YellowFire API, extensibility through a plugin system, configurability through TOML files, and user experience through rich terminal formatting.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI Entry Point                          │
│                    (auryx-agent)                             │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐       ┌───────▼────────┐
│   Chat Mode    │       │  Command Mode  │
│   (REPL Loop)  │       │  (Direct Exec) │
└───────┬────────┘       └───────┬────────┘
        │                        │
        └────────┬───────────────┘
                 │
        ┌────────▼─────────┐
        │  Command Parser  │
        │  & Intent Router │
        └────────┬─────────┘
                 │
        ┌────────┴─────────┐
        │                  │
┌───────▼────────┐  ┌─────▼──────────┐
│  YellowFire    │  │ Network Tools  │
│  AI Client     │  │   Adapters     │
└───────┬────────┘  └─────┬──────────┘
        │                 │
        │           ┌─────▼──────────┐
        │           │ network_tools  │
        │           │   Repository   │
        │           └────────────────┘
        │
┌───────▼────────────────────────┐
│      Formatter & Output        │
│  (ANSI, Cards, Spinners)       │
└────────────────────────────────┘
```

### Component Responsibilities

1. **CLI Entry Point**: Argument parsing, mode selection, configuration loading
2. **Chat Mode**: REPL loop, user input handling, session management
3. **Command Mode**: Direct command execution, exit code handling
4. **Command Parser**: Intent detection, command routing, parameter extraction
5. **YellowFire AI Client**: Model selection, API communication, response handling
6. **Network Tools Adapters**: Wrapper layer for network_tools repository functions
7. **Formatter**: Output rendering, ANSI styling, card layouts, spinners

## Components and Interfaces

### 1. CLI Entry Point (`cli/__main__.py`)

**Responsibilities:**
- Parse command-line arguments
- Load configuration from `~/.config/auryx-agent/config.toml`
- Initialize logging
- Route to Chat Mode or Command Mode

**Interface:**
```python
def main() -> int:
    """Entry point for auryx-agent CLI."""
    args = parse_arguments()
    config = load_config()
    
    if args.subcommand:
        return command_mode(args, config)
    else:
        return chat_mode(config)
```

### 2. Configuration Manager (`core/config.py`)

**Responsibilities:**
- Load and parse TOML configuration
- Provide default values
- Validate configuration
- Create config directory structure

**Interface:**
```python
@dataclass
class Config:
    default_model: str
    theme: str
    auto_update: bool
    yellowfire_api_key: str
    network_timeout: int
    
def load_config() -> Config:
    """Load configuration from ~/.config/auryx-agent/config.toml"""
    
def create_default_config() -> None:
    """Create default configuration file"""
```

### 3. YellowFire AI Client (`core/yellowfire_client.py`)

**Responsibilities:**
- Communicate with YellowFire unified API
- Handle model selection and fallback
- Manage API authentication
- Maintain chat history for multi-turn conversations

**Interface:**
```python
@dataclass
class ChatMessage:
    role: str  # 'user' or 'assistant'
    content: str

class YellowFireClient:
    def __init__(self, api_key: str, default_model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.current_model = default_model
        self.api_url = "https://yellowfire.ru/api/v2/chatgpt"
        self.chat_history: List[ChatMessage] = []
        
    def list_models(self) -> List[str]:
        """List all available models from YellowFire API"""
        
    def set_model(self, model_name: str) -> bool:
        """Set the active model"""
        
    def generate(self, prompt: str, use_history: bool = True) -> str:
        """Generate response from current model"""
        
    def clear_history(self) -> None:
        """Clear chat history"""
        
    def get_balance(self) -> float:
        """Get current account balance"""
```

**Available Models (via YellowFire):**
- GPT models: gpt-5, gpt-4o, gpt-4o-mini, gpt-3.5, etc.
- Claude models: claude-4-5-sonnet, claude-3.5-sonnet, etc.
- Gemini models: gemini-3.0-pro, gemini-2.5-pro, etc.
- DeepSeek models: deepseek-r1, deepseek-v3, etc.
- Other models: grok-4, command-r-plus, minimax-02, etc.

### 4. Command Parser (`core/command_parser.py`)

**Responsibilities:**
- Parse user input in chat mode
- Detect intent (network tool vs general query)
- Extract parameters for network tools
- Route to appropriate handler

**Interface:**
```python
@dataclass
class ParsedCommand:
    intent: str  # 'ping', 'dns', 'ports', 'traceroute', 'chat'
    target: Optional[str]
    parameters: Dict[str, Any]
    raw_input: str

class CommandParser:
    def __init__(self, ai_client: YellowFireClient):
        self.ai_client = ai_client
        
    def parse(self, user_input: str) -> ParsedCommand:
        """Parse user input and determine intent"""
        
    def _detect_intent(self, user_input: str) -> str:
        """Use AI to detect user intent"""
```

### 5. Network Tools Adapters (`tools/adapters/`)

**Responsibilities:**
- Wrap network_tools repository functions
- Normalize output format
- Handle errors consistently
- Apply timeout configuration

**Interface:**
```python
@dataclass
class NetworkResult:
    success: bool
    tool: str
    target: str
    data: Dict[str, Any]
    error: Optional[str]
    duration_ms: float

class PingAdapter:
    def execute(self, host: str, count: int = 4, timeout: int = 5) -> NetworkResult:
        """Execute ping and return normalized result"""

class DNSAdapter:
    def execute(self, host: str, record_type: str = 'A', timeout: int = 5) -> NetworkResult:
        """Execute DNS lookup and return normalized result"""

class PortScanAdapter:
    def execute(self, host: str, ports: List[int], timeout: int = 5) -> NetworkResult:
        """Execute port scan and return normalized result"""

class TracerouteAdapter:
    def execute(self, host: str, max_hops: int = 30, timeout: int = 5) -> NetworkResult:
        """Execute traceroute and return normalized result"""
```

### 6. Formatter (`core/formatter.py`)

**Responsibilities:**
- Render network results as formatted cards
- Apply ANSI color schemes
- Display spinners for long operations
- Format AI summaries
- Display ASCII art logo
- Format balance and usage information

**Interface:**
```python
class Formatter:
    def __init__(self, theme: str = 'dark'):
        self.theme = theme
        self.colors = self._load_theme()
        
    def format_logo(self) -> str:
        """Return ASCII art logo with colors"""
        
    def format_result(self, result: NetworkResult) -> str:
        """Format network result as a card"""
        
    def format_ai_summary(self, summary: str) -> str:
        """Format AI summary with styling"""
        
    def format_balance(self, balance: float, show_warning: bool = False) -> str:
        """Format balance display with optional low balance warning"""
        
    def format_usage(self, usage_entries: List[UsageEntry]) -> str:
        """Format usage history as a table"""
        
    def spinner(self, message: str) -> ContextManager:
        """Context manager for displaying spinner"""
        
    def format_error(self, error: str) -> str:
        """Format error message"""
```

**ASCII Logo:**
```
    ___                           
   /   | __  ___________  ___  __
  / /| |/ / / / ___/ __ \/ / |/ /
 / ___ / /_/ / /  / /_/ /|   /  
/_/  |_\__,_/_/   \____/_/|_|   
                                 
 Network Diagnostic AI Agent
```

### 7. Chat Mode (`cli/chat_mode.py`)

**Responsibilities:**
- Implement REPL loop
- Handle user input
- Coordinate between parser, AI router, and network tools
- Manage session history

**Interface:**
```python
class ChatSession:
    def __init__(self, config: Config):
        self.config = config
        self.ai_client = YellowFireClient(config.yellowfire_api_key, config.default_model)
        self.parser = CommandParser(self.ai_client)
        self.formatter = Formatter(config.theme)
        self.history = HistoryManager()
        
    def run(self) -> int:
        """Run interactive chat loop"""
        
    def handle_input(self, user_input: str) -> None:
        """Process user input and display results"""
```

### 8. Command Mode (`cli/command_mode.py`)

**Responsibilities:**
- Execute direct commands from CLI arguments
- Return appropriate exit codes
- Format output for scripting
- Handle balance and usage commands

**Interface:**
```python
def execute_command(args: argparse.Namespace, config: Config) -> int:
    """Execute command and return exit code"""
    
def execute_balance_command(ai_router: AIRouter, formatter: Formatter) -> int:
    """Display current balance"""
    
def execute_usage_command(ai_router: AIRouter, formatter: Formatter) -> int:
    """Display usage history"""
```

### 9. History Manager (`core/history.py`)

**Responsibilities:**
- Save command history to JSON
- Load and display history
- Manage history size limits

**Interface:**
```python
@dataclass
class HistoryEntry:
    timestamp: str
    command: str
    model: str
    result_summary: str

class HistoryManager:
    def __init__(self, max_entries: int = 1000):
        self.history_file = Path.home() / '.config' / 'auryx-agent' / 'history.json'
        self.max_entries = max_entries
        
    def add_entry(self, entry: HistoryEntry) -> None:
        """Add entry to history"""
        
    def get_history(self, limit: Optional[int] = None) -> List[HistoryEntry]:
        """Retrieve history entries"""
        
    def clear(self) -> None:
        """Clear all history"""
```

### 10. Report Generator (`core/report_generator.py`)

**Responsibilities:**
- Generate Markdown reports from session data
- Include timestamps and formatting
- Save to reports directory

**Interface:**
```python
class ReportGenerator:
    def __init__(self):
        self.reports_dir = Path.home() / '.config' / 'auryx-agent' / 'reports'
        
    def generate(self, session_data: List[HistoryEntry]) -> Path:
        """Generate Markdown report and return file path"""
```

### 11. Plugin System (`core/plugin_loader.py`)

**Responsibilities:**
- Discover plugins in plugins directory
- Load and validate plugin adapters
- Register plugin commands

**Interface:**
```python
class PluginAdapter(ABC):
    @abstractmethod
    def get_command_name(self) -> str:
        """Return command name for this plugin"""
        
    @abstractmethod
    def execute(self, **kwargs) -> NetworkResult:
        """Execute plugin tool"""

class PluginLoader:
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, PluginAdapter] = {}
        
    def load_plugins(self) -> None:
        """Discover and load all plugins"""
        
    def get_plugin(self, command: str) -> Optional[PluginAdapter]:
        """Get plugin by command name"""
```

## Data Models

### Configuration Schema (TOML)

```toml
default_model = "gpt-4o-mini"
theme = "dark"
auto_update = true

# YellowFire API key - get yours at https://t.me/YellowFireBot
yellowfire_api_key = ""

[network]
default_timeout = 5

[history]
max_entries = 1000

[output]
show_spinners = true
card_width = 60
```

### History Entry Schema (JSON)

```json
{
  "entries": [
    {
      "timestamp": "2025-11-20T10:30:45Z",
      "command": "check google.com latency",
      "model": "gpt-4o-mini",
      "intent": "ping",
      "target": "google.com",
      "result_summary": "Avg latency: 24.3ms",
      "ai_summary": "Google is reachable with low latency."
    }
  ]
}
```

### Network Result Data Structure

```python
@dataclass
class NetworkResult:
    success: bool
    tool: str  # 'ping', 'dns', 'ports', 'traceroute'
    target: str
    data: Dict[str, Any]  # Tool-specific result data
    error: Optional[str]
    duration_ms: float
    timestamp: str
```

**Tool-Specific Data Formats:**

**Ping:**
```python
{
    "packets_sent": 4,
    "packets_received": 4,
    "packet_loss_percent": 0.0,
    "min_ms": 20.1,
    "avg_ms": 24.3,
    "max_ms": 28.7,
    "stddev_ms": 3.2
}
```

**DNS:**
```python
{
    "record_type": "A",
    "records": ["142.250.150.101", "142.250.150.102"],
    "ttl": 300
}
```

**Port Scan:**
```python
{
    "ports_scanned": [80, 443, 22, 3306],
    "open_ports": [80, 443],
    "closed_ports": [22, 3306],
    "scan_duration_ms": 1250
}
```

**Traceroute:**
```python
{
    "hops": [
        {"hop": 1, "ip": "192.168.1.1", "hostname": "router.local", "rtt_ms": 1.2},
        {"hop": 2, "ip": "10.0.0.1", "hostname": "isp-gateway", "rtt_ms": 15.3},
        # ...
    ],
    "destination_reached": true,
    "total_hops": 12
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Configuration loading consistency
*For any* valid TOML configuration file placed at ~/.config/auryx-agent/config.toml, when the Auryx Agent starts, it should successfully load and apply all configuration values.
**Validates: Requirements 1.2, 8.1**

### Property 2: Theme application consistency
*For any* theme value specified in configuration, the formatter should use color schemes corresponding to that theme.
**Validates: Requirements 1.5, 6.5, 8.4**

### Property 3: Model display on startup
*For any* configured default model, when the agent starts, the output should contain the model name.
**Validates: Requirements 1.5**

### Property 3a: Logo display on startup
*For any* agent startup, the output should contain the ASCII art logo.
**Validates: Requirements 1.2**

### Property 3b: Balance display on startup
*For any* agent startup with valid API key, the output should contain the current account balance.
**Validates: Requirements 1.6**

### Property 4: Intent detection and routing
*For any* user query in chat mode, the command parser should produce a valid ParsedCommand with an intent that maps to either a network tool or general chat.
**Validates: Requirements 2.1, 2.2**

### Property 5: Result formatting consistency
*For any* NetworkResult, the formatter should produce output containing box-drawing characters for card borders.
**Validates: Requirements 2.3, 6.2**

### Property 6: AI summary generation
*For any* network tool result, the agent should generate and display an AI summary below the raw results.
**Validates: Requirements 2.4, 10.1, 10.2**

### Property 7: Conversational fallback
*For any* user query that cannot be mapped to a network tool, the agent should provide an AI-generated conversational response.
**Validates: Requirements 2.5**

### Property 8: Model selection override
*For any* model name provided via --model flag, the agent should use that model instead of the default_model from configuration.
**Validates: Requirements 4.1, 8.2**

### Property 9: YellowFire API connection
*For any* valid YellowFire API key, the client should successfully initialize and connect to the API.
**Validates: Requirements 4.2**

### Property 10: Model listing completeness
*For any* set of configured and available models, the list_models() function should return all of them.
**Validates: Requirements 4.3**

### Property 11: Fallback model usage
*For any* unavailable selected model with a configured fallback, the AI Router should attempt to use the fallback model.
**Validates: Requirements 4.4**

### Property 12: Default model selection
*For any* configuration with a default_model set and no CLI override, the agent should use the default_model.
**Validates: Requirements 4.5**

### Property 13: Provider routing correctness
*For any* selected model, the AI Router should route generation requests to the provider that owns that model.
**Validates: Requirements 5.1**

### Property 14: YellowFire API key usage
*For any* model selection, the YellowFire client should use the YELLOWFIRE_API_KEY from configuration.
**Validates: Requirements 5.2, 8.5**

### Property 15: YellowFire API response handling
*For any* successful API response from YellowFire, the client should extract and return the generated text.
**Validates: Requirements 5.3**

### Property 16: Chat history inclusion
*For any* generation request with use_history=True, the YellowFire client should include previous messages in the request.
**Validates: Requirements 5.5**

### Property 18: ANSI color code presence
*For any* formatted output, the result should contain ANSI escape sequences for color.
**Validates: Requirements 6.1**

### Property 19: Multiple result separation
*For any* sequence of multiple NetworkResults, the formatted output should contain visual boundary markers between each result.
**Validates: Requirements 6.4**

### Property 20: History persistence
*For any* command executed in chat mode, the command should appear in the history file after execution.
**Validates: Requirements 7.1**

### Property 21: History entry completeness
*For any* history entry, it should contain command, timestamp, and model fields.
**Validates: Requirements 7.4**

### Property 22: History size management
*For any* history file with more than max_entries, the oldest entries should be removed to maintain the limit.
**Validates: Requirements 7.3**

### Property 23: Timeout configuration propagation
*For any* default_timeout value in configuration, network tool adapters should use that timeout value.
**Validates: Requirements 8.3**

### Property 24: Network tools integration
*For any* network tool adapter initialization, it should successfully import the corresponding function from network_tools repository.
**Validates: Requirements 9.1**

### Property 25: Ping delegation
*For any* ping operation request, the PingAdapter should invoke the ping function from network_tools.
**Validates: Requirements 9.2**

### Property 26: DNS record type support
*For any* DNS record type (A, AAAA, MX, TXT), the DNSAdapter should support lookup of that record type.
**Validates: Requirements 9.3**

### Property 27: Port scan delegation
*For any* port scan request, the PortScanAdapter should invoke the port scanner function from network_tools.
**Validates: Requirements 9.4**

### Property 28: Traceroute delegation
*For any* traceroute request, the TracerouteAdapter should invoke the traceroute function from network_tools.
**Validates: Requirements 9.5**

### Property 29: Report timestamp inclusion
*For any* generated report, it should include timestamps for each command entry.
**Validates: Requirements 11.2**

### Property 30: Report content completeness
*For any* generated report, it should include both raw results and AI summaries for each command.
**Validates: Requirements 11.3**

### Property 31: Report file location and naming
*For any* generated report, it should be saved to ~/.config/auryx-agent/reports/ with a timestamp-based filename.
**Validates: Requirements 11.4**

### Property 32: Plugin discovery
*For any* valid plugin adapter placed in the plugins directory, the PluginLoader should discover and load it.
**Validates: Requirements 12.1**

### Property 33: Plugin command registration
*For any* loaded plugin, its command name should be registered and available in the command parser.
**Validates: Requirements 12.2**

### Property 34: Plugin invocation
*For any* loaded plugin, the agent should be able to invoke its execute method through the unified interface.
**Validates: Requirements 12.3**

### Property 35: Built-in command priority
*For any* plugin that conflicts with a built-in command name, the built-in command should be used.
**Validates: Requirements 12.5**

### Property 36: Timeout error message clarity
*For any* network operation timeout, the error message should include both the timeout event and the configured timeout value.
**Validates: Requirements 13.1**

### Property 37: Missing API key error clarity
*For any* missing API key, the error message should specify which configuration field or environment variable needs to be set.
**Validates: Requirements 13.2**

### Property 38: Provider error message clarity
*For any* provider error, the error message should include the provider's error and suggest checking API key validity.
**Validates: Requirements 13.3**

### Property 39: Network tool error message clarity
*For any* network tool failure, the error message should include the error and suggest common solutions.
**Validates: Requirements 13.4**

### Property 40: Interrupt handling - operation cancellation
*For any* operation in progress, when Ctrl+C is pressed, the operation should be cancelled and the prompt should be restored.
**Validates: Requirements 14.1, 14.5**

### Property 41: Interrupt handling - history preservation
*For any* cancelled operation, partial results should be saved to history before returning to the prompt.
**Validates: Requirements 14.2**

### Property 42: Interrupt handling - configuration integrity
*For any* configuration write operation, if interrupted, the configuration file should remain valid (either old or new, but not corrupted).
**Validates: Requirements 14.3**

### Property 43: Balance retrieval
*For any* valid YellowFire API key, calling get_balance() should return a numeric balance value.
**Validates: Requirements 15.1**

### Property 44: Usage history completeness
*For any* usage entry, it should contain timestamp, comment, and balance_change fields.
**Validates: Requirements 15.4**

### Property 45: Low balance warning
*For any* balance below 0.10 credits, the balance display should include a warning message.
**Validates: Requirements 15.5**

## Error Handling

### Error Categories

1. **Network Errors**
   - Connection timeouts
   - DNS resolution failures
   - Unreachable hosts
   - Port connection failures

2. **Configuration Errors**
   - Missing configuration file
   - Invalid TOML syntax
   - Missing required fields
   - Invalid values

3. **AI Provider Errors**
   - Missing API keys
   - Invalid API keys
   - Rate limiting
   - Service unavailable
   - Network errors to provider

4. **Plugin Errors**
   - Malformed plugin
   - Plugin import failures
   - Plugin execution errors

5. **User Input Errors**
   - Invalid command syntax
   - Invalid host format
   - Invalid parameters

### Error Handling Strategy

**Graceful Degradation:**
- If AI provider fails, display raw results without summary
- If primary model unavailable, fall back to configured fallback model
- If plugin fails to load, log warning and continue with built-in tools

**User-Friendly Messages:**
- All errors should include:
  - Clear description of what went wrong
  - Specific information about the failure (e.g., which API key is missing)
  - Actionable suggestions for resolution
  - Relevant configuration paths or commands

**Error Recovery:**
- Network timeouts should not crash the application
- Invalid user input should prompt for correction
- Configuration errors should offer to create default config
- Interrupted operations should save state before exiting

**Logging:**
- All errors logged to `~/.config/auryx-agent/logs/auryx.log`
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Configurable log level in config.toml
- Log rotation at 10MB with 5 backup files

### Example Error Messages

```
❌ Network Timeout
Failed to reach google.com after 5 seconds.
Configured timeout: 5s (adjust in ~/.config/auryx-agent/config.toml)

💡 Suggestions:
  - Check your internet connection
  - Try increasing the timeout value
  - Verify the host is reachable
```

```
❌ Missing API Key
OpenAI model selected but OPENAI_API_KEY is not configured.

💡 To fix:
  1. Get an API key from https://platform.openai.com
  2. Add it to ~/.config/auryx-agent/config.toml:
     [api_keys]
     openai = "sk-..."
  
  Or set environment variable:
     export OPENAI_API_KEY="sk-..."
```

## Testing Strategy

### Unit Testing

The project will use **pytest** as the testing framework for Python.

**Unit Test Coverage:**

1. **Configuration Management**
   - Test TOML parsing with valid configurations
   - Test default configuration creation
   - Test configuration validation
   - Test handling of missing/invalid config files

2. **AI Router**
   - Test provider initialization with different API key configurations
   - Test model selection and fallback logic
   - Test routing to correct provider based on model
   - Mock external API calls to test error handling

3. **Command Parser**
   - Test intent detection with various user inputs
   - Test parameter extraction for each tool type
   - Test handling of ambiguous queries

4. **Network Tool Adapters**
   - Test adapter initialization
   - Test result normalization
   - Test error handling and timeout behavior
   - Mock network_tools functions to isolate adapter logic

5. **Formatter**
   - Test card layout generation
   - Test ANSI color code application
   - Test theme switching
   - Test multi-result formatting

6. **History Manager**
   - Test entry addition and retrieval
   - Test size limit enforcement
   - Test handling of corrupted history files

7. **Report Generator**
   - Test Markdown generation
   - Test file naming and location
   - Test directory creation

8. **Plugin System**
   - Test plugin discovery
   - Test plugin loading and validation
   - Test command registration
   - Test conflict resolution

### Property-Based Testing

The project will use **Hypothesis** for property-based testing in Python.

**Configuration:**
- Each property-based test should run a minimum of 100 iterations
- Use `@given` decorator with appropriate strategies
- Set `max_examples=100` in test settings

**Property Test Coverage:**

Each property-based test must be tagged with a comment explicitly referencing the correctness property from the design document using this format: `# Feature: auryx-cli-agent, Property {number}: {property_text}`

1. **Configuration Loading (Property 1)**
   - Generate random valid TOML configurations
   - Verify all values are correctly loaded and applied

2. **Theme Application (Property 2)**
   - Generate random theme names
   - Verify formatter uses corresponding color schemes

3. **Intent Detection (Property 4)**
   - Generate random user queries
   - Verify parser always produces valid ParsedCommand

4. **Result Formatting (Property 5)**
   - Generate random NetworkResult objects
   - Verify output contains box-drawing characters

5. **AI Summary Generation (Property 6)**
   - Generate random network results
   - Verify AI summary is generated and positioned correctly

6. **Model Selection (Properties 8, 12)**
   - Generate random model configurations and CLI overrides
   - Verify correct model is selected based on precedence

7. **Provider Routing (Property 13)**
   - Generate random model selections
   - Verify requests route to correct provider

8. **History Persistence (Property 20, 21)**
   - Generate random commands
   - Verify they appear in history with all required fields

9. **History Size Management (Property 22)**
   - Generate more than max_entries commands
   - Verify oldest entries are removed

10. **Timeout Propagation (Property 23)**
    - Generate random timeout values
    - Verify adapters receive correct timeout

11. **DNS Record Type Support (Property 26)**
    - Generate random record types (A, AAAA, MX, TXT)
    - Verify adapter supports all types

12. **Report Generation (Properties 29, 30, 31)**
    - Generate random session data
    - Verify reports contain all required elements and are saved correctly

13. **Plugin Discovery (Property 32)**
    - Generate random valid plugin files
    - Verify all are discovered and loaded

14. **Error Message Clarity (Properties 36-39)**
    - Generate random error conditions
    - Verify error messages contain required information

15. **Interrupt Handling (Properties 40-42)**
    - Simulate interrupts at various points
    - Verify graceful cancellation and state preservation

### Integration Testing

**Integration Test Scenarios:**

1. **End-to-End Chat Mode Flow**
   - Start agent, enter query, verify tool execution and output
   - Test with multiple AI providers

2. **End-to-End Command Mode Flow**
   - Execute direct commands, verify results and exit codes

3. **Configuration to Execution Flow**
   - Load config, verify settings applied throughout execution

4. **Plugin Integration**
   - Load plugin, execute plugin command, verify results

5. **History and Report Generation**
   - Execute commands, verify history saved, generate report, verify content

**Integration tests will:**
- Use real configuration files in temporary directories
- Mock external API calls (AI providers, network operations)
- Verify file system operations (config, history, reports)
- Test error scenarios and recovery

### Test Organization

```
/tests
  /unit
    test_config.py
    test_ai_router.py
    test_command_parser.py
    test_adapters.py
    test_formatter.py
    test_history.py
    test_report_generator.py
    test_plugin_loader.py
  /property
    test_properties_config.py
    test_properties_routing.py
    test_properties_formatting.py
    test_properties_history.py
    test_properties_errors.py
  /integration
    test_chat_mode.py
    test_command_mode.py
    test_plugin_integration.py
  /fixtures
    sample_configs.py
    mock_providers.py
    mock_network_tools.py
```

### Mocking Strategy

**External Dependencies to Mock:**
- AI provider APIs (OpenAI, Gemini, Claude, Ollama)
- network_tools repository functions
- File system operations (for testing error conditions)
- Network operations (for testing timeouts)

**Mocking Libraries:**
- `unittest.mock` for standard mocking
- `pytest-mock` for pytest integration
- `responses` for mocking HTTP requests to Ollama

## Implementation Notes

### Technology Stack

- **Language**: Python 3.10+
- **CLI Framework**: `argparse` for argument parsing, `prompt_toolkit` for interactive REPL
- **Configuration**: `tomli` (Python 3.10) or `tomllib` (Python 3.11+) for TOML parsing
- **AI Service**: YellowFire unified API via `requests` library
- **Formatting**: `rich` library for terminal formatting, colors, and spinners
- **Testing**: `pytest`, `hypothesis`, `pytest-mock`
- **Network Tools**: Integration with existing `network_tools` repository from GitHub

### Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.31.0"
rich = "^13.7.0"
prompt-toolkit = "^3.0.43"
tomli = "^2.0.1"  # For Python < 3.11

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
hypothesis = "^6.92.0"
pytest-mock = "^3.12.0"
responses = "^0.24.0"
```

### Project Structure

```
auryx-agent/
├── auryx_agent/
│   ├── __init__.py
│   ├── __main__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── yellowfire_client.py
│   │   ├── command_parser.py
│   │   ├── formatter.py
│   │   ├── history.py
│   │   ├── report_generator.py
│   │   └── plugin_loader.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── ping_adapter.py
│   │   │   ├── dns_adapter.py
│   │   │   ├── ports_adapter.py
│   │   │   └── traceroute_adapter.py
│   │   └── models.py
│   └── cli/
│       ├── __init__.py
│       ├── chat_mode.py
│       └── command_mode.py
├── plugins/
│   └── .gitkeep
├── tests/
│   ├── unit/
│   ├── property/
│   ├── integration/
│   └── fixtures/
├── pyproject.toml
├── README.md
└── LICENSE
```

### Configuration File Template

```toml
# Auryx Agent Configuration

# Default AI model to use (see YellowFire API docs for available models)
default_model = "gpt-4o-mini"

# Fallback model if primary is unavailable
fallback_model = "gpt-3.5-turbo"

# UI theme (dark, light)
theme = "dark"

# Enable automatic updates
auto_update = true

# YellowFire API Key
# Get your free API key: https://t.me/YellowFireBot -> /get_api
# Free balance: $1
[api_keys]
yellowfire = ""

# Network settings
[network]
default_timeout = 5

# History settings
[history]
max_entries = 1000

# Output settings
[output]
show_spinners = true
card_width = 60
show_logo = true

# Logging settings
[logging]
level = "INFO"
file = "~/.config/auryx-agent/logs/auryx.log"
```

### Security Considerations

1. **API Key Storage**
   - Configuration file should have restricted permissions (600)
   - Warn user if config file has overly permissive permissions
   - Support environment variables as alternative to config file
   - Never log API keys

2. **Input Validation**
   - Validate all user inputs before passing to network tools
   - Sanitize inputs to prevent command injection
   - Validate host formats and IP addresses

3. **Plugin Security**
   - Plugins should run with same permissions as main application
   - Validate plugin structure before loading
   - Catch and handle plugin exceptions to prevent crashes

4. **Network Operations**
   - Respect timeout configurations
   - Handle malicious responses gracefully
   - Validate data from network operations before processing

### Performance Considerations

1. **AI Provider Calls**
   - Implement request timeout (30 seconds default)
   - Cache provider initialization
   - Reuse HTTP connections where possible

2. **History Management**
   - Load history lazily (only when needed)
   - Use efficient JSON serialization
   - Implement history size limits to prevent unbounded growth

3. **Plugin Loading**
   - Load plugins once at startup
   - Cache plugin metadata
   - Skip invalid plugins quickly

4. **Output Formatting**
   - Stream output for long results
   - Limit output size for very large results
   - Use efficient string building

### Future Enhancements

1. **Additional Network Tools**
   - HTTP/HTTPS connectivity checks
   - SSL certificate inspection
   - Bandwidth testing
   - Packet capture analysis

2. **Enhanced AI Features**
   - Multi-turn conversations with context
   - Learning from user corrections
   - Automated troubleshooting workflows

3. **Collaboration Features**
   - Share reports with team members
   - Export results in multiple formats (JSON, CSV)
   - Integration with monitoring systems

4. **Advanced UI**
   - Split-pane view for results
   - Interactive result exploration
   - Graph visualization for traceroute

5. **Automation**
   - Scheduled diagnostic runs
   - Alert on threshold violations
   - Integration with CI/CD pipelines
