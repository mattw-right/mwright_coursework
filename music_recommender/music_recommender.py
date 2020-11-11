from flask import Blueprint

bp = Blueprint("music_recommender", __name__)


@bp.route("/")
def index():

    return 'Hello'