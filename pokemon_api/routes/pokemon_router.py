import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

load_dotenv(dotenv_path='constants.env')
router = APIRouter()
api_pokemon_url = os.getenv("pokapi_url")


@router.get("/pokemon_api/info/{pokemon_name}")
def get_pokemon_info_using_api(pokemon_name: str):
    api_url = f"{api_pokemon_url}{pokemon_name.lower()}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise HTTPError for non-2xx status codes

        data = response.json()

        types = []
        for d in data["types"]:
            types.append(d["type"]["name"])

        pokemon_info = [data["id"], data["species"]["name"], data["height"], data["weight"], types]

        return pokemon_info

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from external API: {str(e)}")
