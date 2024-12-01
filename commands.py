import discord
import logging
from datetime import datetime
import asyncio
import random
import re
import subprocess
import os

# Define colors for logging
COLORS = {
    'YELLOW': "\033[33m",
    'GREEN': "\033[32m",
    'RESET': "\033[0m",
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = {
            'DEBUG': "\033[36m",    # Cyan
            'INFO': "\033[32m",     # Green
            'WARNING': "\033[33m",  # Yellow
            'ERROR': "\033[31m",    # Red
            'CRITICAL': "\033[41m", # White text on Red background
            'RESET': "\033[0m",     # Reset to default
        }.get(record.levelname, COLORS['RESET'])
        return f"{log_color}{super().format(record)}{COLORS['RESET']}"

# Set up logging with colored formatter
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())
logger.handlers = [handler]

async def handle_command(client, message):
    # Check if the message starts with the prefix '>'
    if not message.content.startswith('>'):
        return

    command = message.content[len(client.prefix):].strip().split()
    
    # Log the command execution with colored components
    logger.debug(f"{COLORS['RESET']}Received [{COLORS['YELLOW']}COMMAND{COLORS['RESET']}] from {COLORS['GREEN']}{message.author}{COLORS['RESET']} in {COLORS['YELLOW']}{message.guild.name}{COLORS['RESET']} - Content: '{COLORS['GREEN']}{command[0]}{COLORS['RESET']}'")

    if command[0] == 'setprefix':
        await set_prefix_command(client, message, command)
    elif command[0] == 'unbspam':
        await unbspam_command(client, message)
    elif command[0] == 'stopspam':
        await stopspam_command(client, message)
    elif command[0] == 'uptime':
        await uptime_command(client, message)
    elif command[0] == 'help':
        await help_command(client, message)
    elif command[0] == 'greet':
        await greet_command(client, message)
    elif command[0] == 'coinflip':
        await coinflip_command(client, message)
    elif command[0] == 'byebye':
        await clear_command(client, message, command)
    elif command[0] == 'calculate':
        await calculate_command(client, message, command)
    elif command[0] == 'userinfo':
        await userinfo_command(client, message)
    elif command[0] == 'serverinfo':
        await serverinfo_command(client, message)

async def set_prefix_command(client, message, command):
    if len(command) > 1:
        new_prefix = command[1]
        if len(new_prefix) == 1:
            client.prefix = new_prefix
            await message.channel.send(f"Prefix set to: `{client.prefix}`")
        else:
            await message.channel.send("Error: Prefix must be a single character.", delete_after=5)
    else:
        await message.channel.send("Usage: >setprefix <new_prefix>", delete_after=5)

async def unbspam_command(client, message):
    if not hasattr(client, "unbspam_task") or client.unbspam_task is None or client.unbspam_task.done():
        client.unbspam_task = client.loop.create_task(unbspam_task(message.channel))
        #await message.channel.send("Started spamming commands.")
    else:
        #await message.channel.send("Spam is already running.")

async def stopspam_command(client, message):
    if hasattr(client, "unbspam_task") and client.unbspam_task:
        client.unbspam_task.cancel()
        client.unbspam_task = None
        await message.channel.send("Stopped spamming commands.")
    else:
        await message.channel.send("Spam is not running.")

async def unbspam_task(channel):
    while True:
        await channel.send("!!collect")
        await asyncio.sleep(2)
        await channel.send("!!work")
        await asyncio.sleep(2)
        await channel.send("!!crime")
        await asyncio.sleep(2)
        await channel.send("!!slut")
        await asyncio.sleep(610)

async def uptime_command(client, message):
    current_time = datetime.now()
    uptime_duration = current_time - client.start_time
    days, seconds = uptime_duration.days, uptime_duration.seconds
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    uptime_message = f"Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds."
    await message.channel.send(uptime_message)

async def help_command(client, message):
    help_message = (
        "```md\n"
        "# Bot Commands\n"
        "| Command                | Description                         |\n"
        "|------------------------|-------------------------------------|\n"
        "| help                   | Prints command sheet                |\n"
        "| greet                  | Greets the user                     |\n"
        "| setprefix <new_prefix> | Sets a custom prefix                |\n"
        "| uptime                 | Displays the bot's uptime           |\n"
        "| unbspam                | Starts spamming certain commands    |\n"
        "| stopspam               | Stops the spam commands             |\n"
        "| coinflip               | Simulates a coin flip               |\n"
        "| calculate <expression> | Performs basic math (e.g., `3 + 5`) |\n"
        "| userinfo <@user>       | Displays user info                  |\n"
        "| serverinfo             | Displays server info                |\n"
        "```"
    )
    await message.channel.send(help_message)

async def greet_command(client, message):
    await message.channel.send("Hello :)")

async def coinflip_command(client, message):
    result = random.choice(["Heads", "Tails"])
    await message.channel.send(f"Coin flip result: {result}")

async def clear_command(client, message, command):
    # Check if the command author is the bot itself
    if message.author != client.user:
        await message.channel.send("You do not have permission to use this command.", delete_after=5)
        return

    if len(command) > 1 and command[1].isdigit():
        num_to_clear = int(command[1])
        deleted = 0
        async for msg in message.channel.history(limit=100):
            if msg.author == client.user:
                await msg.delete()
                deleted += 1
            if deleted >= num_to_clear:
                break
        await message.channel.send(f"Cleared {deleted} bot message(s).", delete_after=5)
    else:
        await message.channel.send("Please specify a valid number, e.g., `>clear 10`.", delete_after=3)

async def calculate_command(client, message, command):
    expression = " ".join(command[1:])
    if re.match(r'^[\d\s\+\-\*/\.]+$', expression):
        try:
            result = eval(expression, {"__builtins__": None}, {})
            await message.channel.send(f"Result: {result}")
        except Exception as e:
            await message.channel.send(f"Error in calculation: {e}", delete_after=3)
    else:
        await message.channel.send("Invalid input. Use numbers and operators (+, -, *, /) only.", delete_after=3)

async def userinfo_command(client, message):
    user = message.mentions[0] if message.mentions else message.author
    roles = [role.name for role in user.roles[1:]]
    user_info = (
        f"**User Info:**\n"
        f"Name: {user.name}\n"
        f"ID: {user.id}\n"
        f"Joined: {user.joined_at.strftime('%Y-%m-%d')}\n"
        f"Roles: {', '.join(roles) if roles else 'No roles'}"
    )
    await message.channel.send(user_info)

async def serverinfo_command(client, message):
    server = message.guild
    server_info = (
        f"**Server Info:**\n"
        f"Name: {server.name}\n"
        f"ID: {server.id}\n"
        f"Member Count: {server.member_count}\n"
        f"Created On: {server.created_at.strftime('%Y-%m-%d')}\n"
    )
    await message.channel.send(server_info)
