import hikari
import lightbulb
import SuecaBot.utils.ruleembeds
import miru
from miru.ext import nav


class MyNavButton(nav.NavButton):
    def __init__(self):
        super().__init__(label="Page: 1", row=1)


    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond("Why click this?", flags=hikari.MessageFlag.EPHEMERAL)

    async def before_page_change(self) -> None:
        # This function is called before the new page is sent by
        # NavigatorView.send_page()
        self.label = f"Page: {self.view.current_page+1}"


info_rules = lightbulb.Plugin("Rules and Info", "A bunch of commands showing")


@info_rules.command
@lightbulb.command("gameinfo", "Get info about sueca", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def on_game_info_view(ctx: lightbulb.SlashContext) -> None:
    pages = [SuecaBot.utils.ruleembeds.info1, SuecaBot.utils.ruleembeds.info2, SuecaBot.utils.ruleembeds.info3]
    buttons = [nav.PrevButton(), nav.StopButton(), nav.NextButton(), MyNavButton()]
    navigator = nav.NavigatorView(pages=pages, buttons=buttons)
    await ctx.respond("View the information below")
    await navigator.send(ctx.channel_id, responded=False)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_rules)
    miru.install(info_rules.bot)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(info_rules)
    