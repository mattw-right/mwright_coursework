
from flask import Blueprint
from flask import render_template

bp = Blueprint("landing", __name__)


@bp.route("/")
def index():
    return render_template('landing_page.html')
