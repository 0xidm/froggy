import re

import discord

from . import MorphexHandler

class AutomodRpcHandler(MorphexHandler):

    async def check(self, message:discord.Message):
        return re.search(r"site.+slow|load.+slow|wallet.+not.+work|submit.+transaction", message.content.lower())

    async def respond(self, message):
        embed = discord.Embed(
            title=f"How to fix your Fantom RPC",
            description="Your wallet talks to a server called an RPC to interact with the blockchain. If you are getting error messages, it may be that your RPC is having trouble. One possible fix is to change your RPC to a different one.",
            colour=discord.Color.blue(),
        )

        embed.add_field(
            name="The problem with overloaded RPC servers",
            value="What do you think happens if everyone tries to use the same RPC at the same time? Well.... nothing good! As more users try to send transactions through the same RPC, the server can slow down, or worse.",
            inline=False)

        embed.add_field(
            name="How to find a new RPC",
            value="ChainlistInfo has nice list of Fantom RPCs to choose from: https://chainlist.xyz/?search=FTM By clicking on the down arrow under 'Connect Wallet', you will be able to view different RPCs for the $FTM network! Users usually set this up the very first time connecting to a new network, then treat it as a 'set and forget' setting, but this can lead to poor User Experience!",
            inline=False)

        embed.add_field(
            name="Obtaining an RPC from SakuraRPC",
            value="Our friends at Sakura RPC also have a solution you can evaluate. https://www.sakurarpc.io/",
            inline=False)

        embed.add_field(
            name="How to add a custom network RPC to Metamask",
            value="Each wallet has a different way of adding a custom RPC. Here is a guide for Metamask: https://metamask.zendesk.com/hc/en-us/articles/360015489331-How-to-add-a-custom-Network-RPC",
            inline=False)

        return await message.channel.send(embed=embed)


class AutomodGasPriceHandler(MorphexHandler):

    async def check(self, message:discord.Message):
        return re.search(r"transaction.+fail|tx.*fail|fail.+tx|fail.+transaction|revert", message.content.lower())

    async def respond(self, message):
        embed = discord.Embed(
            title=f"Changing gas price can help your transactions go through",
            description="Whenever there are an unusually large number of transactions on the blockchain, this leads to increased gas prices and contributes to user frustration when transactions don't go through.",
            colour=discord.Color.blue(),
        )

        embed.add_field(
            name="Why does gas price matter?",
            value="In order to prioritize the transactions, each transaction on a blockchain has a 'gas fee' that is paid to confirm the transaction. When a large number of people are using a network, gas prices can increase significantly. Without the appropriate gas price on your transactions, your transaction will be lower priority than transactions that pay a higher price for gas, leading to a very long wait for transaction validation.",
            inline=False)

        embed.add_field(
            name="How do you know what is the right amount of gas to use for each transaction?",
            value="Gas price depends on how much each user decides to use - so you can look at current network usage to determine how much people are currently paying for gas. A tool like https://ftmscan.com can help you see what the current gas price is, and you can use this to determine how much gas to use for your transactions.",
            inline=False)

        embed.add_field(
            name="How to change gas prices on MetaMask?",
            value="On MetaMask, gas is automatically calculated for you when submitting a transaction. In order to have more control, you may click 'Market' and select a higher amount of gas. See the MetaMask guide for more information: https://support.metamask.io/hc/en-us/articles/360022895972",
            inline=False)

        embed.add_field(
            name="Gas Price Summary",
            value="When faced with transaction issues - check https://ftmscan.com to see whether the current gas price is sufficient for your transaction. If not, you can increase the gas price on your transaction to ensure that it is confirmed quickly.",
            inline=False)

        return await message.channel.send(embed=embed)

class AutomodMLPFaqHandler(MorphexHandler):
    async def check(self, message:discord.Message):
        return re.search(r"how.+mlp calculate|how.+mlp price|", message.content.lower())

    async def respond(self, message):
        embed = discord.Embed(
            title=f"MLP Prices",
            description=mlp_description,
            colour=discord.Color.blue(),
        )
        return await message.channel.send(embed=embed)


mlp_description = """The index price is calculated as a combination of stables, FTM, ETH, and BTC. Let's assume the index displayed is 48%% stables and 25%% FTM, 13.5%% ETH and 13.5%% BTC. This index is rebalanced to these perfect weights daily and is to serve as a benchmark.

In contrast to the index, MLP does not have daily rebalances. When we rebalance, MLP does not directly adjust to that by swapping assets in the index for each other, this rebalancing only changes the target weights, which influence what kind of fee users will pay for minting/redeeming MLP, as well as regular spot swaps.

In essence, this incentivizes users to bring the assets in the index closer to their targets, but in reality the weights differ. These weights can actually vary quite a bit throughout the day, changing a few %% during very volatile periods of time, since we have good aggregator volume coming through us where people swap one asset for the other.

During a recent market drop, we saw on the most volatile days that people were selling some crypto for stables, which means MLP would take their crypto and give out the stables, increasing crypto exposure.
"""
