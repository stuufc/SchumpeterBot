import discord
import apimanagement
import guessquotemgt
import usermanagement
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
discord_token = os.environ.get('DISCORD_TOKEN')

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in bot.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name}")

        # INCREMENTS THE GUILD COUNTER.
        guild_count += 1

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
    # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "hello".
    if message.content == "hello":
        # SENDS BACK A MESSAGE TO THE CHANNEL.
        await message.channel.send("hey dirtbag")
    if message.content == "game":
        await message.channel.send("Hey there! Looks like you want some fun. Use the `!guide` command and start playing. Good luck!")
    #with !translate the bot receives a message, and translates it via the API using the GetYodaQuote function from the apimanagement.py file
    if message.content.startswith("!translate "):
        user_input = message.content[11:]  #remove "!translate " from the message

        yoda_quote = apimanagement.GetYodaQuote(user_input)

        #send the yoda quote as a response
        await message.channel.send(f"Yoda says: {yoda_quote}")

    await bot.process_commands(message)

#game mode 1
game_state = {}
#command that allows players to enter the game. If they enter the game their name is added to the list of active players
@bot.command(name='enter')
async def enter_game(ctx):
    channel_id = ctx.channel.id
    if channel_id not in game_state:
        game_state[channel_id] = {'is_active': False, 'active_players': []}

    player_name = ctx.author.name
    if player_name not in game_state[channel_id]['active_players']:
        game_state[channel_id]['active_players'].append(player_name)
        await ctx.send(f"{player_name} has entered the game!")
    else:
        await ctx.send("You're already in the game.")


#using ctx method because it allows us to take discord accounts as users and also identify infos such as channels where the bot is active in
@bot.command(name='mode1')
async def start_game_mode(ctx):
    global solution_showed, hint_claimed

    channel_id = ctx.channel.id  #define channel_id here

    #checks if channel_id is already a key in the game_state dict and therefore checks if game is initialized in this channel
    if channel_id not in game_state:
        game_state[channel_id] = {'is_active': False, 'active_players': []}

    #checks if there is already an active game in this channel
    if game_state[channel_id].get('is_active'):
        await ctx.send(
            "A game is already in progress. Use `!restart` to start a new game with the same players or `!reset` to reset the game.")
        return
    #checks if players have entered the game already, else shows hint for them to !enter
    if not game_state[channel_id]['active_players']:
        await ctx.send("No players have entered the game. Use `!enter` to join.")
        return

    #retrieve a new quote and set it as the global quote
    original_quote, translated_quote = guessquotemgt.GetRandomStarwarsQuote()
    guessquotemgt.SetGlobalQuote(original_quote, False)  #set the new quote

    #reset solution_showed and hint_claimed flags for the new game
    solution_showed = False
    hint_claimed = False

    #update the game state to start a new game
    random.shuffle(game_state[channel_id]['active_players'])
    game_state[channel_id].update({
        'quote': original_quote,
        'is_active': True,
        'hint_used': False,
        'awaiting_guess': True,
        'active_players': game_state[channel_id]['active_players'],
        'current_turn_index': 0
    })

    #adding a message in the first round of the game to announce which player starts the game
    starting_player = game_state[channel_id]['active_players'][0]
    await ctx.send(f"The game is starting. **{starting_player}**, it's your turn to guess!")

    if translated_quote:
        await ctx.send(f"**Star Wars Quote:** {translated_quote}\n\n"
                       f"Try to guess who said this quote by typing `!guess [your guess]`.\n"
                       f"If you're stuck, you can ask for a hint using `!hint`.")
    else:
        await ctx.send("Error: Unable to fetch a Star Wars quote.")

@bot.command(name='guess')
async def guess_quote(ctx, *, guess=None):
    if guess is None:
        await ctx.send("Please provide a guess.")
        return

    channel_id = ctx.channel.id
    #check for active game in this channel
    if channel_id not in game_state or not game_state[channel_id]['is_active']:
        await ctx.send("No active game in this channel. Start with !mode1.")
        return

    #check if player has entered the game
    if ctx.author.name not in game_state[channel_id]['active_players']:
        await ctx.send("You need to enter the game first with `!enter`.")
        return

    #check that only allows the player to guess who is active in the current turn
    current_player = game_state[channel_id]['active_players'][game_state[channel_id]['current_turn_index']]
    if ctx.author.name != current_player:
        await ctx.send(f"It's not your turn. It's currently {current_player}'s turn to guess.")
        return

    #process the guess
    try:
        response = guessquotemgt.CheckAnswerForSaidBy(guess, ctx.author.name)
        await ctx.send(response)
        if "Congratulations" in response:
            #players are given the option to start another game with the same players or to reset it
            await ctx.send("To start a new game with the same players, type `!restart`.\n"
                           "To reset the game with new players, type `!reset`.")
            game_state[channel_id]['awaiting_guess'] = False
        else:
            #restart option in the response for a wrong guess
            await ctx.send(
                "The answer was wrong. Try again or type `!restart` to start a new game with the same players.\n"
                "To reset the game with new players, type `!reset`.")

            #update the turn to the next player
            game_state[channel_id]['current_turn_index'] = (game_state[channel_id]['current_turn_index'] + 1) % len(
                game_state[channel_id]['active_players'])
            next_player = game_state[channel_id]['active_players'][game_state[channel_id]['current_turn_index']]
            await ctx.send(f"It's now {next_player}'s turn to guess.")

    except Exception as e:
        print(f"Error in CheckAnswerForSaidBy: {e}")
        await ctx.send("An error occurred while processing your guess. Try again!")

