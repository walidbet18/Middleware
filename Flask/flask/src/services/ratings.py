import json
import requests

from marshmallow import EXCLUDE
from flask_login import current_user
from schemas.ratings import RatingSchema
from models.http_exceptions import *



ratings_url = "https://ratings-echo.edu.forestier.re"  



def create_rating(rating_register, song_id):
    print(rating_register)
    # on récupère le schéma rating pour la requête vers l'API ratings
    rating_schema = RatingSchema().loads(json.dumps(rating_register), unknown=EXCLUDE)
    rating_schema["user_id"] = current_user.id

    # on crée la chonson côté API ratings
    response = requests.request(method="POST", url=ratings_url+"/songs/"+song_id+"/ratings", json=rating_schema)
     
    print(response.json())

    if response.status_code != 201:
        return response.json(), response.status_code

  

    return response.json(), response.status_code

def get_ratings(song_id):
    response = requests.request(method="GET", url=ratings_url+"/songs/"+song_id+"/ratings")
    return response.json(), response.status_code

def get_rating(song_id,id):
    response = requests.request(method="GET", url=ratings_url+"/songs/"+song_id+"/ratings/"+id)
    return response.json(), response.status_code

def update_rating(song_id,id, rating_update):
    rating_schema = RatingSchema().loads(json.dumps(rating_update), unknown=EXCLUDE)
    print(rating_schema)
    response = None
    if not RatingSchema.is_empty(rating_schema):
        response = requests.request(method="PUT", url=ratings_url+"/songs/"+song_id+"/ratings/"+id, json=rating_schema)
        print(response.status_code)
        if response.status_code != 200:
            return response.json(), response.status_code

    return response.json(), response.status_code

def delete_rating(song_id,id):
    response = requests.request(method="DELETE", url=ratings_url+"/songs/"+song_id+"/ratings/"+id)

    if response.status_code == 204:
        return "Deleted", 204

    return  response.status_code