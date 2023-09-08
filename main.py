#Dev By sirrsina
#IG : @sirrsina
#Telegram : @sirrsina
#Discord : @vlww
#Second Acc Discord : @vlwu
import discord
from discord.ext import commands, tasks
import asyncio
from discord.ui import Button, button, View
import chat_exporter
import time
import os
from queue import Queue
from discord import Embed
import random
from discord.ext.commands import has_permissions
import threading
import requests
import json
import sys
import traceback
import re
import json
import os
from discord import Client, Intents
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', description='Commands', intents=intents, case_insensitive=True)

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           command_signature = [self.get_command_signature(c) for c in commands]
           if command_signature :
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signature), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()

#Status-Chanegr--------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

   
    @tasks.loop(seconds=3)
    async def change_status():
        await asyncio.sleep(1)
        await bot.change_presence(status=discord.Status.online)
        await asyncio.sleep(1)
        await bot.change_presence(status=discord.Status.dnd)
        await asyncio.sleep(1)
        await bot.change_presence(status=discord.Status.idle)
    
   
    change_status.start()

#Join-Voice---------------------------------------------------------------------------------------------
    channel_id = 1143158871150579743

    @tasks.loop(seconds=3)
    async def change_status():
        voice_channel = bot.get_channel(channel_id)
        if voice_channel and isinstance(voice_channel, discord.VoiceChannel):
            if not voice_channel.guild.voice_client:
                await voice_channel.connect()

    change_status.start()



#Embed---------------------------------------------------------------------------------------------
@bot.command()
async def embed(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author
    name = member.display_name
    embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙-BOT", description="Dev by @vlww (sirrsina)", color=discord.Color.random())
    embed.set_author(name=f"{name}", url="https://discord.gg/r9695HhGHb", icon_url="https://cdn.discordapp.com/icons/1009505066014744756/a_e508b28b4fe64b2750e43201b565c383.gif?size=1024")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1009505066014744756/a_e508b28b4fe64b2750e43201b565c383.gif?size=1024")
    # embed.add_field(name='RULES', value="")
    embed.add_field(name='Update', value="Bad words option fixed.")
    # embed.add_field(name='This is 1 field', value="this is inline False", inline=False)
    embed.set_footer(text=f"{name} Made this embed")
    await ctx.send(embed=embed)
#Ticket---------------------------------------------------------------------------------------------
async def get_transcript(member: discord.Member, channel: discord.TextChannel):
    export = await chat_exporter.export(channel=channel)
    file_name=f"{member.id}.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(export)

def upload(file_path: str, member_name: str):
    github = Github(bot.run)
    repo = github.get_repo("ayush-py-dev/ticket")
    file_name = f"{int(time.time())}"
    repo.create_file(
        path=f"tickets/{file_name}.html",
        message="Ticket Log for {0}".format(member_name),
        branch="main",
        content=open(f"{file_path}","r",encoding="utf-8").read()
    )
    os.remove(file_path)

    return file_name


async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color):
    log_channel = guild.get_channel(1147601501989114028)
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    await log_channel.send(embed=embed)

class CreateButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Create Ticket",style=discord.ButtonStyle.blurple, emoji="🎫",custom_id="ticketopen")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=1113161257017692210)
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!":
                await interaction.followup.send("You already have a ticket in {0}".format(ch.mention), ephemeral=True)
                return

        r1 : discord.Role = interaction.guild.get_role(1067183055552397373)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await category.create_text_channel(
            name=str(interaction.user),
            topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
            overwrites=overwrites
        )
        await channel.send(
            embed=discord.Embed(
                title="Ticket Created!",
                description="Don't ping a support-team member, they will be here soon.",
                color = discord.Color.green()
            ),
            view = CloseButton()
        )
        await interaction.followup.send(
            embed= discord.Embed(
                description = "Created your ticket in {0}".format(channel.mention),
                color = discord.Color.blurple()
            ),
            ephemeral=True
        )

        await send_log(
            title="Ticekt Created",
            description="Created by {0}".format(interaction.user.mention),
            color=discord.Color.green(),
            guild=interaction.guild
        )
        


class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Close the ticket",style=discord.ButtonStyle.red,custom_id="closeticket",emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)



        await asyncio.sleep(0.0)

        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id = 1113161257017692210)
        r1 : discord.Role = interaction.guild.get_role(1067183055552397373)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await interaction.channel.edit(category=category, overwrites=overwrites)
        await interaction.channel.send(
            embed= discord.Embed(
                description="Ticket Closed!",
                color = discord.Color.red()
            ),
            view = TrashButton()
        )
        member = interaction.guild.get_member(int(interaction.channel.topic.split(" ")[0]))
        await get_transcript(member=member, channel=interaction.channel)
        file_name = upload(f'{member.id}.html',member.name)
        link = f"{file_name}"
        await send_log(
            title="Ticket Closed",
            description=f"Closed by: {interaction.user.mention}\n[click for transcript]({link})",
            color=discord.Color.yellow(),
            guild=interaction.guild
        )
    

class TrashButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Delete the ticket", style=discord.ButtonStyle.red, emoji="🚮", custom_id="trash")
    async def trash(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        await interaction.channel.send(embed = discord.Embed(title="", description="Closing this ticket in 5 seconds.", color=discord.Color.random()))
        await asyncio.sleep(5)

        await interaction.channel.delete()
        await send_log(
                title="Ticket Deleted",
                description=f"Deleted by {interaction.user.mention}, ticket: {interaction.channel.name}",
                color=discord.Color.red(),
                guild=interaction.guild
            )

@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    await ctx.send(
        embed = discord.Embed(
            description="Press the button to create a new ticket!"
        ),
        view = CreateButton()
    )




#---------------------------------------------------------------------------------------------

@bot.command()
async def members(ctx):
    guild = ctx.guild
    total_bots = sum(1 for member in guild.members if member.bot)
    human_members = guild.member_count - total_bots
    await ctx.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f'This server have {human_members} Members', color=discord.Color.random()))

#Clear---------------------------------------------------------------------------------------------

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    try:
        message = await ctx.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙 ", description=f'Erasing {amount} messages...', color=discord.Color.random()))
        messages = await ctx.channel.purge(limit=amount)

        await message.delete()
        
    except discord.errors.NotFound:
        pass
    except Exception as e:
        print(e)

#Clear-All--------------------------------------------------------------------------------------------- 

@bot.command(name='clearall', help='Delete all messages')
@commands.has_permissions(administrator=True)
async def clearall(ctx):
    try:
        
        while True:
            
            deleted = await ctx.channel.purge(limit=1000000000000000000000000000000000000000000000000000000000000)
            if not deleted:
                break
            await asyncio.sleep(1) 
    except Exception as e:
        pass
#Welcome---------------------------------------------------------------------------------------------

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1113139522755104821)
    embed=discord.Embed(title="Welcome", description=f"{member.mention} to  the Xray-Community")
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/762023030830399529/862102999782129694/image0.gif')
    embed.set_footer(text="Made by sina")
    await channel.send(embed=embed)
#     embed.thumbnail(icon_url="https://cdn.discordapp.com/icons/1009505066014744756/a_e508b28b4fe64b2750e43201b565c383.gif?size=1024")


#Ban---------------------------------------------------------------------------------------------

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.message.delete()
    try:
        await member.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f'User banned: {reason}', color=discord.Color.random()))
    except discord.Forbidden:
        pass

#Kick---------------------------------------------------------------------------------------------

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.message.delete()
    try:
        await member.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f'The user {reason} kicked', color=discord.Color.random()))
    except discord.Forbidden:
        pass

#Mute---------------------------------------------------------------------------------------------



@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f"Muted {member.mention} for reason {reason}", color=discord.Color.random()))
    await member.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f"You were muted in the server {guild.name} for {reason}", color=discord.Color.random()))

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f"Unmuted {member.mention}", color=discord.Color.random()))
    await member.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f"You were unmuted in the server {ctx.guild.name}", color=discord.Color.random()))

#Inite-Link--------------------------------------------------------------------------------------------

@bot.command()
async def invite(ctx):
    invite = await ctx.channel.create_invite(max_uses=2)
    await ctx.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f'Invitation link: {invite}', color=discord.Color.random()))
        
#Simple-Chatgpt--------------------------------------------------------------------------------------------


@bot.command()
async def hi(ctx):
    await ctx.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description='Hi i am 𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙 and i wrote by sirrsina.', color=discord.Color.random()))
# ____________________________________________________________________________________________________________
blockedWords = [
    "kos",
    "kir",
    "کص",
    "کیر",
    "پورن",
    "پورن هاب",
    "جنده",
    "کص کش",
    "کصکش",
    "تخمم",
    "تخم",
    "کون",
    "کونی",
    "تخمی",
    "مادرت",
    "جنده",
    "گاییدم",
    "خارکصه",
    "قهبه",
    "ولدزنا",
    "مادر کصه",
    "زیرخواب",
    "porn",
    "pornhub",
    "jende",
    "koskesh",
    "kiri",
    "gaiidam",
    "koni",
    "sex",
    "سکس",
    "سکسی",
    "گی",
    "gay",
    "جوین کانال ما بشید",
    "خایه",
    "زنازاده"
]


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(x in message.content for x in blockedWords):
        await message.delete()

        user_mention = message.author.mention
        target_channel_id = 1143293212254031935 
        target_channel = bot.get_channel(target_channel_id)
        if target_channel:
            await target_channel.send(embed = discord.Embed(title="𝐑𝐀𝐒𝐓𝐀𝐊𝐇𝐈𝐙", description=f" {user_mention} send a bad word", color=discord.Color.random()))

    await bot.process_commands(message)







bot.run("")
