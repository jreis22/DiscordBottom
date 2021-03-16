import requests
import urllib

def request_item_price(currency, appid, item):
    url = "https://steamcommunity.com/market/priceoverview/"
    #url ='https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name=P90%20%7C%20Asiimov%20%28Factory%20New%29'  url exemplo
    payload = {'currency': currency, 'appid': appid, 'market_hash_name': item}
    params = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    #usado para o encoding, ou seja, caracteres como espaços sao mudados para codigos especificos
    #espaço - %20
    #( - %28
    #) - %29 etc
    return requests.get(url, params=params)

def request_skin_price(weapon, skin, weapon_cond):
    weapon_hash = generate_weapon_hash(weapon, skin, weapon_cond)
    return request_item_price(3, 730, weapon_hash)

def generate_weapon_hash(weapon, skin, weapon_cond):
    weapon_hash = weapon + ' | ' + skin + ' (' + weapon_cond +')' # url é composto pelo nome da arma seguido de 1 espaço de 1 '|' e de outro espaço depois o nome da skin etc
    return weapon_hash

def request_item_page(appid, item):
    url="https://steamcommunity.com/market/listings/" + appid + "/" + item 
    return requests.get(url)


def reques_weaponPage(weapon, skin, weapon_cond):
    url=""
    return requests.get(url)

#print(generate_weapon_hash('P90', 'Asiimov', 'Factory New'))
#response = request_skin_price('P90', 'Asiimov', 'Factory New')

#print(response.json())
#print('lowest price: ' + response.json()['lowest_price'])