import discord
from discord.ext import commands
import numpy
import string
import gameload

token = 'bot token goes here'
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
#remove default help command, which will be replaced with our own

proficiency = {'sensational': 9,'epic': 8, 'legendary': 7, 'fantastic':6,
               'superb': 5, 'great': 4, 'good': 3, 'fair': 2, 'average': 1,
               'mediocre': 0, 'poor': -1, 'terrible': -2, 'terribly unlucky': -3,
               'an embarrassment to your family': -4}

@bot.event
async def on_ready():
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

    gameload.load()

    #once the bot has interfaced with python and all those things,
    #load the games file into our games dictionary, specified
    #in the gameload module

@bot.event
async def on_message(message):

    if 'Clotho' in message.content:

        if 'thank you' in message.content:
            await bot.send_message(message.channel,'I suppose you are welcome.')

        else: 
            await bot.send_message(message.channel,'Do not speak my name lightly, '
                               'mortal.')
        
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def greetings():

    await bot.say('Greetings, mortal.')
    
@bot.command(pass_context=True)
async def initialize(ctx):

    channel_id = ctx.message.channel.id
    player_id = ctx.message.author
    all_games = gameload.games['file']
    match = False

    for key in all_games:

        if key == channel_id:

            match = True

            await bot.say("It looks like there is already a game associated to "
                          "this channel. Please try a new channel for "
                          "your game.")
    if match is False:

        all_games[channel_id] = {}
        all_games[channel_id][player_id] = {}

        gameload.save_game(all_games)

        await bot.say("Your game has been successfully created. "
                      "Please join the game with the '.name' command.")
    
@bot.command(pass_context=True)
async def name(ctx, *, message:str):

    channel_id = ctx.message.channel.id
    player_id = ctx.message.author
    all_games = gameload.games['file']
    match = False

    for key in all_games:

        if key == channel_id:

            this_game = all_games[key]
            match = True

            if player_id in this_game:
            #such as if they already control one character, or if they
            #were the ones who initialized the game

                this_game[player_id][message] = {}
                this_game[player_id][message]['skills'] = []

                await bot.say('Character %s successfully created.'%(message))

            else:
            #if they were not the ones who initialized the game

                this_game[player_id] = {}
                this_game[player_id][message] = {}
                this_game[player_id][message]['skills'] = []

                await bot.say('Character %s successfully created.'%(message))
                
    if match is False:

        await bot.say("It looks like there is no game associated to this "
                          "channel. Please try the '.initialize' command.")
                
    gameload.save_game(all_games)

@bot.command(pass_context=True)
async def addskill(ctx, *, message:str):

    channel_id = ctx.message.channel.id
    player_id = ctx.message.author
    all_games = gameload.games['file']

    for key in all_games:

        if key == channel_id:

            this_game = all_games[key]

            if player_id in this_game:

                characters = list(this_game[player_id].items())
                #characters is a list of dictionaries, each dicttionary contains
                #a key (player name) and a list of skills

                if len(characters) == 1:
                #there is only one dictonary in characters, so the player
                #controls only one character

                    rank_and_skill = message.lower().split(',')
                    this_character = characters[0][0]

                    for pair in rank_and_skill:

                        split_pair = pair.split()

                        if split_pair[0] not in proficiency.keys():

                            await bot.say('Please try again with a real rank.')

                        #this adds even if you type in just a rank, so addskill
                        #good works. whereas addskill fighting doesn't.
                        #the latter is good, fix the former eventually

                    #i sh  ould have another if statement checking if you already
                    #have that skill. feels bad if everything breaks because
                    #someone forgets, or mistypes

                        else:

                            this_game[player_id][this_character]['skills'].append(split_pair)

                            await bot.say('Skill %s successfully added.'%
                                          (split_pair[1]))

                else:
                #the player controls multiple characters, usually because they
                #are the GM

                    try:
                    #this try/except catches mistakes like a player not having
                    #specified the chracter name before trying to add a skill

                        name_and_skills = message.split(':')
                        this_character = name_and_skills[0]
                        skill_pairs = name_and_skills[1].lstrip()
                        all_pairs = skill_pairs.split(',')

                        for pair in all_pairs:

                            split_pair = pair.split()

                            if split_pair[0] not in proficiency.keys():

                                await bot.say('Please try again with a real rank.')

                            else:
                                
                                this_game[player_id][this_character]['skills'].append(
                                    split_pair)

                                await bot.say('Skill %s successfully added.'
                                              %(split_pair[1]))

                    except:

                        await bot.say('It appears you control multiple characters. '
                              'Make sure to specify which character you want to '
                              "add skills to, by phrasing the command like so: "
                              ".addskill charactername: rank skill, etc.")


            else:

                    await bot.say("It appears you have not joined the game "
                                  "yet. Please join with the '.name' command.")
    gameload.save_game(all_games)       

