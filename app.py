import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/appliance")
def appliance():
    data = []
    with open("data/appliances.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("appliance.html", appliances=data)


@app.route("/share", methods=["GET", "POST"])
def share():
    categories = mongo.db.category.find().sort("category_name", 1)
    types = mongo.db.type.find().sort("type_name", 1)
    if request.method == "POST":
        recipe = {
                "recipe_name": request.form.get("recipe_name"),
                "type": request.form.get("type"),
                "category": request.form.get("category"),
                "instructions": request.form.getlist("instructions"),
                "ingredients": request.form.getlist("ingredients"),
                "Photo": request.form.get("photo")
            }
        mongo.db.recipes.insert_one(recipe)
        return redirect(url_for('home'))

    return render_template("share.html", categories=categories, types=types)


@app.route("/find")
def find():
    recipes = mongo.db.recipes.find()
    return render_template("find.html", recipes=recipes)


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    print(recipe)
    return render_template('recipe.html', recipe=recipe)


@app.route('/update/<recipeId>')
def update(recipeId):
    update = mongo.db.recipes.find_one({"_id": ObjectId(recipeId)})
    categories = mongo.db.category.find().sort("category_name", 1)
    types = mongo.db.type.find().sort("type_name", 1)
    all_ingredients = range(0, len(update['ingredients']))
    all_instructions = range(0, len(update['instructions']))
    return render_template("update.html",
                            recipe=update,
                            categories=categories,
                            types=types,
                            all_ingredients=all_ingredients,
                            all_instructions=all_instructions)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
