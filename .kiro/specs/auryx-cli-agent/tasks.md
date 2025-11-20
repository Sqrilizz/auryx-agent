# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create Python package structure with core/, providers/, tools/, cli/ directories
  - Set up pyproject.toml with Poetry for dependency management
  - Install required dependencies: openai, google-generativeai, anthropic, requests, rich, prompt-toolkit, tomli
  - Set up pytest, hypothesis, pytest-mock for testing
  - Create basic __init__.py files for all packages
  - _Requirements: 1.1, 1.2_

- [x] 2. Implement configuration management
  - Create Config dataclass with all configuration fields
  - Implement load_config() to parse TOML from ~/.config/auryx-agent/config.toml
  - Implement create_default_config() to generate default configuration file
  - Add configuration validation logic
  - Handle missing and corrupted configuration files gracefully
  - _Requirements: 1.2, 1.3, 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 2.1 Write property test for configuration loading
  - **Property 1: Configuration loading consistency**
  - **Validates: Requirements 1.2, 8.1**

- [x] 2.2 Write unit tests for configuration edge cases
  - Test missing configuration file handling
  - Test invalid TOML syntax handling
  - Test default configuration creation
  - _Requirements: 1.3_

- [x] 3. Implement AI Router with YellowFire API integration
  - Create AIRouter class with YellowFire API endpoint configuration
  - Implement generate() method to send requests to YellowFire chatgpt endpoint
  - Implement get_balance() method to retrieve account balance
  - Implement get_usage() method to retrieve usage history
  - Implement list_models() method (can be hardcoded list of YellowFire models)
  - Implement model selection and fallback logic
  - Add proper error handling for API errors
  - _Requirements: 4.1, 4.2, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5, 15.1, 15.3_

- [x] 3.1 Write property test for provider detection
  - **Property 9: Provider detection**
  - **Validates: Requirements 4.2**

- [ ]* 3.2 Write property test for provider routing
  - **Property 13: Provider routing correctness**
  - **Validates: Requirements 5.1**

- [ ]* 3.3 Write property test for model selection
  - **Property 8: Model selection override**
  - **Property 12: Default model selection**
  - **Validates: Requirements 4.1, 4.5, 8.2**

- [ ]* 3.4 Write property test for YellowFire API key usage
  - **Property 14: API key usage - YellowFire**
  - **Validates: Requirements 5.2, 8.5**

- [ ]* 3.5 Write property test for balance retrieval
  - **Property 43: Balance retrieval**
  - **Validates: Requirements 15.1**

- [ ]* 3.6 Write property test for usage history
  - **Property 44: Usage history completeness**
  - **Validates: Requirements 15.4**

- [ ]* 3.7 Write property test for low balance warning
  - **Property 45: Low balance warning**
  - **Validates: Requirements 15.5**

- [ ]* 3.8 Write property test for fallback model
  - **Property 11: Fallback model usage**
  - **Validates: Requirements 4.4**

- [ ]* 3.9 Write unit tests for API error handling
  - Test missing API key scenarios
  - Test API service unavailable scenarios
  - Test rate limiting handling
  - Test insufficient balance scenarios
  - _Requirements: 13.2, 13.3_

- [ ] 4. Implement network tool adapters
  - Create NetworkResult dataclass for normalized results
  - Implement PingAdapter wrapping network_tools ping function
  - Implement DNSAdapter wrapping network_tools DNS lookup with support for A, AAAA, MX, TXT records
  - Implement PortScanAdapter wrapping network_tools port scanner
  - Implement TracerouteAdapter wrapping network_tools traceroute
  - Add timeout configuration support to all adapters
  - Add error handling and result normalization to all adapters
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 8.3_

- [ ]* 4.1 Write property test for network tools integration
  - **Property 24: Network tools integration**
  - **Validates: Requirements 9.1**

- [ ]* 4.2 Write property test for ping delegation
  - **Property 25: Ping delegation**
  - **Validates: Requirements 9.2**

