import hikari
import lightbulb


errors = lightbulb.Plugin("Errors")


@errors.listener(lightbulb.CommandErrorEvent)
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
    

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errors)

def unload(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errors)