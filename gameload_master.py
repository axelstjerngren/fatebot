import os
import pickle

games = {}
games_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'all_games.txt')
#path to this python file. 
#the text file is used for storing information about games, so that groups can
#resume playing seamlessly even if the bot goes offline.

def create_file():

    games_file = open(games_path,'wb')
    games_file.close()

def load():

    create_file()

    if os.path.getsize(games_path) == 0:

            pickle.dump({},open(games_path,'wb'))

            games['file'] = pickle.load(open(games_path,'rb'))

    else:

        games['file'] = pickle.load(open(games_path,'rb'))

def save_game(dictionary):

        pickle.dump(dictionary,open(games_path,'wb'))

