"""
Code in this file keeps bot alive if you host it in a free hosting server.
You need to register somewhere in free site like 'system monitor', what will send a requests to your app.
App in separate tread will cath this requests, hosting will see that you are doing something with code, like it's
always open in your browser.
"""

from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
  return "I'm alive"


def run():
  app.run(host='0.0.0.0', port=80)


def keep_alive():
  t = Thread(target=run)
  t.start()
