import hikari
import lightbulb
import os
from dotenv import load_dotenv
import aiosqlite

load_dotenv()

bot = lightbulb.BotApp(
    token=os.environ["TOKEN"],
    intents=hikari.Intents.ALL
)

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.MissingRequiredRole):
        await event.context.respond(f"You do not have the <@&{exception.missing_roles[0]}> role")
    elif isinstance(exception, lightbulb.NotOwner):
        await event.context.respond(f"You are not the owner: Notorious#1472")
    else:
        raise exception

@bot.listen(hikari.StartedEvent)
async def on_start(event: hikari.StartedEvent) -> None:
    print("Bot started")
    
    bot.d.conn = await aiosqlite.connect("./SuecaBot/database/games.db")
    await bot.d.conn.commit()
    
    print("Database connected")

@bot.listen(hikari.ShardReadyEvent)
async def on_start(event: hikari.ShardReadyEvent) -> None:
    guilds = event.unavailable_guilds
    for guild in guilds:
        print(guild)
    
    print(guilds)

@bot.listen(hikari.StoppedEvent)
async def on_stop(event: hikari.StoppedEvent) -> None:
    await bot.d.conn.close()
    print("Bot stopped")
    

bot.load_extensions_from("./SuecaBot/extensions", recursive=True)


def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()
        
    bot.run()