import requests
from fastapi import APIRouter, Query, HTTPException

router = APIRouter()


@router.get("/pokemons")
def get_pokemons(type: str = Query(None), trainer_name: str = Query(None)):
    if type:
        return requests.get(f'http://pokemon_container:8001/pokemons?type={type}').content
    elif trainer_name:
        return requests.get(f'http://pokemon_container:8001/pokemons?trainer_name={trainer_name}').content
    else:
        raise HTTPException(status_code=400, detail="Specify at least one query parameter: type or trainer_name.")
