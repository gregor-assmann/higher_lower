from threading import Lock
import uuid
from flask import Flask, jsonify, session, redirect, url_for, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path
import logging
import socket
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys
import os
import datetime

from randomgenerator import generate_nickname
from game import Game

# Import from util is scuffed because making it a module or package didnt work
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # project root: higher_lower
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from util.logger import Logger
from util import leaderboard_handler
from util import yamlloader
from util import database_handler
from util import bson_handler


dirname = str(Path(__file__).parent.parent)

games = {}
games_lock = Lock() # to prevent simultaneous access to games dict from cleanup and main thread

#log = logging.getLogger('werkzeug')
#log.setLevel("ERROR")

LOGGER = Logger

ipaddress = socket.gethostbyname(socket.gethostname())
port=8000
LOGGER.log("Server", f"Server Running on http://{ipaddress}:{8000}")


def cleanup_games():
   
   """
   Cleans up expired games.
   """

   with games_lock:
      for game in list(games.items()):
         if game[1].expired():
            LOGGER.log("Game", "Game has expired.")
            games.pop(game[0], None)
         

app = Flask(__name__)
app.secret_key = "jalkdfekllypkekdkdpqwpeioxyvenljjlkjnsnvnasvnela"


@app.route("/")
def index():
   
   """
   #### Index/Home Route 

   Handles updating the Leaderboard after finishing a game. <br>
   Serves the Index Html.

   """

   sesssionID = session.get('sessionID')
   if sesssionID is None:
     session['sessionID'] = uuid.uuid4()

   with games_lock:
      #Add score of last game if not first game
      firstgame =  True if session['sessionID'] not in games else False
      lastScore = 0 if firstgame else games[session['sessionID']].score
      
      #leaderboard logic
      if not firstgame: #leaderboard update
         currentgame = games[session['sessionID']]
         lb_handler.add_score(difficulty=currentgame.difficulty, entry={"name" : session.get('name'), "score": lastScore, "timestamp": datetime.datetime.now()})
         LOGGER.success("Leaderboard", f"Updated: Difficulty:{currentgame.difficulty}, Name:{session.get('name')}, Score:{lastScore}")

      leaderBoardData = lb_handler.get_top_scores_dict(difficulty="all", limit=5) # get all leaderboards from leaderboard.db

      if not firstgame: # adding own score and name to leaderboard data if not first game
         difficulty = games[session['sessionID']].difficulty
         leaderBoardData["own_name"] = session.get('name')
         leaderBoardData["own_score"] = lastScore
         leaderBoardData["own_difficulty"] = difficulty
         leaderBoardData["own_position"] = lb_handler.get_position(difficulty=difficulty, score=lastScore)

        # config for difficulty selector
      difficulties = ["normal", "hard", "extreme"]
      difficulty_names = ["Normal", "Hard", "Extrem"]

      games.pop(session['sessionID'], None) # remove old game if exists
      return render_template("index.html", firstGame = firstgame, difficulties=difficulties, difficulty_names=difficulty_names, leaderBoardData=leaderBoardData)


@app.route("/new_game", methods = ["POST"])
def new_game():
   
   """
   #### Post-Endpoint for creating a new game

   Handles setting the username (also random generation) and difficulty <br>
   Handles the adding of the new game to the games dictionary.
   
   """

   if session["sessionID"] is None:
      LOGGER.failure("New Game", "Invalid Session ID")
      return redirect(url_for("index"))
   else:  
      #set player name
      name = request.form['username']
      session['name'] = name if name != "" else generate_nickname(dirname + r"/server/words.json")

      #set game difficulty
      difficulty = request.form["difficulty"]
      #create new game and add to list of games: games
      game = Game(difficulty=difficulty)
      with games_lock: games[session['sessionID']] = game

      LOGGER.success("New Game", f"Name: {session["name"]}, Difficulty: {difficulty}, SessionID: {session["sessionID"]}")   
    
      return redirect(url_for('game'))


@app.route("/game")
def game():
   
   """
   #### Game Route

   Serves the Game Html<br>
   Redirects the user if he reloads the page after losing
   """

   with games_lock:
      if "sessionID" not in session or session['sessionID'] not in games:
         LOGGER.failure("Game", "Invalid Session or sessionID")
         return redirect(url_for('index'))
      else:
         currentGame = games[session['sessionID']]
         if currentGame.gameOver:
            LOGGER.log("Game", "Redirecting GameOver on Reload")
            return redirect(url_for('index'))
         return render_template("game.html", **currentGame.toDict(True))


@app.route("/guess", methods = ['POST'])
def guess():
   
   """
   #### Post-Endpoint for submiting a guess

   Handles guess logic and returns new products after each guess.<br>
   Redirects if accessed without a valid session or after the game is over.

   """

   LOGGER.request("Guess", "Guess Submitted", "POST")

   with games_lock:
      #Check if session and game exist
      if "sessionID" not in session or session['sessionID'] not in games:
         return redirect(url_for('index'))
      else:
         currentGame = games[session['sessionID']]
         if currentGame.gameOver:
            return redirect(url_for("index"))
         user_guess = request.json['guess']
         guessed_correctly = currentGame.checkGuess(user_guess)
         currentGame.nextProduct()
         dict = currentGame.toDict(True)
         #get user guess from form
         if guessed_correctly: # if correct guess deliver new product
            currentGame.score += 1            
            dict['correct'] = True
            return jsonify(dict) # censor next price
         else:
            dict['correct'] = False
            currentGame.gameOver = True
            return jsonify(dict)

@app.route("/stats")
def stats():
   return render_template("stats.html")

@app.route("/test")
def test():
   """
   Debugging to test sessions
   """
   name = session["name"]
   return name

# setup db connections and products

config = yamlloader.load_config(yaml_file="game_config.yaml")
db_uri = config["db"]["link"].replace("<Password>", config["db"]["password"])
client = MongoClient(db_uri, server_api=ServerApi('1'))
lb_handler = leaderboard_handler.Leaderboardhandler(client)
lb_handler.test_connection()

# creates a local dump of the products database
db_handler = database_handler.DatabaseHandler(client=client)
db_handler.test_connection()
local_db_handler = bson_handler.BsonHandler(db_handler=db_handler)
local_db_handler.create_local_dump()



# Garbage collection to clean expired games each minute, seperate Thread
sheduler = BackgroundScheduler()
sheduler.add_job(func=cleanup_games, trigger="interval", minutes=1)
sheduler.start()


if __name__ == '__main__':
   app.run(debug = True)
   