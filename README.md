# fatebot
A Discord bot written in Python to facilitate games in the roleplaying system Fate Core. 

To run this programme:
1. Make sure Discord is installed on your machine. You can install Discord from https://discordapp.com/
2. Open the command terminal. CD the discord bot's directory and run 'pip install requirements.txt' 
3. Run fatebot_main_master
4. With fatebot_main_master running in the background, go to Discord. You can now type the bot's commands into the Discord chat. Prefix commands with '.' (.help is a good first command to run)

***

List of available commands below:

.greetings : greets you.
.initialize : Initializes the game. There can be only one game per channel. You must initialize a game to have access to all other            commands.
.name (character name) : Gives your character a name. Your character must be named before other character-related commands will work. You may have multiple characters, though this is usually only for the GM.
.addskill (rank skill) : Gives your character a skill(s). If you control multiple characters, you must specify which character you are giving the skill to, eg '.addskill Bob great fight.
.roll (skill) : Rolls dice. It will add your rank modifier to the roll if you specify which skill you are rolling. If you control multiple characters, you must specify which character you are rolling for.
.sheet : Displays your character sheet(s).
.initiative : Displays physical combat initiative. 
.fp : Handles fate points. '.fp set' will set your fate points to 3; '.fp +' increases your total fate points by 1; '.fp -' decreases your total fate points by 1.

***

At the time I started this project, I was GMing a lot of Fate Core. I found it annoying to have to have a desktop open for Discord (my group's platform of choice), a dekstop for the rulebook and a browser tab for character sheets and other miscellanea. So I decided to build a bot which would take care of some basic Fate Core functions, such as rolling dice, keeping track of character sheets and initiative. The objective was to make my life as a GM somewhat easier. 

The bot supports one game per Discord channel, meaning I don't have to create an entirely new server to play with my friends if I don't want to. It also supports offline storage of games.  
