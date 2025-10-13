"""
Comprehensive observability module for the Discord bot.
Provides logging, metrics, error tracking, and monitoring capabilities.
"""

import logging
import logging.handlers
import time
import functools
import traceback
from datetime import datetime
from typing import Dict, Any, Callable
from pathlib import Path
import threading
from collections import defaultdict, deque
import psutil
import asyncio


class MetricsCollector:
    """Collects and stores application metrics."""
    
    def __init__(self):
        self.metrics = defaultdict(lambda: defaultdict(int))
        self.timers = {}
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self._lock = threading.Lock()
    
    def increment(self, metric_name: str, labels: Dict[str, str] = None, value: int = 1):
        """Increment a counter metric."""
        with self._lock:
            key = self._format_key(metric_name, labels)
            self.counters[key] += value
    
    def gauge(self, metric_name: str, value: float, labels: Dict[str, str] = None):
        """Set a gauge metric."""
        with self._lock:
            key = self._format_key(metric_name, labels)
            self.gauges[key] = value
    
    def histogram(self, metric_name: str, value: float, labels: Dict[str, str] = None):
        """Record a value in a histogram."""
        with self._lock:
            key = self._format_key(metric_name, labels)
            self.histograms[key].append(value)
            # Keep only last 1000 values to prevent memory issues
            if len(self.histograms[key]) > 1000:
                self.histograms[key] = self.histograms[key][-1000:]
    
    def timer(self, metric_name: str, labels: Dict[str, str] = None):
        """Context manager for timing operations."""
        return TimerContext(self, metric_name, labels)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all current metrics."""
        with self._lock:
            return {
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'histograms': {k: {
                    'count': len(v),
                    'min': min(v) if v else 0,
                    'max': max(v) if v else 0,
                    'avg': sum(v) / len(v) if v else 0,
                    'p95': self._percentile(v, 95) if v else 0,
                    'p99': self._percentile(v, 99) if v else 0
                } for k, v in self.histograms.items()}
            }
    
    def _format_key(self, metric_name: str, labels: Dict[str, str] = None) -> str:
        """Format metric key with labels."""
        if not labels:
            return metric_name
        label_str = ','.join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{metric_name}{{{label_str}}}"
    
    def _percentile(self, values: list, percentile: float) -> float:
        """Calculate percentile of values."""
        if not values:
            return 0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]


class TimerContext:
    """Context manager for timing operations."""
    
    def __init__(self, collector: MetricsCollector, metric_name: str, labels: Dict[str, str] = None):
        self.collector = collector
        self.metric_name = metric_name
        self.labels = labels
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            self.collector.histogram(f"{self.metric_name}_duration", duration, self.labels)


class StructuredLogger:
    """Enhanced logger with structured logging capabilities."""
    
    def __init__(self, name: str, log_dir: str = "logs"):
        self.logger = logging.getLogger(name)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up logging configuration."""
        # Clear existing handlers
        self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler with colored output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / 'bot.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / 'errors.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)
    
    def log_with_context(self, level: int, message: str, **context):
        """Log with additional context information."""
        context_str = " | ".join(f"{k}={v}" for k, v in context.items())
        full_message = f"{message} | {context_str}" if context_str else message
        self.logger.log(level, full_message)
    
    def info(self, message: str, **context):
        self.log_with_context(logging.INFO, message, **context)
    
    def warning(self, message: str, **context):
        self.log_with_context(logging.WARNING, message, **context)
    
    def error(self, message: str, **context):
        self.log_with_context(logging.ERROR, message, **context)
    
    def debug(self, message: str, **context):
        self.log_with_context(logging.DEBUG, message, **context)
    
    def exception(self, message: str, **context):
        """Log exception with full traceback."""
        context_str = " | ".join(f"{k}={v}" for k, v in context.items())
        full_message = f"{message} | {context_str}" if context_str else message
        self.logger.exception(full_message)


