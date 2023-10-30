import copy
import time
import asyncio
import datetime
from pprint import pprint

import discord
from discord.ext import commands

from crypto_watcher.models import Keeper, KeeperBalance
from disco.cog import BaseCog


keepers_list = {
    "liquidator-1": {
        "alarm_threshold": 300,
        "emergency_threshold": 150,
    },
    "order-1": {
        "alarm_threshold": 300,
        "emergency_threshold": 150,
    },
    "position-1": {
        "alarm_threshold": 300,
        "emergency_threshold": 150,
    },
    "price-1": {
        "alarm_threshold": 300,
        "emergency_threshold": 150,
    },
    "liquidator-1-bsc": {
        "alarm_threshold": 0.3,
        "emergency_threshold": 0.15,
    },
    "order-1-bsc": {
        "alarm_threshold": 0.3,
        "emergency_threshold": 0.15,
    },
    "position-1-bsc": {
        "alarm_threshold": 0.3,
        "emergency_threshold": 0.15,
    },
    "price-1-bsc": {
        "alarm_threshold": 0.3,
        "emergency_threshold": 0.15,
    },
    "liquidator-1-base": {
        "alarm_threshold": 0.03,
        "emergency_threshold": 0.015,
    },
    "order-1-base": {
        "alarm_threshold": 0.03,
        "emergency_threshold": 0.015,
    },
    "position-1-base": {
        "alarm_threshold": 0.03,
        "emergency_threshold": 0.015,
    },
    "price-1-base": {
        "alarm_threshold": 0.03,
        "emergency_threshold": 0.015,
    },
}


class KeepersStats(BaseCog):
    def __init__(self):
        super().__init__()
        self.user_rate_limit = False
        self.allowed_channels = {
            'w3n': ['bot-local'],
            'Morphex': ['keepers', '🤖│keepers'],
        }

        self.tag_alarm = "<@&933897653757034598>" # developers
        self.tag_emergency = "<@&892431894761861161> <@&933897653757034598>" # devs and mods
        self.idm = "<@761222249176629259>" # idm

        self.status_period = 60 # minutes between status updates
        self.alarm_period = 5 # minutes between repeating alarms

        self.alarm_pause = 0
        self.elapsed = 0
        self.cooldown = 0

        self.previous_balances = {}
        self.channel = None

    @commands.command()
    async def keepers(self, ctx, command=None):
        # ensure this command is only used in the keepers channel
        if not await self.is_allowed(ctx=ctx):
            return

        if command == "daily":
            working_msg = await ctx.send(f"Working...")
            await ctx.reply(daily_report())
            await working_msg.delete()
            self.logger.info(f"Daily report sent")
        elif command == "weekly":
            working_msg = await ctx.send(f"Working...")
            await ctx.reply(weekly_report())
            # await self.get_weekly_report_embed()
            await working_msg.delete()
            self.logger.info(f"Weekly report sent")
        elif command == "quiet":
            quiet_time = 60 # minutes
            self.alarm_pause = quiet_time
            await ctx.reply(f"Alarm paused for {quiet_time} minutes")
            self.logger.info(f"Alarm paused for {quiet_time} minutes")
        elif command == "balances":
            balances = get_balances()
            balances_embed = self.get_balances_embed(balances=balances)
            await ctx.send(embed=balances_embed)
            self.logger.info(f"Balances sent")
        else:
            buf = "```\n"
            buf += "usage: f.keepers <command> [args]\n\n"
            buf += "commands:\n\n"
            buf += "- daily:    daily gas report\n"
            buf += "- weekly:   weekly gas report\n"
            buf += "- quiet:    tags off for 60 mins\n"
            buf += "- balances: view current balances\n"
            buf += "```"
            await ctx.reply(buf)

    def get_balances_embed(self, balances):
        embed = discord.Embed(
            title="Keepers: OK",
            colour=discord.Color.blue()
        )

        buf = []
        for name, values in balances.items():
            if name in self.previous_balances:
                delta = values["balance"] - self.previous_balances[name]["balance"]
            else:
                delta = 0

            if 'bsc' in name:
                report_str = f"`{values['balance']:8.2f} BNB {delta:+7.2f}` [`{name:<17}`](https://bscscan.com/address/{values['address']})"
            elif 'base' in name:
                report_str = f"`{values['balance']:8.2f} ETH {delta:+7.2f}` [`{name:<17}`](https://base.blockscout.com/address/{values['address']})"
            else:
                report_str = f"`{values['balance']:8.2f} FTM {delta:+7.2f}` [`{name:<17}`](https://ftmscan.com/address/{values['address']})"
            buf.append(report_str)

        embed.description = "\n".join(buf)
        update_time = balances["price-1"]["timestamp"]
        embed.set_footer(text=f"Balances updated at: {update_time}")

        return embed

    async def get_weekly_report_embed(self, ctx):
        embed = discord.Embed(
            title="Weekly Report",
            colour=discord.Color.blue()
        )

        fh, fd, filename = self.get_plot("Gas per day", ts, duration=duration, yaxis="safe_gwei")
        embed.set_image(url=f"attachment://{filename}")
        await ctx.send(file=fh, embed=embed)

    async def send_alarm_if_necessary(self, balances):
        if self.cooldown > 0:
            return

        embed = discord.Embed(
            colour=discord.Color.red()
        )

        send_alarm = False

        if balance_below_alarm_threshold(balances):
            send_alarm = True
            alarm_msg = f"{self.tag_alarm} Keepers are low"
            embed.title = "Keepers: Low Balance"

        if balance_below_emergency_threshold(balances):
            send_alarm = True
            alarm_msg = f"{self.tag_emergency} **Urgent** Keepers are low"
            embed.title = "Keepers: Urgent Low Balance"

        if send_alarm:
            self.cooldown = self.alarm_period

            if self.alarm_pause == 0:
                await self.channel.send(alarm_msg)
            else:
                self.logger.info(f"Alarm silenced; paused for {self.alarm_pause} minutes")

            for name, values in balances.items():
                if values["balance"] < keepers_list[name]["alarm_threshold"]:
                    if 'bsc' in name:
                        value = f"[`{values['address']}`](https://bscscan.com/address/{values['address']})\n`{values['balance']}` BNB"
                    if 'base' in name:
                        value = f"[`{values['address']}`](https://base.blockscout.com/address/{values['address']})\n`{values['balance']}` ETH"
                    else:
                        value = f"[`{values['address']}`](https://ftmscan.com/address/{values['address']})\n`{values['balance']}` FTM"

                    embed.add_field(
                        name=f"{name}",
                        value=value,
                        inline=False
                    )

            update_time = balances["price-1"]["timestamp"]
            embed.set_footer(text=f"Balances updated at: {update_time}")

            await self.channel.send(embed=embed)
            return True

    def is_new_epoch(self):
        return self.elapsed % self.status_period == 0

    async def check_balances(self):
        balances = get_balances()
        alarm_was_sent = await self.send_alarm_if_necessary(balances)

        # run every "status_period" minutes
        if self.is_new_epoch():
            balances_embed = self.get_balances_embed(balances=balances)

            if alarm_was_sent:
                balances_embed.title = "Keepers: Alarm was sent"

            await self.channel.send(embed=balances_embed)
            self.previous_balances = copy.deepcopy(balances)

        # run at midnight
        if is_midnight():
            await self.channel.send(daily_report())
            await self.channel.send(weekly_report())
            await asyncio.sleep(1)

    def tick(self):
        if self.alarm_pause > 0:
            self.alarm_pause -= 1

        if self.cooldown > 0:
            self.cooldown -= 1

        self.elapsed += 1

    async def run_loop(self, client):
        "run the keepers loop, which sends reports periodically"
        self.channel = await client.fetch_channel(self.config["keepers_channel_id"])

        error_count = 0
        while True:
            try:
                await self.check_balances()
                self.tick()
                error_count = 0
            except Exception as e:
                if error_count < 5:
                    embed = discord.Embed(
                        title="Keepers: Monitor Error",
                        description=f"{self.idm} check logs for details",
                        colour=discord.Color.red()
                    )
                    await self.channel.send(embed=embed)
                error_count += 1
                self.logger.error(f"keepers_loop: Error '{e}', count={error_count}")

            await asyncio.sleep(60)


