import pandas as pd

class API_return_parser_track:
    '''Parses the return of an API call for a track, retrieving certain data from it'''

    def __init__(self, raw_body):
        '''Initiates the object, setting the local body attribute to what the API has returned'''
        self.body = raw_body

    def return_track_name(self, result_index=0):
        '''Returns the name of the track at index result_index'''
        return self.body['tracks']['items'][result_index]['name']

    def return_track_uri(self, result_index=0):
        '''Returns the uri of the track at index result_index'''
        return self.body['tracks']['items'][result_index]['uri']

    def return_first_artist_name(self, result_index=0):
        '''Returns the name of the first artist of a track at index result_index'''
        return self.body['tracks']['items'][result_index]['artists'][0]['name']

    def return_all_artists(self, result_index=0):
        '''Returns the all data about all the artists of a track at index result_index'''
        return self.body['tracks']['items'][result_index]['artists']

    def return_first_artist_uri(self, result_index=0):
        '''Returns the uri of the first artist of a track at index result_index'''
        return self.body['tracks']['items'][result_index]['artists'][0]['uri']

    def return_album_name(self, result_index=0):
        '''Returns the album name of the track at index result_index'''
        return self.body['tracks']['items'][result_index]['album']['name']

    def return_album_uri(self, result_index=0):
        '''Returns the uri of the album of the track at index result_index'''
        return self.body['tracks']['items'][result_index]['album']['uri']

    def return_release_date(self, result_index=0):
        '''Returns the release date of the track at index result_index'''
        return self.body['tracks']['items'][result_index]['album']['release_date']

    def return_preview_url(self, result_index=0):
        '''Returns the preview url of the track at index result_index'''
        return str(self.body['tracks']['items'][result_index]['preview_url'])

    def return_cover_art_url(self, result_index=0):
        '''Returns the url of the covert art of the album of the track at index result_index'''
        return self.body['tracks']['items'][result_index]['album']['images'][0]['url']

    def to_table(self):
        '''Converts the song data into a Pandas dataframe so that it might be displayed '''
        df = pd.DataFrame(columns = ['Track Name', 'Artist', 'Album', 'Preview URL', 'Cover Art URL'])
        for i in range(len(self.body['tracks']['items'])):
            df.loc[i] = [self.return_track_name(result_index=i), self.return_first_artist_name(result_index=i), self.return_album_name(result_index=i), self.return_preview_url(result_index=i), self.return_cover_art_url(result_index=i)]
        return df






class API_return_parser_album:

    def __init__(self, raw_body):
        self.body = raw_body

    def r(self):
        return self.body
