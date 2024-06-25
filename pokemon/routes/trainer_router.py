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
            raise HTTPException(status_code=409, detail=f"{trainer_name} already has {pokemon_name} pokemon add")

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


"""
 Evolve a Pokémon for a specific trainer.
 This endpoint checks if the given trainer and Pokémon exist, and if the trainer owns the Pokémon.
 If the Pokémon can evolve, it will be evolved and updated in the trainer's list.
 Parameters:
 - trainer_name: str - The name of the trainer.
 - pokemon_name: str - The name of the Pokémon to be evolved.
 Raises:
 - HTTPException: 404 if the trainer does not exist.
 - HTTPException: 404 if the Pokémon does not exist.
 - HTTPException: 404 if the trainer does not own the specified Pokémon.
 - HTTPException: 400 if the Pokémon cannot evolve.
 - HTTPException: 409 if the trainer already owns the evolved Pokémon.
 Returns:
 - dict: A message indicating the successful evolution of the Pokémon.
 """


@router.get("/trainers/{trainer_name}/pokemons/{pokemon_name}")
def get_evolve_pokemon(trainer_name: str, pokemon_name: str):
    try:

        if not trainer.trainer_exists(trainer_name):
            raise HTTPException(status_code=404, detail=f"{trainer_name} trainer not found.")
        if not pokemon.pokemon_exists(pokemon_name):
            raise HTTPException(status_code=404, detail=f"{pokemon_name} pokemon not found.")
        if not trainer.trainer_has_pokemon(trainer_name, pokemon_name):
            raise HTTPException(status_code=404, detail=f"{trainer_name} does not have {pokemon_name} pokemon")

        evolved_pokemon_name = requests.get(f'http://api_service:8003/pokemon_api/evolved_pokemon/{pokemon_name}')

        if evolved_pokemon_name.status_code != 200:
            raise HTTPException(status_code=evolved_pokemon_name.status_code,
                                detail=evolved_pokemon_name.content.decode())

        if trainer.trainer_has_pokemon(trainer_name, evolved_pokemon_name.json()):
            raise HTTPException(status_code=409,
                                detail=f"{trainer_name} already has {evolved_pokemon_name.json()} pokemon ")
        return evolved_pokemon_name.json()
    except HTTPException as e:
        raise e
