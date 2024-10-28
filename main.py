import discord
import subprocess
import re
import random
import time
import asyncio
from datetime import datetime
import os

# ANSI escape sequences for colors
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    CYAN = "\033[36m"

# Clear the terminal
subprocess.run(['clear'])
debug = True

# Set the bot token for debugging or manual input
if debug:
    LoginToken = ''  # Replace with your bot token
    print(Colors.GREEN + "DebugMode: ON" + Colors.RESET)
else:
    LoginToken = input("Please enter your bot token: ")

# Define allowed server IDs
allowed_servers = {1212896057261031504, 1294950253811732480, 877468377411625021}

class MyClient(discord.Client):
    def __init__(self, prefix='>'):
        super().__init__()  # Remove intents here
        self.prefix = prefix
        self.unbspam_task = None

    async def on_ready(self):
        ascii_art = """
██╗   ██╗██╗██████╗ ██████╗ 
██║   ██║██║██╔══██╗██╔══██╗
██║   ██║██║██████╔╝██████╔╝
╚██╗ ██╔╝██║██╔═══╝ ██╔══██╗
 ╚████╔╝ ██║██║     ██║  ██║
  ╚═══╝  ╚═╝╚═╝     ╚═╝  ╚═╝
"""
        subprocess.run(['clear'])
        terminal_width = os.get_terminal_size().columns
        for line in ascii_art.strip().split('\n'):
            print(line.center(terminal_width))

        print(Colors.BLUE + 'Logged on as: ' + Colors.GREEN + str(self.user) + Colors.RESET)
        print(Colors.BLUE + 'Prefix:       ' + Colors.GREEN + self.prefix + Colors.RESET)
        print('─' * terminal_width)

    async def unbspam(self, channel):
        while True:
            await channel.send("!!collect")
            await asyncio.sleep(2)
            await channel.send("!!work")
            await asyncio.sleep(2)
            await channel.send("!!crime")
            await asyncio.sleep(90)

    async def on_message(self, message):
        # Ensure bot operates only in allowed servers
        if message.guild and message.guild.id not in allowed_servers:
            return

        # Debug: Log received message details
        print(f"Received [{Colors.YELLOW}message{Colors.RESET}] from {Colors.GREEN}{message.author}{Colors.RESET} in {Colors.YELLOW}{message.guild.name}{Colors.RESET} - Content: {message.content}")

        # Process message commands
        if message.content.startswith(self.prefix):
            command = message.content[len(self.prefix):].strip().split()

            if command[0] == 'setprefix':
                
                if len(command) > 1:
                    new_prefix = command[1]
                    if len(new_prefix) == 1:
                        self.prefix = new_prefix
                        print(Colors.BLUE + f'Prefix updated to: {Colors.GREEN}{self.prefix}{Colors.RESET}')
                        await message.channel.send(f"Prefix set to: `{self.prefix}`")
                        print(f"{Colors.CYAN}Command executed: setprefix to {self.prefix} at {datetime.now()}{Colors.RESET}")
                    else:
                        await message.channel.send(f"{Colors.RED}Error: Prefix must be a single character.{Colors.RESET}", delete_after=5)
                else:
                    await message.channel.send(f"{Colors.RED}Usage: !setprefix <new_prefix>{Colors.RESET}", delete_after=5)

            elif command[0] == 'unbspam':
                
                if self.unbspam_task is None or self.unbspam_task.done():
                    self.unbspam_task = self.loop.create_task(self.unbspam(message.channel))
                    #await message.channel.send("Started spamming commands.")
                    print(f"{Colors.CYAN}Command executed: unbspam start at {datetime.now()}{Colors.RESET}")
                else:
                    await message.channel.send("Spam is already running.")

            elif command[0] == 'stopspam':
                
                if self.unbspam_task is not None:
                    self.unbspam_task.cancel()
                    self.unbspam_task = None
                    await message.channel.send("Stopped spamming commands.")
                    print(f"{Colors.CYAN}Command executed: stopspam at {datetime.now()}{Colors.RESET}")
                else:
                    await message.channel.send("Spam is not running.")

            # Handle "!uptime" command
            elif command[0] == 'uptime':
                
                current_time = datetime.now()
                uptime_duration = current_time - start_time

                # Format the uptime duration
                days, seconds = uptime_duration.days, uptime_duration.seconds
                hours = seconds // 3600
                seconds %= 3600
                minutes = seconds // 60
                seconds %= 60

                uptime_message = f"Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds."
                await message.channel.send(uptime_message)
                print(f"{Colors.CYAN}Command executed: uptime at {datetime.now()}{Colors.RESET}")

            # Handle "!help" command
            elif command[0] == 'help':
                
                help_message = (
                    "```md\n"
                    "# Bot Commands\n"
                    "| Command                | Description                         |\n"
                    "|------------------------|-------------------------------------|\n"
                    "| help                  | Prints command sheet                |\n"
                    "| greet                 | Greets the user                     |\n"
                    "| clear <n>             | Clears <n> messages sent by the bot |\n"
                    "| calculate <expression>| Performs basic math (e.g., `3 + 5`) |\n"
                    "| userinfo <@user>      | Displays user info                  |\n"
                    "| serverinfo            | Displays server info                |\n"
                    "| roll <dice>           | Rolls dice in the format `XdY`      |\n"
                    "| avatar <@user>        | Displays user avatar                |\n"
                    "| coinflip              | Simulates a coin flip               |\n"
                    "| setprefix <new_prefix>| Sets a custom prefix                |\n"
                    "| uptime                | Displays the bot's uptime           |\n"
                    "```"
                )
                await message.channel.send(help_message)
                print(f"{Colors.CYAN}Command executed: help at {datetime.now()}{Colors.RESET}")  # Print timestamp with command

            # Handle "!greet" command
            elif command[0] == 'greet':
                
                await message.channel.send('Hello :)')
                print(f"{Colors.CYAN}Command executed: greet at {datetime.now()}{Colors.RESET}")  # Print timestamp with command

            # Handle "!clear" command
            elif command[0] == 'clear':
                
                if len(command) > 1 and command[1].isdigit():
                    num_to_clear = int(command[1])

                    deleted = 0
                    async for msg in message.channel.history(limit=100):
                        if msg.author == self.user:
                            await msg.delete()
                            deleted += 1
                        if deleted >= num_to_clear:
                            break

                    await message.channel.send(f"Cleared {deleted} bot message(s).", delete_after=5)
                    print(f"{Colors.CYAN}Command executed: clear {num_to_clear} at {datetime.now()}{Colors.RESET}")  # Print timestamp with command
                else:
                    await message.channel.send("Please specify a valid number, e.g., `!clear 10`.", delete_after=3)

            # Handle "!calculate" command
            elif command[0] == 'calculate':
                
                expression = " ".join(command[1:])
                if re.match(r'^[\d\s\+\-\*/\.]+$', expression):
                    try:
                        result = eval(expression, {"__builtins__": None}, {})
                        await message.channel.send(f"Result: {result}")
                    except Exception as e:
                        await message.channel.send(f"{Colors.RED}Error in calculation: {e}{Colors.RESET}", delete_after=3)
                else:
                    await message.channel.send(f"{Colors.RED}Invalid input. Please use numbers and operators (+, -, *, /) only.{Colors.RESET}", delete_after=3)
                print(f"{Colors.CYAN}Command executed: calculate at {datetime.now()}{Colors.RESET}")  # Print timestamp with command

            # Handle "!userinfo" command
            elif command[0] == 'userinfo':
                
                user = message.mentions[0] if message.mentions else message.author
                roles = [role.name for role in user.roles[1:]]  # Skip the @everyone role
                user_info = (f"**User Info:**\n"
                             f"Name: {user.name}\n"
                             f"ID: {user.id}\n"
                             f"Joined: {user.joined_at.strftime('%Y-%m-%d')}\n"
                             f"Roles: {', '.join(roles) if roles else 'No roles'}")
                await message.channel.send(user_info)
                print(f"{Colors.CYAN}Command executed: userinfo at {datetime.now()}{Colors.RESET}")  # Print timestamp with command

            # Handle "!serverinfo" command
            elif command[0] == 'serverinfo':
                
                server = message.guild
                server_info = (f"**Server Info:**\n"
                               f"Name: {server.name}\n"
                               f"ID: {server.id}\n"
                               f"Owner: {server.owner}\n"
                               f"Member Count: {server.member_count}\n"
                               f"Created On: {server.created_at.strftime('%Y-%m-%d')}")
                await message.channel.send(server_info)
                print(f"{Colors.CYAN}Command executed: serverinfo at {datetime.now()}{Colors.RESET}")  # Print timestamp with command

            # Handle "!roll" command
            elif command[0] == 'roll':
                
                if len(command) > 1:
                    dice = command[1]
                    try:
                        num, sides = map(int, dice.lower().split('d'))
                        if num <= 0 or sides <= 0:
                            await message.channel.send(f"{Colors.RED}Error: Number of dice and sides must be positive.{Colors.RESET}", delete_after=5)
                            return
                        rolls = [random.randint(1, sides) for _ in range(num)]
                        await message.channel.send(f"You rolled: {', '.join(map(str, rolls))} (Total: {sum(rolls)})")
                        print(f"{Colors.CYAN}Command executed: roll {dice} at {datetime.now()}{Colors.RESET}")  # Print timestamp with command
                    except ValueError:
                        await message.channel.send(f"{Colors.RED}Error: Invalid dice format. Use XdY (e.g., 2d6).{Colors.RESET}", delete_after=5)
                else:
                    await message.channel.send(f"{Colors.RED}Usage: !roll <dice>{Colors.RESET}", delete_after=5)

            # Handle "!avatar" command
            elif command[0] == 'avatar':
                
                user = message.mentions[0] if message.mentions else message.author
                await message.channel.send(user.avatar.url)
                print(f"{Colors.CYAN}Command executed: avatar at {datetime.now()}{Colors.RESET}")  # Print timestamp with command

            # Handle "!coinflip" command
            elif command[0] == 'coinflip':
                
                result = random.choice(['Heads', 'Tails'])
                await message.channel.send(f"Coin flip result: {result}")
                print(f"{Colors.CYAN}Command executed: coinflip at {datetime.now()}{Colors.RESET}")  # Print timestamp with command

# Start the bot
start_time = datetime.now()
client = MyClient()
client.run(LoginToken)
