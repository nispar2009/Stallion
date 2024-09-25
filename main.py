from flask import Flask, render_template, redirect, request, abort
from func import *
from random import choice

app = Flask("__main__")

@app.errorhandler(404)
def not_found(e):
    return render_template("msg.html", title="Error 404", msg="The URL you are searching for does not exist, or it has been deleted"), 404

@app.errorhandler(500)
def server_fault(e):
    return render_template("msg.html", title="Error 500", msg="The server could not process your request. This could be due to repetitive/long data or a fault on our side. If a form caused this error, please check your input and shorten it if possible"), 500

@app.route("/")
def index():
    user_feed = feed()
    quote = choice(quotes)

    return render_template("index.html", feed=user_feed, quote=quote)

@app.route("/post-<_id>")
def post(_id):
    if fetch(_id) == 404:
        abort(404)
        
    return render_template("post.html", post=fetch(_id), js="")
    
@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return render_template("write.html")

    author = request.form["author"]
    title = request.form["title"]
    content = request.form["content"]
    topic = request.form["topic"]
    add_post(author, title, content, topic)

    return render_template("msg.html", title="Post uploaded", msg="Your post has been successfully uploaded")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cal", methods=["GET", "POST"])
def cal():
    if request.method == "GET":
        return render_template("cal.html", overall_food=(food())[0], weight_food=(food())[1], muscle_food=(food())[2])
    
    item = request.form["item"]
    energy = request.form["energy"]
    protein = request.form["protein"]
    carbs = request.form["carbs"]
    fats = request.form["fats"]
    na = request.form["na"]
    add_food(item, energy, protein, carbs, fats, na)

    return redirect("/cal")

@app.route("/rate", methods=["GET", "POST"])
def rate():
    if request.method == "GET":
        return render_template("rate.html", ratings=show_ratings())
    
    author = request.form["author"]
    comment = request.form["comment"]
    stars = int(request.form["stars"])
    add_rating(author, comment, stars)

    return redirect("/rate")

@app.route("/like-<_id>")
def like(_id):
    add_like(_id)
    return render_template("post.html", post=fetch(_id), js=f"like({_id})")

@app.route("/report", methods=["POST"])
def report():
    item = request.form["item"]
    email = request.form["email"]
    add_report(item, email)
    return render_template("msg.html", title="Reported", msg="Your concern has been noted, and the accuracy of this data will be verified")

if __name__ == "__main__":
    app.run(port=5000)