import typer
import ram_analyzer

app = typer.Typer()

TYPE = "episodes"


RULES = ["episode", "id", "name", "air_date"]

@app.command()
def ls(episode: bool = typer.Option(True, "--episode", "-e"),
       id: bool = typer.Option(False, "--id", "-i"),
       name: bool = typer.Option(False, "--name", "-n"),
       air_date: bool = typer.Option(False, "--air_date", "-ad"),
       characters: bool = typer.Option(False, "--characters", "-c"),
       length: int = typer.Option(1, "--length", "-l")):
    """
    this function will list all episodes with the flags that are specified default is episode code
    :param episode: the episode code (S01E02)
    :param id: episode id
    :param name: the name
    :param air_date: the date it aired
    :param characters: a list of the characters id that were in
    :return: void (it prints it)
    """
    vars_dict = locals()
    vars_dict.pop("length")
    rules = list(filter(lambda rule: vars_dict[rule], vars_dict.keys()))
    ram_analyzer.ls_analyzer(rules, TYPE, length);


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
    vars_dict.pop("top")
    rules = list(filter(lambda rule: vars_dict[rule], vars_dict.keys()))
    rules.append("count")
    ram_analyzer.ls_with_count_property_analyzer(rules, TYPE, top)


SEGNIFICATE_FLAGS_FETCH = ["id", "episode"]


@app.command()
def code(episode: int = typer.Option(True, "--episode", "-e"),
         season: int = typer.Option(False, "--season", "-s")):
    """
    code you can put a specific episode and season and list all episodes
    :param episode:
    :param season:
    :param length:
    :return:
    """
    the_code = "S" + "{:02d}".format(season) + "E" + "{:02d}".format(episode)
    fetch(episode=the_code, id=None, name=None)

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
def fetch(episode: str = typer.Option(None, "--episode", "-e"),
          id: int = typer.Option(None, "--id", "-i"),
          name: str = typer.Option(None, "--name", "-n")):
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

@app.command()
def date(befor: bool = typer.Option(False, "--befor", "-b"),
         date: str = typer.Option(None, "--date", "-d")):
    """
    this function shows episodes after date that specified (or flag -b was used)
    :param befor: if used then it will show episodes befor
    :param date: the data
    :return: print episodes
    """
    ram_analyzer.analyze_date(befor, TYPE, date, RULES)
