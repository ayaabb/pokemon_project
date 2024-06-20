import requests
from fastapi import APIRouter, HTTPException
from Queries import pokemon, trainer
from .pokemon_router import add_pokemon

router = APIRouter()

"""
Get a list of trainers who own a specific Pokémon.
Args:
    pokemon_name (str): The name of the Pokémon.
Returns:
    List[str]: A list of trainer names.
Raises:
    HTTPException: If no trainers are found for the given Pokémon.
"""
@router.get("/trainers")
def get_trainers_by_pokemon(pokemon_name: str):
    if not pokemon.pokemon_exists(pokemon_name):
        raise HTTPException(status_code=404, detail=f"{pokemon_name} pokemon not found.")

    trainers = pokemon.get_trainers_by_pokemon(pokemon_name)
    if len(trainers) < 1:
        raise HTTPException(status_code=404, detail="No trainers found for the given Pokémon.")
    return trainers

"""
Add a Pokémon to a trainer's collection.
Args:
    trainer_name (str): The name of the trainer.
    pokemon_name (str): The name of the Pokémon.
Returns:
    dict: A confirmation message with trainer and Pokémon names.
Raises:
    HTTPException: If the insertion fails due to a database error or invalid data.
"""


@router.post("/trainers")
def add_pokemon_to_trainer(trainer_name: str, pokemon_name: str):
    try:
        if not trainer.trainer_exists(trainer_name):
            raise HTTPException(status_code=404, detail=f"{trainer_name} trainer not found.")

        if trainer.trainer_has_pokemon(trainer_name, pokemon_name):
            raise HTTPException(status_code=409, detail=f"{trainer_name} already has {pokemon_name} pokemon")

        if not pokemon.pokemon_exists(pokemon_name):
            add_pokemon(pokemon_name)
            image_response = requests.post(f'http://images:8002/pokemon_images/{pokemon_name}')
            if image_response.status_code != 200:
                raise HTTPException(status_code=image_response.status_code, detail=image_response.text)

        result = trainer.insert_into_ownership(pokemon_name, trainer_name)
        if "Failed" in result:
            raise HTTPException(status_code=400, detail=result)

        return {"message": result}

    except HTTPException:
        raise
