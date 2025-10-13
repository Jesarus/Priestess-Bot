"""
Tests for the observability system.
"""

import pytest
import tempfile
from pathlib import Path
from observability import ObservabilityManager, MetricsCollector, StructuredLogger, ErrorTracker, HealthMonitor


def test_metrics_collector():
    """Test metrics collection functionality."""
    collector = MetricsCollector()
    
    # Test counter
    collector.increment('test_counter', {'label': 'value'})
    collector.increment('test_counter', {'label': 'value'}, 5)
    
    # Test gauge
    collector.gauge('test_gauge', 42.5, {'label': 'value'})
    
    # Test histogram
    collector.histogram('test_histogram', 1.5, {'label': 'value'})
    collector.histogram('test_histogram', 2.5, {'label': 'value'})
    
    # Test timer context
    with collector.timer('test_timer', {'label': 'value'}):
        pass
    
    metrics = collector.get_metrics()
    
    assert 'test_counter{label=value}' in metrics['counters']
    assert metrics['counters']['test_counter{label=value}'] == 6
    
    assert 'test_gauge{label=value}' in metrics['gauges']
    assert metrics['gauges']['test_gauge{label=value}'] == 42.5
    
    assert 'test_histogram{label=value}' in metrics['histograms']
    hist_data = metrics['histograms']['test_histogram{label=value}']
    assert hist_data['count'] == 2
    assert hist_data['min'] == 1.5
    assert hist_data['max'] == 2.5


def test_structured_logger():
    """Test structured logging functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        logger = StructuredLogger("test_logger", temp_dir)
        
        # Test different log levels
        logger.info("Test info message", key1="value1", key2="value2")
        logger.warning("Test warning message", key="value")
        logger.error("Test error message", error_code=500)
        logger.debug("Test debug message", debug_info="test")
        
        # Check if log files were created
        log_dir = Path(temp_dir)
        assert (log_dir / "bot.log").exists()
        assert (log_dir / "errors.log").exists()
        
        # Check log file contents
        with open(log_dir / "bot.log", "r") as f:
            log_content = f.read()
            assert "Test info message" in log_content
            assert "key1=value1" in log_content
            assert "key2=value2" in log_content
        
        with open(log_dir / "errors.log", "r") as f:
            error_content = f.read()
            assert "Test error message" in error_content
            assert "error_code=500" in error_content


def test_error_tracker():
    """Test error tracking functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        logger = StructuredLogger("test_logger", temp_dir)
        tracker = ErrorTracker(logger)
        
        # Track some errors
        try:
            raise ValueError("Test error message")
        except Exception as e:
            tracker.track_error(e, {'context': 'test'})
        
        try:
            raise KeyError("Missing key")
        except Exception as e:
            tracker.track_error(e, {'operation': 'test_op'})
        
        # Get error summary
        summary = tracker.get_error_summary()
        
        assert summary['error_counts']['ValueError'] == 1
        assert summary['error_counts']['KeyError'] == 1
        assert summary['total_errors'] == 2
        assert len(summary['recent_errors']) == 2


def test_health_monitor():
    """Test health monitoring functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        logger = StructuredLogger("test_logger", temp_dir)
        monitor = HealthMonitor(logger)
        
        # Register a test health check
        def test_health_check():
            return True
        
        monitor.register_health_check("test_check", test_health_check)
        
        # Run health check
        health_status = monitor.check_health()
        
        assert 'test_check' in health_status['results']
        assert health_status['results']['test_check']['healthy'] is True
        assert 'system' in health_status['results']


def test_observability_manager():
    """Test the main observability manager."""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ObservabilityManager(temp_dir)
        
        # Test initial state
        assert not manager.bot_ready
        
        # Set bot ready
        manager.set_bot_ready(True)
        assert manager.bot_ready
        
        # Test system info
        system_info = manager.get_system_info()
        assert 'uptime_seconds' in system_info
        assert 'bot_ready' in system_info
        assert 'metrics' in system_info
        assert 'error_summary' in system_info
        assert 'health_status' in system_info
        
        # Test command logging
        manager.log_command_usage("test_command", "123", "456", True)
        
        # Test performance logging
        manager.log_performance("test_operation", 1.5, user_id="123")
        
        # Verify metrics were updated
        metrics = manager.metrics.get_metrics()
        assert any('test_command' in counter for counter in metrics['counters'])
        assert any('test_operation' in hist for hist in metrics['histograms'])


def test_performance_decorator():
    """Test the performance monitoring decorator."""
    from observability import monitor_performance
    
    @monitor_performance("test_function")
    def test_function():
        return "success"
    
    @monitor_performance("test_function_error")
    def test_function_error():
        raise ValueError("Test error")
    
    # Test successful function
    result = test_function()
    assert result == "success"
    
    # Test function with error
    with pytest.raises(ValueError):
        test_function_error()
    
    # Note: In a real test, we'd need to access the global observability instance
    # to verify metrics were recorded, but for unit testing we use a local collector


def test_log_command_usage_decorator():
    """Test the command usage logging decorator."""
    from observability import log_command_usage
    
    # This would require a mock Discord context object
    # For now, we just test that the decorator can be applied
    @log_command_usage("test_command")
    async def test_command(ctx):
        return "success"
    
    # Verify the decorator was applied (function still exists)
    assert callable(test_command)
