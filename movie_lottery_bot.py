import os
import discord
from dotenv import load_dotenv
import random

class MovieLotteryClient(discord.Client):
    channel = "bots"
    bot_username = "Eiga Niijima#3932"
    brenda_username = "Bmanpereira#8054"
    lottery_lst = {}
    
    async def add_to_lst(self, message):
        movie = message.content.lower().strip().split("add ")
        if len(movie) < 2:
            await message.channel.send("Sorry, that doesn't look like a movie")
            return 
        movie = ' '.join(movie[1:]).strip()
        movie = ' '.join([word[0].upper() + word[1:] for word in movie.split(' ')])
        self.lottery_lst.setdefault(message.guild, {})[message.author] = movie
        await message.channel.send("I have added the movie " +  movie + " to your movie lottery")
        print('Adding "' + movie + '" to the movie lottery list of', message.guild)
    
    async def get_lst(self, message):
        lst = self.lottery_lst.get(message.guild, None)
        if not lst:
            await message.channel.send("There aren't any movies on your movie lottery list")
            return
        
        await message.channel.send("Your movie lottery list is:")
        for user, movie in lst.items():
            if str(user) == self.brenda_username:
                await message.channel.send("Brenda: " + movie)
                continue
            await message.channel.send(user.display_name + ": " + movie)
        
    async def reset_lst(self, message):
        self.lottery_lst[message.guild] = {}
        await message.channel.send("I have reset your movie lottery list")
        
    async def pick_movie(self, message):
        lst = self.lottery_lst.get(message.guild, None)
        if not lst:
            await message.channel.send("There aren't any movies on your movie lottery list")
            return
        
        ind = random.randint(0, len(lst) - 1)
        movie = list(lst.values())[ind]
        await message.channel.send('The movie that you are watching is "' + movie + '"')
    
    # Add a don't pick Brenda option (call command to enable or disable)
    
    funcs_check = {"add": add_to_lst, "list": get_lst, "reset": reset_lst, "pick": pick_movie}
    
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
    
    async def on_message(self, message):
        if str(message.author) == self.bot_username:
            return

        if str(message.channel) == self.channel:
            func = None
            for word, rel_func in self.funcs_check.items():
                if word in message.content:
                    func = rel_func
                    break
                
            if func != None:
                await func(self, message)
                
        
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = MovieLotteryClient()
    client.run(TOKEN)