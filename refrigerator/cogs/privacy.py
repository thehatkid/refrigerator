import discord
from discord.ext.commands import Cog
from discord.ext import commands, tasks
import json
import re
import config
import datetime
import asyncio
import hashlib
import time
from helpers.checks import check_if_staff
from helpers.sv_config import get_config


class Privacy(Cog):
    """
    For when you want to be forgotten.
    """

    def __init__(self, bot):
        self.bot = bot
        hashlib.sha1().update(str(time.time()).encode("utf-8"))
        self.verifycode = hashlib.sha1().hexdigest()[:10]

    def add_erased(self, guild, user):
        pass

    @commands.guild_only()
    @commands.command()
    async def erase(self, ctx, verify=None):
        if not verify:
            return await ctx.reply(
                f"**THIS IS A VERY DESTRUCTIVE AND IRREVERSIBLE ACTION!**\nThe `erase` command will systematically and painstakingly wipe your post history from the current server, leaving **NOTHING** behind!\nAfter this is complete, you will be DMed a link containing all of your files and images uploaded to this server. Download it within one week, or it will be gone forever.\nI __strongly__ recommend you request your Data Package first by going to the following location on your client:\n- `Settings`\n- `Privacy & Safety`\n- `Request all of my data`\nWait for it to arrive before proceeding.\n\nIf you are SURE that you want to do this, rerun this command with the following code: `{self.verifycode}`"
            )
        if verify != self.verifycode:
            return await ctx.reply("You specified an incorrect verification code.")
        else:
            add_erased(guild.user)
            hashlib.sha1().update(str(time.time()).encode("utf-8"))
            self.verifycode = hashlib.sha1().hexdigest()[:10]
            pass


async def setup(bot):
    await bot.add_cog(Privacy(bot))
