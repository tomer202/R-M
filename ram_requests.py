import requests
import json

"""Declaring global variables (URL's for api)"""

ram_urls = requests.get("https://rickandmortyapi.com/api")
ram_json = ram_urls.json()

CHARACTER_URL = ram_json["characters"]
EPISODES_URL = ram_json["episodes"]
LOCATIONS_URL = ram_json["locations"]


def multiple_results(page_json):
    """
    this function will cooperate with a json result with multiple values, it will make a list with all results and return it
    :param page_json: the json page got from r&m api
    :return: the list of results
    """
    the_list = []
    if len(page_json["results"]) > 1:
        for item in page_json["results"]:
            the_list.append(item)
    else:
        the_list = page_json["results"]
    return the_list


def get_all_pages_info(page_json, length):
    """
    get all pages info will get from the first json page, will check if its valid, and make a list of all returned values.
    :param page_json: the json page from R&M api
    :param length: the length we will cooperate (length is the number of pages it will check)
    :return: returns the list of results
    """
    the_list = []
    if list(page_json.keys())[0] == 'error':
        return the_list

    if not page_json["info"]["next"]:
        the_list = the_list + multiple_results(page_json)

    while page_json["info"]["next"] is not None and length != 0:
        the_list = the_list + multiple_results(page_json)
        page_json = json.loads(requests.get(page_json["info"]["next"]).text)
        length = length - 1

    return the_list


def ls(type, length):
    """
    this function lists the specific type characters/location/episode
    :param type: the type to list (character, location, episode)
    :return: returns a list of JSONs
    """
    json_page = json.loads(requests.get(ram_json[type]).text)
    return get_all_pages_info(json_page, length)


def filter_by_id(url, ids):
    """
    this function gets an id or a lists of ids and returns all ids
    :param ids:
    :return:
    """
    formated_id = ((','.join(map(str, ids))) if isinstance(ids, list) else str(ids))
    page_json = json.loads(requests.get(url + f"/{formated_id}").text)
    the_list = []
    if not isinstance(ids, list):
        the_list.append(page_json)
    else:
        the_list = page_json
    return the_list


def map_key_for_value(args):
    """
    this function makes a key value pair and concats them
    :param args: dict
    :return: key=value&key=value......
    """
    args_to_string = []
    for key in args:
        args_to_string.append(f"{key}={args[key]}")
    format_args = '&'.join(args_to_string)
    return format_args


def filter_by_args(url, args):
    """
    this function gets a dictionary of keys and value and finds all pages that matches these results

    :param args: dict
    :return: return all pages....
    """
    format_args = map_key_for_value(args)
    page_json = json.loads(requests.get(url + f"/?{format_args}").text)
    return get_all_pages_info(page_json, -1)
