import peeweedbevolve
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from models import *

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

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

@app.route("/store", methods=["GET"])
def add_store():
   stores = Store.select()
   return render_template('store.html', stores=stores)

@app.route("/store/<int:id>")
def view_individual_store(id):
   store = Store.get_by_id(id)
   return render_template('view-store.html', store=store)

@app.route("/accept-add-store-request", methods=["POST"])
def receive_store():
   store_name = request.form['store_name']
   store = Store(name = store_name)
   store.save()
   return render_template('accept_store.html', store_name=store_name)

@app.route("/store/<int:id>/update", methods=["POST"])
def edit_store(id):
    store = Store(
        id=id,
        name=request.form['name']
    )
    if store.save(only=[Store.name]):
        flash("Your store's name has been updated!")
    else:
        flash("Unable to edit store name!")
    return redirect(url_for('add_store', id=id))

@app.route("/store/<int:id>/delete", methods=["POST"])
def delete_store(id):
    store = Store.get_by_id(id)
    if store.delete_instance(recursive=True):
        flash("Successfully deleted store!")
    else:
        flash("Unable to delete store!")
    return redirect(url_for('add_store'))

@app.route("/warehouse")
def add_warehouse():
   stores = Store.select()
   return render_template('warehouse.html', stores = stores)

@app.route("/accept-add-warehouse-request", methods=["POST"])
def receive_warehouse():
   store = Store.get_by_id(request.form['store_id'])
   warehouse_location = request.form['warehouse_location']
   warehouse = Warehouse(location = warehouse_location, store_id = store)
   warehouse.save()
   return render_template('accept_warehouse.html', location = warehouse_location, store = store)

if __name__ == '__main__':
   app.run()
