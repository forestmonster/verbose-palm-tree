from flask import Blueprint

main = Blueprint("main", __name__)

# Import these /after/ the declaration above, to avoid circular dependencies.
from . import views, errors
from ..models import Permission
