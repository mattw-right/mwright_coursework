from flask import Flask
from flask import render_template, request, g, url_for, redirect
from flask import Blueprint
from recommend.auth import login_required


app = Flask(__name__)

bp = Blueprint("my_profile", __name__, url_prefix="/my_profile")

@bp.route('/')
@login_required
def index():
    '''Renders the initial search page of the app'''
    return render_template('my_profile.html')

