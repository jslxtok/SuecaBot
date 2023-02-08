import lightbulb
import sqlite3


errors = lightbulb.Plugin("Errors")


@errors.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:

    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.MissingRequiredRole):
        await event.context.respond(f"You do not have the <@&{exception.missing_roles[0]}> role")
    elif isinstance(exception, lightbulb.NotOwner):
        await event.context.respond(f"You are not the owner: Notorious#1472")
    elif isinstance(exception, sqlite3.OperationalError):
        error = exception.args[0]
        if error.startswith('no such table:'):
            await event.context.respond("The ID you entered is not valid")
        if error.startswith('near'):
            await event.context.respond("Enter a valid ID form")
    else:
        raise exception
    

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errors)


def unload(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errors)
