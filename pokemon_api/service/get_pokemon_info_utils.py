import json

import requests


def http_request_data(pokemon_name):
    with open('service/constants.json') as f:
        constants = json.load(f)
    print(constants)
    # return requests.get(f"{constants["pokapi_url"]}/pokemon/{pokemon_name.lower()}")


def get_pokemon_info(pokemon_name):
    response = http_request_data(pokemon_name)
    response.raise_for_status()
    data = response.json()
    types = []
    for d in data["types"]:
        types.append(d["type"]["name"])

    return [data["id"], data["species"]["name"], data["height"], data["weight"], types]
