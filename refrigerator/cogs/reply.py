import discord
from discord.ext.commands import Cog
from discord.ext import commands, tasks
import json
import re
import config
import datetime
import asyncio
from helpers.checks import check_if_staff
from helpers.sv_config import get_config


class Reply(Cog):
    """
    A cog that stops people from ping replying people who don't want to be.
    """

    def __init__(self, bot):
        self.bot = bot
        self.usercounts = {}
        self.counttimer.start()
        self.last_eval_result = None
        self.previous_eval_code = None

    def cog_unload(self):
        self.counttimer.cancel()

    async def handle_message_with_reference(self, message):
        reference_message = await message.channel.fetch_message(
            message.reference.message_id
        )
        reference_author = reference_message.author
        if (
            message.author.bot
            or not message.guild
            or not message.guild.get_member(reference_author.id)
            or reference_author.id == message.author.id
            or not get_config(message.guild.id, "noreply", "enable")
            or reference_author.get_role(
                get_config(message.guild.id, "noreply", "noreply_role")
            )
            is None
        ):
            return

        staff_role = get_config(message.guild.id, "staff", "staff_role")
        if staff_role and message.author.get_role(staff_role):
            return

        if reference_author in message.mentions:
            if message.author.id not in self.usercounts:
                self.usercounts[message.author.id] = 1
            else:
                self.usercounts[message.author.id] += 1

            if self.usercounts[message.author.id] == 5:
                await message.reply(
                    content=f"{message.guild.get_role(staff_role).mention} | {message.author.mention} reached `5` reply ping violations.",
                    mention_author=False,
                )
                self.usercounts[message.author.id] = 0
                return

            await message.add_reaction("🗞️")
            nagmsg = await message.reply(
                content=f"This is violation number `{self.usercounts[message.author.id]}`. Do not exceed `5` violations today.",
                file=discord.File("assets/noreply.png"),
                mention_author=True,
            )
            await nagmsg.add_reaction("🛑")

            def check(r, u):
                return (
                    u.id == reference_author.id
                    and str(r.emoji) == "🛑"
                    and r.message.id == nagmsg.id
                )

            try:
                await self.bot.wait_for("reaction_add", timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await nagmsg.delete()
            else:
                self.usercounts[message.author.id] -= 1
                await message.remove_reaction("🗞️", self.bot.user)
                await nagmsg.edit(
                    content=f"Violation pardoned. You now have `{self.usercounts[message.author.id]}` violations.",
                    attachments=[],
                    delete_after=15,
                )
            return

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def reset(self, ctx, target: discord.Member):
        if target.id not in self.usercounts or self.usercounts[target.id] == 0:
            return await ctx.reply(
                content="This user doesn't have any reply ping violations.",
                mention_author=False,
            )
        else:
            self.usercounts[target.id] = 0
            return await ctx.reply(
                content="This user's reply ping counter has been reset.",
                mention_author=False,
            )

    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()

        if message.reference and message.type == discord.MessageType.reply:
            await self.handle_message_with_reference(message)

    @tasks.loop(hours=24)
    async def counttimer(self):
        await self.bot.wait_until_ready()
        self.usercounts = {}


async def setup(bot):
    await bot.add_cog(Reply(bot))
