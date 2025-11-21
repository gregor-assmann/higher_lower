from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo


import sys
import os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # project root: higher_lower
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from util import logger
LOGGER = logger.Logger

class Leaderboardhandler:

    def __init__(self, client:MongoClient):
        self.client:MongoClient = client
        self.db_name = self.client["Leaderboard"]

    def test_connection(self):

        """
        Tests the connection to the Database
        """

        try:
            self.client.admin.command('ping')
            LOGGER.success("Database", "Connected to MongoDB")
        except Exception as e:
            LOGGER.error("Database", "Error while connecting to MongoDB", e)

    def add_score(self, difficulty, entry):

        """
        Adds a score to the corresponding difficulty and pushes it to the Database
        """

        try:
            collection_name = self.db_name[difficulty]
            collection_name.insert_one(entry)
            collection_name = self.db_name["total"]
            entry["difficulty"] = difficulty
            collection_name.insert_one(entry)
            LOGGER.success("Writing data", f"Added a leaderboard entry.")
        except:
            LOGGER.error("Writing data", "Failed to write data in MongoDB")

    def get_top_scores(self, difficulty, limit=5):

        """
        Gets Gets the top scores within a `limit`, for a `difficulty`. <br>
        returns as a list of `dict` with 
        """

        try:
            collection_name = self.db_name[difficulty]
            entries = collection_name.find().sort("score", pymongo.DESCENDING).limit(limit)
            return entries
        except:
            LOGGER.error("Getting data", f"Failed to get top scores")
            return []

    def get_top_scores_dict(self, difficulty, limit=5):

        """
        Gets the top scores within a `limit`, for a `difficulty`. <br>
        Returns as a `dictionary` of difficulties with lists of tuples of name and score
        """

        difficulties = []
        if difficulty == "all": difficulties = ["normal","hard", "extreme"]
        else: difficulties = [difficulty]
        score_dict = {}
        try:
            for diff in difficulties:
                collection_name = self.db_name[diff]
                data = list(collection_name.find(projection={'_id': False}).sort("score", pymongo.DESCENDING).limit(limit))
                entries = []
                for entry in data:
                    entries.append((entry["name"], entry["score"]))
                if len(entries) < limit:
                    missing = limit - len(entries)
                    for i in range(missing):
                        entries.append(("",""))
                score_dict[diff] = entries
            return score_dict
        except:
            LOGGER.error("Getting data", f"Failed to get top scores")
            return []
        
    def get_position(self, difficulty, score):

        """
        Gets the top position one can get with a peticular score.
        """

        try:
            collection_name = self.db_name[difficulty]
            entries = list(collection_name.find().sort("score", pymongo.DESCENDING))
            for index, game in enumerate(entries):
                if game["score"]==score:
                    return index + 1
            return None
        except:
            LOGGER.error("Getting data", f"Failed to get top scores")
            return []
        