def diceroll():

    diceNo = 1
    result = 0
    
    while diceNo <4:

            roll = numpy.random.randint(low=1,high=7)

            if roll in range(1,3):

                result = result -1
                
            elif roll in range(5,7):

                result = result +1
                
            diceNo += 1

    return result

def get_skill(result):

    for name, number in proficiency.items():

        if number == result:

            return name

def return_skills(game,player,character,message,result):

    #set them as if the character doesn't have the skill
    #at the start, in case they don't

    result_with_skill = result

    skill_name = get_skill(result_with_skill)

    for pair in game[player][character]['skills']:

        if message in pair:

            result_with_skill = result + proficiency[pair[0]]

            skill_name = get_skill(result_with_skill)
            
    #then we iterate over all of their skills, and if they do have that,
    #then we update result with skill and skill name
            
    return (result_with_skill, skill_name)
        
@bot.command(pass_context=True)
async def roll(ctx, *, message=None):

    if not message:

        result = diceroll()
        rank = get_skill(result)

        if result > 0:

            await bot.say("The dice yielded a result of %s (+%s)."
                              %(rank,result))

        else:

            await bot.say("The dice yielded a result of %s (%s)."
                              %(rank,result))
            
    else:

        channel_id = ctx.message.channel.id
        player_id = ctx.message.author
        player_name = ctx.message.author.name
        all_games = gameload.games['file']

        for key in all_games:

            if key == channel_id:

                this_game = all_games[key]

                if player_id in this_game:

                    characters = list(this_game[player_id].items())

                    if len(characters) == 1:
                    #if the player controls only one character

                        this_character = characters[0][0]
                        result = diceroll()
                        result_with_skill = return_skills(this_game,player_id,
                                                         this_character,message,
                                                         result)[0]
                        skill_name = return_skills(this_game,player_id,
                                                   this_character,message,
                                                   result)[1]

                        if result_with_skill < 0:
                
                            await bot.say("%s's (%s's) total is %s (%s), with "
                                          "a roll of %s."%(this_character,
                                                           player_name,
                                                           skill_name,
                                                           proficiency[skill_name],
                                                           result))
                        else:
                            await bot.say("%s's (%s's) total is %s (+%s), with a "
                                          "roll of %s."%(this_character,
                                                         player_name,
                                                         skill_name,
                                                         proficiency[skill_name],
                                                         result))
                    else:

                        try:

                            char_and_skill = message.split(':')
                            this_character = char_and_skill[0]
                            skill = char_and_skill[1]
                            s_skill = skill.lstrip().rstrip()
                            #otherwise the space after the colon is counted and
                            #the skill isn't found
                            result = diceroll()


                            result_with_skill = return_skills(this_game,
                                                              player_id,
                                                              this_character,
                                                              s_skill,result)[0]
                            skill_name = return_skills(this_game,player_id,
                                                       this_character,s_skill,
                                                       result)[1]

                            if result_with_skill < 0:
                        
                                await bot.say("%s's (%s's) total is %s (%s), with "
                                              "a roll of %s"%(this_character,
                                                              player_name,
                                                              skill_name,
                                                              proficiency[skill_name],
                                                              result))
                            else:
                                await bot.say("%s's (%s's) total is %s (+%s), with "
                                              "a roll of %s."%(this_character,
                                                               player_name,
                                                               skill_name,
                                                               proficiency[skill_name],
                                                               result))

                        except:

                            await bot.say("It appears you control multiple "
                                          "characters. "
                                          "Make sure to specify which character "
                                          "you want to roll for, by phrasing the "
                                          "command like so: '.roll charactername: "
                                          "skill'")

                else:

                    await bot.say("It appears you have not joined the game "
                                  "yet. Please join with the '.name' command.")

@bot.command(pass_context=True)
async def sheet(ctx):

    channel_id = ctx.message.channel.id
    player_id = ctx.message.author
    all_games = gameload.games['file']

    for key in all_games:

        if key == channel_id:

            this_game = all_games[key]
            
    if player_id in this_game:

        charsheet = list(this_game[player_id].items())
       
        #charsheet is a list which contains a tuple for each character
        #the player controls.
        
        #The tuple contains two elements (attribute),the character's name and
        #a dictionary. the dictionary has two keys: skills and fate points.
        #the value of skills is a list of lists, the latter being skill rank
        #and skill name. The value of fate points is an integer corresponding
        #to the character's current fate points. 
        
        for attribute in charsheet:
        
            message = 'Name: ' + attribute[0] + '\nSkills: '

            skill_list = attribute[1]['skills']
    
            for item in skill_list:

                message = message + str(item[0]) + ' ' + str(item[1])
            
                if skill_list.index(item) == len(skill_list)-1:

                    message = message + '.\n'

                else:

                   message = message + ', '

            try:

                message = message +'Fate Points: '+str(attribute[1]
                                                       ['fate points'])
                
            except KeyError:

                pass
            #the reason being that if the GM calls the sheet command, his
            #characters won't have the 'fate points' entry (since a GM's
            #characters don't have fate points), and this will raise a KeyError.
            #in the GM's case, we can safely ignore the fate points entry.
            
            await bot.say(message)
            #even if you control multiple characters, the bot says the message
            #as it iterates through, at the end of each 'sheet'.
    else:

        await bot.say("Please name your character with the '.name' command "
                      "before attempting to add a skill.")

