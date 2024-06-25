import io
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import requests
from starlette.responses import StreamingResponse

from service.service import fetch_data

load_dotenv(dotenv_path='constants.env')
router = APIRouter()
api_image_pokemon_url = os.getenv("images_url")

@router.get("/pokemon_api/images/{id}")
def get_pokemon_image_using_api(id: int):
    try:

        image = fetch_data(f"{api_image_pokemon_url}{str(id)}.png")

        return StreamingResponse(io.BytesIO(image.content), media_type="image/png")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching image: {str(e)}")
