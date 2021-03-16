from default_config import DEFAULT_CONFIG
from bot_commands import bot
from card_image_dictionary import CardImageDictionary

#cards_config = json.load(open('cards-config.json', 'r'))
#print(Suit.DIAMONDS.name)
#print(Suit.DIAMONDS.name in cards_config)
#for key in Suit.get_all():
#    print(f"{key.name}: {not key.name in cards_config}")
#    
#    for second_key in Rank.get_all():
#        print(f"{second_key.name}: {second_key.name in cards_config[key.name]}")
CardImageDictionary.load_deck()

bot.run(DEFAULT_CONFIG["TOKEN"])
