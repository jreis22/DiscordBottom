class BotCommands:
    def __init__(self):
        self.list = {}

    def on(self, command, handler):
        # TODO verificar se o comando ja existe
        self.list[command] = handler
