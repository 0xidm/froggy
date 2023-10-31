import asyncio

import discord

from disco.bot import DiscoBot

from disco.cogs.help import HelpMenus

from disco.listener.wen import WenHandler
from disco.listener.hello import HelloHandler
from disco.listener.gm import GmHandler
from disco.listener.gn import GnHandler
from disco.listener.thankyou import ThankYouHandler
from disco.listener.bad import BadHandler

from .cogs.keepers import KeepersStats
from .cogs.mpx import MetricsMPX

from .listener.exchanges import ExchangesHandler
from .listener.contracts import ContractsHandler
from .listener.mcap import McapHandler
from .listener.automod import AutomodRpcHandler
from .listener.automod import AutomodGasPriceHandler
from .listener.automod import AutomodMLPFaqHandler


class Froggy(DiscoBot):
    def run(self):
        self.create_bot(command_prefix=['f.', 'F.'])

        # disco cogs
        self.add_cog(HelpMenus(help_messages))

        # disco listeners
        self.add_listener(WenHandler())
        self.add_listener(HelloHandler())
        self.add_listener(GmHandler())
        self.add_listener(GnHandler())
        self.add_listener(ThankYouHandler())
        self.add_listener(BadHandler())

        # froggy cogs
        self.add_cog(KeepersStats())
        self.add_cog(MetricsMPX())

        # froggy listeners
        self.add_listener(ExchangesHandler())
        self.add_listener(ContractsHandler())
        self.add_listener(McapHandler())
        self.add_listener(AutomodRpcHandler())
        self.add_listener(AutomodGasPriceHandler())
        # self.add_listener(AutomodMLPFaqHandler())

        self.connect()

    async def handle_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="f.help for help")
            )

        # start keepers balance reporter
        if not self.config["debug"]:
            await asyncio.gather(
                self.bot.get_cog("KeepersStats").run_loop(client=self.bot)
            )

        self.logger.info(f'{self.bot.user.name} has connected')
        print("Froggy is ready to go!")


help_messages = {
    "main": """
The following help topics are available:

- `f.help mpx      `: MPX-related commands
- `f.help about    `: About Froggy
""",
    "mpx": """
- `f.mpx       `: price of MPX
- `circulating `: MPX circulating supply
- `swap mpx    `: where to swap MPX
- `mpx contract`: MPX contract address
""",
    "ecosystem": """
- `f.gas [blockchain]`: Current gas prices (`ftm`, `eth`)
- `t [symbol]        `: spot price for `symbol` (tsuki style)
""",
    "about": """
**Froggy** is a price bot that watches the Fantom Ecosystem - including MPX, FTM, YFI, and more.

**Froggy** commands are invoked with the `f.` prefix.

**Froggy** includes curious market monitoring widgets that could unlock the secrets of the Fantom economy. 

Help is available with the command `f.help`.
""",
}
