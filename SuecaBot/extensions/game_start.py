import hikari
import lightbulb
import secrets
import string
import SuecaBot.utils.colors
import SuecaBot.database.dbfuncs


game_start = lightbulb.Plugin("Game Start", "Commands to starting a game")


@game_start.command
@lightbulb.add_checks(lightbulb.has_roles(1062809530477592667))
@lightbulb.command("start", "Start a game", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def on_game_start(ctx: lightbulb.SlashContext) -> None:
    gameid = (''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(10)))
    async with game_start.bot.d.conn.cursor() as cursor:
        await cursor.execute(f"""CREATE TABLE IF NOT EXISTS {gameid}(
                       userid TEXT,
                       owner TEXT,
                       cards TEXT,
                       trump_card TEXT
                       ) """)
        await cursor.execute("INSERT INTO {id} (userid, owner) VALUES (?,?)".format(id=gameid), (ctx.member.id, "Yes"))
    await game_start.bot.d.conn.commit()
    await ctx.respond(f"Game created with ID: {gameid}")


@game_start.command
@lightbulb.option("id", "Enter the game id you're trying to join")
@lightbulb.command("join", "Join a game", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def on_game_join(ctx: lightbulb.SlashContext) -> None:
    answer = await SuecaBot.database.dbfuncs.game_join(game_id=ctx.options.id, player=str(ctx.member.id))
    if answer == "AlreadyJoined":
        await ctx.respond("Game already Joined")
    elif answer == "FullGame":
        await ctx.respond("Game is full")
    else:
        await ctx.respond("Game Joined successfully")


@game_start.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("add", "Name of the column being added")
@lightbulb.option("table", "Which table to add to")
@lightbulb.command("create", "Create a column", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def on_column_add(ctx: lightbulb.SlashContext) -> None:
    async with game_start.bot.d.conn.cursor() as cursor:
        await cursor.execute(f"ALTER TABLE {ctx.options.table} ADD COLUMN {ctx.options.add} text")
    await game_start.bot.d.conn.commit()
    await ctx.respond(f"{ctx.options.add} inserted into {ctx.options.table}")
 
    
@game_start.command
@lightbulb.option("id", "ID of the game you want information for")
@lightbulb.command("info", "Get information about a game", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def on_game_check(ctx: lightbulb.SlashContext) -> None:
    players = await SuecaBot.database.dbfuncs.player_info(game_id=ctx.options.id)
    parsed_players = [f"<@{i}>" for i in players[0]]
    trump_card_pile = players[1][0]
    trump_card = trump_card_pile.split(" ")[0]
    info_embed = hikari.Embed(
        title=f"Game information: {ctx.options.id}",
        description=f"Players: {len(players[0])}/4",
        color=SuecaBot.utils.colors.get_color()
    )
    info_embed.add_field("Player Names", " | ".join(parsed_players) if parsed_players else "No players")
    info_embed.add_field("Trump Card", trump_card, inline=True)
    info_embed.add_field("Game Dealer", f"<@{players[0][0]}>", inline=True)
    if len(parsed_players) == 4:
        info_embed.add_field("Teams", f"Team 1: {parsed_players[0]}, {parsed_players[2]}\nTeam 2: {parsed_players[1]}, {parsed_players[3]}")
    await ctx.respond(info_embed)
    
    
@game_start.command
@lightbulb.option("id", "The game you want to deal to")
@lightbulb.command("deal", "Deal the cards", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def on_deal(ctx: lightbulb.SlashContext) -> None:
    deal_done = await SuecaBot.database.dbfuncs.dealing(game_id=ctx.options.id, player=str(ctx.author.id))
    players = await SuecaBot.database.dbfuncs.player_info(ctx.options.id)
    
    if deal_done == "Done":
        await ctx.respond("Cards have already been dealt. Use </info:1063888495875211334> to see the trump card")
    elif deal_done == "Dealt":
        await ctx.respond("Cards have been dealt. Use </info:1063888495875211334> to see the trump card")
    elif deal_done == "NotEnoughPlayers":
        await ctx.respond(f"More people need to join the game. Currently only {len(players[0])} have joined")
    elif deal_done == "NotOwner":
        await ctx.respond(f"You aren't the designated dealer of this game. <@{players[0][0]}> is the dealer")
    else:
        await ctx.respond("If you see this error, please DM Notorious#1472 immediately")

     
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(game_start)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(game_start)
