from flask import Flask
from threading import Thread
import urllib.request
app = Flask('')
url = "https://o7-api.glitch.me/api/json/graphical/classification/https://cdn.discordapp.com/attachments/817424676762025987/824620368723574814/madattak_chan_manga.png"
@app.route('/')
def main():
  return "Your bot is aliven't!<br>" +  str(urllib.request.urlopen(url).read().decode())

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()