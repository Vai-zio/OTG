# File: bot.py
"""Discord bot with prefix and slash commands; fixed DEV_GUILD_ID handling and single on_ready."""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import dotenv
import discord
from discord import Object
from discord.ext import commands
from discord import app_commands
import random
import asyncio


# Load .env
dotenv.load_dotenv()

# Logging
LOG_LVL = os.getenv("LOG_LVL", "DEBUG")
log = logging.getLogger(__name__)
h = logging.StreamHandler(sys.stdout)
h.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
log.addHandler(h)
# convert string level to numeric if needed
try:
    log.setLevel(getattr(logging, LOG_LVL.upper()))
except Exception:
    log.setLevel(logging.DEBUG)

# Environment (token required)
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    log.error("`DISCORD_TOKEN` must be set in .env file")
    sys.exit(1)

# DEV_GUILD_ID: optional, convert to int if present and valid
DEV_GUILD_ID: Optional[int] = None
dev_gid_raw = os.getenv("DEV_GUILD_ID")
if dev_gid_raw:
    try:
        DEV_GUILD_ID = int(dev_gid_raw)
    except ValueError:
        log.error("DEV_GUILD_ID in .env must be an integer if set; ignoring it.")
        DEV_GUILD_ID = None

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

LOC_FILE = Path("loc.json")


def ensure_loc_file() -> None:
    if not LOC_FILE.exists():
        LOC_FILE.write_text(json.dumps({}), encoding="utf-8")


def get_file_data() -> dict:
    ensure_loc_file()
    with LOC_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def write_file_data(data: dict) -> None:
    ensure_loc_file()
    with LOC_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_map_url(locations: list[dict]) -> str:
    SEARCH_URL = "https://www.google.com/maps/search/?api=1&query="
    DIRECTIONS_URL = "https://www.google.com/maps/dir/?api=1&"
    if not locations:
        return ""
    if len(locations) == 1:
        return f"{SEARCH_URL}{locations[0]['coordinates']}"
    if len(locations) == 2:
        return f"{DIRECTIONS_URL}origin={locations[0]['coordinates']}&destination={locations[1]['coordinates']}"
    origin = locations[0]["coordinates"]
    destination = locations[-1]["coordinates"]
    waypoints = [loc["coordinates"] for loc in locations[1:-1]]
    waypoints_url = "|".join(waypoints)
    return f"{DIRECTIONS_URL}origin={origin}&destination={destination}&waypoints={waypoints_url}"


class MyBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=["!","?","+","-"], intents=intents)

    async def setup_hook(self) -> None:
        # Sync app (slash) commands on startup.
        await self.tree.sync()
        log.debug("App command tree synced.")


bot = MyBot(intents=intents)


@bot.event
async def on_ready():
    # single consolidated on_ready
    log.info("Bot logged in as `%s` (id %s)", bot.user, bot.user.id)
    log.info("Member of the following servers/guilds:")
    for guild in bot.guilds:
        log.info("  %s", guild.name)

    # diagnostic output
    print(f"READY: running bot instance {bot!r}")
    print("Prefix commands loaded:", [c.name for c in bot.commands])
    app_cmds = []
    for c in bot.tree.walk_commands():
        app_cmds.append((c.name, getattr(c, "description", "")))
    print("App (slash) commands in tree:", app_cmds)

    # If DEV_GUILD_ID provided, fetch API-side commands for that guild only
    if DEV_GUILD_ID is not None:
        try:
            guild_obj = Object(id=DEV_GUILD_ID)
            commands_on_api = await bot.tree.fetch_commands(guild=guild_obj)
            print("API-side slash commands for dev guild:", [(c.name, c.id) for c in commands_on_api])
        except Exception as exc:
            log.error("Failed to fetch API-side commands for DEV_GUILD_ID=%s: %s", DEV_GUILD_ID, exc)
    else:
        print("DEV_GUILD_ID not set; skipping fetch of API-side guild commands.")
    print("Local tree.walk_commands:", [(c.name, c.description) for c in bot.tree.walk_commands()])


@bot.event
async def on_message(message: discord.Message):
    # ignore self
    if message.author.id == bot.user.id:
        return
    print("MSG:", message.author, message.channel, repr(message.content))
    await bot.process_commands(message)


# ----------------
# Prefix commands
# ----------------
@bot.command(name="greet", aliases=["yo"])
async def helloworld(ctx: commands.Context):
    await ctx.send(f"Greetings {ctx.author.name}, how may I assist you today?")