def is_midnight():
    "run true when it is midnight"
    current_time = time.localtime()
    return current_time.tm_hour == 0 and current_time.tm_min == 0

def balance_below_emergency_threshold(keeper_data):
    for name, values in keeper_data.items():
        if values["balance"] < keepers_list[name]["emergency_threshold"]:
            return True

def balance_below_alarm_threshold(keeper_data):
    for name, values in keeper_data.items():
        if values["balance"] < keepers_list[name]["alarm_threshold"]:
            return True

def get_balances():
    balances = {}

    for keeper_name in keepers_list:
        keeper = Keeper.find(name=keeper_name)
        latest = keeper.balances.order_by(KeeperBalance.timestamp.desc()).first()
        balances[keeper_name] = {
            "address": keeper.address,
            "balance": latest.balance,
            "timestamp": latest.timestamp.astimezone(datetime.timezone.utc),
        }
    
    return balances

def get_use_since_time(start_time, chain):
    keeper_stats = {}

    for keeper in Keeper.query().filter(Keeper.chain.has(name=chain)).all():
        balances = keeper.balances.filter(KeeperBalance.timestamp >= start_time).order_by(KeeperBalance.timestamp).all()
        balance_values = [b.balance for b in balances]
        deltas = rolling_difference(balance_values)
        keeper_stats[keeper.name] = sum([abs(v) for v in deltas if v < 0])

    return keeper_stats

def render_report(days):
    buf = "```\n"

    for chain in ['ftm', 'bsc']:
        now = datetime.datetime.now()
        then = now - datetime.timedelta(days=days)
        keeper_stats = get_use_since_time(then, chain=chain)
        total = sum(keeper_stats.values())

        if chain == 'ftm':
            gas_token = "FTM"
        elif chain == 'bsc':
            gas_token = "BNB"
        elif chain == 'base':
            gas_token = "ETH"

        buf += f"{days}-day {chain.upper()} Keepers Report\n"
        buf += f"From: {then.strftime('%Y-%m-%d %H:%M')}\n"
        buf += f"To  : {now.strftime('%Y-%m-%d %H:%M')}\n"
        buf += "----------------------------------\n"
        for keeper, balance in keeper_stats.items():
            buf += f"{keeper:<20s}: {balance:>8.2f} {gas_token}\n"
        buf += "==================================\n"
        buf += f"Total               : {total:>8.2f} {gas_token}\n"
        buf += "\n"

    buf += "```"

    return buf

def daily_report():
    "Create a daily report of the keepers stats"
    return render_report(days=1)

def weekly_report():
    "Create a weekly report of the keepers stats"
    return render_report(days=7)

def rolling_difference(lst):
    diffs = []
    for i in range(1, len(lst)):
        diff = lst[i] - lst[i-1]
        diffs.append(diff)
    return diffs
