import logging
import os
import sys

import discord
from discord.ext import commands
import dotenv

import json
from datetime import datetime
from discord import app_commands

# Load variables from .env file
dotenv.load_dotenv()

# Configure logging
LOG_LVL = os.getenv('LOG_LVL')
log = logging.getLogger(__name__)
if not LOG_LVL:
    LOG_LVL = 'DEBUG'

log = logging.getLogger(__name__)
h = logging.StreamHandler(sys.stdout)
h.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log.addHandler(h)
log.setLevel(LOG_LVL)


# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')

#Create client
class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()


intents = discord.Intents.default()
client = Bot(intents=intents)

if not TOKEN:
    log.error('`DISCORD_TOKEN` must be set in .env file')
    sys.exit()


# Create bot
intents = discord.Intents.none()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)
#bot.remove_command('help')


@bot.event
async def on_ready():
    log.info('Bot logged in as `%s` (id %s)', bot.user, bot.user.id)
    log.info('Member of the following servers/guilds:')
    for guild in bot.guilds:
        log.info('  %s', guild.name)

#Bot commands

#Simple commands
@bot.command(name='hello', aliases=['yo'], help='hello world test command')
async def helloworld(ctx):
    await ctx.send(f"Greetings {ctx.author.name}, how may I assist you today?")

@bot.command(name='support', aliases=['wtf'], help='hello world test command')
async def support(ctx):
    await ctx.send(f"{ctx.author.name}, I hope this soothes your pain :3")
    await ctx.send(f"Here is the help list:\n 1. Use ! for commands \n 2. Use !help for a list of all commands \n 3. Use !hello or !yo for a greeting \n 4. Use !nuke [Coordinates] to send a present to someones location \n 5. Remember to be silly :3")

#Advanced commands

#location tracker
def get_file_data():
    with open('loc.json', 'r') as f:
        data = json.load(f)
    return data

def write_file_data(data):
    with open('loc.json', 'w') as f:
        json.dump(data, f)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print('--------------')


@client.tree.command()
async def storeloc(interaction: discord.Interaction, coordinates: str):
    uid = str(interaction.user.id)

    time = datetime.now().timestamp()
    current_loc = {"time": time,
    "coordinates" : coordinates.replace(" ", "")
    }

    data = get_file_data()
    if uid in data:
        data[uid].append(current_loc)
    else :
        data[uid] = [current_loc]
    write_file_data(data)

    await interaction.response.send_message(f"Location stored successfully : {coordinates} ")

def get_map_url(locations):
    SEARCH_URL = "https://www.google.com/maps/search/?api=1&query="
    DIRECTIONS_URL = " https://www.google.com/maps/dir/?api=1&"
    if len(locations) == 1:
        return f"{SEARCH_URL}{locations[0]['coordinates']}"

    if len(locations) == 2:
        return f"{DIRECTIONS_URL}origin={locations[0]['coordinates']}&destination={locations[1]['coordinates']}"

    if len(locations) > 2:
        origin = locations[0]['coordinates']
        destination = locations[-1]['coordinates']
        waypoints = []
        for location in locations[1:-1]:
            waypoints.append(location['coordinates'])
        waypoints_url = "|".join(waypoints)
        print(waypoints)
        return f"{DIRECTIONS_URL}origin={origin}&destination={destination}&waypoints={waypoints_url}"



@client.tree.command()
async def getloc(interaction: discord.Interaction, user: discord.Member):

    uid = str(user.id)

    data = get_file_data()

    try: 
        locations = data[uid]
        if not locations:
            raise KeyError
        print(locations)
        url = get_map_url(locations)

        await interaction.response.send_message(url)
    except KeyError as e:
        await interaction.response.send_message(f'User {user.name} has not registered any location')


@client.tree.command()
async def purge(interaction: discord.Interaction):

    uid = str(interaction.user.id)

    data = get_file_data()

    if uid in data:
        data[uid] = []

    write_file_data(data)

    await interaction.response.send_message(f"Locations for user {interaction.user.name} successfully deleted")

#@bot.command(name='help')
#async def help(ctx):
#
#    about_text = ('A Python Discord template-bot, '
#                 'demonstrating how to write a bot.')
#
#    embed = discord.Embed(colour = discord.Colour.blue())
#    embed.set_author(name='Help')
#    embed.add_field(name='About', value=about_text, inline=False)
#                          
#    embed.add_field(name='`!hello` | `!yo`',
#                    value=('hello world test command.',
#                    inline=False))
#
#    await ctx.send(embed=embed)

# Start bot
try:
    bot.run(TOKEN)
except discord.errors.LoginFailure:
    log.error('Bot login failed, improper/invalid token')
    sys.exit()
