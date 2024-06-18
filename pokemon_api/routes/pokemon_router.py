import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv(dotenv_path='constants.env')
router = APIRouter()
api_pokemon_url = os.getenv("pokapi_url")


@router.get("/pokemon_api/info/{pokemon_name}")
def get_pokemon_info_using_api(pokemon_name: str):
    response = requests.get(f"{api_pokemon_url}{pokemon_name.lower()}")
    response.raise_for_status()
    data = response.json()
    types = []
    for d in data["types"]:
        types.append(d["type"]["name"])

    return [data["id"], data["species"]["name"], data["height"], data["weight"], types]
