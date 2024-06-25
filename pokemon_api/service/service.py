import requests


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def find_evolution(chain, target_name):
    if chain["species"]["name"] == target_name:
        if chain.get("evolves_to"):
            return chain["evolves_to"][0]["species"]["name"]
        else:
            return None
    for evolves_to in chain.get("evolves_to", []):
        result = find_evolution(evolves_to, target_name)
        if result:
            return result
    return None
