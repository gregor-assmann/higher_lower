from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from datetime import datetime
from datetime import timedelta

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
    
# TODO make all the stat endpoints return value label list pairs for ease of use

    def get_games_by_name(self):
        
        """
        Returns a list of the top ten entries by Played Games by Name.<br>
        Entries contain a `name`, `total` and `difficulties` field. <br>
        The `difficulties` field contains the count by difficulty.
        """

        pipeline=[
            {
                '$group': {
                    '_id': '$name', 
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    'count': -1
                }
            }, {
                '$limit': 10
            }, {
                '$lookup': {
                    'from': 'total', 
                    'localField': '_id', 
                    'foreignField': 'name', 
                    'as': 'difficulties'
                }
            }, {
                '$unwind': '$difficulties'
            }, {
                '$group': {
                    '_id': {
                        'name': '$_id', 
                        'difficulty': '$difficulties.difficulty'
                    }, 
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$group': {
                    '_id': '$_id.name', 
                    'difficulties': {
                        '$push': {
                            'difficulty': '$_id.difficulty', 
                            'count': '$count'
                        }
                    }
                }
            }
        ]
        try:
            collection_name = self.db_name["total"]
            entries = list(collection_name.aggregate(pipeline=pipeline))
            for entry in entries:
                difficulties_temp = entry["difficulties"]
                entry["difficulties"] = {}
                entry["name"] = entry["_id"]
                del entry["_id"]
                total = 0
                for diff in difficulties_temp:
                    entry["difficulties"][diff["difficulty"]] = diff["count"]
                    total += diff["count"]
                entry["total"] = total
            entries.sort(key=lambda x: -x["total"]) # minus to reverse the order from greates to lowest
            return entries
        except:
            LOGGER.error("Getting data", "Failed to get Games by name")


    def get_total_score_by_date(self, timespan = 7):
        current_date = datetime.now()
        past_date = current_date - timedelta(timespan)
        pipeline = [
            {
                "$match": {
                    "timestamp": {
                        "$gte": past_date
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$timestamp"
                        }
                    },
                    "totalScore": {
                        "$sum": "$score"
                    }
                }
            }
        ]


        try:
            collection_name = self.db_name["total"]
            games = list(collection_name.aggregate(pipeline=pipeline))
            #create empty game dict for the past days within the timespan
            game_dict = {}
            for i in range(timespan):
                day = past_date + timedelta(days=i + 1) 
                game_dict[day.date().__str__()] = 0

            # fill the game dict with the total scores
            for game in games:
                game_dict[game["_id"]] = game["totalScore"]
            #return game_dict  #returns the dict as is

            labels = []
            values = []
            for k, v in game_dict.items():
                labels.append(k)
                values.append(v)
            return {"labels" : labels, "values" : values}

        except:
            LOGGER.error("Getting data", "Failed to get score by date")

    def get_games_by_date(self, timespan = 7):

        current_date = datetime.now()
        past_date = current_date - timedelta(timespan)
        
        # vlt nochmal aufräumen wenn zeit und lust
        pipeline = [
            {
                '$match': {
                    'timestamp': {
                        '$gte': past_date
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'date': {
                            '$dateToString': {
                                'format': '%Y-%m-%d', 
                                'date': '$timestamp'
                            }
                        }, 
                        'difficulty': '$difficulty'
                    }, 
                    'totalGames': {
                        '$sum': 1
                    }
                }
            }, {
                '$group': {
                    '_id': '$_id.date', 
                    'gamesPerDay': {
                        '$sum': '$totalGames'
                    }, 
                    'difficultyDistribution': {
                        '$push': {
                            'difficulty': '$_id.difficulty', 
                            'totalGames': '$totalGames'
                        }
                    }
                }
            }
        ]

        try:
            collection_name = self.db_name["total"]
            games = list(collection_name.aggregate(pipeline=pipeline))

            #create empty game dict for the past days within the timespan
            game_dict = {}
            for i in range(timespan):
                day = past_date + timedelta(days=i + 1) 
                game_dict[day.date().__str__()] = {"total": 0, "normal": 0, "hard": 0, "extreme": 0}

            for entry in games:
                diff_list_as_dict = {}
                for diff in entry["difficultyDistribution"]:
                    diff_list_as_dict[diff["difficulty"]] = diff["totalGames"]
                day_dict = {
                    "total": entry["gamesPerDay"],
                    "normal": diff_list_as_dict["normal"] if "normal" in diff_list_as_dict else 0,
                    "hard": diff_list_as_dict["hard"] if "hard" in diff_list_as_dict else 0,
                    "extreme": diff_list_as_dict["extreme"] if "extreme" in diff_list_as_dict else 0}
                game_dict[entry["_id"]] = day_dict

            return game_dict
        except:
            LOGGER.error("Getting data", "Failed to get score by date")
