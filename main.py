import discord
import subprocess
import os
import logging
from datetime import datetime
from commands import handle_command
from colorama import init

# Initialize colorama
init(autoreset=True)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Colors:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    LIGHT_CYAN = "\033[96m"

subprocess.run(['clear'])
debug = True

if debug:
    LoginToken = 'M T A w M D A zNDUxNDMyNTc0OTkzMQ.Gp47r6.xvMgYl_9aF39wCQNgzWbBMf3IvIZDuc_zl f t i o'  # Replace with your actual token
    print(Colors.GREEN + "DebugMode: ON" + Colors.RESET)
else:
    LoginToken = input("Please enter your bot token: ")

allowed_servers = {1212896057261031504, 1294950253811732480, 877468377411625021}  # Replace with specific server IDs

class MyClient(discord.Client):
    def __init__(self, prefix='>'):
        super().__init__()
        self.prefix = prefix
        self.start_time = datetime.now()  # Initialize start_time here

    async def on_ready(self):
        ascii_art = [
            "██╗   ██╗██╗██████╗ ██████╗ ",
            "██║   ██║██║██╔══██╗██╔══██╗",
            "██║   ██║██║██████╔╝██████╔╝",
            "╚██╗ ██╔╝██║██╔═══╝ ██╔══██╗",
            " ╚████╔╝ ██║██║     ██║  ██║",
            "  ╚═══╝  ╚═╝╚═╝     ╚═╝  ╚═╝"
        ]

        subprocess.run(['clear'])
        terminal_width = os.get_terminal_size().columns

        # Create a gradient effect from blue to cyan
        gradient_colors = [f'\033[38;5;{i}m' for i in range(0, 255)]  # From blue (34) to cyan (46)

        # Calculate the length of the longest line in the ASCII art
        max_length = max(len(line) for line in ascii_art)

        # Calculate padding to center the ASCII art
        padding = (terminal_width - max_length) // 2

        # Print each line with a gradient color
        for i, line in enumerate(ascii_art):
            color = gradient_colors[i % len(gradient_colors)]
            centered_line = ' ' * padding + line  # Add padding for centering
            print(f"{color}{centered_line}{Colors.RESET}")

        print(Colors.BLUE + 'Logged on as: ' + Colors.GREEN + str(self.user) + Colors.RESET)
        print(Colors.BLUE + 'Prefix:       ' + Colors.GREEN + self.prefix + Colors.RESET)
        print('═' * terminal_width)

    async def on_message(self, message):
        if message.guild and message.guild.id not in allowed_servers:
            return

        # Call the command handler
        await handle_command(self, message)

# Start the bot
client = MyClient()
client.run(LoginToken)
