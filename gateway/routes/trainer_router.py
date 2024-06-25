import json
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/trainers")
def add_pokemon_to_trainer(trainer_name: str, pokemon_name: str):
    response = requests.post(
        f'http://pokemon_container:8001/trainers?pokemon_name={pokemon_name}&trainer_name={trainer_name}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.content.decode())
    return response.json()


@router.get("/trainers")
def get_trainers_by_pokemon(pokemon_name: str):
    response = requests.get(
        f'http://pokemon_container:8001/trainers?pokemon_name={pokemon_name}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.content.decode())
    return response.json()


@router.patch("/trainers/{trainer_name}/pokemons/{pokemon_name}")
def evolve_pokemon(trainer_name: str, pokemon_name: str):
    evolve_pokemon_name = requests.get(f'http://pokemon_container:8001/trainers/{trainer_name}/pokemons/{pokemon_name}')

    if evolve_pokemon_name.status_code != 200:
        raise HTTPException(status_code=evolve_pokemon_name.status_code, detail=evolve_pokemon_name.json())
    add_evolved_response = requests.post(
        f'http://pokemon_container:8001/trainers?pokemon_name={evolve_pokemon_name.json()}&trainer_name={trainer_name}')

    if add_evolved_response.status_code != 200:
        raise HTTPException(status_code=add_evolved_response.status_code, detail=add_evolved_response.json())
    delete_pokemon_response = requests.patch(
        f'http://pokemon_container:8001/pokemons/{pokemon_name}/trainers/{trainer_name}')

    if delete_pokemon_response.status_code != 200:
        raise HTTPException(status_code=delete_pokemon_response.status_code, detail=delete_pokemon_response.json())
    return {"message": f"Evolved {pokemon_name} to {evolve_pokemon_name.json()} for trainer {trainer_name}"}

