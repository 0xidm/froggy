import re
import datetime

import discord
import requests

from . import MorphexHandler
from crypto_watcher.models import Quote, Metrics


class McapHandler(MorphexHandler):
    def __init__(self):
        super().__init__()
        self.delete_own_delay = 180

    async def check(self, message:discord.Message):
        return re.search(r'mcap|market cap|\smc[\s$]|marketcap|circulating', message.content.lower())

    async def respond(self, message):
        # query the circulating supply endpoint
        resp = requests.get("https://token-api.morphex.trade/api/v1/mpx.json")
        if resp.status_code != 200:
            self.logger.warning("Error fetching mpx.json from Token API")
            # quietly return
            return
        else:
            circulating_supply = float(resp.json()["circulating"])

        mpx_price = Quote.get_pair_metrics_current("MPX-USDC")['price']
        msg = f"`{circulating_supply:<0,.0f} MPX ({circulating_supply * mpx_price:<0,.0f} USD)`"

        embed = discord.Embed(
            title=f"MPX",
            colour=discord.Color.blue(),
        )
        embed.add_field(name="Circulating supply", value=msg, inline=False)
        embed.set_thumbnail(url="https://assets.coingecko.com/coins/images/28965/small/mpx_logo_256.png?1675744910")

        return await message.channel.send(embed=embed)
