from pathlib import Path
import aiosqlite
import lightbulb
from random import shuffle

db_funcs = lightbulb.Plugin("DBFunctions")


async def on_connect(db: str | Path) -> aiosqlite.Connection:
    conn = await aiosqlite.connect(f"{db}")
    return conn


async def player_info(game_id: str) -> tuple:
    select = f"SELECT userid, cards from {game_id}"
    async with db_funcs.bot.d.conn.cursor() as cursor:
        await cursor.execute(select)

        rows = await cursor.fetchall()
    players = []
    cards = []
    
    for row in rows:
        players.append(row[0])
        cards.append(row[1])
    return players, cards


async def game_join(game_id: str, player: str) -> str:
    players = await player_info(game_id)
    if player in players[0]:
        return "AlreadyJoined"
    elif len(players[0]) <= 4:
        async with db_funcs.bot.d.conn.cursor() as cursor:
            await cursor.execute(f"INSERT INTO {game_id} (userid, owner) VALUES (?, ?)", (player, "No"))
        await db_funcs.bot.d.conn.commit()
        return "Joined"
    else:
        return "FullGame"

lst_of_cards = ['AS', 'AD', 'AH', 'AC', '7S', '7D', '7H', '7C', 'KS', 'KD', 'KH', 'KC', 'JS', 'JD', 'JH', 'JC', 'QS', 'QD', 'QH', 'QC', '6S', '6D', '6H', '6C', '5S', '5D', '5H', '5C', '4S', '4D', '4H', '4C', '3S', '3D', '3H', '3C', '2S', '2D', '2H', '2C']


def shuffle_and_return(lst: list) -> list:
    shuffle(lst)
    return lst


async def dealing(game_id: str, player: str) -> str:
    shuffled_cards = shuffle_and_return(lst_of_cards)
    trump_card = shuffled_cards[1]
    players = await player_info(game_id)
    lst_of_players = []


    for p in players[0]:
        lst_of_players.append(p)
    if player != lst_of_players[0]:
        return "NotOwner"
    elif len(lst_of_players) != 4:
        return "NotEnoughPlayers"
    elif players[1][0] is not None:
        return "Done"
    else:
        sets_of_cards = [shuffled_cards[i::4] for i in range(4)]
        async with db_funcs.bot.d.conn.cursor() as cursor:
            for i in range(4):
                await cursor.execute(f"UPDATE {game_id} set cards = ?, trump_card = ? WHERE userid = ?", (' '.join(map(str, sets_of_cards[i])), trump_card, lst_of_players[i]))
        await db_funcs.bot.d.conn.commit()
        return "Dealt"


async def cards_view(game_id: str, player: str) -> str:
    async with db_funcs.bot.d.conn.cursor() as cursor:
        await cursor.execute(f"SELECT cards FROM {game_id} WHERE userid = ?", (player,))
        rows = await cursor.fetchone()
    cards = rows[0]
    if cards is None:
        return "None"
    else:
        cards_list = cards.split(" ")
        return cards_list


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(db_funcs)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(db_funcs)
