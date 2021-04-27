import os
import discord
from dotenv import load_dotenv
import random
import json

class MovieLotteryClient(discord.Client):
    # The channel that the bot reads in
    channels = {}
    # The discord bot's username
    bot_username = "Eiga Niijima#3932"
    # Brenda's username (used for special cases)
    brenda_username = "Bmanpereira#8054"
    lottery_lst = {}
    
    async def save_info(self, info, filename):
        '''
        Save some info about the discord bot in a json format
        '''
        data = json.dumps(info)
        f = open("Bot Info/" + filename, "w")
        f.write(data)
        f.close()
        
    async def load_info(self, info, filename):
        '''
        Load some info about the discord bot in a json format
        '''        
        f = open("Bot Info/" + filename, "r")
        data = f.read()
        f.close()
        # If the file is empty, then ignore
        if data != '':
            info = json.loads(data)
    
    async def add_to_lst(self, message):
        '''
        Add a movie to the list
        '''
        # Split up the message by the words before "add" and the movie
        movie = message.content.lower().strip().split("add ")
        # If there is nothing after the word "add" then its not a valid movie
        if len(movie) < 2:
            await message.channel.send("Sorry, that doesn't look like a movie")
            return 
        movie = ' '.join(movie[1:]).strip()
        # Capitalize each word in the movie
        movie = ' '.join([word[0].upper() + word[1:] for word in movie.split(' ')])
        # Add the movie to the list
        self.lottery_lst.setdefault(message.guild, {})[message.author] = movie
        # Notify the user & the server that their movie was added
        await message.channel.send("I have added the movie " +  movie + " to your movie lottery")
        print('Adding "' + movie + '" to the movie lottery list of', message.guild)
    
    async def get_lst(self, message):
        '''
        Return the server's list
        '''
        # Get the list for the specific server
        lst = self.lottery_lst.get(message.guild, None)
        if not lst:
            await message.channel.send("There aren't any movies on your movie lottery list")
            return
        
        # Send the message containing the movie list
        # Put in multiple messages so phone users can easily copy a single movie
        await message.channel.send("Your movie lottery list is:")
        for user, movie in lst.items():
            # If the movie is from the user "Brenda"
            if str(user) == self.brenda_username:
                await message.channel.send("Brenda: " + movie)
                continue
            await message.channel.send(user.display_name + ": " + movie)
        
    async def reset_lst(self, message):
        '''
        Make the list for that specific server empty
        '''
        self.lottery_lst[message.guild] = {}
        await message.channel.send("I have reset your movie lottery list")
        
    async def pick_movie(self, message):
        '''
        Decide on the movie using a random number generator
        '''
        # Get the list for the specific server
        lst = self.lottery_lst.get(message.guild, None)
        if not lst:
            await message.channel.send("There aren't any movies on your movie lottery list")
            return
        
        # Decide on the movie
        ind = random.randint(0, len(lst) - 1)
        movie = list(lst.values())[ind]
        await message.channel.send('The movie that you are watching is "' + movie + '"')

    async def remove_movie(self, message):
        '''
        Remove a person's movie from the list
        '''
        # Get the list for the specific server
        lst = self.lottery_lst.get(message.guild, None)
        if not lst:
            await message.channel.send("There aren't any movies on your movie lottery list")
            return

        # Split up the message by the words before "add" and the movie
        words = message.content.lower().strip().split("remove ")
        # If there is nothing after the word "remove" then its not a valid username
        if len(words) < 2:
            await message.channel.send("Sorry, that doesn't look like a username")
            return

        # Break up the words after the word remove
        words = ' '.join(words[1:]).strip().split(" ")

        # For every username in the list, check if it contains a 'user' (a word that appears after remove)
        for lst_user in lst:
            for user in words:
                # If the username contains the word, remove it from the list
                if user in str(lst_user):
                    lst.pop(lst_user)
    
    async def change_channel(self, message):
        '''
        Change the channel for the specific server
        '''
        # Split up the message by the words before "change channel" and the movie
        channel_name = message.content.lower().strip().split("change channel")
        # If there is nothing after the phrase "change channel" then its not a valid channel
        if len(channel_name) < 2:
            await message.channel.send("Sorry, that doesn't look like a channel name")
            return
        # Save the channel to the channels dictionary
        channels[message.guild] = channel_name[1].strip().split(" ")
        # Save the channels dictionary to a file
        await self.save_info(self.channels, "channels.json")
    
    # The list of functions that are callable through commands     
    funcs_check = {"add": add_to_lst, "list": get_lst, "reset": reset_lst, "pick": pick_movie, "remove": remove_movie}
    # The list of functions that are callable through server wide commands (does not matter what channel is called)
    server_funcs_check = {"change channel": change_channel}
    
    async def on_ready(self):
        '''
        Tell the server when the bot has connected to discord
        '''
        await self.load_info(self.channels, "channels.json")
        print(f"{self.user} has connected to Discord!")
    
    async def __check_command(self, message, command_lst):
        '''
        Check and return the function that is being called through the command
        '''
        # Check if in the message, it contains a command        
        func = None
        for word, rel_func in command_lst.items():
            if word in message.content:
                func = rel_func
                break
        return func     
    
    async def on_message(self, message):
        '''
        When a message is received, call the corresponding command's function
        '''
        # Ignore the bot's messages
        if str(message.author) == self.bot_username:
            return

        # Check for the server side commands
        func = await self.__check_command(message, self.server_funcs_check)
        if func != None:
            await func(self, message)
            return

        # Ignore messages that aren't in the bot's channel
        if str(message.channel) == self.channels.get(message.guild, "bots"):
            func = await self.__check_command(message, self.funcs_check)            
            if func != None:
                await func(self, message)
            return
                
        
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = MovieLotteryClient()
    client.run(TOKEN)