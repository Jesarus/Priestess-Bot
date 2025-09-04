import interactions
from config import TOKEN

bot = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT,
)


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.me.name}")


# Load the slash commands extension
bot.load_extension("commands.guess_who")

bot.start()