- [ ]* 4.3 Write property test for DNS record type support
  - **Property 26: DNS record type support**
  - **Validates: Requirements 9.3**

- [ ]* 4.4 Write property test for port scan delegation
  - **Property 27: Port scan delegation**
  - **Validates: Requirements 9.4**

- [ ]* 4.5 Write property test for traceroute delegation
  - **Property 28: Traceroute delegation**
  - **Validates: Requirements 9.5**

- [ ]* 4.6 Write property test for timeout propagation
  - **Property 23: Timeout configuration propagation**
  - **Validates: Requirements 8.3**

- [ ]* 4.7 Write unit tests for adapter error handling
  - Test network timeout scenarios
  - Test invalid host handling
  - Test connection failures
  - _Requirements: 13.1, 13.4, 13.5_

- [ ] 5. Implement formatter and output rendering
  - Create Formatter class with theme support
  - Design and implement ASCII art logo for Auryx Agent
  - Implement format_logo() to display colored ASCII art
  - Implement format_result() to render NetworkResult as bordered cards using box-drawing characters
  - Implement ANSI color code application for syntax highlighting
  - Implement format_ai_summary() for AI summary styling
  - Implement format_balance() to display balance with optional low balance warning
  - Implement format_usage() to display usage history as formatted table
  - Implement format_error() for error message formatting
  - Implement spinner() context manager using rich library
  - Add support for dark and light themes
  - Implement multi-result formatting with visual boundaries
  - _Requirements: 1.2, 6.1, 6.2, 6.3, 6.4, 6.5, 15.2, 15.4, 15.5_

- [ ]* 5.1 Write property test for result formatting
  - **Property 5: Result formatting consistency**
  - **Validates: Requirements 2.3, 6.2**

- [ ]* 5.2 Write property test for ANSI color codes
  - **Property 18: ANSI color code presence**
  - **Validates: Requirements 6.1**

- [ ]* 5.3 Write property test for theme application
  - **Property 2: Theme application consistency**
  - **Validates: Requirements 1.5, 6.5, 8.4**

- [ ]* 5.4 Write property test for multiple result separation
  - **Property 19: Multiple result separation**
  - **Validates: Requirements 6.4**

- [ ]* 5.5 Write property test for logo display
  - **Property 3a: Logo display on startup**
  - **Validates: Requirements 1.2**

- [ ]* 5.6 Write property test for balance display
  - **Property 3b: Balance display on startup**
  - **Validates: Requirements 1.6**

- [ ]* 5.7 Write unit tests for formatter edge cases
  - Test very long result data
  - Test special characters in results
  - Test empty results
  - Test balance formatting with different values
  - _Requirements: 6.1, 6.2, 15.2_

- [ ] 6. Implement command parser and intent detection
  - Create ParsedCommand dataclass for parsed user input
  - Implement CommandParser class with AI-powered intent detection
  - Implement parse() method to analyze user input and extract intent
  - Implement parameter extraction for each tool type (host, ports, record types, etc.)
  - Add routing logic to map intents to network tools or general chat
  - Handle ambiguous queries gracefully
  - _Requirements: 2.1, 2.2, 2.5_

- [ ]* 6.1 Write property test for intent detection
  - **Property 4: Intent detection and routing**
  - **Validates: Requirements 2.1, 2.2**

- [ ]* 6.2 Write property test for conversational fallback
  - **Property 7: Conversational fallback**
  - **Validates: Requirements 2.5**

- [ ]* 6.3 Write unit tests for parameter extraction
  - Test host extraction from various query formats
  - Test port list extraction
  - Test DNS record type extraction
  - _Requirements: 2.1_

- [ ] 7. Implement history management
  - Create HistoryEntry dataclass with timestamp, command, model, result_summary fields
  - Implement HistoryManager class with JSON file operations
  - Implement add_entry() to append commands to ~/.config/auryx-agent/history.json
  - Implement get_history() to retrieve and display history entries
  - Implement size limit enforcement (remove oldest entries when exceeding max_entries)
  - Add graceful handling of missing or corrupted history files
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 7.1 Write property test for history persistence
  - **Property 20: History persistence**
  - **Validates: Requirements 7.1**

