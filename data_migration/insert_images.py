import os
import pymongo
import requests
import gridfs

api_image_pokemon_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/"
mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")

def connect_to_mongo():
    mongodb = pymongo.MongoClient(mongodb_url)
    db = mongodb["pokemons"]
    fs = gridfs.GridFS(db)
    return fs

def insert_pokemon_images():
    fs = connect_to_mongo()
    for i in range(1, 151):
        if not fs.exists({"_id": i}):
            fs.put(get_image(i), _id=i)


def get_image(i):
    response = requests.get(f"{api_image_pokemon_url}{str(i)}.png")
    response.raise_for_status()
    return response.content

if __name__ == "__main__":
    insert_pokemon_images()
