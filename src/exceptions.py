"""
Custom exceptions for the Discord bot.
"""


class BotError(Exception):
    """Base exception for bot-related errors."""
    pass


class ConfigurationError(BotError):
    """Raised when there's a configuration issue."""
    pass


class DataError(BotError):
    """Raised when there's an issue with data loading or processing."""
    pass


class GameError(BotError):
    """Raised when there's an issue with game logic."""
    pass


class ImageProcessingError(BotError):
    """Raised when there's an issue with image processing."""
    pass


class OperatorNotFoundError(GameError):
    """Raised when an operator is not found."""
    pass


class InvalidGameStateError(GameError):
    """Raised when the game is in an invalid state."""
    pass


class ScoreError(DataError):
    """Raised when there's an issue with score management."""
    pass


class FileNotFoundError(BotError):
    """Raised when a required file is not found."""
    pass
