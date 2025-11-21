"""Long-term memory system for AI agent (like ChatGPT memory).

Author: sqrilizz
GitHub: https://github.com/Sqrilizz/auryx-agent
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from auryx_agent.core.paths import get_data_dir


@dataclass
class MemoryEntry:
    """A single memory entry."""
    id: str
    content: str
    category: str  # "preference", "fact", "context", "skill"
    timestamp: float
    importance: int  # 1-10
    tags: List[str]
    access_count: int = 0
    last_accessed: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create from dictionary."""
        return cls(**data)


class MemorySystem:
    """Long-term memory system for the AI agent.
    
    This system allows the agent to remember:
    - User preferences (language, style, topics)
    - Important facts about the user
    - Context from previous conversations
    - Learned skills and patterns
    """
    
    def __init__(self, memory_file: Optional[str] = None):
        """Initialize memory system.
        
        Args:
            memory_file: Path to memory file (default: ~/.local/share/auryx-agent/memory.json)
        """
        if memory_file:
            self.memory_file = Path(memory_file).expanduser()
        else:
            data_dir = get_data_dir()
            self.memory_file = data_dir / "memory.json"
        
        self.memories: List[MemoryEntry] = []
        self.load()
    
    def load(self) -> None:
        """Load memories from file."""
        if not self.memory_file.exists():
            self.memories = []
            return
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.memories = [MemoryEntry.from_dict(m) for m in data]
        except Exception as e:
            print(f"Warning: Failed to load memories: {e}")
            self.memories = []
    
    def save(self) -> None:
        """Save memories to file."""
        try:
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                data = [m.to_dict() for m in self.memories]
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to save memories: {e}")
    
    def add(self, content: str, category: str = "fact", 
            importance: int = 5, tags: Optional[List[str]] = None) -> str:
        """Add a new memory.
        
        Args:
            content: Memory content
            category: Memory category (preference, fact, context, skill)
            importance: Importance level 1-10
            tags: Optional tags for categorization
            
        Returns:
            Memory ID
        """
        import uuid
        
        memory_id = str(uuid.uuid4())
        timestamp = time.time()
        
        memory = MemoryEntry(
            id=memory_id,
            content=content,
            category=category,
            timestamp=timestamp,
            importance=importance,
            tags=tags or [],
            access_count=0,
            last_accessed=timestamp
        )
        
        self.memories.append(memory)
        self.save()
        
        return memory_id
    
    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Search memories by content.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching memories
        """
        query_lower = query.lower()
        results = []
        
        for memory in self.memories:
            # Simple keyword matching
            if query_lower in memory.content.lower():
                memory.access_count += 1
                memory.last_accessed = time.time()
                results.append(memory)
        
        # Sort by importance and recency
        results.sort(key=lambda m: (m.importance, m.timestamp), reverse=True)
        
        self.save()
        return results[:limit]
    
    def get_by_category(self, category: str, limit: int = 10) -> List[MemoryEntry]:
        """Get memories by category.
        
        Args:
            category: Memory category
            limit: Maximum number of results
            
        Returns:
            List of memories in category
        """
        results = [m for m in self.memories if m.category == category]
        results.sort(key=lambda m: (m.importance, m.timestamp), reverse=True)
        return results[:limit]
    
    def get_by_tags(self, tags: List[str], limit: int = 10) -> List[MemoryEntry]:
        """Get memories by tags.
        
        Args:
            tags: List of tags to search for
            limit: Maximum number of results
            
        Returns:
            List of memories with matching tags
        """
        results = []
        for memory in self.memories:
            if any(tag in memory.tags for tag in tags):
                results.append(memory)
        
        results.sort(key=lambda m: (m.importance, m.timestamp), reverse=True)
        return results[:limit]
    
    def get_recent(self, limit: int = 10) -> List[MemoryEntry]:
        """Get most recent memories.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of recent memories
        """
        sorted_memories = sorted(self.memories, key=lambda m: m.timestamp, reverse=True)
        return sorted_memories[:limit]
    
    def get_important(self, limit: int = 10) -> List[MemoryEntry]:
        """Get most important memories.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of important memories
        """
        sorted_memories = sorted(self.memories, key=lambda m: m.importance, reverse=True)
        return sorted_memories[:limit]
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory.
        
        Args:
            memory_id: ID of memory to delete
            
        Returns:
            True if deleted, False if not found
        """
        for i, memory in enumerate(self.memories):
            if memory.id == memory_id:
                del self.memories[i]
                self.save()
                return True
        return False
    
    def clear(self) -> None:
        """Clear all memories."""
        self.memories = []
        self.save()
    
    def get_context_summary(self) -> str:
        """Get a summary of important memories for AI context.
        
        Returns:
            Formatted string with key memories
        """
        if not self.memories:
            return "No memories stored yet."
        
        # Get top memories by importance
        important = self.get_important(limit=5)
        
        # Get preferences
        preferences = self.get_by_category("preference", limit=3)
        
        summary_parts = []
        
        if preferences:
            summary_parts.append("User Preferences:")
            for pref in preferences:
                summary_parts.append(f"  - {pref.content}")
        
        if important:
            summary_parts.append("\nImportant Context:")
            for mem in important:
                if mem.category != "preference":
                    summary_parts.append(f"  - {mem.content}")
        
        return "\n".join(summary_parts)
    
    def stats(self) -> Dict[str, Any]:
        """Get memory statistics.
        
        Returns:
            Dict with statistics
        """
        if not self.memories:
            return {
                "total": 0,
                "by_category": {},
                "avg_importance": 0
            }
        
        by_category = {}
        for memory in self.memories:
            by_category[memory.category] = by_category.get(memory.category, 0) + 1
        
        avg_importance = sum(m.importance for m in self.memories) / len(self.memories)
        
        return {
            "total": len(self.memories),
            "by_category": by_category,
            "avg_importance": round(avg_importance, 2),
            "most_accessed": max(self.memories, key=lambda m: m.access_count).content if self.memories else None
        }
