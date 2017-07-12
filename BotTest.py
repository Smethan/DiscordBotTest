import discord
from discord.ext.commands import Bot
my_bot = Bot(command_prefix="!")
Client = discord.Client()
@my_bot.event
async def on_read():
    print("Client logged in")
@my_bot.command()
async def hello(*args):
    return await my_bot.say("Hello, world!")
my_bot.run("MzM0Nzk2ODU2MDQxNDA2NDY0.DEglSw.lO2uWavgkzQnWvarkqk5_P04nQk")