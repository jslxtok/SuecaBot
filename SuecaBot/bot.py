import hikari
import lightbulb
import os
from dotenv import load_dotenv
from SuecaBot.database.dbfuncs import on_connect, player_info

load_dotenv()

bot = lightbulb.BotApp(
    token=os.environ["TOKEN"],
    intents=hikari.Intents.ALL
)


@bot.listen(hikari.StartedEvent)
async def on_start(event: hikari.StartedEvent) -> None:
    print("Bot started")
    
    bot.d.conn = await on_connect("./SuecaBot/database/games.db")

    await bot.d.conn.commit()
    
    print("Database connected")


@bot.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("id", "Test")
@lightbulb.command("testcmd", "A testing command")
@lightbulb.implements(lightbulb.SlashCommand)
async def on_test(ctx: lightbulb.Context) -> None:
    players = await player_info(ctx.options.id)
    await ctx.respond(players)


@bot.listen(hikari.StoppedEvent)
async def on_stop(event: hikari.StoppedEvent) -> None:
    await bot.d.conn.close()
    print("Bot stopped")
    

bot.load_extensions_from("./SuecaBot/extensions", recursive=True)
bot.load_extensions_from("./SuecaBot/database", recursive=True)



def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()
        
    bot.run()