"""
https://flask.palletsprojects.com/en/2.0.x/quickstart/
"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


"""
To run the application, use the flask command or python -m flask. Before you can do that you need to tell your terminal 
the application to work with by exporting the FLASK_APP environment variable:

$ export FLASK_APP=hello  # hello=hello.py, i.e. __name__ of this file, but this is not required in my run
$ flask run
"""

"""
To enable all development features, set the FLASK_ENV environment variable to development before calling flask run.

$ export FLASK_ENV=development
$ flask run
"""
