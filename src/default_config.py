import json
with open('user-config.json', 'r') as f:
    user_config = json.load(f)

DEFAULT_CONFIG = {
    "TOKEN": user_config["TOKEN"],
    "prefix": "!"
}
