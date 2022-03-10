from __future__ import annotations

from typing import TYPE_CHECKING

from discord.utils import escape_mentions
from discord.ext import commands

from core import BoboContext, Cog, group

if TYPE_CHECKING:
    from asyncpg.pool import Pool


class TagManager:
    def __init__(self, db: Pool):
        self.db = db
    
    async def new_tag(self, ctx: BoboContext, name: str, content: str):
        await self.db.execute(
            'INSERT INTO tags (name, content, author_id, message_id) VALUES ($1, $2, $3)',
            name, content, ctx.author.id, ctx.message.id
        )
    
    async def get_tag_content(self, name: str) -> str | None:
        return await self.db.fetchval(
            'SELECT content FROM tags WHERE name = $1', name
        )


class Tag(Cog):
    def init(self):
        self.tag_manager = TagManager(self.bot.db)
    
    @commands.group(invoke_without_command=True)
    async def tag(self, ctx: BoboContext, *, name: str) -> None:
        """Shows the content of a tag."""
        content = await self.tag_manager.get_tag_content(name)
        if not content:
            await ctx.send('Tag not found.')
        
        await ctx.send(escape_mentions(content))
    
    @tag.command(alias=['create'])
    async def new(self, ctx: BoboContext, name: str, *, content: str) -> None:
        """Creates a new tag."""
        if len(name) > 200:
            await ctx.send('Tag name is too long.')

            return

        await self.tag_manager.new_tag(ctx, name, content)
        
        await ctx.send('Tag created.')
    

setup = Tag.setup
