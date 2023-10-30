import re

import discord

from . import MorphexHandler

class ContractsHandler(MorphexHandler):

    async def check(self, message):
        return re.search(r'contract address|token address|mpx address|mlp address|token contract|mpx contract|mlp contract', message.content.lower())

    async def respond(self, message):
        embed = discord.Embed(
            title=f"Contract Addresses",
            colour=discord.Color.blue(),
        )

        embed.add_field(name="MPX Token", value=f"[0x66eEd5FF1701E6ed8470DC391F05e27B1d0657eb](https://ftmscan.com/address/0x66eEd5FF1701E6ed8470DC391F05e27B1d0657eb)", inline=False)
        embed.add_field(name="esMPX Token", value=f"[0xe0f606e6730bE531EeAf42348dE43C2feeD43505](https://ftmscan.com/address/0xe0f606e6730bE531EeAf42348dE43C2feeD43505)", inline=False)
        embed.add_field(name="MLP Token", value=f"[0xd5c313DE2d33bf36014e6c659F13acE112B80a8E](https://ftmscan.com/address/0xd5c313DE2d33bf36014e6c659F13acE112B80a8E)", inline=False)
        embed.add_field(name="sMPX (Tracker)", value=f"[0xa4157E273D88ff16B3d8Df68894e1fd809DbC007](https://ftmscan.com/address/0xa4157E273D88ff16B3d8Df68894e1fd809DbC007)", inline=False)
        embed.add_field(name="sMPX (Distributor)", value=f"[0x05D97A8a5eF11010a6A5f89B3D4628ce43092614](https://ftmscan.com/address/0x05D97A8a5eF11010a6A5f89B3D4628ce43092614)", inline=False)
        embed.add_field(name="sbMPX (Tracker)", value=f"[0xa2242d0A8b0b5c1A487AbFC03Cd9FEf6262BAdCA](https://ftmscan.com/address/0xa2242d0A8b0b5c1A487AbFC03Cd9FEf6262BAdCA)", inline=False)
        embed.add_field(name="sbMPX (bonusDistributor)", value=f"[0x06c35893Ba9bc454e12c36F4117BC99f75e34346](https://ftmscan.com/address/0x06c35893Ba9bc454e12c36F4117BC99f75e34346)", inline=False)
        embed.add_field(name="sbfMPX (Tracker)", value=f"[0x2D5875ab0eFB999c1f49C798acb9eFbd1cfBF63c](https://ftmscan.com/address/0x2D5875ab0eFB999c1f49C798acb9eFbd1cfBF63c)", inline=False)
        embed.add_field(name="sbfMPX (Distributor)", value=f"[0x1d556F411370E5F1850A51EB66960798e6F5eDeC](https://ftmscan.com/address/0x1d556F411370E5F1850A51EB66960798e6F5eDeC)", inline=False)
        embed.add_field(name="fMLP (Tracker)", value=f"[0xd3C5dEd5F1207c80473D39230E5b0eD11B39F905](https://ftmscan.com/address/0xd3C5dEd5F1207c80473D39230E5b0eD11B39F905)", inline=False)
        embed.add_field(name="fMLP (Distributor)", value=f"[0x7724dfE8E461C59F5017d9A0eB510dD0e2d61eDC](https://ftmscan.com/address/0x7724dfE8E461C59F5017d9A0eB510dD0e2d61eDC)", inline=False)
        embed.add_field(name="fsMLP (Tracker)", value=f"[0x49A97680938B4F1f73816d1B70C3Ab801FAd124B](https://ftmscan.com/address/0x49A97680938B4F1f73816d1B70C3Ab801FAd124B)", inline=False)
        embed.add_field(name="fsMLP (Distributor)", value=f"[0x7278Ab8dEAe0b9e9408354CE1b82F004F59128a9](https://ftmscan.com/address/0x7278Ab8dEAe0b9e9408354CE1b82F004F59128a9)", inline=False)
        embed.add_field(name="MPXVester", value=f"[0x8753a83c928939F86341251d7DFAd8cf5471410c](https://ftmscan.com/address/0x8753a83c928939F86341251d7DFAd8cf5471410c)", inline=False)
        embed.add_field(name="MLPVester", value=f"[0xdBa3A9993833595eAbd2cDE1c235904ad0fD0b86](https://ftmscan.com/address/0xdBa3A9993833595eAbd2cDE1c235904ad0fD0b86)", inline=False)
        #embed.add_field(name="", value=f"[](https://ftmscan.com/address/)", inline=False)

        # embed.add_field(name="explorer", value=f"[ftmscan.com](https://ftmscan.com/token/0x66eed5ff1701e6ed8470dc391f05e27b1d0657eb)", inline=False)

        # embed.set_thumbnail(url="https://assets.coingecko.com/coins/images/28965/small/mpx_logo_256.png?1675744910")

        return await message.channel.send(embed=embed)
