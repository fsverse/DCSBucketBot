# py -3.11 -m pip install -U discord.py
# py -3.11 -m pip install -U dotenv
# py -3.11 -m pip install -U requests
# py -3.11 -m pip install python-certifi-win32
# py -3.11 -m pip install tabulate

# bot.py

import os
import random
import discord
import requests
import json
from tabulate import tabulate

from discord.ext import commands
from dotenv import load_dotenv
import dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('JSON_URL')

intents = discord.Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents) 
#client = discord.Client(intents=discord.Intents.default())

@bot.command(name='raw')
async def get_data(ctx):
    try:
        # Retrieve data from the HTTP URL
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.text
            await ctx.send(f"Data from URL:\n```\n{table}\n```")
            
        else:
            await ctx.send(f"Failed to retrieve data. Status code: {response.status_code}")

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='pilots')
async def get_allxp(ctx):
    try:
        # Retrieve data from the HTTP URL
        response = requests.get(URL)
        
        if response.status_code == 200:
            data = response.json()  # Convert JSON to dictionary

            player_info_list = []

            # Iterate through the players dictionary and extract player names and units
            for player_data in data['players']:
                player_name = player_data.get('name', 'Unknown Player')
                player_unit = player_data.get('unit', 'Unknown Unit')
                player_info_list.append(f"{player_name} ({player_unit})")

            # Create a formatted string with player names and units
            player_info_string = "\n".join(player_info_list)

            # Get the name of the user making the request
            user_name = ctx.author.display_name

            await ctx.send(f"Name and Unit for each player - Requested by {user_name}:\n{player_info_string}")
        else:
            await ctx.send(f"Failed to retrieve data. Status code: {response.status_code}")


    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='xpme')
async def get_xp(ctx):
    try:
        # Retrieve data from the HTTP URL
        response = requests.get(URL)
        player_name = ctx.author.display_name
        await ctx.send(f"XP for {player_name}")
        
        if response.status_code == 200:
            data = response.json()  # Convert JSON to dictionary

            # Check if the player exists in the "stats" dictionary
            if player_name in data['stats']:
                player_xp = data['stats'][player_name]['XP']
                await ctx.send(f"XP for {player_name}: {player_xp}")
            else:
                await ctx.send(f"Player {player_name} not found in the data.")

        else:
            await ctx.send(f"Failed to retrieve data. Status code: {response.status_code}")

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='xpall')
async def get_allxp(ctx):
    try:
        # Retrieve data from the HTTP URL
        response = requests.get(URL)
        
        if response.status_code == 200:
            data = response.json()  # Convert JSON to dictionary

            # Check if the player exists in the "stats" dictionary
            player_xp_list = []

            for player_name, player_data in data['stats'].items():
                if isinstance(player_data, dict):  # Check if the player data is a dictionary
                    player_xp = player_data.get('XP', 0)
                    player_xp_list.append(f"{player_name}: {player_xp}")

            # Combine the list of player XP values into a single string
            xp_string = '\n'.join(player_xp_list)

            await ctx.send(f"XP for each player:\n```\n{xp_string}\n```")
        else:
            await ctx.send(f"Failed to retrieve data. Status code: {response.status_code}")



    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='xp')
async def get_allxp_sorted(ctx):
    try:
        # Retrieve data from the HTTP URL
        response = requests.get(URL)
        
        if response.status_code == 200:
            data = response.json()  # Convert JSON to dictionary

            # Check if the player exists in the "stats" dictionary
            player_xp_list = []

            # Iterate through the stats dictionary and extract player names and XP values
            for player_name, player_data in data['stats'].items():
                if isinstance(player_data, dict):  # Check if the player data is a dictionary
                    player_xp = player_data.get('XP', 0)
                    player_xp_list.append((player_name, player_xp))

            # Sort the list of player XP values by XP in descending order
            sorted_player_xp_list = sorted(player_xp_list, key=lambda x: x[1], reverse=True)

            # Create a formatted string with sorted player XP values
            xp_string = "\n".join([f"{player_name}: {xp}" for player_name, xp in sorted_player_xp_list])

            await ctx.send(f"XP for each player (sorted by XP):\n```\n{xp_string}\n```")
        else:
            await ctx.send(f"Failed to retrieve data. Status code: {response.status_code}")



    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
# Run the bot
bot.run(TOKEN)

