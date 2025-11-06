from pathlib import Path
import datetime

from next_product_getter import Product, ProductCollection, Difficulty
from randomgenerator import generate_parceltime


dirname = str(Path(__file__).parent.parent)

class Game:
   def __init__(self, difficulty, article_file_path = None):
      self.score = 0
      self.difficulty = difficulty
      self.collection = ProductCollection(config_path="game_config.yaml", file_path=(dirname + r'/scraper/articles.json') if article_file_path is None else article_file_path)
      
      self.productLast = self.collection.next_product()
      self.productNext = self.collection.next_product()

      self.LastParcelTime = generate_parceltime()
      self.NextParcelTime = generate_parceltime()

      self.nextProduct()

      self.gameOver = False
      self.expiresAt = datetime.datetime.now() + datetime.timedelta(minutes=5) # game expires in 30 minutes
   

   def expired(self):
      """
      Checks if the current game is expired.
      """
      return datetime.datetime.now() > self.expiresAt
   
   def extend_time(self, minutes=5):
      """
      Extends time until expiration by the given minutes.

      :param minutes: Amount to extend the expiration time by, default: `minutes = 5`
      """
      self.expiresAt = datetime.datetime.now() + datetime.timedelta(minutes=minutes)



   def nextProduct(self):
      
      """
      Generates the next Product based on the Games difficulty level and the previous product.
      """

      diff = Difficulty()
      if self.difficulty == "normal" : diff = diff.normal
      if self.difficulty == "hard"   : diff = diff.hard
      if self.difficulty == "extreme": diff = diff.extreme

      self.productLast = self.productNext
      self.productNext = self.collection.next_product(self.productLast, difficulty=diff)

      self.LastParcelTime = self.NextParcelTime
      self.NextParcelTime = generate_parceltime()
   
   def checkGuess(self, userGuess):
      
      """
      Checks a guess and returns if its correct. If the prices of 2 given Products are identical it always returns `True`
      """

      self.extend_time()

      rightGuess = ""
      if (self.productNext.price > self.productLast.price):
         rightGuess = "higher"
      elif (self.productNext.price < self.productLast.price):
         rightGuess = "lower"
      else: 
         return True # if prices are equal always correct
      if userGuess == rightGuess:
         return True
   
   def toDict(self, CensorNextPrice = True):
      
      """
      Converts a game to a Dictionary to be send to the client. Censors the next products price if game is still going.
      """

      return {
         "score": self.score,
         "productLast_brand": self.productLast.brand,
         "productLast_price": self.productLast.price,
         "productLast_link": self.productLast.link,
         "productLast_name": self.productLast.name,
         "productLast_img": self.productLast.img,
         "productLast_high_q_img": self.productLast.high_q_img,
         "productLast_parcel_time": self.LastParcelTime,

         "productNext_brand": self.productNext.brand,
         "productNext_price": self.productNext.price if not CensorNextPrice else "???",
         "productNext_link": self.productNext.link if not CensorNextPrice else None,
         "productNext_name": self.productNext.name,
         "productNext_img": self.productNext.img,
         "productNext_high_q_img": self.productNext.high_q_img,
         "productNext_parcel_time": self.NextParcelTime,
      }