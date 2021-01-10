import requests
import numpy as np
from recommend.db import *
import sqlite3
from pydub import AudioSegment
import io
from recommend.api.api_call import retrieve_artists_top_tracks, search_track_by_uri


'''THIS CODE IS STILL UNDER DEVELOPMENT AND IS NOT USED IN PHASE 3'''


def fourier_from_preview_url(preview_url, n=100):
    '''Returns the fourier analysis of a track given its preview url. N is the number of frequencies analysed'''
    return np.fft.fft(AudioSegment.from_file(io.BytesIO(requests.get(preview_url + '.mp3').content), format="mp3").get_array_of_samples(), n=n)

def fourier_from_track_uri(uri):
    db = get_db()
    preview_url = db.execute('SELECT preview_url FROM songs WHERE uri=?', (uri, )).fetchone()
    try:#try if it is in database, where the preview url is already stored
        print(preview_url[0])
        return fourier_from_preview_url(preview_url[0])
    except:#not in database, so search api
        preview_url = search_track_by_uri(uri)['preview_url']
        if preview_url == None:
            return None
        else:
            return fourier_from_preview_url(preview_url)

def fourier_artists_top_songs_from_uri(uri):
    fouriers = []
    averaged_fouriers = []
    for i in retrieve_artists_top_tracks(uri):
        fourier = fourier_from_track_uri(i)
        if fourier is not None: fouriers.append(fourier)
    if fouriers != []:
        for i in range(len(fouriers[0])):

            average = 0
            for j in range(3):
                try: average += fouriers[j][i]
                except: pass
            average /= 3
            averaged_fouriers.append(average)
        return averaged_fouriers
    return None

def convert_fourier_to_string(fourier):
    '''Converts a list of numpy.complex128 fourier results into a string that can be stored in sqlite'''
    if fourier is not None: return ';'.join([str(i) for i in fourier])
    return ''
