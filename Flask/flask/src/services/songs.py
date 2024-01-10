import json
import requests
from sqlalchemy import exc
from marshmallow import EXCLUDE
from flask_login import current_user

from schemas.songs import SongSchema
from models.http_exceptions import *

# Define the URL of the songs API
songs_url = "http://localhost:4010/songs"

# Function to create a new song
def create_song(song_register):
    # Load the JSON data into a SongSchema object
    song_schema = SongSchema().loads(json.dumps(song_register), unknown=EXCLUDE)
    
    # Make a POST request to the songs API with the song data
    response = requests.request(method="POST", url=songs_url, json=song_schema)
     
    # Check if the request was successful (status code 201)
    if response.status_code != 201:
        return response.json(), response.status_code

    return response.json(), response.status_code

# Function to get details of a song by its ID
def get_song(id):
    response = requests.request(method="GET", url=songs_url+"/"+id)
    return response.json(), response.status_code

# Function to update a song by its ID
def update_song(id, song_update):
    # Load the JSON data into a SongSchema object
    song_schema = SongSchema().loads(json.dumps(song_update), unknown=EXCLUDE)
    
    # Check if the song data is not empty
    if not SongSchema.is_empty(song_schema):
        # Make a PUT request to update the song with the new data
        response = requests.request(method="PUT", url=songs_url+"/"+id, json=song_schema)
        
        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            return response.json(), response.status_code

    return response.json(), response.status_code

# Function to delete a song by its ID
def delete_song(id):
    # Make a DELETE request to remove the song by its ID
    response = requests.request(method="DELETE", url=songs_url+"/"+id)
    
    # Check if the deletion was successful (status code 204)
    if response.status_code == 204:
        return "supprime avec succes", 204

    return response.json(), response.status_code

# Function to get a list of all songs
def get_songs():
    # Make a GET request to retrieve all songs from the API
    response = requests.request(method="GET", url=songs_url)
    return response.json(), response.status_code
