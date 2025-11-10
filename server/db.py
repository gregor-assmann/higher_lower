import sqlite3

import sys
import os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # project root: higher_lower
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import util.logger as logger

LOGGER =  logger.Logger

"""

###############################################

                    UNUSED

Only as backup. Uses leaderboard_handler instead.

###############################################

"""


class leaderBoard:
    def __init__(self, dbPath):
        LOGGER.log("Leaderboard", f"Path: {dbPath}")
        try:
            open(dbPath, 'x').close()
        except:
            pass
        self.conn = sqlite3.connect(dbPath, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_leaderboard("normal")
        self.create_leaderboard("hard")
        self.create_leaderboard("extreme")

    def create_leaderboard(self, name):
        """
        Creates a leaderboard if it doesnt exist yet
        """
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS leaderboard_{name} (name TEXT, score INTEGER)")
        self.conn.commit()

    def add_score(self, difficulty, name, score):
        """
        Adds a `score` with the corresponding `difficulty` and `name` into the database.
        """
        self.cursor.execute(f"INSERT INTO leaderboard_{difficulty} (name, score) VALUES (?, ?)", (name, score))
        self.conn.commit()
    
    def get_top_scores(self, difficulty, limit=5):
        """
        Gets the top scores within a `limit`, for a `difficulty`.
        """
        self.cursor.execute(f"SELECT name, score FROM leaderboard_{difficulty} ORDER BY score DESC LIMIT ?", (limit,))
        data = self.cursor.fetchall()
        #ensures that if less entrys than limit empty tuples are created
        if len(data) < limit:
            missing = limit - len(data)
            for i in range(missing):
                data.append(("",""))
        return data
            

    
    def get_top_scores_dict(self, difficulty, limit=5):
        """
        Gets the top scores within a `limit`, for a `difficulty`. <br>
        Returns as a `dictionary` 
        """
        difficulties = []
        if difficulty == "all": difficulties = ["normal","hard", "extreme"]
        else: difficulties = [difficulty]

        scoreDict = {}
        for diff in difficulties:
            scores = self.get_top_scores(diff, limit)
            scoreDict[diff] = scores
            
        return scoreDict
    
    def get_position(self, difficulty, score):
        """
        Gets the position of a game based on `difficulty` and `score`
        """
        self.cursor.execute(f"SELECT COUNT(*) FROM leaderboard_{difficulty} WHERE score > ?", (score,))
        return self.cursor.fetchone()[0] + 1
    