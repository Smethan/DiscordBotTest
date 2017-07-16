import random

import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
import logging


bot = commands.Bot(command_prefix="!")
def embed_split(text: str) -> [str]:
    """Split a string so it will fit inside an embed."""
    while text:
        yield text[:1024]
        text = text[1024:]


class APIinstance:

    def __init__(self, session):
        self.session = session

    @property
    def baseURL(self):
        return None

    @property
    def apiExtension(self):
        return None

    @property
    def thumbURL(self):
        return None

    @property
    def headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }

    async def find_valid_url(self, urls, key=None, base=""):
        random.shuffle(urls)
        for i in urls:
            url = i[key] if key is not None else i
            async with self.session.head(base + url, headers=self.headers) as resp:
                if resp.status == 200:
                    return i
        raise Exception("No valid images")

    async def grab_data(self, **kwargs):
        async with self.session.get(self.baseURL + self.apiExtension, params=kwargs, headers=self.headers) as resp:
            if resp.status == 200:
                return await resp.json()
            raise Exception(f"Could not grab data from api, status: {resp.status}")

    def gen_embed(self, image_url, tags, source=None):
        em = discord.Embed(colour=19773, title=f"Booru result from {self.__class__.__name__}", url=source)
        em.set_image(url=image_url)
        if self.thumbURL:
            em.set_thumbnail(url=self.thumbURL)
        for i in embed_split(tags):
            em.add_field(name="Tags", value=i, inline=True)
        return em

    async def parse_req_tags(self, *tags):
        responses = await self.grab_data(tags="?".join(tags))
        valid = await self.find_valid_url(responses, key="file_url")
        tags = valid.get("tags")
        image_url = valid["file_url"]
        source = valid.get("source")

        return self.gen_embed(image_url, tags, source)





class e926(APIinstance):

    @property
    def baseURL(self):
        return "https://e926.net"
    @property
    def apiExtension(self):
        return "/post/index.json"

    @property
    def thumbURL(self):
        return "http://emblemsbf.com/img/63681.jpg"

    @property
    def headers(self):
        return {
            'User-Agent': 'CoolBot/1.0 (by pekka4597 on e926)'
        }
class Booru:
    """Collection of booru related commands for the bot."""

    def __init__(self, bot):
        self.bot = bot
        self.e926_ = e926(bot.session)
        
    
    @commands.command()
    async def e926(self, *tags: str):
        """Search e926 for images.
        Enter multiple tags by seperating them with spaces
        """
        
        await ctx.send(embed=await self.e926_.parse_req_tags(*tags))
async def __error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("NSFW boorus can only be used in channels marked NSFW.", delete_after=10.0)
    else:
        await ctx.send("Failed to get an image for requested tags", delete_after=10.0)


def setup(bot):
    bot.add_cog(Booru(bot))
