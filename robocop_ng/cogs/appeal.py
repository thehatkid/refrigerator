import discord
from discord.ext.commands import Cog
import json
import re
import config
import datetime
from helpers.restrictions import get_user_restrictions
from helpers.checks import check_if_staff


class Appeal(Cog):
    """
    Automatic responses for the Ban Appeal system.
    """

    def __init__(self, bot):
        self.bot = bot
        self.last_eval_result = None
        self.previous_eval_code = None

    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()
        
        if message.channel.id == "402019542345449472":
            await message.channel.send(content=f"Pass.\n{message.author.id}\n{message.author.display_name}\n{message.embeds[0].fields[1].value}")
            if message.author.id == "402016472878284801":
                await message.channel.send(content="Pass.")
                if message.embeds[0].fields[1].value is not None:
                    await message.add_reaction("✅")
                    await message.add_reaction("❎")
                    await message.add_reaction("✳️")
                    appealthread = await message.create_thread(name=f"{message.embeds[0].fields[1].value[:-5]}'s Appeal", reason="Automatic Appeal Thread Generating by Dishwasher.")
                    appealthread.send(content=f"Until it can be coded to automatically appear here, use `pws logs {message.embeds[0].fields[2].value}`.\n\n**Voting has MOVED to the appeal post itself! Vote using reactions, and use this thread for discussion.\nRemember to post ban context if available (ban record, modmail logs, etc.).")
                
async def setup(bot):
    await bot.add_cog(Appeal(bot))