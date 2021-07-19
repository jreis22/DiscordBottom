import json
with open('user-config.json', 'r') as f:
    user_config = json.load(f)

TEST_CONFIG = {
    "SRC_PATH": user_config["SRC_PATH"]
}
