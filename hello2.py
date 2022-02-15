"""
https://flask.palletsprojects.com/en/2.0.x/server/
"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World2!</p>"


@app.route("/<name>")
def hello(name):
    return f"Hello2, {escape(name)}!"


if __name__ == "__main__":
    app.run(debug=True)
