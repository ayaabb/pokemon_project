import io
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import requests
from starlette.responses import StreamingResponse

load_dotenv(dotenv_path='constants.env')
router = APIRouter()
api_image_pokemon_url = os.getenv("pokapi_url")

@router.get("/pokemon_images/{id}")
def get_pokemon_image_using_api(id: int):
    try:

        response = requests.get(f"{api_image_pokemon_url}{str(id)}.png")
        response.raise_for_status()  # Raise HTTPError for bad responses
        return StreamingResponse(io.BytesIO(response.content), media_type="image/png")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching image: {str(e)}")
