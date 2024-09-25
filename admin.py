from flask import Flask, redirect, render_template
from func import *

app = Flask("__main__")

@app.route("/")
def admin():
    return render_template("admin.html", reports=show_reports(), ratings=show_ratings())

@app.route("/ignore-<_id>")
def ignore(_id):
    delete(_id)
    return redirect("/")

@app.route("/resolve-<_id>")
def resolve(_id):
    act(_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5001)