from calendar import calendar
from datetime import datetime
import pandas as pd
import ram_requests
import requests
from PIL import Image
from typing import List

COMMANDS = ["ls", "filter", "get"]

LS_RULES = ["name", "episode", "characters", "id", "air_date"]

ram_urls = requests.get("https://rickandmortyapi.com/api")
ram_json = ram_urls.json()

PROPERTY_TO_COUNT = {"characters": "episode", "locations": "residents", "episodes": "characters"}


def format_date(date):
    """
    this function formats a date from MONTH(str) DAY(Number) YEAR(str)
    :param date: the date
    :return: formated date (12/12/2012)
    """
    str_date = date.split()
    formated_month = list(calendar.month_name).index(str_date[0])
    formated_day = "{:02d}".format(str_date[1][:-1])
    formated_year = str_date[2]

    return f"{formated_day}/{formated_month}/{formated_year}"


def filter_date(json_list, date, befor):
    """
    this function gets a list of episodes, a date, and returns a list of all dates after/befor (depends on flag) the date.
    :param json_list: the list of JSON's
    :param date: the date given
    :param befor: the flag that will return if befor a date and after
    :return: returns a lists of objects befor or after the date
    """
    final_entities = []
    for episode in json_list:
        formated_date = datetime.strptime(format_date(episode["air_date"]), "%d/%m/%Y")
        current_date = datetime.strptime(date, "%d/%m/%Y")
        if formated_date > current_date:
            final_entities.append(episode)
    if befor == True:
        final_entities = list(set(json_list) - set(final_entities))
    return final_entities


def analyze_date(befor, type, date, rules):
    """
    this function will get all the episodes before a specific date or after (depend if befor is true).
    the rules are the columns that are specified
    :param befor: the flag that will return if befor a date and after
    :param type: the type (character/location/episode)
    :param date: the date given
    :param rules: the columns specified
    :return: prints a table
    """
    json_entities = ram_requests.show(type, -1)
    table = []
    filter_entities = filter_date(json_entities, date, befor)
    for entity in filter_entities:
        table.append(format_json_item(entity, rules))
    print_table(table, rules)


def count_item_properties(json_list: list, type) -> List[int]:
    """
    this function gets a type and counts their property per item
    :param json_list: the list
    :param type: the type
    :return: a list of count
    """
    count_entities = []
    for item in json_list:
        property_to_count = PROPERTY_TO_COUNT[type]
        count_property = len(item[property_to_count])
        count_entities.append(count_property)
    return count_entities


def show_with_count_property_analyzer(type, flags):
    """
    this function lists a type with a count property
    :param rules: the coulmns
    :param type: type
    :param length: length wanted
    :return: print table
    """
    top = flags["top"]
    flags.pop("top")
    rules = list(filter(lambda rule: flags[rule], flags.keys()))
    rules.append("count")

    table = []
    json_entities = ram_requests.show(type, -1)
    count_for_entity = count_item_properties(json_entities, type)
    for count_item, json_item in zip(count_for_entity, json_entities):
        json_item["count"] = count_item
        row = format_json_item(json_item, rules)
        table.append(row)

    final_table = table[:top][:]
    print_table(final_table, rules)


def format_json_item(row_json, rules):
    """
    this function gets a JSON output page and returns a string with a row output.
    :param row_json:
    :param rules:
    :return:
    """
    formated_row = []
    for rule in rules:
        formated_row.append(str(row_json[rule]))
    return formated_row


def print_table(table, rules):
    """
    this function print a table using Pandas dataFrame, this will format a table with the headers
    :param table: the table
    :param rules: the headers
    :return: prints
    """
    df = pd.DataFrame(table, columns=rules)
    print(df)


def show_analyzer(type, flags):
    """
    this function gets the rules (a list of the working flags) and returns the formated output
    :param rules: list of the working flags
    :param length: the length of the ls
    :return:
    """
    length = flags["length"]
    flags.pop("length")
    rules = list(filter(lambda rule: flags[rule], flags.keys()))

    table = []
    json_entities = ram_requests.show(type, length)
    for item in json_entities:
        table.append(format_json_item(item, rules))
    print_table(table, rules)


def get_image(json_results):
    url_str = json_results[0]["image"]
    img = Image.open(requests.get(url_str, stream=True).raw)
    img.show()


def fetch_analyzer(type, flags):
    """
    the fetch_analyzer will get arguments, type, and rules and will fetch all the the matching objects.
    if the id option is selected it will use the filter_by_id to fetch the matching id, it will format the result and print
    :param args: the arguments (they will be formated)
    :param type: type (character/location/episode)
    :param rules: the cloumns that are selected
    :return: prints the table
    """
    rules = list(flags.keys())
    args_keys = list(filter(lambda rule: flags[rule], flags.keys()))
    args = {key: flags[key] for key in args_keys}

    url = ram_json[type]
    if "id" in args:
        filtered_entities = ram_requests.filter_by_id(url, args["id"])
    else:
        filtered_entities = ram_requests.filter_by_args(url, args)

    table = []
    for item in filtered_entities:
        table.append(format_json_item(item, rules))

    if len(filtered_entities) == 1 and type == "characters":
        get_image(filtered_entities)

    print_table(table=table, rules=rules)
