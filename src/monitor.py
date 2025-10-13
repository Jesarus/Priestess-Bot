#!/usr/bin/env python3
"""
Simple monitoring dashboard for the Discord bot.
Run this script to get real-time monitoring information.
"""

import time
import os
from datetime import datetime
from observability import observability


def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def print_section(title):
    """Print a formatted section header."""
    print(f"\n--- {title} ---")


def format_uptime(seconds):
    """Format uptime in human readable format."""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{days}d {hours}h {minutes}m"


def display_health_status():
    """Display bot health status."""
    health = observability.health_monitor.check_health()
    
    status = "🟢 HEALTHY" if health['overall_healthy'] else "🔴 UNHEALTHY"
    print(f"Overall Status: {status}")
    
    for check_name, result in health['results'].items():
        emoji = "✅" if result.get('healthy', False) else "❌"
        print(f"  {emoji} {check_name}")
        
        if check_name == 'system' and result.get('healthy'):
            print(f"    CPU: {result.get('cpu_percent', 0):.1f}%")
            print(f"    Memory: {result.get('memory_percent', 0):.1f}%")
            print(f"    Disk: {result.get('disk_percent', 0):.1f}%")
        
        if 'error' in result:
            print(f"    Error: {result['error']}")


def display_metrics():
    """Display key metrics."""
    system_info = observability.get_system_info()
    metrics = system_info['metrics']
    
    print_section("Key Metrics")
    
    # Counters
    if metrics['counters']:
        print("Counters:")
        for metric, count in sorted(metrics['counters'].items()):
            print(f"  {metric}: {count}")
    
    # Performance metrics
    if metrics['histograms']:
        print("\nPerformance (Average Response Times):")
        for metric, stats in sorted(metrics['histograms'].items()):
            if stats['count'] > 0:
                print(f"  {metric}: {stats['avg']:.3f}s (P95: {stats['p95']:.3f}s)")


def display_errors():
    """Display recent errors."""
    error_summary = observability.error_tracker.get_error_summary()
    
    print_section("Error Summary")
    print(f"Total Errors: {error_summary['total_errors']}")
    
    if error_summary['error_counts']:
        print("Error Types:")
        for error_type, count in sorted(error_summary['error_counts'].items(), 
                                      key=lambda x: x[1], reverse=True):
            print(f"  {error_type}: {count}")
    
    if error_summary['recent_errors']:
        print("\nRecent Errors (Last 5):")
        for error in error_summary['recent_errors'][-5:]:
            timestamp = error['timestamp'][:19]  # Remove microseconds
            print(f"  {timestamp} - {error['type']}: {error['message'][:50]}...")


def display_system_info():
    """Display system information."""
    system_info = observability.get_system_info()
    
    print_section("System Information")
    print(f"Uptime: {format_uptime(system_info['uptime_seconds'])}")
    print(f"Start Time: {system_info['start_time']}")
    print(f"Bot Ready: {'Yes' if system_info['bot_ready'] else 'No'}")


def main():
    """Main monitoring loop."""
    print_header("Discord Bot Monitoring Dashboard")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        while True:
            # Clear screen (works on most terminals)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print_header("Discord Bot Monitoring Dashboard")
            print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("Press Ctrl+C to exit")
            
            display_health_status()
            display_system_info()
            display_metrics()
            display_errors()
            
            print(f"\n{'='*60}")
            print("Refreshing in 30 seconds...")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
    except Exception as e:
        print(f"\nError in monitoring: {e}")


if __name__ == "__main__":
    main()
