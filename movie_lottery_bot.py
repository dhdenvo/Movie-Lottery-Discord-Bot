import os
import discord
from dotenv import load_dotenv
import random

class MovieLotteryClient(discord.Client):
    # The channel that the bot reads in
    channel = "bots"
    # The discord bot's username
    bot_username = "Eiga Niijima#3932"
    # Brenda's username (used for special cases)
    brenda_username = "Bmanpereira#8054"
    lottery_lst = {}
    
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
        words = ' '.join(words[1:]).strip().strip(" ")

        # For every username in the list, check if it contains a 'user' (a word that appears after remove)
        for lst_user in lst:
            for user in words:
                # If the username contains the word, remove it from the list
                if user in str(lst_user):
                    lst.pop(lst_user)
    
    # The list of functions that are callable through commands     
    funcs_check = {"add": add_to_lst, "list": get_lst, "reset": reset_lst, "pick": pick_movie, "remove": remove_movie}
    
    async def on_ready(self):
        '''
        Tell the server when the bot has connected to discord
        '''
        print(f"{self.user} has connected to Discord!")
    
    async def on_message(self, message):
        '''
        When a message is received, call the corresponding command's function
        '''
        # Ignore the bot's messages
        if str(message.author) == self.bot_username:
            return

        # Ignore messages that aren't in the bot's channel
        if str(message.channel) == self.channel:
            # Check if in the message, it contains a command
            func = None
            for word, rel_func in self.funcs_check.items():
                if word in message.content:
                    func = rel_func
                    break
                
            # Call the command's associated function if there is one
            if func != None:
                await func(self, message)
                
        
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = MovieLotteryClient()
    client.run(TOKEN)