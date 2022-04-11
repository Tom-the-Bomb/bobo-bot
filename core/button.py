from operator import truediv
import discord

from config import Emojis

__all__ = ('DeleteButton',)


class DeleteButton(discord.ui.Button):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(
            emoji=discord.PartialEmoji.from_str(Emojis.Trash),
            style=discord.ButtonStyle.grey,
        )

    async def interaction_check(self, interaction) -> bool:
        return interaction.user.id == self.user_id

    async def callback(self, interaction) -> None:
        if interaction.message:
            await interaction.message.delete()
