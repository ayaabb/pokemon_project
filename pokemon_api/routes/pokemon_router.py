import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from service.service import fetch_data, find_evolution

load_dotenv(dotenv_path='service/constants.env')
api_pokemon_url = os.getenv("pokapi_url")

router = APIRouter()

@router.get("/pokemon_api/info/{pokemon_name}")
def get_pokemon_info_using_api(pokemon_name: str):
    try:
        data = fetch_data(f"{api_pokemon_url}{pokemon_name.lower()}").json()
        types = []
        for d in data["types"]:
            types.append(d["type"]["name"])
        pokemon_info = [data["id"], data["species"]["name"], data["height"], data["weight"], types]
        return pokemon_info
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from external API: {str(e)}")


@router.get("/pokemon_api/evolved_pokemon/{pokemon_name}")
async def get_evolved_pokemon_using_api(pokemon_name: str):
    try:

        pokemon_url = f"{api_pokemon_url}{pokemon_name.lower()}"
        pokemon_data = fetch_data(pokemon_url).json()

        species_url = pokemon_data["species"]["url"]
        species_data = fetch_data(species_url).json()

        evolution_chain_url = species_data["evolution_chain"]["url"]
        evolution_chain_data = fetch_data(evolution_chain_url).json()

        chain = evolution_chain_data["chain"]
        evolved_pokemon = find_evolution(chain, pokemon_name.lower())
        if evolved_pokemon:
            return evolved_pokemon
        else:
            raise HTTPException(status_code=404, detail=f"pokemon {pokemon_name} don't evolve")

    except requests.HTTPError as http_err:
        if http_err.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        else:
            raise HTTPException(status_code=http_err.response.status_code, detail="HTTP error occurred")
    except requests.RequestException as req_err:
        raise HTTPException(status_code=500, detail="Request error occurred") from req_err
