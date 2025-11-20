# Requirements Document

## Introduction

The Auryx CLI Agent is a local command-line interface tool that combines AI-powered natural language processing with network diagnostic utilities. The system integrates tools from the network_tools repository (ping, nslookup, traceroute, port scanner) and provides an interactive interface similar to kiro.dev. Users can select from multiple AI models through the YellowFire unified API service, which provides access to GPT, Claude, Gemini, DeepSeek, and other models through a single API key.

## Glossary

- **Auryx Agent**: The CLI application system that combines AI and network tools
- **AI Router**: The module responsible for managing AI model selection and requests
- **Network Tools**: The collection of diagnostic utilities (ping, DNS lookup, traceroute, port scanner, etc.)
- **Chat Mode**: Interactive conversational interface where users type natural language queries
- **Command Mode**: Direct invocation of network tools via CLI arguments
- **TUI**: Text User Interface with ANSI colors and formatted output
- **YellowFire API**: Unified API service providing access to multiple AI models (GPT, Claude, Gemini, DeepSeek, etc.) through a single endpoint

## Requirements

### Requirement 1

**User Story:** As a network administrator, I want to launch the CLI agent with a single command, so that I can quickly access network diagnostic tools through an AI-powered interface.

#### Acceptance Criteria

1. WHEN a user executes the command "auryx-agent" THEN the Auryx Agent SHALL start and display the interactive interface
2. WHEN the Auryx Agent starts THEN the Auryx Agent SHALL display an ASCII art logo
3. WHEN the Auryx Agent starts THEN the Auryx Agent SHALL load configuration from ~/.config/auryx-agent/config.toml
4. WHEN the configuration file does not exist THEN the Auryx Agent SHALL create a default configuration file with placeholder values
5. WHEN the Auryx Agent starts THEN the Auryx Agent SHALL display the currently selected AI model name
6. WHEN the Auryx Agent starts THEN the Auryx Agent SHALL display the current account balance from YellowFire API
7. WHEN the Auryx Agent starts THEN the Auryx Agent SHALL apply the theme specified in the configuration

### Requirement 2

**User Story:** As a user, I want to interact with the agent in chat mode using natural language, so that I can perform network diagnostics without memorizing command syntax.

#### Acceptance Criteria

1. WHEN a user enters a natural language query in chat mode THEN the Auryx Agent SHALL interpret the intent using the selected AI model
2. WHEN the AI model identifies a network diagnostic task THEN the Auryx Agent SHALL execute the corresponding network tool function
3. WHEN a network tool completes execution THEN the Auryx Agent SHALL display the results in a formatted card layout
4. WHEN network tool results are available THEN the Auryx Agent SHALL generate an AI summary of the results
5. WHEN a user query cannot be mapped to a network tool THEN the Auryx Agent SHALL provide a conversational AI response

### Requirement 3

**User Story:** As a power user, I want to invoke network tools directly via command-line arguments, so that I can integrate the agent into scripts and automation workflows.

#### Acceptance Criteria

1. WHEN a user executes "auryx-agent ping <host>" THEN the Auryx Agent SHALL perform a ping operation and display results
2. WHEN a user executes "auryx-agent ports scan <host>" THEN the Auryx Agent SHALL perform a port scan and display results
3. WHEN a user executes "auryx-agent dns <host>" THEN the Auryx Agent SHALL perform DNS lookup and display results
4. WHEN a user executes "auryx-agent traceroute <host>" THEN the Auryx Agent SHALL perform a traceroute and display results
5. WHEN invalid command arguments are provided THEN the Auryx Agent SHALL display usage help and exit with a non-zero status code

### Requirement 4

**User Story:** As a user, I want to select from multiple AI models through the YellowFire API, so that I can choose the best model for my needs without managing multiple API keys.

#### Acceptance Criteria

