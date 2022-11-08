import typer
import requests
import ram_analyzer

import location
import episode
import character

"""Declaring global variables (URL's for api)"""

ram_urls = requests.get("https://rickandmortyapi.com/api")
ram_json = ram_urls.json()

CHARACTER_URL = ram_json["characters"]
EPISODES_URL = ram_json["episodes"]
LOCATIONS_URL = ram_json["locations"]

app = typer.Typer()

app.add_typer(location.app, name="location")
app.add_typer(episode.app, name="episode")
app.add_typer(character.app, name="character")

if __name__ == "__main__":
    app()
