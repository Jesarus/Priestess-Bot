import interactions
from config import TOKEN
from observability import observability

# Initialize observability system
observability.logger.info("Starting Discord bot initialization")

bot = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT,
)


@bot.event
async def on_ready():
    observability.set_bot_ready(True)
    observability.logger.info(
        f"Bot {bot.user.username} is online!",
        bot_id=str(bot.user.id),
        guild_count=len(bot.guilds)
    )
    observability.metrics.gauge('bot_online', 1)


@bot.event
async def on_guild_join(guild):
    observability.logger.info(
        f"Joined guild: {guild.name}",
        guild_id=str(guild.id),
        guild_name=guild.name,
        member_count=guild.member_count
    )
    observability.metrics.increment('guild_joins')


@bot.event
async def on_guild_remove(guild):
    observability.logger.info(
        f"Left guild: {guild.name}",
        guild_id=str(guild.id),
        guild_name=guild.name
    )
    observability.metrics.increment('guild_leaves')


@bot.event
async def on_error(event, *args, **kwargs):
    observability.logger.error(
        f"Error in event: {event}",
        event=event,
        args=args,
        kwargs=kwargs
    )
    observability.metrics.increment('bot_errors', {'event': event})


# Load the slash commands extension
try:
    bot.load_extension("commands.guess_who")
    observability.logger.info("Loaded guess_who extension")
except Exception as e:
    observability.error_tracker.track_error(e, {'extension': 'guess_who'})

try:
    bot.load_extension("commands.arkdle")
    observability.logger.info("Loaded arkdle extension")
except Exception as e:
    observability.error_tracker.track_error(e, {'extension': 'arkdle'})

try:
    bot.load_extension("commands.ranking")
    observability.logger.info("Loaded ranking extension")
except Exception as e:
    observability.error_tracker.track_error(e, {'extension': 'ranking'})

try:
    bot.load_extension("commands.sextou")
    observability.logger.info("Loaded sextou extension")
except Exception as e:
    observability.error_tracker.track_error(e, {'extension': 'sextou'})

try:
    bot.load_extension("commands.health")
    observability.logger.info("Loaded health extension")
except Exception as e:
    observability.error_tracker.track_error(e, {'extension': 'health'})

observability.logger.info("All extensions loaded, starting bot...")
bot.start()
