import requests
import urllib

def request_skin_price(weapon, skin, weapon_cond):
    weapon_hash = generate_weapon_hash(weapon, skin, weapon_cond)
    payload = {'currency': '3', 'appid': '730', 'market_hash_name': weapon_hash}
    url = "https://steamcommunity.com/market/priceoverview/"
    #url ='https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name=P90%20%7C%20Asiimov%20%28Factory%20New%29'
    params = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote) #usado para o encoding dos "espaços" ser '%20' em vez de '+'
    return requests.get(url, params=params)

def generate_weapon_hash(weapon, skin, weapon_cond):
    weapon_hash = weapon + ' | ' + skin + ' (' + weapon_cond +')'
    #weapon_hash = weapon_hash.replace(' ', '%20') #usado para encoding, mas já nao é necessario
    return weapon_hash

#print(generate_weapon_hash('P90', 'Asiimov', 'Factory New'))
response = request_skin_price('P90', 'Asiimov', 'Factory New')

print(response.json())
print('lowest price: ' + response.json()['lowest_price'])