import random
from flask import g, Flask, render_template
import sqlite3

app = Flask(__name__)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("users.db")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# Our old method
# @app.route("/")
# def hello():
#     return "Hello World!"

# Basic HTML Template
# names = ["John", "Jane", "Joe"]
# @app.route("/")
# def hello():
#     return render_template("index.html", names=names)

@app.route("/")
def index():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    user_names = []
    for user in users:
        user_names.append(user[1])
    return render_template("index.html", names=user_names)


@app.route("/about")
def about():
    return "This is a basic Flask website"


@app.route("/fact")
def fact():
    facts = [
        "The first computer bug was an actual bug",
        "The first computer virus was created in 1983",
        "The first computer virus was created in 1983",
    ]

    return random.choice(facts)


@app.route("/user/<username>")
def username(username):
    return f"Hello {username}"


if __name__ == "__main__":
    app.run(debug=True)
