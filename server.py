import sys, time

from flask import Flask, send_from_directory, jsonify, request, render_template

from random import randint

app = Flask(__name__, static_folder='views')

# - - - - - - - - - - - - - - - - 
# Routes
# - - - - - - - - - - - - - - - - 

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/api/bid/", methods=["GET"])
def numberOfSpadesGet():
  return "Use POST"

@app.route("/api/bid/", methods=["POST"])
def numberOfSpadesResponse():
  data = request.get_json()
  if data["strategy"] == "numberOfSpades":
    #print(data["handCards"])
    #for d in data:
    #  print(d);
    #print("");
    spades = 0;
    for i in range(0, len(data["handCards"])):
      if (data["handCards"][i]["suitName"] == "spades"):
        spades += 1
    if spades == 0:
      spades = "Nil"
  responseJSON = jsonify({"bid": spades})
  #time.sleep(1)
  return responseJSON

@app.route("/api/play/", methods=["GET"])
def randomGet():
  return "Use POST"

@app.route("/api/play/", methods=["POST"])
def randomIndexResponse():
  data = request.get_json()
  if data["strategy"] == "random":
    #print(data["handCards"])
    #for d in data:
    #  print(d);
    #print("");
    legalCards = []
    for i in range(0, len(data["handCards"])):
      if (data["handCards"][i]["legal"] == True):
        legalCards.append(i)
    randomIndex = legalCards[randint(0,len(legalCards) - 1)]
    print(data["handCards"][randomIndex]["fullPrintableName"] + ": " + str(randomIndex))
  responseJSON = jsonify({"index": randomIndex})
  #time.sleep(1)
  return responseJSON

@app.route("/api/trick-taker/", methods=["POST"])
def logTrickWinner():
  print("TRICK TAKER!!")
  data = request.get_json()
  print(data["winnerId"])
  print(data["gameId"])
  return "OK"

@app.route("/api/hand-score/", methods=["POST"])
def logHandScore():
  data = request.get_json()
  print(data["scoreChange"])
  print(data["bagsChange"])
  print(data["playerId"])
  print(data["gameId"])
  return "OK"

@app.route("/api/final-score/", methods=["POST"])
def logFinalScore():
  print("FINAL SCORE!!")
  data = request.get_json()
  print(data["gameId"])
  print(data["playerId"])
  print(data["finalScore"])
  print(data["finalBags"])
  print(data["winner"])
  return "OK"


# Public Directory:

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