1. WHEN a user executes "auryx-agent --model <model_name>" THEN the Auryx Agent SHALL use the specified model for that session
2. WHEN the AI Router initializes THEN the AI Router SHALL connect to the YellowFire API using the configured API key
3. WHEN a user requests to list models THEN the Auryx Agent SHALL display all available models from YellowFire API
4. WHEN a selected model is unavailable THEN the AI Router SHALL attempt to use the fallback model specified in configuration
5. WHERE multiple models are available THEN the Auryx Agent SHALL use the default_model from configuration unless overridden

### Requirement 5

**User Story:** As a developer, I want the AI Router to use the YellowFire unified API, so that I can access multiple AI models with a single API key and simplified implementation.

#### Acceptance Criteria

1. WHEN the AI Router receives a generation request THEN the AI Router SHALL send it to the YellowFire API with the selected model parameter
2. WHEN communicating with YellowFire API THEN the AI Router SHALL use the YELLOWFIRE_API_KEY from configuration
3. WHEN the YellowFire API returns a response THEN the AI Router SHALL extract and return the generated text
4. WHEN the YellowFire API returns an error THEN the AI Router SHALL handle it gracefully and provide a clear error message
5. WHEN sending requests THEN the AI Router SHALL include chat history for multi-turn conversations

### Requirement 6

**User Story:** As a user, I want network diagnostic results displayed in a visually appealing format, so that I can quickly understand the information.

#### Acceptance Criteria

1. WHEN displaying results THEN the Auryx Agent SHALL use ANSI color codes for syntax highlighting
2. WHEN displaying results THEN the Auryx Agent SHALL render information in bordered card layouts using box-drawing characters
3. WHEN executing long-running operations THEN the Auryx Agent SHALL display an animated spinner
4. WHEN multiple results are displayed THEN the Auryx Agent SHALL separate them with clear visual boundaries
5. WHERE a dark theme is configured THEN the Auryx Agent SHALL use color schemes optimized for dark terminal backgrounds

### Requirement 7

**User Story:** As a user, I want my command history saved across sessions, so that I can review past diagnostics and repeat commands easily.

#### Acceptance Criteria

1. WHEN a user executes a command in chat mode THEN the Auryx Agent SHALL append it to ~/.config/auryx-agent/history.json
2. WHEN a user executes "auryx-agent history" THEN the Auryx Agent SHALL display previous commands with timestamps
3. WHEN the history file exceeds 1000 entries THEN the Auryx Agent SHALL remove the oldest entries
4. WHEN storing history THEN the Auryx Agent SHALL include the command, timestamp, and selected model
5. WHEN reading history THEN the Auryx Agent SHALL handle missing or corrupted history files gracefully

### Requirement 8

**User Story:** As a user, I want to configure the agent's behavior through a configuration file, so that I can customize settings without modifying code.

#### Acceptance Criteria

1. WHEN the Auryx Agent reads configuration THEN the Auryx Agent SHALL parse the TOML file at ~/.config/auryx-agent/config.toml
2. WHEN configuration specifies default_model THEN the Auryx Agent SHALL use that model unless overridden by command-line arguments
3. WHEN configuration specifies default_timeout THEN the Network Tools SHALL use that timeout for network operations
4. WHEN configuration specifies theme THEN the Auryx Agent SHALL apply the corresponding color scheme
5. WHEN configuration contains the YellowFire API key THEN the AI Router SHALL use it for authenticating with the YellowFire API

### Requirement 9

**User Story:** As a user, I want the agent to integrate seamlessly with network_tools repository functions, so that I can leverage existing diagnostic capabilities.

#### Acceptance Criteria

1. WHEN the Auryx Agent initializes THEN the Auryx Agent SHALL import and wrap functions from the network_tools repository
2. WHEN executing a ping operation THEN the Auryx Agent SHALL call the ping function from network_tools
3. WHEN executing a DNS lookup THEN the Auryx Agent SHALL call the DNS lookup function and support A, AAAA, MX, and TXT record types
4. WHEN executing a port scan THEN the Auryx Agent SHALL call the port scanner function from network_tools
5. WHEN executing a traceroute THEN the Auryx Agent SHALL call the traceroute function from network_tools

### Requirement 10

**User Story:** As a user, I want the AI to analyze network diagnostic results, so that I can understand issues without deep networking knowledge.

