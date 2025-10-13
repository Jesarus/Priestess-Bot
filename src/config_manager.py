"""
Configuration management system for the Discord bot.
Handles environment variables, validation, and default values.
"""

import os
from typing import Dict, Any, List
from pathlib import Path

from constants import (
    REQUIRED_ENV_VARS, REQUIRED_FILES, REQUIRED_DIRECTORIES,
    DEFAULT_LOG_LEVEL, DEFAULT_CPU_THRESHOLD, DEFAULT_MEMORY_THRESHOLD,
    DEFAULT_DISK_THRESHOLD, DEFAULT_SLOW_THRESHOLD, DEFAULT_CRITICAL_THRESHOLD,
    ENV_BOT_TOKEN, ENV_LOG_LEVEL, ENV_CPU_THRESHOLD, ENV_MEMORY_THRESHOLD,
    ENV_DISK_THRESHOLD, ENV_DEBUG_MODE
)
from exceptions import ConfigurationError
from logging_utils import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """Manages configuration for the Discord bot."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self._config = {}
        self._load_configuration()
        self._validate_configuration()
    
    def _load_configuration(self) -> None:
        """Load configuration from environment variables."""
        # Required configuration
        self._config[ENV_BOT_TOKEN] = os.getenv(ENV_BOT_TOKEN)
        
        # Optional configuration with defaults
        self._config[ENV_LOG_LEVEL] = os.getenv(ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL)
        self._config[ENV_CPU_THRESHOLD] = float(os.getenv(ENV_CPU_THRESHOLD, DEFAULT_CPU_THRESHOLD))
        self._config[ENV_MEMORY_THRESHOLD] = float(os.getenv(ENV_MEMORY_THRESHOLD, DEFAULT_MEMORY_THRESHOLD))
        self._config[ENV_DISK_THRESHOLD] = float(os.getenv(ENV_DISK_THRESHOLD, DEFAULT_DISK_THRESHOLD))
        self._config[ENV_DEBUG_MODE] = os.getenv(ENV_DEBUG_MODE, "false").lower() == "true"
        
        # Additional optional settings
        self._config["LOG_DIR"] = os.getenv("LOG_DIR", "logs")
        self._config["PERFORMANCE_SLOW_THRESHOLD"] = float(
            os.getenv("PERFORMANCE_SLOW_THRESHOLD", DEFAULT_SLOW_THRESHOLD)
        )
        self._config["PERFORMANCE_CRITICAL_THRESHOLD"] = float(
            os.getenv("PERFORMANCE_CRITICAL_THRESHOLD", DEFAULT_CRITICAL_THRESHOLD)
        )
        
        logger.info("Configuration loaded successfully")
    
    def _validate_configuration(self) -> None:
        """Validate the loaded configuration."""
        errors = []
        
        # Check required environment variables
        for var in REQUIRED_ENV_VARS:
            if not self._config.get(var):
                errors.append(f"Required environment variable '{var}' is not set")
        
        # Validate numeric values
        numeric_vars = [
            (ENV_CPU_THRESHOLD, 0, 100),
            (ENV_MEMORY_THRESHOLD, 0, 100),
            (ENV_DISK_THRESHOLD, 0, 100),
            ("PERFORMANCE_SLOW_THRESHOLD", 0, 60),
            ("PERFORMANCE_CRITICAL_THRESHOLD", 0, 300)
        ]
        
        for var, min_val, max_val in numeric_vars:
            value = self._config.get(var)
            if value is not None and (value < min_val or value > max_val):
                errors.append(f"Configuration '{var}' must be between {min_val} and {max_val}, got {value}")
        
        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self._config[ENV_LOG_LEVEL] not in valid_log_levels:
            errors.append(f"Invalid log level '{self._config[ENV_LOG_LEVEL]}'. Must be one of: {valid_log_levels}")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
        
        logger.info("Configuration validation passed")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def get_bot_token(self) -> str:
        """
        Get the Discord bot token.
        
        Returns:
            Bot token string
            
        Raises:
            ConfigurationError: If token is not configured
        """
        token = self._config.get(ENV_BOT_TOKEN)
        if not token:
            raise ConfigurationError("Discord bot token is not configured")
        return token
    
    def get_log_level(self) -> str:
        """Get the log level."""
        return self._config[ENV_LOG_LEVEL]
    
    def get_health_thresholds(self) -> Dict[str, float]:
        """Get health check thresholds."""
        return {
            "cpu": self._config[ENV_CPU_THRESHOLD],
            "memory": self._config[ENV_MEMORY_THRESHOLD],
            "disk": self._config[ENV_DISK_THRESHOLD]
        }
    
    def get_performance_thresholds(self) -> Dict[str, float]:
        """Get performance monitoring thresholds."""
        return {
            "slow": self._config["PERFORMANCE_SLOW_THRESHOLD"],
            "critical": self._config["PERFORMANCE_CRITICAL_THRESHOLD"]
        }
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return self._config[ENV_DEBUG_MODE]
    
    def get_log_directory(self) -> str:
        """Get the log directory path."""
        return self._config["LOG_DIR"]
    
    def validate_files_and_directories(self) -> List[str]:
        """
        Validate that required files and directories exist.
        
        Returns:
            List of missing files/directories
        """
        missing = []
        
        # Check required files
        for file_path in REQUIRED_FILES:
            if not Path(file_path).exists():
                missing.append(f"File: {file_path}")
        
        # Check required directories
        for dir_path in REQUIRED_DIRECTORIES:
            if not Path(dir_path).exists():
                missing.append(f"Directory: {dir_path}")
        
        return missing
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current configuration.
        
        Returns:
            Dictionary with configuration summary
        """
        return {
            "bot_token_configured": bool(self._config.get(ENV_BOT_TOKEN)),
            "log_level": self._config[ENV_LOG_LEVEL],
            "debug_mode": self._config[ENV_DEBUG_MODE],
            "health_thresholds": self.get_health_thresholds(),
            "performance_thresholds": self.get_performance_thresholds(),
            "log_directory": self._config["LOG_DIR"]
        }


# Global configuration manager instance
config = ConfigManager()
