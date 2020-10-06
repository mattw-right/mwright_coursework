

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

def create_api_query(track=False, artist=False, album=False, year=False):
    '''Formats the API query based on the arguments'''
    q = ''
    if track: q += 'track:' + track
    elif artist: q += 'artist:' + artist
    elif album: q += 'album:' + album
    elif year: q += 'year:' + year
    return q


def create_api_call(track=None, year=None, artist=None, album=None, genre=None, type='track', limit=10, market=None, offset=0, error_catch=10, advanced_query=False):
    '''Creates a Spotify API call and returns the results'''
    i = 0
    while True:
        try:
            if advanced_query:
                results = sp.search(advanced_query, limit=limit, offset=offset, type=type, market=market)
            else:
                results = sp.search(create_api_query(track=track, artist=artist, album=album, year=year), limit=limit, offset=offset, type=type, market=market)
            break
        except:
            i += 1
            time.sleep(1)
            print('Trouble connecting. Trying again')
            if i>10:
                break
    return results
