import aiosqlite
from random import shuffle


async def player_count(id: str):
    async with aiosqlite.connect("SuecaBot/database/games.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f"SELECT userid, cards FROM {id}")
            rows = await cursor.fetchall()
    players = []
    for row in rows:
        players.append(row[0])

    trump_card = rows[0][1]
    if trump_card is None:
        return players, None
    else:
        dealer_cards = trump_card.split(" ")
        trump = dealer_cards[0]
        return players, trump


async def game_join(id: str, player: str):
    async with aiosqlite.connect("SuecaBot/database/games.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f"SELECT userid from {id}")
            rows = await cursor.fetchall()
    players = []
    for row in rows:
        players.append(row[0])
    is_owner = "No"
    if player in players:
        return "No"
    elif len(players) == 4:
        return "Game Full"
    else:
        async with aiosqlite.connect("SuecaBot/database/games.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute(f"INSERT INTO {id} (userid, owner) VALUES (?, ?)", (player, is_owner))

            await db.commit()
        return "Ok"


deck = ['AS', 'AD', 'AH', 'AC', '7S', '7D', '7H', '7C', 'KS', 'KD', 'KH', 'KC', 'JS', 'JD', 'JH', 'JC', 'QS', 'QD',
        'QH', 'QC', '6S', '6D', '6H', '6C', '5S', '5D', '5H', '5C', '4S', '4D', '4H', '4C', '3S', '3D', '3H', '3C',
        '2S', '2D', '2H', '2C']


def shuffle_and_return(lst: list) -> list:
    shuffle(lst)
    return lst


async def dealing(id: str, player: str, cards=deck):
    dealing_cards = shuffle_and_return(cards)
    async with aiosqlite.connect("SuecaBot/database/games.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f"SELECT userid, owner FROM {id}")
            rows = await cursor.fetchall()
    players = []
    for row in rows:
        players.append(row[0])

    if player == players[0]:
        j = 0
        cards = []
        for i in range(4):
            cards.append(dealing_cards[j:j + 10])
            j += 10
        async with aiosqlite.connect("SuecaBot/database/games.db") as db:
            async with db.cursor() as cursor:
                for i in range(4):
                    await cursor.execute(f"UPDATE {id} SET cards = ?, trump_card = ? WHERE userid = ?",
                                         (' '.join(map(str, cards[i])), dealing_cards[0], players[i]))
            await db.commit()
        return "Done"
    elif len(players) != 4:
        return "NotEnough"
    else:
        return "Nope"


async def cards_view(id: str, player: id):
    async with aiosqlite.connect("SuecaBot/database/games.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f"SELECT cards FROM {id} WHERE userid = ?", (player,))
            rows = await cursor.fetchone()
    cards = rows[0]
    if cards is None:
        return "None"
    else:
        cards_list = cards.split(" ")
        return cards_list
