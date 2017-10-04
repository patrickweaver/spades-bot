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


@app.route("/api/random", methods=['GET', 'POST'])
def randomIndexResponse():
  data = request.get_json()
  legalCards = []
  for i in range(0, len(data["handCards"])):
    if (data["handCards"][i]["legal"] == True):
      legalCards.append(i)
  randomIndex = randint(0,len(legalCards) - 1);
  responseJSON = {"index": randomIndex}
  return jsonify(responseJSON)


# Public Directory:

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