@bot.command(name="support", aliases=["wtf"])
async def support(ctx: commands.Context):
    await ctx.send(f"{ctx.author.name}, I hope this soothes your pain :3")
    await ctx.send(
        "Here is the help list:\n"
        " 1. Use ! for prefix commands \n"
        " 2. Use / for slash commands \n"
        " 3. Use !hello or !yo for a greeting \n"
        " 4. Use /storeloc and /getloc for location features \n"
        " 5. Remember to be silly :3"
    )
@bot.command(name="gay", aliases=["startgame","c","hello", "hi", "hai"])
async def gay(ctx: commands.Context):
    await ctx.send(f"Greetings {ctx.author.name}, how may I assist you today?")
#if discord.Interaction:
    await ctx.send("https://tenor.com/view/astolfo-blink-gay-men-trap-gif-8514447830464686723")
# ----------------
# Slash / app commands
# ----------------

@bot.tree.command(name="guess", description="Play a guessing game (slash).")
async def guess(interaction: discord.Interaction):
    # Prompt the user to provide the upper limit
    await interaction.response.send_message(
        "🎯 Send me the **maximum number** for the guessing range (e.g. `10`). You have 20s.",
        ephemeral=True,  # optional: only the user sees the prompt
    )

    def check_limit(m: discord.Message):
        return m.author.id == interaction.user.id and m.channel == interaction.channel

    try:
        # Wait for the user's message that sets the limit
        limit_msg = await bot.wait_for("message", check=check_limit, timeout=20.0)
        limit = int(limit_msg.content.strip())
        if limit <= 0:
            await interaction.followup.send("⚠️ Please provide a positive integer greater than zero.")
            return

        target = random.randint(0, limit)
        await interaction.followup.send(
            f"✅ Great — I picked a number between 0 and {limit}. Send your guess (you have 20s)."
        )

        def check_guess(m: discord.Message):
            return m.author.id == interaction.user.id and m.channel == interaction.channel
        msg_count = 0
        while True:
                try:
                    guess_msg = await bot.wait_for("message", check=check_guess, timeout=20.0)
                    guess_val = int(guess_msg.content.strip())
                    msg_count += 1
                    print("msg_count:", msg_count)
                    if guess_val == target:
                        await interaction.followup.send(f"🎉 Correct — the number was {target}!")
                        await interaction.followup.send(f"You took {msg_count} times to guess the number")
                        break
                    else:
                        if guess_val > target:
                            await interaction.followup.send(
                                f"❌ Nope, {guess_val} is greater than it. Try again — you still have time!"
                            )
                        elif guess_val < target:
                            await interaction.followup.send(
                            f"❌ Nope, {guess_val} is lesser than it. Try again — you still have time!"
                            )

                except asyncio.TimeoutError:
                    await interaction.followup.send("⏰ Time’s up! You didn’t guess in time.")
                    break
                except ValueError:
                    await interaction.followup.send("⚠️ Please type a number!")
    except asyncio.TimeoutError:
        await interaction.followup.send("⏰ You never set a limit. Game cancelled.")
    except ValueError:
        await interaction.followup.send("⚠️ Invalid limit — not a number.")


@bot.tree.command(name="storeloc", description="Store your current coordinates or address")
@app_commands.describe(coordinates="Coordinates (e.g. 55.6761,12.5683 or an address)")
async def storeloc(interaction: discord.Interaction, coordinates: str):
    uid = str(interaction.user.id)
    time = datetime.now().timestamp()
    current_loc = {"time": time, "coordinates": coordinates.replace(" ", "")}
    data = get_file_data()
    if uid in data:
        data[uid].append(current_loc)
    else:
        data[uid] = [current_loc]
    write_file_data(data)
    await interaction.response.send_message(f"Location stored successfully: {coordinates}")


@bot.tree.command(name="getloc", description="Get a user's stored locations (you can mention a user)")
@app_commands.describe(user="Member to look up")
async def getloc(interaction: discord.Interaction, user: discord.Member):
    uid = str(user.id)
    data = get_file_data()
    try:
        locations = data[uid]
        if not locations:
            raise KeyError
        url = get_map_url(locations)
        await interaction.response.send_message(url)
    except KeyError:
        await interaction.response.send_message(f"User {user.name} has not registered any location")


@bot.tree.command(name="purge", description="Delete your stored locations")
async def purge(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    data = get_file_data()
    if uid in data:
        data[uid] = []
        write_file_data(data)
        await interaction.response.send_message(f"Locations for user {interaction.user.name} successfully deleted")
    else:
        await interaction.response.send_message("You had no stored locations.")


if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        log.error("Bot login failed, improper/invalid token")
        sys.exit(1)
