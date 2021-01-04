import requests
import numpy as np
from recommend.db import *
import sqlite3
from recommend.api.api_call import retrieve_artists_top_tracks, search_track_by_uri


'''STILL UNDER DEVELOPMENT, THIS CODE IS NOT USED IN PHASE 3'''


def fourier_from_preview_url(preview_url):
    '''Returns the fourier analysis of a track given its preview url'''
    return np.fft.fft(list(requests.get(preview_url + '.mp3').content))

def fourier_from_track_uri(uri):
    #db = get_db()
    #preview_url = db.execute('SELECT preview_url FROM songs WHERE uri=?', (uri, )).fetchone()
    c = sqlite3.connect('/Users/School/Documents/coursework/instance/recommend.sqlite')
    preview_url = c.execute('SELECT preview_url FROM songs WHERE uri=?', (uri, )).fetchone()
    try:#try if it is in database, where the preview url is already stored
        return fourier_from_preview_url(preview_url[0])
    except:#not in database, so search api
        preview_url = search_track_by_uri(uri)['preview_url']
        if preview_url == None:
            raise LookupError('There is no preview url available for that track')
        else:
            return fourier_from_preview_url(preview_url)

def fourier_artists_top_songs_from_uri(uri):
    fouriers = []
    averaged_fouriers = []
    for i in retrieve_artists_top_tracks(uri):
        try:
            fouriers.append(fourier_from_track_uri(i))
        except LookupError as e:
            print(e, uri)
    for i in range(len(fouriers[0])):
        average = 0
        for j in range(3):
            try: average += fouriers[j][i]
            except: pass
        average /= 3
        averaged_fouriers.append(average)
    return averaged_fouriers

print(len(fourier_artists_top_songs_from_uri('spotify:artist:7y97mc3bZRFXzT2szRM4L4')))
print(len(fourier_from_track_uri('spotify:track:61OkaSO7VxyXf5jyOURtab')))
