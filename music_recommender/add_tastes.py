
from music_recommender.add_tastes.api_call import create_api_call
from music_recommender.add_tastes.api_return_parser import API_return_parser_track
from flask import Flask
from flask import render_template, request
from flask import Blueprint
app = Flask(__name__)

bp = Blueprint("add_tastes", __name__, url_prefix="/add_tastes")

@app.route('/')
def main():
    '''Renders the initial search page of the app'''
    return render_template('index.html', display_boolean='none')

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

@app.route('/', methods=['POST'])
def search():
    '''Responds to a user query, and renders the result in an HTML table'''
    query = request.form['song']
    flag, message = validate_query(query)
    if flag:
        type = 'track'
        track, year, artist, album, genre = None, None, None, None, None
        if ':' in list(query):
            advanced_query = query
        if type == 'track': track=query
        elif type == 'year': year=query
        elif type == 'artist': artist=query
        elif type == 'album': album=query
        elif type == 'genre': genre=query
        r = create_api_call(track=track, year=year, artist=artist, album=album, genre=genre, type=type, advanced_query=query)
        r = API_return_parser_track(r)
        print(r.to_table())
        return render_template("index.html", results=r.to_table().values.tolist(), display_boolean="block")
    else:
        #message
        return render_template('search_page.html')
