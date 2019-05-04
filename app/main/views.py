from datetime import datetime
from ..email import send_email
from flask import render_template, session, redirect, url_for, current_app
from .forms import NameForm
from .. import db
from . import main
from ..models import User


@main.route("/")
def index():
    return render_template('index.html')