class ErrorTracker:
    """Tracks and analyzes errors."""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.error_counts = defaultdict(int)
        self.recent_errors = deque(maxlen=100)
        self._lock = threading.Lock()
    
    def track_error(self, error: Exception, context: Dict[str, Any] = None):
        """Track an error occurrence."""
        error_type = type(error).__name__
        error_message = str(error)
        
        with self._lock:
            self.error_counts[error_type] += 1
            self.recent_errors.append({
                'timestamp': datetime.now().isoformat(),
                'type': error_type,
                'message': error_message,
                'context': context or {},
                'traceback': traceback.format_exc()
            })
        
        self.logger.error(
            f"Error tracked: {error_type}",
            error_type=error_type,
            error_message=error_message,
            **(context or {})
        )
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error statistics."""
        with self._lock:
            return {
                'error_counts': dict(self.error_counts),
                'recent_errors': list(self.recent_errors),
                'total_errors': sum(self.error_counts.values())
            }


class HealthMonitor:
    """Monitors system and application health."""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.health_checks = {}
        self.last_check = None
        self._lock = threading.Lock()
    
    def register_health_check(self, name: str, check_func: Callable[[], bool]):
        """Register a health check function."""
        self.health_checks[name] = check_func
    
    def check_health(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {}
        overall_healthy = True
        
        # System health checks
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            results['system'] = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
                'healthy': cpu_percent < 80 and memory.percent < 85 and disk.percent < 90
            }
            
            if not results['system']['healthy']:
                overall_healthy = False
                
        except Exception as e:
            results['system'] = {'healthy': False, 'error': str(e)}
            overall_healthy = False
        
        # Custom health checks
        for name, check_func in self.health_checks.items():
            try:
                result = check_func()
                results[name] = {'healthy': result}
                if not result:
                    overall_healthy = False
            except Exception as e:
                results[name] = {'healthy': False, 'error': str(e)}
                overall_healthy = False
        
        with self._lock:
            self.last_check = {
                'timestamp': datetime.now().isoformat(),
                'overall_healthy': overall_healthy,
                'results': results
            }
        
        return self.last_check


class ObservabilityManager:
    """Main observability manager that coordinates all components."""
    
    def __init__(self, log_dir: str = "logs"):
        self.logger = StructuredLogger("observability", log_dir)
        self.metrics = MetricsCollector()
        self.error_tracker = ErrorTracker(self.logger)
        self.health_monitor = HealthMonitor(self.logger)
        
        # Register default health checks
        self.health_monitor.register_health_check("bot_ready", self._check_bot_ready)
        
        self.bot_ready = False
        self.start_time = datetime.now()
        
        self.logger.info("Observability system initialized")
    
    def set_bot_ready(self, ready: bool = True):
        """Mark bot as ready."""
        self.bot_ready = ready
        self.logger.info(f"Bot ready status set to: {ready}")
    
    def _check_bot_ready(self) -> bool:
        """Health check for bot readiness."""
        return self.bot_ready
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        uptime = datetime.now() - self.start_time
        
        return {
            'uptime_seconds': uptime.total_seconds(),
            'uptime_formatted': str(uptime),
            'start_time': self.start_time.isoformat(),
            'bot_ready': self.bot_ready,
            'metrics': self.metrics.get_metrics(),
            'error_summary': self.error_tracker.get_error_summary(),
            'health_status': self.health_monitor.check_health()
        }
    
    def log_command_usage(self, command_name: str, user_id: str, guild_id: str = None, success: bool = True):
        """Log command usage for analytics."""
        self.metrics.increment('commands_total', {
            'command': command_name,
            'success': str(success)
        })
        
        self.logger.info(
            f"Command executed: {command_name}",
            command=command_name,
            user_id=user_id,
            guild_id=guild_id,
            success=success
        )
    
    def log_performance(self, operation: str, duration: float, **context):
        """Log performance metrics."""
        self.metrics.histogram(f"{operation}_duration", duration, context)
        self.logger.debug(
            f"Performance: {operation} took {duration:.3f}s",
            operation=operation,
            duration=duration,
            **context
        )


# Global observability instance
observability = ObservabilityManager()


def monitor_performance(operation_name: str, **labels):
    """Decorator to monitor function performance."""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            with observability.metrics.timer(operation_name, labels):
                try:
                    result = await func(*args, **kwargs)
                    observability.metrics.increment(f"{operation_name}_success", labels)
                    return result
                except Exception as e:
                    observability.metrics.increment(f"{operation_name}_error", labels)
                    observability.error_tracker.track_error(e, {
                        'operation': operation_name,
                        'labels': labels
                    })
                    raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            with observability.metrics.timer(operation_name, labels):
                try:
                    result = func(*args, **kwargs)
                    observability.metrics.increment(f"{operation_name}_success", labels)
                    return result
                except Exception as e:
                    observability.metrics.increment(f"{operation_name}_error", labels)
                    observability.error_tracker.track_error(e, {
                        'operation': operation_name,
                        'labels': labels
                    })
                    raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator


def log_command_usage(command_name: str):
    """Decorator to log command usage."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            # Determine if this is an instance method (has 'self') or standalone function
            if len(args) >= 2 and hasattr(args[1], 'author'):
                # Instance method: args[0] is self, args[1] is ctx
                ctx = args[1]
                func_args = args
            elif len(args) >= 1 and hasattr(args[0], 'author'):
                # Standalone function: args[0] is ctx
                ctx = args[0]
                func_args = args
            else:
                # Fallback - try to find context in args
                ctx = None
                for arg in args:
                    if hasattr(arg, 'author'):
                        ctx = arg
                        break
                
                if ctx is None:
                    # If we can't find context, just call the function without logging
                    return await func(*args, **kwargs)
                
                func_args = args
            
            try:
                result = await func(*func_args, **kwargs)
                return result
            except Exception as e:
                success = False
                if ctx:
                    observability.error_tracker.track_error(e, {
                        'command': command_name,
                        'user_id': str(ctx.author.id),
                        'guild_id': str(ctx.guild.id) if ctx.guild else None
                    })
                raise
            finally:
                if ctx:
                    duration = time.time() - start_time
                    observability.log_command_usage(
                        command_name,
                        str(ctx.author.id),
                        str(ctx.guild.id) if ctx.guild else None,
                        success
                    )
                    observability.log_performance(
                        f"command_{command_name}",
                        duration,
                        user_id=str(ctx.author.id)
                    )
        
        return wrapper
    return decorator
