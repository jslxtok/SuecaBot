import lightbulb
import hikari
import SuecaBot.utils.dbhelpers


player_cmds = lightbulb.Plugin("Player Commands", "Commands for players to use")


@player_cmds.command
@lightbulb.option("id", "Which game you want to view your cards for")
@lightbulb.command("cards", "View your cards", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def on_card_view(ctx: lightbulb.SlashContext) -> None:
    cards = await SuecaBot.utils.dbhelpers.cards_view(id=ctx.options.id, player=str(ctx.member.id))
    if cards == "None":
        await ctx.respond("Cards have not been dealt yet")
    else:
        await ctx.respond(", ".join(cards))
    

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(player_cmds)
    
    
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(player_cmds)