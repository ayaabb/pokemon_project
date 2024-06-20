import json
import requests
from fastapi import APIRouter,  HTTPException

router = APIRouter()




@router.post("/trainers")
def add_pokemon_to_trainer(trainer_name: str, pokemon_name: str):
    response = requests.post(f'http://pokemon_container:8001/trainers?pokemon_name={pokemon_name}&trainer_name={trainer_name}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.content.decode())
    return response.json()

