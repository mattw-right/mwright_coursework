
from recommend.api.api_call import create_api_call
from recommend.api.api_return_parser import *
from flask import Flask
from flask import render_template, request, g, url_for, redirect
from flask import Blueprint
from recommend.auth import login_required
from recommend.db import get_db, fetch_raw_listener_data

app = Flask(__name__)

bp = Blueprint("add_tastes", __name__, url_prefix="/add_tastes")

class Most_Recent_Return:
    '''Acts as a global variable, which is much harder to do in the Flask framework.
    It stores the raw results of the most recent search'''

    def __init__(self):
        self.x = False
        pass

    def set(self, x):
        self.x = x

    def get(self):
        return self.x

    def set_artists_and_tracks(self, tracks, artists):
        self.tracks = tracks
        self.artists = artists

    def get_artists_and_tracks(self):
        return self.artists, self.tracks

def sort_raw_listener_data(raw_data):
    raw_data = list(raw_data)
    structured_data = []
    for i in raw_data: structured_data.append(tuple(raw_data))
    tracks = []
    artists = []
    try:
        for i in structured_data[0]:
            if i[-1].split(':')[1] == 'track': tracks.append(i[2])
            else: artists.append(i[2])
        most_recent_return.set_artists_and_tracks(tracks, artists)
        return tracks, artists
    except:
        return [], []

def cut_off_length(list, max_length):
    output = []
    for i in list:
        if len(i) > max_length: output.append(i[:max_length])
        else: output.append(i)
    return output

most_recent_return = Most_Recent_Return()


@bp.route('/')
@login_required
def index():
    '''Renders the initial search page of the app'''
    tracks, artists = sort_raw_listener_data(fetch_raw_listener_data())
    tracks, artists = cut_off_length(tracks, 25), cut_off_length(artists, 25)
    return render_template('add_tastes.html', display_boolean='none', tracks=tracks, artists=artists)


def validate_query(query):
    '''Checks that (1) the query is fewer than fifty characters long; (2) the query doesn't
    contain any illegal characters (@£%^()/\'[]{}`~±§), if so, it returns an appropriate error message'''
    flag = False
    if len(query)>50:
        return False, 'Oops, that search term looks a little long'
    for i in list(query):
        if i in list('@£%^()/\'[]{}`~±§'):
            return False, 'Oops, there look to be some illegal characters in that search term'
    return True, ''


@bp.route('/', methods=['POST'])
@login_required
def search():
    '''The 'umbrella' function for a search: it redirects to the correct type of search (track, artist, or descriptor),
    and renders the result once it is returned'''
    try:
        if request.form['song']: r = search_track()
        elif request.form['artist']: r = search_artist()
        elif request.form['descriptor']: r = search_descriptor()
        else:
            return render_template("add_tastes.html")
    except:
        return render_template("add_tastes.html", connection_error=True)

    most_recent_return.set(r)
    return render_template("add_tastes.html", results=r, display_boolean="block", connection_error=False)



def search_track():
    '''Responds to a user query for a track. It is only called indirectly from the search() function.
    It also checks if the query is an advanced query, and calls an advanced query if it is.'''
    query = request.form['song']
    flag, message = validate_query(query)
    advanced_query = None
    if flag:
        if ':' in list(query):
            advanced_query = query
        r = create_api_call(track=query, type='track', advanced_query=advanced_query)
        r = API_return_parser_track(r)
        return r.to_table().values.tolist()
    else:
        return message


def search_artist():
    '''Responds to a user query for an artist. It is only called indirectly from the search() function.'''
    query = request.form['artist']
    flag, message = validate_query(query)
    advanced_query = None
    if flag:
        if ':' in list(query):
            advanced_query = query
        r = create_api_call(artist=query, type='artist', advanced_query=advanced_query)
        r = API_return_parser_artist(r)
        return r.to_table().values.tolist()
    else:
        return message


def search_descriptor():
    '''Responds to a user query for a descriptor. It is only called indirectly from the search() function.
    There are two types of descriptor: year/year range, and genre, obviously differentiated by the presence of a number.
    This function thus checks for a number, and will carry out a "year:<>" search if it finds one, and "genre:<>" otherwise'''
    number_flag = False
    advanced_query = None
    query = request.form['descriptor']
    flag, message = validate_query(query)

    if flag:
        for i in range(10):
            if str(i) in list(query):
                number_flag = True

        if number_flag:
            r = create_api_call(advanced_query='year:{}'.format(query))
            r = API_return_parser_track(r)
            return r.to_table().values.tolist()
        r = create_api_call(advanced_query='genre:{}'.format(query))
        r = API_return_parser_track(r)
        return r.to_table().values.tolist()
    else:
        return message

@bp.route('/<int:id>')
@login_required
def add_to_listener_profile(id):
    '''When the user clicks the + button on the table of search results, they are redirected to /add_tastes/<id> where
    id is the index of the row of the list they have selected. This row is then added to the listener_raw_data table,
    alongside the username. When added, it redirects back to the add_tastes page.'''
    if most_recent_return.get():
        db = get_db()
        db.execute(
            "INSERT INTO listener_raw_data (username, title, listener_data) VALUES (?, ?, ?)",
            (g.user["username"], most_recent_return.get()[id][0], most_recent_return.get()[id][-1]),
        )
        db.commit()


    return redirect(url_for('add_tastes'))


@bp.route('/delete/artist/<int:id>')
@login_required
def delete_artist_from_listener_profile(id):
    artists, _ = most_recent_return.get_artists_and_tracks()
    db = get_db()
    db.execute('DELETE FROM listener_raw_data WHERE username="{}" AND title="{}"'.format(g.user["username"], artists[id]))
    db.commit()


    return redirect(url_for('add_tastes'))

@bp.route('/delete/track/<int:id>')
@login_required
def delete_track_from_listener_profile(id):
    _, tracks = most_recent_return.get_artists_and_tracks()
    db = get_db()
    db.execute('DELETE FROM listener_raw_data WHERE username="{}" AND title="{}"'.format(g.user["username"], tracks[id]))
    db.commit()


    return redirect(url_for('add_tastes'))


