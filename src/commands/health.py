"""
Health monitoring and system status commands for the Discord bot.
"""

import interactions
import json
from observability import observability, log_command_usage


class HealthExtension(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.slash_command(
        name="health",
        description="Check bot health and system status (admin only)",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    )
    @log_command_usage("health")
    async def health(self, ctx: interactions.SlashContext):
        """Display bot health status and system information."""
        try:
            health_status = observability.health_monitor.check_health()
            system_info = observability.get_system_info()
            
            # Create health status message
            status_emoji = "✅" if health_status['overall_healthy'] else "❌"
            message = f"{status_emoji} **Bot Health Status**\n\n"
            
            # System information
            message += "**System Information:**\n"
            message += f"• Uptime: {system_info['uptime_formatted']}\n"
            message += f"• Bot Ready: {'Yes' if system_info['bot_ready'] else 'No'}\n"
            
            # Health check results
            message += "\n**Health Checks:**\n"
            for check_name, result in health_status['results'].items():
                emoji = "✅" if result.get('healthy', False) else "❌"
                message += f"• {check_name}: {emoji}\n"
                if 'error' in result:
                    message += f"  Error: {result['error']}\n"
                if check_name == 'system' and result.get('healthy'):
                    message += f"  CPU: {result.get('cpu_percent', 0):.1f}%\n"
                    message += f"  Memory: {result.get('memory_percent', 0):.1f}%\n"
                    message += f"  Disk: {result.get('disk_percent', 0):.1f}%\n"
            
            # Metrics summary
            metrics = system_info['metrics']
            if metrics['counters']:
                message += "\n**Key Metrics:**\n"
                for metric, count in list(metrics['counters'].items())[:5]:
                    message += f"• {metric}: {count}\n"
            
            # Error summary
            error_summary = system_info['error_summary']
            if error_summary['total_errors'] > 0:
                message += f"\n**Errors:** {error_summary['total_errors']} total\n"
                for error_type, count in list(error_summary['error_counts'].items())[:3]:
                    message += f"• {error_type}: {count}\n"
            
            await ctx.send(message)
            
        except Exception as e:
            observability.error_tracker.track_error(e, {
                'command': 'health',
                'user_id': str(ctx.author.id)
            })
            await ctx.send("Erro ao verificar status do bot.", ephemeral=True)

    @interactions.slash_command(
        name="metrics",
        description="Show detailed bot metrics (admin only)",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    )
    @log_command_usage("metrics")
    async def metrics(self, ctx: interactions.SlashContext):
        """Display detailed bot metrics."""
        try:
            system_info = observability.get_system_info()
            metrics = system_info['metrics']
            
            message = "**📊 Bot Metrics**\n\n"
            
            # Counters
            if metrics['counters']:
                message += "**Counters:**\n"
                for metric, count in sorted(metrics['counters'].items()):
                    message += f"• {metric}: {count}\n"
                message += "\n"
            
            # Gauges
            if metrics['gauges']:
                message += "**Gauges:**\n"
                for metric, value in sorted(metrics['gauges'].items()):
                    message += f"• {metric}: {value}\n"
                message += "\n"
            
            # Histograms (performance metrics)
            if metrics['histograms']:
                message += "**Performance Metrics:**\n"
                for metric, stats in sorted(metrics['histograms'].items()):
                    if stats['count'] > 0:
                        message += f"• {metric}:\n"
                        message += f"  - Count: {stats['count']}\n"
                        message += f"  - Avg: {stats['avg']:.3f}s\n"
                        message += f"  - P95: {stats['p95']:.3f}s\n"
                        message += f"  - Max: {stats['max']:.3f}s\n"
            
            # Split message if too long
            if len(message) > 2000:
                # Send first part
                await ctx.send(message[:1900] + "...")
                # Send remaining metrics as JSON
                metrics_json = json.dumps(metrics, indent=2)
                if len(metrics_json) > 2000:
                    metrics_json = metrics_json[:1900] + "..."
                await ctx.send(f"**Raw Metrics:**\n```json\n{metrics_json}\n```")
            else:
                await ctx.send(message)
                
        except Exception as e:
            observability.error_tracker.track_error(e, {
                'command': 'metrics',
                'user_id': str(ctx.author.id)
            })
            await ctx.send("Erro ao obter métricas do bot.", ephemeral=True)

    @interactions.slash_command(
        name="logs",
        description="Show recent error logs (admin only)",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    )
    @log_command_usage("logs")
    async def logs(self, ctx: interactions.SlashContext, limit: int = 5):
        """Display recent error logs."""
        try:
            error_summary = observability.error_tracker.get_error_summary()
            recent_errors = error_summary['recent_errors']
            
            if not recent_errors:
                await ctx.send("Nenhum erro recente encontrado. ✅")
                return
            
            message = f"**🚨 Recent Errors (Last {min(limit, len(recent_errors))}):**\n\n"
            
            for error in recent_errors[-limit:]:
                message += f"**{error['type']}** - {error['timestamp']}\n"
                message += f"Message: {error['message'][:100]}...\n"
                if error['context']:
                    context_str = ", ".join(f"{k}={v}" for k, v in error['context'].items())
                    message += f"Context: {context_str}\n"
                message += "\n"
            
            if len(message) > 2000:
                message = message[:1900] + "..."
            
            await ctx.send(message)
            
        except Exception as e:
            observability.error_tracker.track_error(e, {
                'command': 'logs',
                'user_id': str(ctx.author.id)
            })
            await ctx.send("Erro ao obter logs do bot.", ephemeral=True)


def setup(client):
    return HealthExtension(client)