def find_athletics(character_name,list_to_append,game):

    sheets = list(game.values())

    for dictionary in sheets:

        this_sheet = dictionary[character_name]

    for pair in this_sheet['skills']:

        if pair[1] == 'athletics':

            list_to_append.append(proficiency[pair[0]])

    if len(list_to_append) < 2:
    #it contains just the character's name (they don't have the athletics skill)

        list_to_append.append(proficiency['mediocre'])

def ties(initiative_list,game):

    init_counter = 0
    ath_counter = 0
    n = 0
    initiative_athletics = []
    positions = []

    while init_counter < len(initiative_list)-1:

        if initiative_list[init_counter][1] == initiative_list[init_counter+1][1]:

            character_name = initiative_list[init_counter][0]

            initiative_athletics.append([character_name])

            find_athletics(character_name,initiative_athletics[ath_counter],
                           game)

            initiative_list.pop(init_counter)
            #remove the name-skill pair from the first list, beacause we put it
            #in the second list
            initiative_list.insert(init_counter,[initiative_athletics
                                                 [ath_counter][0]])
            #updating the popped element so that first list length stays the
            #same, as we might need to keep looping through it and don't want
            #to mess up the counter

            positions.append(init_counter)
            #keep track of index

            init_counter += 1
            ath_counter += 1
            
            #update counter so we move on to comparing the next elements in the
            #first list (initiative_list)

            try:

                if initiative_list[init_counter][1] == initiative_list[init_counter+1][1]:

                    pass

                    #if the next element and the one after that are the same, we
                    #can do nothing, as we simply move back up to the first if
                    #check

                else:

                    character_name = initiative_list[init_counter][0]

                    initiative_athletics.append([character_name])

                    find_athletics(character_name,initiative_athletics[ath_counter],
                                   game)

                    initiative_list.pop(init_counter)

                    initiative_list.insert(init_counter,[initiative_athletics
                                                         [ath_counter][0]])

                    #if they're not the same, we still need to remove the next
                    #element, because it's the same as the element before it

                    #i need to make edits here, while i'm still in the main loop
                    #once we reach the end of the ties, now i need to reorder
                    #the tied ones, and then keep checking.

                    positions.append(init_counter)
                    #also note the index of this element

                    sorted_athletics = sorted(initiative_athletics,
                                              key=lambda x:x[1],reverse=True)

                    #sort characters that tied

                    for index in positions:

                        initiative_list.pop(index)

                        initiative_list.insert(index,sorted_athletics[n])

                        n += 1

                    #we remove the placeholder we inserted previously (since
                    #we know its position as we stored the counter in the
                    #positions list. At its position we insert the nth element
                    #of the sorted_athletics list.

                    sorted_athletics.clear()
                    initiative_athletics.clear()
                    positions.clear()
                    n = 0
                    ath_counter = 0

                    #clear everything so that they're blank in case there's
                    #more ties later on in the list. 
                    
                    init_counter += 1
                    #increment counter because if they're not the same,
                    #we want to move on to the next one        

            except IndexError:

                character_name = initiative_list[init_counter][0]
                                                
                initiative_athletics.append([character_name])

                find_athletics(character_name,initiative_athletics[ath_counter],
                               game)

                initiative_list.pop(init_counter)

                #if the next element is actually the last element in the list,
                #then we still need to remove it, because it's the same as the
                #previous element

                initiative_list.insert(init_counter,[initiative_athletics
                                                [ath_counter][0]])

                positions.append(init_counter)

                
                sorted_athletics = sorted(initiative_athletics,
                                              key=lambda x:x[1],reverse=True)

                for index in positions:

                    initiative_list.pop(index)

                    initiative_list.insert(index,sorted_athletics[n])

                    n += 1       

        else:

            init_counter += 1
    
