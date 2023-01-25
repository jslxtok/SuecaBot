import hikari
import SuecaBot.utils.colors

info1 = hikari.Embed(
    title="Game Information",
    description="Find out more about the game from https://www.youtube.com/watch?v=UKCijAAIOe8.\nThe game originates from Portugal and its colonies. Frequently played with 2-4 'Games', this render of Sueca includes 1 game only",
    color=SuecaBot.utils.colors.get_color()
)

info2 = (
    hikari.Embed(
        title="How to win!",
        description="In tournaments the strict rule of no talking is enforced, however, since on Discord this cannot be enforced casual rules are applied",
        color=SuecaBot.utils.colors.get_color()
    )
    .add_field("Teams", "Teams are made where Player 1 (Dealer) and Player 3 (Third Person to join game) team up and the remaining 2 players form their own team")
    .add_field("Trump Suit", "The trump card contains the strongest suit (Diamonds, Hearts, Spades, Clubs). Any card containing this suit is automatically the highest rated card of the round until another card of the same suit is played with a higher rank.")
    .add_field("Lead Suit", "The lead suit is a highest rated suit, other than the trump suit of each round. The first card played in each round contains the lead suit")
    .add_field("Point Awarding", "Each round, often called Tricks, is won by the player who placed down the highest rated card that trick. The team who the player belongs to gets awared the points.")
    .add_field("How many points you get", "The total points added to the team is a collection of all the points each card is worth that round. Find out how many points a card is worth on the next page.")
    .add_field("Final scores", "At the end of the round all points are calculated and the team with the most points win. A total of 120 points are awarded")
)

info3 = (
    hikari.Embed(
        title="Points",
        description="This page shows you how many points a card is worth\nAce: 11\nSeven: 10\nKing: 4\nJack: 3\nQueen: 2\nAll other cards are worth 0 points",
        color=SuecaBot.utils.colors.get_color()
    )
)

def get_info_list():
    info_list = [info1, info2, info3]
    return info_list
