import sqlite3

class leaderBoard:
    def __init__(self, dbPath):
        print(dbPath)
        try:
            open(dbPath, 'x').close()
        except:
            pass
        self.conn = sqlite3.connect(dbPath, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS leaderboard (name TEXT, score INTEGER)")
        self.conn.commit()
    
    def add_score(self, name, score):
        self.cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, score))
        self.conn.commit()
    
    def get_top_scores(self, limit=5):
        self.cursor.execute("SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()
    
    def get_top_scores_dict(self, limit=5):
        scores = self.get_top_scores(limit)
        scoreDict = {}
        for i in range(len(scores)):
            scoreDict[f"name_{i+1}"] = scores[i][0]
        for i in range(len(scores)):
            scoreDict[f"score_{i+1}"] = scores[i][1]
        return scoreDict
    
    def get_position(self, score):
        self.cursor.execute("SELECT COUNT(*) FROM leaderboard WHERE score > ?", (score,))
        return self.cursor.fetchone()[0] + 1
    