- [ ]* 7.2 Write property test for history entry completeness
  - **Property 21: History entry completeness**
  - **Validates: Requirements 7.4**

- [ ]* 7.3 Write property test for history size management
  - **Property 22: History size management**
  - **Validates: Requirements 7.3**

- [ ]* 7.4 Write unit tests for history edge cases
  - Test corrupted history file handling
  - Test missing history file handling
  - Test concurrent access scenarios
  - _Requirements: 7.5_

- [ ] 8. Implement report generator
  - Create ReportGenerator class
  - Implement generate() method to create Markdown reports from session data
  - Include timestamps for each command in reports
  - Include both raw results and AI summaries in reports
  - Save reports to ~/.config/auryx-agent/reports/ with timestamp-based filenames
  - Create reports directory if it doesn't exist
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ]* 8.1 Write property test for report timestamp inclusion
  - **Property 29: Report timestamp inclusion**
  - **Validates: Requirements 11.2**

- [ ]* 8.2 Write property test for report content completeness
  - **Property 30: Report content completeness**
  - **Validates: Requirements 11.3**

- [ ]* 8.3 Write property test for report file location
  - **Property 31: Report file location and naming**
  - **Validates: Requirements 11.4**

- [ ]* 8.4 Write unit tests for report generation edge cases
  - Test empty session data
  - Test missing reports directory
  - Test report generation with special characters
  - _Requirements: 11.5_

- [ ] 9. Implement plugin system
  - Create PluginAdapter abstract base class with get_command_name() and execute() methods
  - Implement PluginLoader class to discover plugins in plugins directory
  - Implement load_plugins() to scan and load plugin adapters
  - Add plugin validation to handle malformed plugins gracefully
  - Implement command registration for loaded plugins
  - Add conflict resolution to prioritize built-in commands over plugins
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ]* 9.1 Write property test for plugin discovery
  - **Property 32: Plugin discovery**
  - **Validates: Requirements 12.1**

- [ ]* 9.2 Write property test for plugin command registration
  - **Property 33: Plugin command registration**
  - **Validates: Requirements 12.2**

- [ ]* 9.3 Write property test for plugin invocation
  - **Property 34: Plugin invocation**
  - **Validates: Requirements 12.3**

- [ ]* 9.4 Write property test for built-in command priority
  - **Property 35: Built-in command priority**
  - **Validates: Requirements 12.5**

- [ ]* 9.5 Write unit tests for plugin error handling
  - Test malformed plugin handling
  - Test plugin import failures
  - Test plugin execution errors
  - _Requirements: 12.4_

- [ ] 10. Implement chat mode
  - Create ChatSession class with REPL loop
  - Initialize AIRouter, CommandParser, Formatter, and HistoryManager
  - Implement run() method for interactive loop using prompt_toolkit
  - Display ASCII art logo on startup
  - Display current model name on startup
  - Display account balance on startup with low balance warning if needed
  - Implement handle_input() to process user queries
  - Coordinate between parser, AI router, and network tools
  - Display formatted results and AI summaries
  - Add session history tracking
  - _Requirements: 1.2, 1.5, 1.6, 2.1, 2.2, 2.3, 2.4, 2.5, 10.1, 10.2_

- [ ]* 10.1 Write property test for AI summary generation
  - **Property 6: AI summary generation**
  - **Validates: Requirements 2.4, 10.1, 10.2**

- [ ]* 10.2 Write property test for model display
  - **Property 3: Model display on startup**
  - **Validates: Requirements 1.5**

- [ ]* 10.3 Write integration tests for chat mode
  - Test end-to-end chat flow with mocked AI and network tools
  - Test multiple commands in sequence
  - Test history persistence during session
  - Test startup display (logo, model, balance)
  - _Requirements: 1.2, 1.5, 1.6, 2.1, 2.2, 2.3, 2.4_

