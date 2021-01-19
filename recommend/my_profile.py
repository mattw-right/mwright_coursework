from flask import Flask
from flask import render_template, g
from flask import Blueprint
from recommend.auth import login_required
from flask import request
from werkzeug.security import generate_password_hash
from recommend.validate import *
from music_recommender.db import get_db





app = Flask(__name__)

bp = Blueprint("my_profile", __name__, url_prefix="/my_profile")

@bp.route('/')
@login_required
def index():
    '''Renders the initial search page of the app'''
    return render_template('my_profile.html', username=g.user["username"])

def change_password():
    password = request.form["password"]
    password_verification = request.form["password_verification"]
    email = request.form['email']
    db = get_db()
    error = []

    if not password:
        error.append("Password is required")
    if not validate_password(password):
        error.append('That password is invalid')
        password = ''
    if is_common_password(password):
        error.append('That password is too common')
        password = ''
    if password != password_verification:
        error.append("Those passwords don't match")
    if error == []:
        # the name is available, store it in the database and go to
        # the login page
        db.execute("UPDATE user SET password=? WHERE username=?", (g.user["username"], generate_password_hash(password)),)
        db.commit()
        return render_template('my_profile.html', username=g.user["username"])
    else:
        return
