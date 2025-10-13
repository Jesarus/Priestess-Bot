#!/usr/bin/env python3
"""
Simple test to verify the observability system works.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from observability import observability
    print("✅ Observability system imported successfully")
    
    # Test logging
    observability.logger.info("Test log message", test="setup")
    print("✅ Logging system working")
    
    # Test metrics
    observability.metrics.increment('setup_test', {'phase': 'initialization'})
    print("✅ Metrics collection working")
    
    # Test error tracking
    try:
        raise ValueError("Test error for setup")
    except Exception as e:
        observability.error_tracker.track_error(e, {'test': 'setup'})
    print("✅ Error tracking working")
    
    # Test health monitoring
    health_status = observability.health_monitor.check_health()
    print(f"✅ Health monitoring working (status: {'healthy' if health_status['overall_healthy'] else 'unhealthy'})")
    
    # Test system info
    system_info = observability.get_system_info()
    print(f"✅ System info available (uptime: {system_info['uptime_seconds']:.1f}s)")
    
    print("\n🎉 All observability tests passed!")
    print("\nNext steps:")
    print("1. Run your bot: python bot.py")
    print("2. Monitor your bot: python monitor.py")
    print("3. Use /health, /metrics, and /logs commands in Discord")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
