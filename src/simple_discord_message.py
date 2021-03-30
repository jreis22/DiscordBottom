import discord
from typing import List, Union

class SimpleDiscordMessage:
    def __init__(self, content: str = None, embed: discord.Embed = None, reactions: List[str] = None, channel: Union[discord.abc.Messageable, int] = None):
        self.content = content
        self.embed = embed
        self.set_reactions(reactions=reactions)
        self.set_channel(channel)

    def set_reactions(self, reactions: List[str]):
        if reactions is None:
            self.reactions = []
        else:
            self.reactions = reactions

    def set_channel(self, channel: Union[discord.abc.Messageable, int]):
        if channel is None or isinstance(channel, discord.abc.Messageable):
            self.channel = channel
        else:
            self.channel = None
            self.channel_id = channel

