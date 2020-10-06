
from api_call import create_api_call
from api_return_parser import API_return_parser_track, API_return_parser_album
from flask import Flask
from flask import render_template, request
app = Flask(__name__)


@app.route('/')
def main():
    '''Renders the initial search page of the app'''
    return render_template('search_page.html')

@app.route('/', methods=['POST'])
def search():
    '''Responds to a user query, and renders the result in an HTML table'''
    query = request.form['search']
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
    return render_template("results.html", results=r.to_table().values.tolist())
