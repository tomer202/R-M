import typer
import ram_analyzer

app = typer.Typer()

TYPE = "locations"


@app.command()
def ls(name: bool = typer.Option(True, "--name", "-n"),
       id: bool = typer.Option(False, "--id", "-i"),
       type: bool = typer.Option(False, "--type", "-t"),
       dimension: bool = typer.Option(False, "--dimension", "-d"),
       residents: bool = typer.Option(False, "--residents", "-r"),
       length: int = typer.Option(1, "--length", "-l")):
    """
    this function will list all location with the flags that are specified default is name
    :return: void (it prints it)
    """
    vars_dict = locals()
    vars_dict.pop("length")
    rules = list(filter(lambda rule: vars_dict[rule], vars_dict.keys()))
    ram_analyzer.ls_analyzer(rules, TYPE, length)


SEGNIFICATE_FLAGS_FETCH = ["id"]


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
          id: int = typer.Option(None, "--id", "-i"),
          type: str = typer.Option(None, "--type", "-t"),
          dimension: str = typer.Option(None, "--dimension", "-d")):
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