@bot.command(name='restart')
async def restart_game(ctx):
    channel_id = ctx.channel.id
    if channel_id in game_state and game_state[channel_id]['is_active']:
        #start a new game with the same players
        original_quote, translated_quote = guessquotemgt.GetRandomStarwarsQuote()
        guessquotemgt.SetGlobalQuote(original_quote, False) #update the global quote

        #update game state for new game
        game_state[channel_id].update({
            'quote': original_quote,
            'hint_used': False,
            'awaiting_guess': True
        })
        await ctx.send(f"Game restarted with the same players.\n\n"
                       f"New Star Wars Quote: {translated_quote if translated_quote else 'No quote found'}\n\n"
                       f"Guess who said this quote by typing `!guess [your guess]`.")
        #add message whose players turn it is after restarting the game
        current_player = game_state[channel_id]['active_players'][game_state[channel_id]['current_turn_index']]
        await ctx.send(f"It's now {current_player}'s turn to guess.")

    else:
        await ctx.send("There's no active game to restart. Start with `!mode1`.")

@bot.command(name='reset')
async def reset_game(ctx):
    channel_id = ctx.channel.id
    if channel_id in game_state and game_state[channel_id]['is_active']:
        #reset points for all active players
        for player_name in game_state[channel_id]['active_players']:
            usermanagement.ResetPointsForPlayer(player_name)

        #reset the game state
        game_state[channel_id]['active_players'] = []
        game_state[channel_id]['is_active'] = False
        game_state[channel_id]['awaiting_guess'] = False
        await ctx.send("The game has been reset. Players can join the next game with `!enter`.")
    else:
        await ctx.send("There's no active game to reset.")


"""@bot.command(name='continue')
async def continue_game(ctx):
    channel_id = ctx.channel.id
    if channel_id in game_state and not game_state[channel_id]['awaiting_guess']:
        game_state[channel_id]['is_active'] = True
        await ctx.send("Continue with the same players. Start the next round with `!mode1`.")
    else:
        await ctx.send("There's no game to continue or a guess is being awaited.")"""

@bot.command(name='players')
async def show_players(ctx):
    channel_id = ctx.channel.id
    if channel_id not in game_state:
        await ctx.send("No game is currently active in this channel.")
        return

    active_players = game_state[channel_id].get('active_players', [])
    if not active_players:
        await ctx.send("No players have entered the game.")
        return

    player_info = "Active players and their points:\n"
    for player_name in active_players:
        player_data = usermanagement.FindUser(player_name)
        points = player_data["points"] if player_data else 0
        player_info += f"{player_name}: {points} points\n"

    await ctx.send(player_info)

@bot.command(name='hint')
async def give_hint(ctx):
    #set game state to hin_used. player will only get 0.5 points for a correct guess
    if ctx.channel.id in game_state and not game_state[ctx.channel.id]['hint_used']:
        hint = guessquotemgt.ClaimHint()
        await ctx.send(f"Hint: {hint}\n\n"
                       f"Remember to make your guess using `!guess [your guess]`.")
        game_state[ctx.channel.id]['hint_used'] = True
    else:
        await ctx.send("Hint already used or no active game.")

#Command gets all the Actors from the Database and send it to the Discord
@bot.command(name='actors')
async def give_actors(ctx):
    actor_info = "The game contains the following actors:\n"
    all_actors_list = guessquotemgt.GetAllActors()
    for actor in all_actors_list:
        actor_info += f"ID: {actor[0]}, Name: {actor[1]}\n"
    await ctx.send(actor_info)

@bot.command(name='guide')
async def help_command(ctx):
    help_text = (
        "**Bot Commands:**\n"
        "`!enter` - Enter the current game. Must be used before making guesses.\n"
        "`!mode1` - Start a new game round with a Star Wars quote.\n"
        "`!actors` - Get the List of Actors with the IDs you can guess.\n"
        "`!guess` - Guess who said the Star Wars quote.\n"
        "`!hint` - Get a hint for the current quote. Can only be used once per round.\n"
        "`!restart` - Restart the game with the same players and a new quote.\n"
        #"`!continue` - Continue to a new round with the same players.\n"
        "`!reset` - Reset the game. This clears all players and their points.\n"
        "`!players` - Show a list of all active players and their points.\n\n"
        "**Game Rules:**\n"
        "1. Players must use `!enter` to join the game.\n"
        "2. The bot presents a Star Wars quote in Yoda-style language.\n"
        "3. Players take turns to guess who originally said the quote using `!guess`.\n"
        "4. Points are awarded for correct guesses. Use of hints reduces the points.\n"
        "5. `!restart` to start a new new round; `!reset` clears the game.\n"
        "6. The game is turn-based, so wait for your turn to guess."
    )

    await ctx.send(help_text)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(discord_token)