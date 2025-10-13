"""
Type definitions and data structures for the Discord bot.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class GameState(Enum):
    """Enumeration for game states."""
    IDLE = "idle"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class OperatorRarity(Enum):
    """Enumeration for operator rarities."""
    ONE_STAR = "1"
    TWO_STAR = "2"
    THREE_STAR = "3"
    FOUR_STAR = "4"
    FIVE_STAR = "5"
    SIX_STAR = "6"


class OperatorClass(Enum):
    """Enumeration for operator classes."""
    GUARD = "Guard"
    DEFENDER = "Defender"
    VANGUARD = "Vanguard"
    SNIPER = "Sniper"
    CASTER = "Caster"
    MEDIC = "Medic"
    SUPPORTER = "Supporter"
    SPECIALIST = "Specialist"


@dataclass
class Operator:
    """Data class representing an Arknights operator."""
    name: str
    rarity: str
    class_type: str
    subclass: Optional[str] = None
    faction: Optional[str] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    infection_status: Optional[str] = None
    
    def __post_init__(self):
        """Validate operator data after initialization."""
        if not self.name:
            raise ValueError("Operator name cannot be empty")
        if self.rarity not in [r.value for r in OperatorRarity]:
            raise ValueError(f"Invalid rarity: {self.rarity}")


@dataclass
class UserScore:
    """Data class representing a user's score."""
    username: str
    pontos: int
    arkdle_last_win: Optional[str] = None
    
    def __post_init__(self):
        """Validate score data after initialization."""
        if self.pontos < 0:
            raise ValueError("Score cannot be negative")


@dataclass
class GameRound:
    """Data class representing a game round state."""
    round_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state: GameState = GameState.IDLE
    current_operator: Optional[str] = None
    correct_answer: Optional[List[str]] = None
    answers: Dict[str, str] = field(default_factory=dict)
    start_time: Optional[str] = None
    
    def reset(self) -> None:
        """Reset the round to initial state."""
        self.state = GameState.IDLE
        self.current_operator = None
        self.correct_answer = None
        self.answers.clear()
        self.start_time = None


@dataclass
class HealthCheckResult:
    """Data class representing a health check result."""
    name: str
    healthy: bool
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class SystemMetrics:
    """Data class representing system metrics."""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    uptime_seconds: float
    bot_ready: bool


@dataclass
class CommandUsage:
    """Data class representing command usage statistics."""
    command_name: str
    user_id: str
    guild_id: Optional[str]
    success: bool
    execution_time: float
    timestamp: str


# Type aliases for better readability
UserID = str
GuildID = str
OperatorName = str
ScoreDict = Dict[UserID, UserScore]
OperatorList = List[Operator]
ImagePath = str
LogLevel = str
