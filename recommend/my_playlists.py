
from flask import Flask
from flask import render_template, request, g, url_for, redirect
from flask import Blueprint
from recommend.auth import login_required
from recommend.db import get_db, fetch_raw_listener_data

app = Flask(__name__)

bp = Blueprint("my_playlists", __name__, url_prefix="/my_playlists")

@bp.route('/')
@login_required
def index():
    '''Renders the my playlists of the app'''
    return render_template('my_playlists.html')