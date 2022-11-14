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

MONTH_DICT = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07",
              "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}


def format_date(date):
    """
    this function formats a date from MONTH(str) DAY(Number) YEAR(str)
    :param date: the date
    :return: formated date (12/12/2012)
    """
    str_date = date.split()
    return "{:02d}".format(str_date[1][0]) + "/" + MONTH_DICT[str_date[0]] + "/" + str_date[2]


def filter_date(json_list, date, befor):
    """
    this function gets a list of episodes, a date, and returns a list of all dates after/befor (depends on flag) the date.
    :param json_list: the list of JSON's
    :param date: the date given
    :param befor: the flag that will return if befor a date and after
    :return: returns a lists of objects befor or after the date
    """
    final_list = []
    for episode in json_list:
        formated_date = datetime.strptime(format_date(episode["air_date"]), "%d/%m/%Y")
        current = datetime.strptime(date, "%d/%m/%Y")
        if formated_date > current:
            final_list.append(episode)
    if befor == True:
        final_list = list(set(json_list) - set(final_list))
    return final_list


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
    listed_jsons = ram_requests.ls(type, -1)
    table = []
    filter_ls = filter_date(listed_jsons, date, befor)
    for item in filter_ls:
        table.append(format_json_item(item, rules))
    print_table(table, rules)


def count_item_properties(json_list: list, type) -> List[int]:
    """
    this function gets a type and counts their property per item
    :param json_list: the list
    :param type: the type
    :return: a list of count
    """
    count_list = []
    for item in json_list:
        count_list.append(len(item[PROPERTY_TO_COUNT[type]]))
    return count_list


def ls_with_count_property_analyzer(rules, type, top):
    """
    this function lists a type with a count property
    :param rules: the coulmns
    :param type: type
    :param length: length wanted
    :return: print table
    """
    table = []
    listed_json = ram_requests.ls(type, -1)
    count_list = count_item_properties(listed_json, type)
    for count_item, json_item in zip(count_list, listed_json):
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


def ls_analyzer(rules, type, length):
    """
    this function gets the rules (a list of the working flags) and returns the formated output
    :param rules: list of the working flags
    :param length: the length of the ls
    :return:
    """
    table = []
    listed_json = ram_requests.ls(type, length)
    for item in listed_json:
        table.append(format_json_item(item, rules))
    print_table(table, rules)


def get_image(json_results):
    url_str = json_results[0]["image"]
    img = Image.open(requests.get(url_str, stream=True).raw)
    img.show()


def fetch_analyzer(args, type, rules):
    """
    the fetch_analyzer will get arguments, type, and rules and will fetch all the the matching objects.
    if the id option is selected it will use the filter_by_id to fetch the matching id, it will format the result and print
    :param args: the arguments (they will be formated)
    :param type: type (character/location/episode)
    :param rules: the cloumns that are selected
    :return: prints the table
    """
    url = ram_json[type]
    if "id" in args:
        filtered_list = ram_requests.filter_by_id(url, args["id"])
    else:
        filtered_list = ram_requests.filter_by_args(url, args)
    table = []
    for item in filtered_list:
        table.append(format_json_item(item, rules))

    if len(filtered_list) == 1 and type == "characters":
        get_image(filtered_list)

    print_table(table=table, rules=rules)
