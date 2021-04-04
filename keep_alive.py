from flask import Flask
from threading import Thread
import urllib.request
import os
import time
app = Flask('')
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        'Authorization': os.getenv('o7APIKey'),
 }
url = "https://o7-api.glitch.me/api/json/graphical/classification/https://github.com/o7-Fire/General/raw/master/Human/Logo/o7A.png"
@app.route('/')
def main():
  return "Your bot is aliven't!<br>" + fetch(url) + '<br><img src="https://github.com/o7-Fire/General/raw/master/Human/Logo/o7A.png" alt="o7A.png">'

def fetch(url):
  req = urllib.request.Request(url, headers=hdr)
  response = urllib.request.urlopen(req)
  return str(response.read().decode())

def alive():
  while True:
    time.sleep(20)
    fetch(url)

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()
  aliveT = Thread(target=alive)
  aliveT.start()