
from flask import Blueprint
from flask import render_template

bp = Blueprint("body", __name__)


@bp.route("/")
def index():
    return render_template("body/index.html")
