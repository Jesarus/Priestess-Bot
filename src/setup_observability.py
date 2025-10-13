#!/usr/bin/env python3
"""
Setup script for the observability system.
Creates necessary directories and initializes the logging system.
"""

import sys
from pathlib import Path
from observability import observability


def create_directories():
    """Create necessary directories for the observability system."""
    directories = [
        "logs",
        "data",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        "interactions.py",
        "Pillow",
        "numpy",
        "opencv-python",
        "psutil"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_").replace(".", "_"))
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    return True


def test_observability_system():
    """Test the observability system functionality."""
    print("\nTesting observability system...")
    
    try:
        # Test logging
        observability.logger.info("Test log message", test="setup")
        print("✓ Logging system working")
        
        # Test metrics
        observability.metrics.increment('setup_test', {'phase': 'initialization'})
        print("✓ Metrics collection working")
        
        # Test error tracking
        try:
            raise ValueError("Test error for setup")
        except Exception as e:
            observability.error_tracker.track_error(e, {'test': 'setup'})
        print("✓ Error tracking working")
        
        # Test health monitoring
        health_status = observability.health_monitor.check_health()
        print(f"✓ Health monitoring working (status: {'healthy' if health_status['overall_healthy'] else 'unhealthy'})")
        
        return True
        
    except Exception as e:
        print(f"✗ Observability system test failed: {e}")
        return False


def create_env_example():
    """Create an example .env file for configuration."""
    env_example = """# Observability Configuration
LOG_LEVEL=INFO
LOG_DIR=logs
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# Health Check Thresholds
CPU_THRESHOLD=80.0
MEMORY_THRESHOLD=85.0
DISK_THRESHOLD=90.0

# Performance Monitoring
PERFORMANCE_SLOW_THRESHOLD=1.0
PERFORMANCE_CRITICAL_THRESHOLD=5.0

# Development Settings
DEBUG_MODE=false
VERBOSE_LOGGING=false

# Bot Token (required)
PRIESTESS_BOT_TOKEN=your_bot_token_here
"""
    
    env_file = Path(".env.example")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_example)
        print("✓ Created .env.example file")
    else:
        print("✓ .env.example already exists")


def main():
    """Main setup function."""
    print("Discord Bot Observability System Setup")
    print("=" * 40)
    
    # Create directories
    print("\n1. Creating directories...")
    create_directories()
    
    # Check dependencies
    print("\n2. Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Setup failed: Missing dependencies")
        sys.exit(1)
    
    # Test observability system
    print("\n3. Testing observability system...")
    if not test_observability_system():
        print("\n❌ Setup failed: Observability system test failed")
        sys.exit(1)
    
    # Create example configuration
    print("\n4. Creating configuration files...")
    create_env_example()
    
    print("\n" + "=" * 40)
    print("✅ Observability system setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure your bot token")
    print("2. Run your bot: python bot.py")
    print("3. Monitor your bot: python monitor.py")
    print("4. Use /health, /metrics, and /logs commands in Discord")
    print("\nFor more information, see OBSERVABILITY_README.md")


if __name__ == "__main__":
    main()
