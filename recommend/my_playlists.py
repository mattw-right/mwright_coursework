
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
    username = g.user["username"]
    db = get_db()
    playlists = db.execute('SELECT * FROM listener_profiles WHERE username=?', (username, )).fetchall()
    return render_template('my_playlists.html', playlists=playlists)

@bp.route('/<int:id>')
@login_required
def open_indv_playlist(id):
    '''Renders the my playlists of the app'''
    db = get_db()
    playlist = db.execute('SELECT * FROM listener_profiles WHERE id=?', (id, )).fetchone()
    playlist_items = []
    for i in playlist[3].split(';'):
        if i.split(':')[1] == 'artist':
            playlist_items.append(db.execute('SELECT artist, photo_link FROM artists WHERE uri=?', (i, )).fetchone())
        elif i.split(':')[1] == 'track':
            playlist_items.append(db.execute('SELECT title, photo_link, artist_name, preview_url FROM songs WHERE uri=?', (i, )).fetchone())
    for i in playlist_items: print(list(i))
    return render_template('playlist.html', playlist_title=playlist[2], playlist_items=playlist_items)
