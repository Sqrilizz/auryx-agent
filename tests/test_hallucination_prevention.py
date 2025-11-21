"""Tests for hallucination prevention in agent responses."""

import pytest


class MockAgent:
    """Mock agent with only hallucination detection method."""
    
    def _detect_hallucination_risk(self, user_input: str, response: str) -> bool:
        """Detect if response might contain hallucinated data."""
        system_info_keywords = [
            'neofetch', 'system info', 'disk usage', 'disk space', 'memory', 'cpu', 'processes',
            'running', 'network', 'connections', 'files', 'directory', 'ls',
            'ps', 'top', 'df', 'free', 'ifconfig', 'ip addr', 'netstat',
            'uname', 'hostname', 'uptime', 'who', 'w', 'last', 'kernel'
        ]
        
        user_lower = user_input.lower()
        asking_for_system_info = any(keyword in user_lower for keyword in system_info_keywords)
        
        if not asking_for_system_info:
            return False
        
        has_specific_data = any([
            'GB' in response or 'MB' in response or 'KB' in response or 'TB' in response,
            'CPU:' in response or 'Memory:' in response,
            'Kernel:' in response or 'OS:' in response,
            '/dev/' in response or '/home/' in response,
            'PID' in response and 'USER' in response,
        ])
        
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


class TestHallucinationPrevention:
    """Test suite for hallucination detection and prevention."""
    
    def test_detect_system_info_keywords(self):
        """Test detection of system info requests."""
        agent = MockAgent()
        
        # Should detect system info requests
        assert agent._detect_hallucination_risk(
            "show me neofetch output",
            "OS: Ubuntu 22.04\nCPU: Intel i7\nMemory: 16GB"
        ) is True
        
        assert agent._detect_hallucination_risk(
            "what's my disk usage?",
            "Disk: 500GB / 1TB used"
        ) is True
        
        assert agent._detect_hallucination_risk(
            "show running processes",
            "PID USER COMMAND\n1234 root nginx"
        ) is True
    
    def test_no_false_positives(self):
        """Test that normal responses don't trigger false positives."""
        agent = MockAgent()
        
        # Should NOT detect as hallucination
        assert agent._detect_hallucination_risk(
            "what is neofetch?",
            "Neofetch is a command-line tool that displays system information."
        ) is False
        
        assert agent._detect_hallucination_risk(
            "how do I check disk usage?",
            "You can use the 'df' command or the get_disk_usage tool."
        ) is False
        
        assert agent._detect_hallucination_risk(
            "hello",
            "Hello! How can I help you today?"
        ) is False
    
    def test_detect_specific_data_patterns(self):
        """Test detection of specific data patterns that indicate fabrication."""
        agent = MockAgent()
        
        # Responses with specific system data should be flagged
        test_cases = [
            ("show system info", "CPU: Intel Core i7-10700K @ 3.70GHz"),
            ("memory usage", "Memory: 7031MiB / 15731MiB"),
            ("disk space", "Disk: 1.8TB / 1.2TB (used/free)"),
            ("show processes", "PID: 1234 USER: root COMMAND: nginx"),
            ("kernel version", "Kernel: 5.10.0-arch1-1"),
        ]
        
        for user_input, response in test_cases:
            assert agent._detect_hallucination_risk(user_input, response) is True, \
                f"Failed to detect hallucination in: {response}"
    
    def test_system_info_keywords_coverage(self):
        """Test that all common system info commands are covered."""
        agent = MockAgent()
        
        commands = [
            'neofetch', 'system info', 'disk usage', 'memory', 'cpu',
            'processes', 'running', 'network', 'connections', 'files',
            'directory', 'ls', 'ps', 'top', 'df', 'free', 'ifconfig',
            'ip addr', 'netstat', 'uname', 'hostname', 'uptime'
        ]
        
        for cmd in commands:
            # Each command should trigger detection when combined with specific data
            assert agent._detect_hallucination_risk(
                f"run {cmd}",
                "CPU: Intel i7 @ 3.5GHz"
            ) is True, f"Failed to detect system info keyword: {cmd}"


    def test_detect_excuses(self):
        """Test detection of agent making excuses instead of using tools."""
        agent = MockAgent()
        
        # Agent making excuses should be detected
        excuses = [
            ("show neofetch", "Похоже, что вывод команды neofetch содержит слишком много данных"),
            ("disk usage", "Информация не может быть полностью отображён здесь из-за ограничений"),
            ("show processes", "Обычно neofetch отображает информацию о системе"),
            ("memory info", "Если вам нужно что-то конкретное из этого вывода, пожалуйста, уточните"),
        ]
        
        for user_input, response in excuses:
            assert agent._detect_hallucination_risk(user_input, response) is True, \
                f"Failed to detect excuse in: {response}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
