import sys
from card_game_logic.card_games.bisca import Bisca
from card_game_logic.cards.card_enums import Suit
from card_game_logic.card_games.card_game_type import CardGameType

msg = "asdadasdasdasdsad"
msg = "asd"
print(f"string is {msg[:5]}.")
customer = "asdasdadll"
balance = 1.2
print("{:.<5s}{:.>8.2f}".format(customer, balance))

customer = "asdasdadll"
balance = 1.2
print("{:<5s}{:>8.2f}".format(customer[:5], balance))