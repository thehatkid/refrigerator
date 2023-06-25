import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.checks import check_if_staff
from helpers.sv_config import get_config


class OneShot(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(hidden=True, aliases=["renavi"])
    async def ren(self, ctx):
        """[U] What does Dishwasher think about ren?"""
        await ctx.send("HELP! HELP! HELP!")

    @commands.guild_only()
    @commands.command()
    async def staff(self, ctx):
        """[U] Shows currently active staff."""
        staff_role = ctx.guild.get_role(get_config(ctx.guild.id, "staff", "staff_role"))
        embed = discord.Embed(
            color=staff_role.color,
            title="🛠️ Staff List",
            description=f"Voting requirement is `{int(len(staff_role.members)/2//1+1)}`.",
            timestamp=datetime.datetime.now(),
        )
        embed.set_footer(text="Dishwasher")
        online = []
        away = []
        dnd = []
        offline = []
        for m in staff_role.members:
            u = f"{m.mention}"
            if m.is_on_mobile():
                u = f"{m.mention} 📱"
            if m.raw_status == "online":
                online.append(u)
            elif m.raw_status == "offline":
                offline.append(u)
            elif m.raw_status == "dnd":
                dnd.append(u)
            elif m.raw_status == "idle":
                away.append(u)
        if online:
            embed.add_field(
                name=f"🟢 Online [`{len(online)}`/`{len(staff_role.members)}`]",
                value=f"{','.join(online)}",
                inline=False,
            )
        if away:
            embed.add_field(
                name=f"🟡 Idle [`{len(away)}`/`{len(staff_role.members)}`]",
                value=f"{','.join(away)}",
                inline=False,
            )
        if dnd:
            embed.add_field(
                name=f"🔴 Do Not Disturb [`{len(dnd)}`/`{len(staff_role.members)}`]",
                value=f"{','.join(dnd)}",
                inline=False,
            )
        if offline:
            embed.add_field(
                name=f"⚫ Offline [`{len(offline)}`/`{len(staff_role.members)}`]",
                value=f"{','.join(offline)}",
                inline=False,
            )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.guild_only()
    @commands.command(aliases=["pingmods", "summonmods"])
    async def pingmod(self, ctx):
        """[U] Pings mods, only use when there's an emergency."""
        await ctx.reply(
            f"<@&{get_config(ctx.guild.id, 'staff', 'staff_role')}>, {ctx.author.display_name} is requesting assistance.",
            mention_author=False,
        )

    @commands.guild_only()
    @commands.command(aliases=["togglemod"])
    async def modtoggle(self, ctx):
        """[S] Toggles your Staff role.

        If you have Staff, it will replace it with Ex-Staff, and vice versa."""
        staff_role = ctx.guild.get_role(get_config(ctx.guild.id, "staff", "staff_role"))
        exstaff_role = ctx.guild.get_role(
            get_config(ctx.guild.id, "staff", "exstaff_role")
        )

        if staff_role in ctx.author.roles:
            await ctx.author.remove_roles(
                staff_role, reason="Staff self-unassigned Staff role"
            )
            await ctx.author.add_roles(
                exstaff_role, reason="Staff self-unassigned Staff role"
            )
            await ctx.message.reply(content="`🔴 Staff`", mention_author=False)
        elif exstaff_role in ctx.author.roles:
            await ctx.author.add_roles(
                staff_role, reason="Staff self-assigned Staff role"
            )
            await ctx.author.remove_roles(
                exstaff_role, reason="Staff self-assigned Staff role"
            )
            await ctx.message.reply(content="`🟢 Staff`", mention_author=False)
        else:
            await ctx.reply(
                content="You are unable to use this command.", mention_author=False
            )


async def setup(bot):
    await bot.add_cog(OneShot(bot))
