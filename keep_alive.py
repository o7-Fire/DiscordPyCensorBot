from flask import Flask
from threading import Thread
import urllib.request
import os
import time
import random
app = Flask('')
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        #'Authorization': os.getenv('o7APIKey'),
 }
url = os.getenv("o7API") + "/api/json/graphical"


def main():
  return fetch(url)

def assad(path):
  return path +" assad" + str(random.randint(60, 250))

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def all_routes(path):
    if path.startswith('assad'):
      return assad(path)
    else:
      return main()


def fetch(url):
  try:
   req = urllib.request.Request(url, headers=hdr)
   response = urllib.request.urlopen(req)
   return str(response.read().decode())
  except Exception as e:
    return str(e)

def alive():
  print("ALIVEEEEEE")
  while True:
    time.sleep(int(random.randint(16, 25)))
    try:
      print(fetch("https://o7-Fire-API-Java-Replit.o7fire.repl.co"))
    except Exception as e:
      print(e)

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()
  aliveT = Thread(target=alive)
  aliveT.start()
