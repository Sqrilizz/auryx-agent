"""Formatter for beautiful console output."""

from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    
    # Basic colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class Formatter:
    """Formatter for beautiful console output."""
    
    def __init__(self, theme: str = "dark"):
        """Initialize formatter with theme.
        
        Args:
            theme: Color theme (dark or light)
        """
        self.theme = theme
        self.colors = Colors()
    
    def logo(self) -> str:
        """Return ASCII art logo with colors."""
        logo = f"""
{self.colors.BRIGHT_CYAN}{self.colors.BOLD}
    ___                           
   /   | __  ___________  ___  __
  / /| |/ / / / ___/ __ \\/ / |/ /
 / ___ / /_/ / /  / /_/ /|   /  
/_/  |_\\__,_/_/   \\____/_/|_|   
{self.colors.RESET}                                 
{self.colors.BRIGHT_MAGENTA}Network Diagnostic AI Agent{self.colors.RESET}
{self.colors.DIM}Powered by YellowFire API{self.colors.RESET}
"""
        return logo
    
    def header(self, text: str, width: int = 70) -> str:
        """Format a header with borders.
        
        Args:
            text: Header text
            width: Width of header
            
        Returns:
            Formatted header string
        """
        border = "═" * width
        padding = (width - len(text) - 2) // 2
        
        return f"""
{self.colors.BRIGHT_BLUE}{border}{self.colors.RESET}
{self.colors.BRIGHT_BLUE}{self.colors.BOLD}{' ' * padding} {text} {' ' * padding}{self.colors.RESET}
{self.colors.BRIGHT_BLUE}{border}{self.colors.RESET}
"""
    
    def success(self, text: str) -> str:
        """Format success message.
        
        Args:
            text: Message text
            
        Returns:
            Formatted success message
        """
        return f"{self.colors.BRIGHT_GREEN}✓{self.colors.RESET} {text}"
    
    def error(self, text: str) -> str:
        """Format error message.
        
        Args:
            text: Error text
            
        Returns:
            Formatted error message
        """
        return f"{self.colors.BRIGHT_RED}✗{self.colors.RESET} {self.colors.RED}{text}{self.colors.RESET}"
    
    def warning(self, text: str) -> str:
        """Format warning message.
        
        Args:
            text: Warning text
            
        Returns:
            Formatted warning message
        """
        return f"{self.colors.BRIGHT_YELLOW}⚠{self.colors.RESET} {self.colors.YELLOW}{text}{self.colors.RESET}"
    
    def info(self, text: str) -> str:
        """Format info message.
        
        Args:
            text: Info text
            
        Returns:
            Formatted info message
        """
        return f"{self.colors.BRIGHT_CYAN}ℹ{self.colors.RESET} {self.colors.CYAN}{text}{self.colors.RESET}"
    
    def prompt(self, text: str) -> str:
        """Format user prompt.
        
        Args:
            text: Prompt text
            
        Returns:
            Formatted prompt
        """
        return f"{self.colors.BRIGHT_GREEN}{self.colors.BOLD}You:{self.colors.RESET} {text}"
    
    def assistant(self, name: str, text: str) -> str:
        """Format assistant response.
        
        Args:
            name: Assistant name
            text: Response text
            
        Returns:
            Formatted response
        """
        return f"{self.colors.BRIGHT_MAGENTA}{self.colors.BOLD}{name}:{self.colors.RESET} {text}"
    
    def model_badge(self, model: str, is_current: bool = False) -> str:
        """Format model name as a badge.
        
        Args:
            model: Model name
            is_current: Whether this is the current model
            
        Returns:
            Formatted model badge
        """
        if is_current:
            return f"{self.colors.BG_BLUE}{self.colors.WHITE}{self.colors.BOLD} {model} {self.colors.RESET}"
        else:
            return f"{self.colors.BRIGHT_BLACK}[{self.colors.RESET}{model}{self.colors.BRIGHT_BLACK}]{self.colors.RESET}"
    
    def section(self, title: str, emoji: str = "") -> str:
        """Format section header.
        
        Args:
            title: Section title
            emoji: Optional emoji
            
        Returns:
            Formatted section header
        """
        return f"\n{emoji} {self.colors.BRIGHT_WHITE}{self.colors.BOLD}{title}{self.colors.RESET}"
    
    def divider(self, width: int = 70, char: str = "─") -> str:
        """Format a divider line.
        
        Args:
            width: Width of divider
            char: Character to use
            
        Returns:
            Formatted divider
        """
        return f"{self.colors.BRIGHT_BLACK}{char * width}{self.colors.RESET}"
    
    def command(self, cmd: str, description: str) -> str:
        """Format a command with description.
        
        Args:
            cmd: Command text
            description: Command description
            
        Returns:
            Formatted command line
        """
        return f"  {self.colors.BRIGHT_CYAN}{cmd:<20}{self.colors.RESET} {self.colors.DIM}{description}{self.colors.RESET}"
    
    def key_value(self, key: str, value: str, key_color: Optional[str] = None) -> str:
        """Format key-value pair.
        
        Args:
            key: Key text
            value: Value text
            key_color: Optional color for key
            
        Returns:
            Formatted key-value pair
        """
        if key_color is None:
            key_color = self.colors.BRIGHT_WHITE
        
        return f"  {key_color}{key}:{self.colors.RESET} {value}"
    
    def spinner_frame(self, frame: int) -> str:
        """Get spinner animation frame.
        
        Args:
            frame: Frame number
            
        Returns:
            Spinner character
        """
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        return f"{self.colors.BRIGHT_CYAN}{frames[frame % len(frames)]}{self.colors.RESET}"
