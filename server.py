import sys

from flask import Flask, send_from_directory, jsonify, request, render_template

from random import randint

app = Flask(__name__, static_folder='views')

# - - - - - - - - - - - - - - - - 
# Routes
# - - - - - - - - - - - - - - - - 

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/api/bid/number-of-spades/", methods=["GET"])
def numberOfSpadesGet():
  return "Use POST"

@app.route("/api/bid/number-of-spades/", methods=["POST"])
def numberOfSpadesResponse():
  data = request.get_json()
  print(data["handCards"])
  spades = 0;
  for i in range(0, len(data["handCards"])):
    if (data["handCards"][i]["suitName"] == "spades"):
      spades += 1
  if spades == 0:
    spades = "Nil"
  responseJSON = jsonify({"bid": spades})
  return responseJSON

@app.route("/api/play/random/", methods=["GET"])
def randomGet():
  return "Use POST"

@app.route("/api/play/random/", methods=["POST"])
def randomIndexResponse():
  data = request.get_json()
  print(data["handCards"])
  legalCards = []
  for i in range(0, len(data["handCards"])):
    if (data["handCards"][i]["legal"] == True):
      legalCards.append(i)
      print(i)
  randomIndex = legalCards[randint(0,len(legalCards) - 1)]
  responseJSON = jsonify({"index": randomIndex})
  return responseJSON


# Public Directory:

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