def final_initiative(channel,sender):

    all_games = gameload.games['file']
    initiative = {}

    for key in all_games:

        if key == channel:

            this_game = all_games[key]
            
    if sender in this_game:

        for player in this_game:

            charsheet = list(this_game[player].items())

            for item in charsheet:
            #we iterate over character sheet because the GM will probably
            #control multiple characters

                character = item[0]
                skill_list = item[1]['skills']
                
                for pair in skill_list:

                    if pair[1] == 'notice':

                        initiative[character] = proficiency[pair[0]]

                if character not in initiative.keys():
                #e.g because they don't have the notice skill

                    initiative[character] = 0

    initiative_sorted = sorted(initiative.items(),key=lambda x:x[1],
                               reverse=True)
    
    ties(initiative_sorted,this_game)
    
    return initiative_sorted


@bot.command(pass_context=True)
async def initiative(ctx):

    channel_id = ctx.message.channel.id
    player_id = ctx.message.author

    initiative = final_initiative(channel_id,player_id)
    message = 'The order of initiative is: \n'

    for pair in initiative:

        message = message + pair[0] + ' ' + '-' + ' ' + str(pair[1]) + '\n'

    await bot.say(message)

@bot.command(pass_context=True)
async def fp(ctx, *, message:str):

    channel_id = ctx.message.channel.id
    player_id = ctx.message.author
    all_games = gameload.games['file']

    for key in all_games:

        if key == channel_id:

            this_game = all_games[key]

            if player_id in this_game:

                characters = list(this_game[player_id].items())
                this_character = characters[0][0]

                if len(characters) == 1:

                    if message.lower() == "set":

                       this_game[player_id][this_character]['fate points'] = 3

                       await bot.say("Character %s's fate points have been set "
                                     "to %s"%(this_character,
                                   this_game[player_id][this_character]['fate points']))
                       
                    elif message.lower() == "+":

                        fatepoints = this_game[player_id][this_character]['fate points']

                        fatepoints += 1

                        this_game[player_id][this_character]['fate points'] = fatepoints

                        await bot.say("Character %s's fate points have been set "
                                     "to %s"%(this_character,
                                   this_game[player_id][this_character]['fate points']))
                        
                    elif message.lower() == "-":

                        fatepoints = this_game[player_id][this_character]['fate points']

                        fatepoints = fatepoints-1

                        this_game[player_id][this_character]['fate points'] = fatepoints

                        await bot.say("Character %s's fate points have been set "
                                     "to %s"%
                                  (this_character,
                                   this_game[player_id][this_character]['fate points']))
            
                    else:

                        await bot.say("The valid commands for '.fp' are 'set', "
                                      "'+' and '-'")

                else:

                    await bot.say("It appears you control multiple characters. "
                                  "The GM has a pool of fate points equals to "
                                  "one times the number of players, which "
                                  "replenishes at the start of each scene.")
            else:

                await bot.say("It appears you are not in this game. Please join"
                              " the game with the '.name' command.")

    gameload.save_game(all_games)

@bot.command(pass_context=True)
async def help(ctx):

    channel_id = ctx.message.channel.id
    player_id = ctx.message.author
    all_games = gameload.games['file']
    match = False
    embed = discord.Embed(color = 16777215)

    embed.set_author(name = 'Commands list:')
    embed.add_field(name ='.greetings', value = 'Greets you.')
    embed.add_field(name='.initialize',
                    value='Initializes the game. There can be only one game '
                    'per channel. You must initialize a game to have access to '
                    'all other commands.')
    embed.add_field(name='.name character name',value='Gives your character a '
                    'name. Your character must be named before other '
                    'character-related commands will work. You may have '
                    'multiple characters, though this is usually only for the '
                    'GM.' )
    embed.add_field(name='.addskill rank skill, rank skill, etc',
                    value='Gives your character a skill(s). If you control '
                    'multiple characters, you must specify which character you '
                    "are giving the skill to, eg '.addskill Bob great fight .")
    embed.add_field(name='.roll skill',value='Rolls dice. It will add your rank '
                    'modifier to the roll if you specify which skill you '
                    'are rolling. If you control multiple characters, you '
                    'must specify which character you are rolling for.')
    embed.add_field(name='.sheet',value='Displays your character sheet(s).',
                    inline = False)
    embed.add_field(name='.initiative',value='Displays physical combat '
                    'initiative.')
    embed.add_field(name='.fp',value="Handles fate points. '.fp set' will set "
                    "your fate points to 3; '.fp +' increases your total fate "
                    "points by 1; '.fp -' decreases your total fate points by "
                    "1.")

    for key in all_games:

        if key == channel_id:

            this_game = all_games[key]
            match = True

            if player_id in this_game:

                    await bot.say(embed=embed)

            else:

                await bot.say("It appears you are not in this game. You may "
                              "join the game with the '.name' command.")
                #this mitigates the chance of 'randoms' from spamming the help
                #command in a channel that already knows what it's doing

    if match is False:
    #it is helpful for people who do not know how to create a game to be able
    #to view the help command

        await bot.say(embed=embed)

bot.run(token)
