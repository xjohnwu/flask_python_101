from hello import app
from flask import url_for, request


def test_hello():
    """
    URL Building
    To build a URL to a specific function, use the url_for() function. It accepts the name of the function as its first argument and any number of keyword arguments, each corresponding to a variable part of the URL rule. Unknown variable parts are appended to the URL as query parameters.

    Why would you want to build URLs using the URL reversing function url_for() instead of hard-coding them into your templates?

    Reversing is often more descriptive than hard-coding the URLs.

    You can change your URLs in one go instead of needing to remember to manually change hard-coded URLs.

    URL building handles escaping of special characters transparently.

    The generated paths are always absolute, avoiding unexpected behavior of relative paths in browsers.

    If your application is placed outside the URL root, for example, in /myapplication instead of /, url_for() properly handles that for you.

    For example, here we use the test_request_context() method to try out url_for(). test_request_context() tells Flask to behave as though it’s handling a request even while we use a Python shell. See Context Locals.
    """
    with app.test_request_context():
        assert url_for('hello_world') == '/'  # argument is method name
        assert url_for('login') == '/login'
        assert url_for('login', next='/') == '/login?next=%2F'
        assert url_for('show_user_profile', username='John Doe') == '/user/John%20Doe'


def test_request_context():
    with app.test_request_context('/hello', method='POST'):
        # now you can do something with the request until the
        # end of the with block, such as basic assertions:
        assert request.path == '/hello'
        assert request.method == 'POST'
