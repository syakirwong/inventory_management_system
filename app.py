import peeweedbevolve
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

@app.before_request
def before_request():
   db.connect()

@app.after_request
def after_request(response):
   db.close()
   return response

@app.cli.command()
def migrate():
   db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/store")
def add_store():
   return render_template('store.html')

@app.route("/accept-add-store-request", methods=["POST"])
def receive_store():
   store_name = request.form['store_name']
   store = Store(name = store_name)
   store.save()
   return render_template('accept_store.html', store_name=store_name)

if __name__ == '__main__':
   app.run()
