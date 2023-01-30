import random
from pathlib import Path
import aiosqlite
import lightbulb
from random import shuffle

dbfuncs = lightbulb.Plugin("DBFunctions")


async def on_connect(db: str | Path) -> aiosqlite.Connection:
    conn = await aiosqlite.connect(f"{db}")
    return conn


async def player_info(id: str) -> tuple:
    select = "SELECT userid, cards from {id}"
    select = select.format(id=id)
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
            await cursor.execute(f"INSERT INTO {id} (userid, owner) VALUES (?, ?)", (player, "No"))
        await dbfuncs.bot.d.conn.commit()
        return "Joined"
    else:
        return "FullGame"

cards = ['AS', 'AD', 'AH', 'AC', '7S', '7D', '7H', '7C', 'KS', 'KD', 'KH', 'KC', 'JS', 'JD', 'JH', 'JC', 'QS', 'QD', 'QH', 'QC', '6S', '6D', '6H', '6C', '5S', '5D', '5H', '5C', '4S', '4D', '4H', '4C', '3S', '3D', '3H', '3C', '2S', '2D', '2H', '2C']


def shuffle_and_return(lst: list) -> list:
    shuffle(lst)
    return lst


async def dealing(id: str, player: str, dealing_cards=cards) -> str:
    shuffled_cards = shuffle_and_return(dealing_cards)
    trump_card = shuffled_cards[1]
    players = await player_info(id)
    lst_of_players = []
    for player in players[0]:
        lst_of_players.append(player)
    if player != lst_of_players[0]:
        return "NotOwner"
    elif len(lst_of_players) != 4:
        return "NotEnoughPlayers"
    else:
        async with dbfuncs.bot.d.conn.cursor() as cursor:
            for i in range(4):
                await cursor.execute(f"UPDATE {id} set cards = ?, trump_card = ? WHERE userid = ?", (shuffled_cards[i:i+10], trump_card, lst_of_players[i]))
        await dbfuncs.d.conn.commit()
        return "Dealt"


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(dbfuncs)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(dbfuncs)
