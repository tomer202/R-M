import typer
import ram_analyzer

app = typer.Typer()

TYPE = "characters"


@app.command()
def show(name: bool = typer.Option(True, "--name", "-n"),
         id: bool = typer.Option(False, "--id", "-i"),
         status: bool = typer.Option(False, "--status", "-st"),
         species: bool = typer.Option(False, "--species", "-s"),
         gender: bool = typer.Option(False, "--gender", "-g"),
         type: bool = typer.Option(False, "--type", "-t"),
         origin: bool = typer.Option(False, "--origin", "-o"),
         location: bool = typer.Option(False, "--location", "-l"),
         image: bool = typer.Option(False, "--image", "-i"),
         episode: bool = typer.Option(False, "--episode", "-e"),
         length: int = typer.Option(1, "--length", "-l")):
    """
    this function will list all characters with the flags that are specified default is name
    :return: void (it prints it)
    """
    vars_dict = locals()
    ram_analyzer.show_analyzer(TYPE, vars_dict)


@app.command()
def count(name: bool = typer.Option(True, "--name", "-n"),
          top: int = typer.Option(10, "--top", "-t")):
    """
    this function count the number of accurence
    :param name:
    :param top:
    :return:
    """
    vars_dict = locals()
    ram_analyzer.show_with_count_property_analyzer(TYPE, vars_dict)

SEGNIFICATE_FLAGS_FETCH = ["id"]


def break_the_rules_fetch(flags):
    """
    this function check if rules are broken, if SEGNIFICATE_FLAGS_FETCH and more flags are inputed then rulse are broken....
    :param flags: the flags that are used
    :return: if broke rules or not
    """
    rules = list(filter(lambda rule: flags[rule], flags.keys()))
    broke = False
    for flag in rules:
        if flag in SEGNIFICATE_FLAGS_FETCH and len(rules) > 1:
            broke = True
            break
    return broke


@app.command()
def fetch(name: str = typer.Option(None, "--name", "-n"),
          status: str = typer.Option(None, "--status", "-s"),
          id: int = typer.Option(None, "--id", "-i"),
          location: str = typer.Option(None, "--id", "-l"),
          episode: str = typer.Option(None, "--episode", "-e"),
          origin: str = typer.Option(None, "--origin", "-o"),
          type: str = typer.Option(None, "--type", "-t"),
          species: str = typer.Option(None, "--species", "-sp"),
          gender: str = typer.Option(None, "--gender", "-g")):
    """
    fetch will get a specific output, not like ls that you list, in fetch you filter and fetch the specific output that matches
    :param episode: the episode (such as S01E04)
    :param id: the id (list of int)
    :param name: the name (this output will give all outputs that contains the name)
    :return: prints the outputs
    """
    vars_dict = locals()
    if break_the_rules_fetch(vars_dict):
        print("CANT USE THOSE FLAGS TOGETHER")
    else:
        rules = list(vars_dict.keys())
        args_keys = list(filter(lambda rule: vars_dict[rule], vars_dict.keys()))
        args = {key: vars_dict[key] for key in args_keys}
        ram_analyzer.fetch_analyzer(args, TYPE, rules)
