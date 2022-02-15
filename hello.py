"""
https://flask.palletsprojects.com/en/2.0.x/quickstart/
"""

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

"""
To run the application, use the flask command or python -m flask. Before you can do that you need to tell your terminal 
the application to work with by exporting the FLASK_APP environment variable:

$ export FLASK_APP=hello
$ flask run

In fact, above is not necessary because hellp.py is the default value for the "FLASK_APP" environment variable.
If you rename hello.py to hello2.py, then you will see the following error message:

    Error: Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, 
    and a "wsgi.py" or "hello.py" module was not found in the current directory.
"""

"""
To enable all development features, set the FLASK_ENV environment variable to development before calling flask run.

$ export FLASK_ENV=development
$ flask run
"""


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


"""
HTML Escaping
When returning HTML (the default response type in Flask), any user-provided values rendered in the output must be
escaped to protect from injection attacks. HTML templates rendered with Jinja, introduced later, will do this automatically.

escape(), shown here, can be used manually. It is omitted in most examples for brevity, but you should always be aware
of how you’re using untrusted data.
"""


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


"""
Variable Rules
You can add variable sections to a URL by marking sections with <variable_name>. Your function then receives the
<variable_name> as a keyword argument. Optionally, you can use a converter to specify the type of the argument like
<converter:variable_name>.

Note by Han:
http://127.0.0.1:5000/path will route to above "hello" call because it is unable to resolve argument
"""


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


"""
Unique URLs / Redirection Behavior
The following two rules differ in their use of a trailing slash.

The canonical URL for the projects endpoint has a trailing slash. It’s similar to a folder in a file system. 
If you access the URL without a trailing slash (/projects), Flask redirects you to the canonical URL with the trailing 
slash (/projects/).

Note by Han: http://127.0.0.1:5000/projects will route to http://127.0.0.1:5000/projects/

The canonical URL for the about endpoint does not have a trailing slash. It’s similar to the pathname of a file. 
Accessing the URL with a trailing slash (/about/) produces a 404 “Not Found” error. 
This helps keep URLs unique for these resources, which helps search engines avoid indexing the same page twice.
"""


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


def valid_login(username, password):
    return username == 'han' and password == 'Pa$$w0rd'


def log_the_user_in(username):
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],  # make sure content-type is 'multipart/form-data',
                       request.form['password']):  # NOT 'application/json'
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


"""
Rendering Templates
Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the HTML escaping on your own to keep the application secure. Because of that Flask configures the Jinja2 template engine for you automatically.

To render a template you can use the render_template() method. All you have to do is provide the name of the template and the variables you want to pass to the template engine as keyword arguments. Here’s a simple example of how to render a template:
"""


@app.route('/hi/')
@app.route('/hi/<name>')
def hi(name=None):
    return render_template('hi.html', name=name)


"""
APIs with JSON
A common response format when writing an API is JSON. It’s easy to get started writing such an API with Flask. If you return a dict from a view, it will be converted to a JSON response.
"""


@app.route("/me")
def me_api():
    return {
        "username": "han",
        "theme": "blackandwhite"
    }
