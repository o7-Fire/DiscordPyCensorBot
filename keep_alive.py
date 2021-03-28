from flask import Flask
from threading import Thread
import urllib.request
import os
app = Flask('')
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        'Authorization': os.getenv('o7APIKey'),
 }
url = "https://o7-api.glitch.me/api/json/graphical/classification/https://cdn.discordapp.com/attachments/817424676762025987/824620368723574814/madattak_chan_manga.png"
@app.route('/')
def main():
  return "Your bot is aliven't!<br>" + fetch(url)

def fetch(url):
  req = urllib.request.Request(url, headers=hdr)
  response = urllib.request.urlopen(req)
  return str(response.read().decode())

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()