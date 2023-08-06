# install python 3.11 and then do these on the cmd line (windows)
# py -3.11 -m pip install -U discord.py
# py -3.11 -m pip install -U dotenv
# py -3.11 -m pip install -U requests
# py -3.11 -m pip install python-certifi-win32
# py -3.11 -m pip install tabulate
# py -3.11 -m pip install asyncio

#
#  requires a .env file in the same directory as DCSBucketBot.py
#
#  put this in the file
#
#  # .env
#  DISCORD_TOKEN=MTEzNjYwMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxJ2Jmt7Zo
#  JSON_URL=https://url_to_json_file/player_stats.json
#
#
# bot.py

import os
import random
import discord
import requests
import json
from tabulate import tabulate

from discord.ext import commands,tasks
from dotenv import load_dotenv
import dotenv
import asyncio
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('JSON_URL')
CHANNEL = 'scoreboard'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
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

@bot.command(name='zones')
async def get_zones(ctx):
    try:
        # Retrieve data from the HTTP URL
        response = requests.get(URL)
        
        if response.status_code == 200:
            data = response.json()  # Convert JSON to dictionary

            # Check if the player exists in the "stats" dictionary
            zone_list = []
            blue_count = len(data['zones']['blue'])
            neutral_count = len(data['zones']['neutral'])
            red_count = len(data['zones']['red'])
            
            str = f"Blue:{blue_count}\nNeutral:{neutral_count}\nRed:{red_count}\n"
            

            await ctx.send(str)
        else:
            await ctx.send(f"Failed to retrieve data. Status code: {response.status_code}")



    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='pilots')
async def get_pilots(ctx):
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
        channel = discord.utils.get(bot.get_all_channels(), name=CHANNEL)
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if channel:
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
                        
                    
                    if   player_xp < 2000 : player_rank = 'E-1 Airman basic'
                    elif player_xp < 4500 : player_rank = 'E-2 Airman'
                    elif player_xp < 7700 : player_rank = 'E-3 Airman first class'
                    elif player_xp < 11800 : player_rank = 'E-4 Senior airman'
                    elif player_xp < 17000 : player_rank = 'E-5 Staff sergeant'
                    elif player_xp < 23500 : player_rank = 'E-6 Technical sergeant'
                    elif player_xp < 31500 : player_rank = 'E-7 Master sergeant'
                    elif player_xp < 42000 : player_rank = 'E-8 Senior master sergeant'
                    elif player_xp < 52800 : player_rank = 'E-9 Chief master sergeant'
                    elif player_xp < 66500 : player_rank = 'O-1 Second lieutenant'
                    elif player_xp < 82500 : player_rank = 'O-2 First lieutenant'
                    elif player_xp < 101000 : player_rank = 'O-3 Captain'
                    elif player_xp < 122200 : player_rank = 'O-4 Major'
                    elif player_xp < 146300 : player_rank = 'O-5 Lieutenant colonel'
                    elif player_xp < 173500 : player_rank = 'O-6 Colonel'
                    elif player_xp < 204000 : player_rank = 'O-7 Brigadier general'
                    elif player_xp < 238000 : player_rank = 'O-8 Major general'
                    elif player_xp < 275700 : player_rank = 'O-9 Lieutenant general'
                    else            : player_rank = 'O-10 General'

                    player_xp_list.append((player_name, player_xp,player_rank))

                # Sort the list of player XP values by XP in descending order
                sorted_player_xp_list = sorted(player_xp_list, key=lambda x: x[1], reverse=True)

                # Create a formatted string with sorted player XP values
                #xp_string = "\n".join([f"{player_name}: {xp} : {player_rank}" for player_name, xp, player_rank in sorted_player_xp_list])
                xp_string = "\n".join([f"{player_name}: {xp}" for player_name, xp,player_rank in sorted_player_xp_list])

                await ctx.send(f"[{current_datetime}] XP for each player (sorted by XP):\n```\n{xp_string}\n```")
            else:
                await ctx.send(f"Failed to retrieve data. Status code: {response.status_code}")



    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Define a task to retrieve and display name and unit for each player in the dcs-chat channel
@tasks.loop(minutes=30)  # Run the task every 30 minutes
async def get_all_players_task():
    try:
        # Get the channel by name
        channel = discord.utils.get(bot.get_all_channels(), name=CHANNEL)
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if channel:
            # Retrieve data from the HTTP URL
            response = requests.get(URL)

            if response.status_code == 200:
                data = response.json()  # Convert JSON to dictionary

                player_xp_list = []

            # Iterate through the stats dictionary and extract player names and XP values
            for player_name, player_data in data['stats'].items():
                if isinstance(player_data, dict):  # Check if the player data is a dictionary
                    player_xp = player_data.get('XP', 0)
                    
                    if   player_xp < 2000 : player_rank = 'E-1 Airman basic'
                    elif player_xp < 4500 : player_rank = 'E-2 Airman'
                    elif player_xp < 7700 : player_rank = 'E-3 Airman first class'
                    elif player_xp < 11800 : player_rank = 'E-4 Senior airman'
                    elif player_xp < 17000 : player_rank = 'E-5 Staff sergeant'
                    elif player_xp < 23500 : player_rank = 'E-6 Technical sergeant'
                    elif player_xp < 31500 : player_rank = 'E-7 Master sergeant'
                    elif player_xp < 42000 : player_rank = 'E-8 Senior master sergeant'
                    elif player_xp < 52800 : player_rank = 'E-9 Chief master sergeant'
                    elif player_xp < 66500 : player_rank = 'O-1 Second lieutenant'
                    elif player_xp < 82500 : player_rank = 'O-2 First lieutenant'
                    elif player_xp < 101000 : player_rank = 'O-3 Captain'
                    elif player_xp < 122200 : player_rank = 'O-4 Major'
                    elif player_xp < 146300 : player_rank = 'O-5 Lieutenant colonel'
                    elif player_xp < 173500 : player_rank = 'O-6 Colonel'
                    elif player_xp < 204000 : player_rank = 'O-7 Brigadier general'
                    elif player_xp < 238000 : player_rank = 'O-8 Major general'
                    elif player_xp < 275700 : player_rank = 'O-9 Lieutenant general'
                    else            : player_rank = 'O-10 General'

                    player_xp_list.append((player_name, player_xp,player_rank))

            # Sort the list of player XP values by XP in descending order
            sorted_player_xp_list = sorted(player_xp_list, key=lambda x: x[1], reverse=True)

            # Create a formatted string with sorted player XP values
            #xp_string = "\n".join([f"{player_name}: {xp} : {player_rank}" for player_name, xp, player_rank in sorted_player_xp_list])
            xp_string = "\n".join([f"{player_name}: {xp}" for player_name, xp, player_rank in sorted_player_xp_list])
            blue_count = len(data['zones']['blue'])
            neutral_count = len(data['zones']['neutral'])
            red_count = len(data['zones']['red'])
            
            #await ctx.send(f"Blue:{blue_count}\nNeutral:{neutral_count}\nRed:{red_count}\n")

            xp_string += f"\n\nBlue:{blue_count}\nNeutral:{neutral_count}\nRed:{red_count}\n"

            await channel.send(f"[{current_datetime}] XP for each player (sorted by XP):\n```\n{xp_string}\n```")
        else:
            await channel.send(f"Failed to retrieve data. Status code: {response.status_code}")


    except Exception as e:
        await channel.send(f"An error occurred: {str(e)}")

# Start the task
@bot.listen()
async def on_ready():
    get_all_players_task.start() # important to start the loop

# Run the bot
bot.run(TOKEN)

