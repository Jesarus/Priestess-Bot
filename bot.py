import interactions
from config import TOKEN

bot = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT,
)


@bot.event
async def on_ready():


# Load the slash commands extension
bot.load_extension("commands.guess_who")
bot.load_extension("commands.arkdle")

print("Iniciando o bot...")
bot.start()
