import requests
from fastapi import APIRouter, Query, HTTPException
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/pokemons")
def get_pokemons(type: str = Query(None), trainer_name: str = Query(None)):
    if type and trainer_name:
        raise HTTPException(status_code=400, detail="Specify either type or trainer_name, not both.")
    if type:
        parsed_list = requests.get(f'http://pokemon_container:8001/pokemons?type={type}').json()
        return JSONResponse(content=parsed_list)
    elif trainer_name:
        parsed_list = requests.get(f'http://pokemon_container:8001/pokemons?trainer_name={trainer_name}').json()
        return JSONResponse(content=parsed_list)
    else:
        raise HTTPException(status_code=400, detail="Specify at least one query parameter: type or trainer_name.")


@router.post("/pokemons")
def add_pokemon(pokemon_name: str):
    response = requests.post(f'http://pokemon_container:8001/pokemons?pokemon_name={pokemon_name}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.content.decode())
    return response.json()