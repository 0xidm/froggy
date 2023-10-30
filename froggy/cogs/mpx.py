import random

import discord
from discord.ext import commands

from disco.cog import BaseCog
from crypto_watcher.models import Quote, Metrics


class MetricsMPX(BaseCog):
    @commands.command(name="mpx")
    async def on_mpx(self, ctx):
        await ctx.message.delete(delay=1)
        if not await self.is_allowed(ctx=ctx):
            return

        metrics = Quote.get_pair_metrics_current("MPX-USDC")
        pills_summary = Metrics.get_latest("PILLS")
        ftm_usdc = Quote.get_pair_metrics_current("FTM-USDC")["price"]

        embed = discord.Embed(
            title=f"MPX: {metrics['price']:<0.3f} USD ({metrics['price']/ftm_usdc:<0.3f} FTM)",
            colour=discord.Color.blue(),
        )

        embed.add_field(name="percent change", value=f"`1-hour: {metrics['pct_1h']*100:>4.1f}%`\n`1-day : {metrics['pct_1d']*100:>4.1f}%`")

        embed.add_field(name="moving average", value=f"`1-hour: {metrics['ma_1h']:>8.3f}`\n`1-day : {metrics['ma_1d']:>8.3f}`")

        embed.add_field(name="price range", value=f"`1-hour: ({metrics['low_1h']:>0.3f}, {metrics['high_1h']:>0.3f})`\n`1-day : ({metrics['low_1d']:>0.3f}, {metrics['high_1d']:>0.3f})`", inline=False)

        # embed.add_field(name="est. circulating", value=f"`{(pills_summary.burned / 2) * 1.02:<0,.0f} MPX ({(pills_summary.burned / 2) * 1.02 * metrics['price']:<0,.0f} USD)`", inline=False)

        embed.set_thumbnail(url="https://assets.coingecko.com/coins/images/28965/small/mpx_logo_256.png?1675744910")

        # if random.randint(0, 5) == 0:
        embed.add_field(name="command", value="`f.mpx`", inline=True)

        if random.randint(0, 10) == 0:
            embed.add_field(name="for help with froggy", value="`f.help`", inline=True)

        if random.randint(0, 25) == 0:
            embed.add_field(name="about this", value="`f.about`", inline=True)

        await ctx.send(embed=embed)
