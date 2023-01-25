from pathlib import Path
import aiosqlite
import lightbulb

dbfuncs = lightbulb.Plugin("DBFunctions")

async def on_connect(db: str | Path) -> aiosqlite.Connection:
    conn = await aiosqlite.connect(f"{db}")
    return conn

async def player_info(id: str) -> tuple:
    select = "SELECT userid, cards from {id}"
    select = select.format(id = id)
    async with dbfuncs.bot.d.conn.cursor() as cursor:
        await cursor.execute(select)
        
        rows = await cursor.fetchall()
    players = []
    cards = []
    
    for row in rows:
        players.append(row[0])
        cards.append(row[1])
    return players, cards

async def game_join(id: str, player: str) -> str:
    players = await player_info(id)
    if player in players[0]:
        return "AlreadyJoined"
    elif len(players[0]) <= 4:
        async with dbfuncs.bot.d.conn.cursor() as cursor:
            await cursor.execute("INSERT INTO {id} (userid, owner) VALUES (?, ?)".format(id=id), (player, "No"))
        return "Joined"
    else:
        return "FullGame"


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(dbfuncs)
    
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(dbfuncs)       