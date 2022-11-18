import discord 
import os
from discord.ext import commands
bot = commands.Bot(command_prefix="!",description="bot test")
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  else:
    await message.channel.send(f"> {message.content}  \n une citation de {message.author}")
    await bot.process_commands(message)

    
@bot.event
async def on_message_delete(message):
  discord
  await message.channel.send(f"Le message  '{message.content}' \n ecrite par @{message.author} a ete suprimmé")


@bot.event
async def on_group_join(channel, user):
  channel.send(f"**@{user}** \n a **quitte** le channel *{channel}*")