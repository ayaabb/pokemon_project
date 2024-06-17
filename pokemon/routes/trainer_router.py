from Queries import query2, query_exist

from fastapi import APIRouter, HTTPException, Query
from typing import List

from Queries.query_insert_pokemon_to_trainer import insert_into_ownership

router = APIRouter()


@router.get("/trainers")
def get_trainers_by_pokemon(pokemon_name: str):
    """
    Get a list of trainers who own a specific Pokémon.

    Args:
        pokemon_name (str): The name of the Pokémon.

    Returns:
        List[str]: A list of trainer names.

    Raises:
        HTTPException: If no trainers are found for the given Pokémon.
    """
    if not query_exist.pokemon_exists(pokemon_name):
        raise HTTPException(status_code=404, detail=f"{pokemon_name} pokemon not found.")

    trainers = query2.get_trainers_by_pokemon(pokemon_name)
    if len(trainers) < 1:
        raise HTTPException(status_code=404, detail="No trainers found for the given Pokémon.")
    return trainers


@router.post("/trainers")
def add_pokemon_to_trainer(trainer_name: str, pokemon_name: str):
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
    if not query_exist.trainer_exists(trainer_name):
        raise HTTPException(status_code=404, detail=f"{trainer_name} trainer not found.")
    result = insert_into_ownership(pokemon_name, trainer_name)
    if "Failed" in result:
        raise HTTPException(status_code=400, detail=result)
    return {"message": result}
