from flask import Blueprint

auth = Blueprint("auth", __name__)

# We import later to avoid circular dependencies.
from . import views
