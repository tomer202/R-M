import typer

import location
import episode
import character

app = typer.Typer()

app.add_typer(location.app, name="location")
app.add_typer(episode.app, name="episode")
app.add_typer(character.app, name="character")

if __name__ == "__main__":
    app()
