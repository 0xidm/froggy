import re

import discord

from . import MorphexHandler

class ExchangesHandler(MorphexHandler):

    async def check(self, message):
        return re.search(r'equalizer|firebird|buy mpx|get mpx|swap mpx|hoard mpx|acquire mpx', message.content.lower())

    async def respond(self, message):
        embed = discord.Embed(
            title=f"Swap MPX",
            colour=discord.Color.blue(),
        )

        embed.add_field(name="Firebird", value=f"[firebird.finance](https://app.firebird.finance/?utm_source=referral&utm_campaign=oref&aff=45hHgEnwXVixCuXxAWNzTXRMLPkR)", inline=False)
        embed.add_field(name="Equalizer", value=f"[equalizer.exchange](https://equalizer.exchange/swap?outputCurrency=0x66eed5ff1701e6ed8470dc391f05e27b1d0657eb)", inline=False)
        embed.add_field(name="1inch", value=f"[1inch.io](https://app.1inch.io/#/250/simple/swap/FTM/0x66eed5ff1701e6ed8470dc391f05e27b1d0657eb)", inline=False)

        embed.set_thumbnail(url="https://assets.coingecko.com/coins/images/28965/small/mpx_logo_256.png?1675744910")

        return await message.channel.send(embed=embed)
