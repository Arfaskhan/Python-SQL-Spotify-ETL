from logging import exception

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pymysql

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='5999a06d4dc643fb95eb280570fe2b55',
    client_secret='3cffe3941adb49349fc7bf5befd19e96'))

db_config = {
    'host':'localhost',
    'user' : 'root',
    'password' : 'root',
    'database' : 'spotify_db'
}

connection = pymysql.connect(**db_config)
cursor = connection.cursor()

with open('Tracks.txt','r') as file:
    trackk = file.read().split('\n')

for track in trackk:
    track_url = track
    track_id = track_url.split('/track/')[1]
    track_song = sp.track(track_id)
    track_data ={
        'Song_name': track_song['album']['name'],
        'Singer_name': track_song['album']['artists'][0]['name'],
        'Released_date' : track_song['album']['release_date'],
        'Popularity' : track_song['popularity'],
        'Url' : track_song['external_urls']['spotify'],
        'duration(m)' : (track_song['duration_ms']/1000)/60
    }
    try :

        insert_query = """
        INSERT INTO spotify_track(song_name,singer_name,release_date,popularity,url,duration)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(insert_query,(
            track_song['album']['name'],
            track_song['album']['artists'][0]['name'],
            track_song['album']['release_date'],
            track_song['popularity'],
            track_song['external_urls']['spotify'],
            (track_song['duration_ms'] / 1000) / 60
        ))
        connection.commit()
    except Exception as e:
        print(f'Track url : {track_url},Error{e}')
cursor.close()
connection.close()