- [ ] 11. Implement command mode
  - Implement execute_command() function for direct CLI invocation
  - Add support for "auryx-agent ping <host>" command
  - Add support for "auryx-agent ports scan <host>" command
  - Add support for "auryx-agent dns <host>" command
  - Add support for "auryx-agent traceroute <host>" command
  - Add support for "auryx-agent history" command
  - Add support for "auryx-agent report" command
  - Add support for "auryx-agent balance" command to display current balance
  - Add support for "auryx-agent usage" command to display usage history
  - Return appropriate exit codes (0 for success, non-zero for errors)
  - Display usage help for invalid arguments
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 7.2, 11.1, 15.1, 15.3_

- [ ]* 11.1 Write unit tests for command mode
  - Test each direct command invocation
  - Test balance and usage commands
  - Test exit code handling
  - Test invalid argument handling
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 15.1, 15.3_

- [ ]* 11.2 Write integration tests for command mode
  - Test end-to-end command execution
  - Test output formatting in command mode
  - Test balance and usage display
  - Test error scenarios
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 15.1, 15.3_

- [ ] 12. Implement CLI entry point
  - Create main() function in __main__.py
  - Implement argument parsing with argparse for mode selection and options
  - Add --model flag for model selection
  - Load configuration on startup
  - Route to chat_mode() or command_mode() based on arguments
  - Initialize logging system
  - Handle startup errors gracefully
  - _Requirements: 1.1, 1.2, 4.1_

- [ ]* 12.1 Write unit tests for CLI entry point
  - Test argument parsing
  - Test mode routing
  - Test model flag handling
  - _Requirements: 1.1, 4.1_

- [ ] 13. Implement error handling and user-friendly messages
  - Create error message templates for each error category
  - Implement timeout error messages with configured timeout value
  - Implement missing YellowFire API key error with instructions to get key from Telegram bot
  - Implement YellowFire API error messages with troubleshooting suggestions
  - Implement low balance error messages with top-up instructions
  - Implement network tool error messages with common solutions
  - Implement invalid host error messages with format examples
  - Add logging to ~/.config/auryx-agent/logs/auryx.log
  - Implement log rotation
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ]* 13.1 Write property test for timeout error messages
  - **Property 36: Timeout error message clarity**
  - **Validates: Requirements 13.1**

- [ ]* 13.2 Write property test for missing API key errors
  - **Property 37: Missing API key error clarity**
  - **Validates: Requirements 13.2**

- [ ]* 13.3 Write property test for YellowFire API error messages
  - **Property 38: Provider error message clarity**
  - **Validates: Requirements 13.3**

- [ ]* 13.4 Write property test for network tool error messages
  - **Property 39: Network tool error message clarity**
  - **Validates: Requirements 13.4**

- [ ]* 13.5 Write unit tests for error handling
  - Test error message formatting
  - Test logging functionality
  - Test log rotation
  - _Requirements: 13.1, 13.2, 13.3, 13.4_

- [ ] 14. Implement interrupt handling
  - Add Ctrl+C signal handler for graceful cancellation
  - Implement operation cancellation logic
  - Save partial results to history on interruption
  - Ensure configuration writes are atomic to prevent corruption
  - Display cancellation message and restore prompt after interruption
  - _Requirements: 14.1, 14.2, 14.3, 14.5_

- [ ]* 14.1 Write property test for interrupt handling
  - **Property 40: Interrupt handling - operation cancellation**
  - **Property 41: Interrupt handling - history preservation**
  - **Property 42: Interrupt handling - configuration integrity**
  - **Validates: Requirements 14.1, 14.2, 14.3, 14.5**

- [ ]* 14.2 Write unit tests for interrupt scenarios
  - Test interruption during network operations
  - Test interruption during AI generation
  - Test interruption during file writes
  - _Requirements: 14.1, 14.2, 14.3_

- [ ] 15. Create documentation and examples
  - Write README.md with installation instructions
  - Document configuration options
  - Provide usage examples for chat mode and command mode
  - Document plugin development guide
  - Create example plugin
  - Add inline code documentation
  - _Requirements: All_

- [ ] 16. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
