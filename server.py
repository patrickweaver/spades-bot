import sys, time, datetime
import os

from flask import Flask, send_from_directory, jsonify, request, render_template

from flask_pymongo import PyMongo

from random import randint
import pprint

app = Flask(__name__, static_folder='views')

app.config["MONGO_URI"] = os.environ['MONGO_URI']
mongo = PyMongo(app)

# - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - 
# Routes
# - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - -

@app.route("/")
def home():
  #print(datetime.datetime.now())
  #time = {"request_time": datetime.datetime.now()}
  #times = mongo.db.times
  #time_id = times.insert_one(time).inserted_id
  #print(time_id);
  return render_template('index.html')



# Bid GET placeholder
@app.route("/api/bid/", methods=["GET"])
def numberOfSpadesGet():
  return "Use POST"

# - - - - - - - - - - - - -
# Bot Bid:
# - - - - - - - - - - - - -
@app.route("/api/bid/", methods=["POST"])
def numberOfSpadesResponse():
  data = request.get_json()
  bid = False
  
  # Strategy "numberOfSpades"
  # Bid the number of spades in hand
  if data["strategy"] == "numberOfSpades":
    spades = 0
    for i in range(0, len(data["handCards"])):
      if (int(data["handCards"][i]["value"]) > 39):
        spades += 1
    if spades == 0:
      spades = "Nil"
    bid = spades
    
  # Remove bids that haven't been placed yet
  for playerBid in ["bidLeftBid", "bidPartnerBid", "bidRightBid"]:
    if data[playerBid] == 0:
      del data[playerBid]
  
  # Add all cards to data
  for card in data["handCards"]:
    value = card["value"]
    data["card" + str(value)] = True
  del data["handCards"]
  
  # Send bid and data to DB
  data["bidSelfBid"] = bid
  if bid == "Nil":
    data["bidSelfBid"] = 0
  bids = mongo.db.bids
  bid_id = bids.insert_one(data).inserted_id       
  
  # Send response to spades server
  responseJSON = jsonify({"bid": bid})
  #time.sleep(1)
  return responseJSON



# Play GET placeholder
@app.route("/api/play/", methods=["GET"])
def randomGet():
  return "Use POST"



# - - - - - - - - - - - - -
# Bot Play:
# - - - - - - - - - - - - -
@app.route("/api/play/", methods=["POST"])
def randomIndexResponse():
  data = request.get_json()
  cardIndex = False
  
  # Strategy "random"
  # Randomly pick one of the legal cards
  if data["strategy"] == "random":
    legalCards = []
    for i in range(0, len(data["handCards"])):
      if (data["handCards"][i]["legal"] == True):
        legalCards.append(i)
    randomIndex = legalCards[randint(0,len(legalCards) - 1)]
    #print(data["handCards"][randomIndex]["fullPrintableName"] + ": " + str(randomIndex))
  responseJSON = jsonify({"index": randomIndex})
  cardIndex = randomIndex
  
  # Add card played to data
  data["playSelfPlay"] = data["handCards"][cardIndex]["value"]
  
  # Add all cards to data
  for card in data["handCards"]:
    value = card["value"]
    legal = 0
    if card["legal"]:
      legal = 1
    data["card" + str(value)] = legal
  del data["handCards"]
  

  # Remove bid order
  del data["bidSelfOrder"]
  
  # Send bid and data to DB
  plays = mongo.db.plays
  play_id = plays.insert_one(data).inserted_id 
  
  
  #time.sleep(1)
  return responseJSON



# - - - - - - - - - - - - -
# Trick Taker:
# - - - - - - - - - - - - -
@app.route("/api/trick-taker/", methods=["POST"])
def logTrickWinner():
  data = request.get_json()
  
  updated_plays = mongo.db.plays.update_many(
    {
      "gameId": data["gameId"],
      "handNumber": data["handNumber"],
      "trickNumber": data["trickNumber"]
    }, 
    {
      "$set": {"winner": 0}
    }
  )
  
  winner = mongo.db.plays.update_one(
    {
      "gameId": data["gameId"],
      "handNumber": data["handNumber"],
      "trickNumber": data["trickNumber"],
      "playerId": data["winnerId"]
    }, 
    {
      "$set": {"winner": 1}
    }
  )
  
  
  return "OK"

@app.route("/api/hand-score/", methods=["POST"])
def logHandScore():
  data = request.get_json()
  
  old_data = {
    "gameId": data["gameId"],
    "playerId": data["playerId"],
    "handNumber": data["handNumber"]
  }
  
  updated_data = {
    "scoreChange": data["scoreChange"],
    "bagsChange": data["bagsChange"],
    "tricksTaken": data["tricksTaken"]
  }
    
  updated_bids = mongo.db.bids.update_many(old_data, {"$set": updated_data})
  updated_plays = mongo.db.plays.update_many(old_data, {"$set": updated_data})
  
  return "OK"

@app.route("/api/final-score/", methods=["POST"])
def logFinalScore():
  data = request.get_json()
  
  old_data = {
    "gameId": data["gameId"],
    "playerId": data["playerId"]
  }
  
  updated_data = {
    "finalScore": data["finalScore"],
    "finalBags": data["finalBags"]
  }  
  
  updated_bids = mongo.db.bids.update_many(old_data, {"$set": updated_data})
  updated_plays = mongo.db.plays.update_many(old_data, {"$set": updated_data})
    
  return "OK"


# Public Directory:

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
