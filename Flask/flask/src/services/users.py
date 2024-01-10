import json
import requests
from sqlalchemy import exc
from marshmallow import EXCLUDE
from flask_login import current_user

from src.schemas.user import UserSchema
from src.models.user import User as UserModel
from src.models.http_exceptions import *
import src.repositories.users as users_repository


users_url = "http://localhost:4010/users/"  # URL de l'API users (golang)


def get_user(id):
    response = requests.request(method="GET", url=users_url+id)
    return response.json(), response.status_code


def create_user(user_register):
    # on récupère le modèle utilisateur pour la BDD
    user_model = UserModel.from_dict_with_clear_password(user_register)
    # on récupère le schéma utilisateur pour la requête vers l'API users GO
    user_schema = UserSchema().loads(json.dumps(user_register), unknown=EXCLUDE)

    # on crée l'utilisateur côté API users
    response = requests.request(method="POST", url=users_url, json=user_schema)
    if response.status_code != 201:
        return response.json(), response.status_code

    # on ajoute l'utilisateur dans la base de données
    # pour que les données entre API et BDD correspondent
    try:
        user_model.id = response.json()["id"]
        users_repository.add_user(user_model)
    except Exception:
        raise SomethingWentWrong

    return response.json(), response.status_code


def modify_user(id, user_update):
   
    print(user_update,"userupdqte")
    # on vérifie que l'utilisateur se modifie lui-même
    if id != current_user.id:
        raise Forbidden

    # s'il y a quelque chose à changer côté API (username, name)
    user_schema = UserSchema().loads(json.dumps(user_update), unknown=EXCLUDE)
    print(user_schema)
    response = None
    if not UserSchema.is_empty(user_schema):
        # on lance la requête de modification
        response = requests.request(method="PUT", url=users_url+id, json=user_schema)
      
        if response.status_code != 200:

            return response.json(), response.status_code

    # s'il y a quelque chose à changer côté BDD
    user_model = UserModel.from_dict_with_clear_password(user_update)
    if not user_model.is_empty():
        user_model.id = id
        found_user = users_repository.get_user_from_id(id)
        print(found_user)
        if not user_model.username:
            user_model.username = found_user.username
        if not user_model.encrypted_password:
            user_model.encrypted_password = found_user.encrypted_password
        try:
            users_repository.update_user(user_model)
        except exc.IntegrityError as e:
            if "NOT NULL" in e.orig.args[0]:
                raise UnprocessableEntity
            raise Conflict

    return (response.json(), response.status_code) if response else get_user(id)


def get_user_from_db(username):
    return users_repository.get_user(username)


def user_exists(username):
    return get_user_from_db(username) is not None

def get_users():
    response = requests.request(method="GET", url=users_url)
    return response.json(), response.status_code

def delete_user(id):
    # on vérifie que l'utilisateur se modifie lui-même
    if id != current_user.id:
        raise Forbidden

    # on lance la requête de suppression
    response = requests.request(method="DELETE", url=users_url+id)




    if response.status_code == 200:
            # on supprime l'utilisateur de la base de données
        users_repository.delete_user(id)
        return "suppression avec success", 204
    return response.json(), response.status_code
    


