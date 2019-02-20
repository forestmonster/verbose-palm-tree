from flask import Flask
from flask import make_response
from flask import redirect

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hello world!</h1>"


@app.route("/user/<name>")
def user(name):
    return f"<h1>Hello {name}!</h1>", 401


@app.route("/setcookie")
def setCookie():
    response = make_response("<h1>Setting a cookie.</h1>")
    response.set_cookie("answer", "42")
    return response


@app.route("/send")
def send():
    return redirect("https://www.duckduckgo.com")