#### Acceptance Criteria

1. WHEN network tool results are obtained THEN the Auryx Agent SHALL send them to the AI model for analysis
2. WHEN the AI generates a summary THEN the Auryx Agent SHALL display it below the raw results
3. WHEN ping latency exceeds 100ms THEN the AI summary SHALL indicate potential connectivity issues
4. WHEN port scan shows closed ports THEN the AI summary SHALL explain possible causes
5. WHEN DNS lookup fails THEN the AI summary SHALL suggest troubleshooting steps

### Requirement 11

**User Story:** As a user, I want to generate reports of diagnostic sessions, so that I can document network issues for later reference.

#### Acceptance Criteria

1. WHEN a user executes "auryx-agent report" THEN the Auryx Agent SHALL generate a Markdown file with the current session's commands and results
2. WHEN generating a report THEN the Auryx Agent SHALL include timestamps for each command
3. WHEN generating a report THEN the Auryx Agent SHALL include both raw results and AI summaries
4. WHEN generating a report THEN the Auryx Agent SHALL save it to ~/.config/auryx-agent/reports/ with a timestamp-based filename
5. WHEN the reports directory does not exist THEN the Auryx Agent SHALL create it

### Requirement 12

**User Story:** As a developer, I want a plugin system for adding new network tools, so that the agent can be extended without modifying core code.

#### Acceptance Criteria

1. WHEN the Auryx Agent starts THEN the Auryx Agent SHALL scan the plugins directory for available tool adapters
2. WHEN a plugin adapter is found THEN the Auryx Agent SHALL register its commands with the command parser
3. WHEN a plugin provides a tool function THEN the AI Router SHALL be able to invoke it through the unified interface
4. WHEN a plugin is malformed THEN the Auryx Agent SHALL log a warning and continue loading other plugins
5. WHERE a plugin conflicts with a built-in command THEN the Auryx Agent SHALL prioritize the built-in command

### Requirement 13

**User Story:** As a user, I want error messages to be clear and actionable, so that I can resolve issues quickly.

#### Acceptance Criteria

1. WHEN a network operation times out THEN the Auryx Agent SHALL display a message indicating the timeout and the configured timeout value
2. WHEN the YellowFire API key is missing THEN the Auryx Agent SHALL display instructions for obtaining and configuring the API key
3. WHEN the YellowFire API returns an error THEN the Auryx Agent SHALL display the error message and suggest checking API key validity or account balance
4. WHEN a network tool fails THEN the Auryx Agent SHALL display the error and suggest common solutions
5. WHEN an invalid host is provided THEN the Auryx Agent SHALL display a message explaining the expected format

### Requirement 14

**User Story:** As a user, I want the agent to handle interruptions gracefully, so that I can cancel long-running operations without corrupting state.

#### Acceptance Criteria

1. WHEN a user presses Ctrl+C during an operation THEN the Auryx Agent SHALL cancel the operation and return to the prompt
2. WHEN an operation is cancelled THEN the Auryx Agent SHALL save any partial results to history
3. WHEN the agent is interrupted during configuration write THEN the Auryx Agent SHALL ensure the configuration file remains valid
4. WHEN the agent is interrupted during report generation THEN the Auryx Agent SHALL complete writing the current section before exiting
5. WHEN returning from an interruption THEN the Auryx Agent SHALL display a cancellation message and restore the prompt

### Requirement 15

**User Story:** As a user, I want to check my account balance, so that I can monitor my API usage and costs.

#### Acceptance Criteria

1. WHEN a user executes "auryx-agent balance" THEN the Auryx Agent SHALL display the current account balance from YellowFire API
2. WHEN displaying balance THEN the Auryx Agent SHALL show the balance with appropriate precision (8 decimal places)
3. WHEN a user executes "auryx-agent usage" THEN the Auryx Agent SHALL display recent usage history with timestamps
4. WHEN displaying usage history THEN the Auryx Agent SHALL show timestamp, operation description, and balance change for each entry
5. WHEN the balance is low (below 0.10 credits) THEN the Auryx Agent SHALL display a warning message with instructions to top up
