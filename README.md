# Discord Movie Lottery Bot
A discord bot meant for a deciding a movie (or anything really) for a group of people.

Server Wide Commands:

```change channel "channel-name"```
Change the channel that the bot reads. By default, the bot only reads the "bots" channel in a server, but this can be changed with this command.

Commands:

```add "Your Movie To Add"```
Add a movie to your server's movie list. Your movie is all words that appear after the word "add".

```remove "Substring of person's username"```
Remove a person's movie from the discord server's movie list. It removes all users with usernames that have the substring in it. You can remove multiple movies at once by adding more usernames separated by spaces.

```list```
Send the discord server's movie list in the chat.

```reset```
Reset the discord server's movie list to be empty.

```pick```
Randomly pick a movie from the movie list.
