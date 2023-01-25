suits = {
    "H": "Hearts",
    "S": "Spades",
    "D": "Diamonds",
    "C": "Clubs"
}

ranks = {
    "A": "Ace",
    "7": "Seven",
    "K": "King",
    "J": "Jack",
    "Q": "Queen",
    "6": "Six",
    "5": "Five",
    "4": "Four",
    "3": "Three",
    "2": "Two"
}


def get_full_name(card: str):
    card_rank = card[0]
    card_suit = card[1]
    
    card_ranks = ranks[card_rank]
    card_suits = suits[card_suit]
    
    card_name = card_ranks + " of " + card_suits
    
    return card_name
    