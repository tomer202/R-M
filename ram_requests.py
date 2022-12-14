import urllib

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
    json_entities = []
    if len(page_json["results"]) > 1:
        for item in page_json["results"]:
            json_entities.append(item)
    else:
        json_entities = page_json["results"]
    return json_entities


def get_all_pages_info(page_json, length):
    """
    get all pages info will get from the first json page, will check if its valid, and make a list of all returned values.
    :param page_json: the json page from R&M api
    :param length: the length we will cooperate (length is the number of pages it will check)
    :return: returns the list of results
    """
    json_entities = []
    if list(page_json.keys())[0] == 'error':
        return json_entities

    if not page_json["info"]["next"]:
        json_entities = json_entities + multiple_results(page_json)

    while page_json["info"]["next"] is not None and length != 0:
        json_entities = json_entities + multiple_results(page_json)
        page_json = json.loads(requests.get(page_json["info"]["next"]).text)
        length = length - 1
    return json_entities


def show(type, length):
    """
    this function lists the specific type characters/location/episode
    :param type: the type to list (character, location, episode)
    :return: returns a list of JSONs
    """
    api_request = requests.get(ram_json[type]).text
    json_page = json.loads(api_request)
    return get_all_pages_info(json_page, length)


def filter_by_id(url, ids):
    """
    this function gets an id or a lists of ids and returns all ids
    :param ids:
    :return:
    """
    formated_id = str(ids)
    if isinstance(ids, list):
        formated_id = ','.join(map(str, ids))
    api_request = requests.get(f"{url}/{formated_id}").text
    page_json = json.loads(api_request)
    the_list = []
    if not isinstance(ids, list):
        the_list.append(page_json)
    else:
        the_list = page_json
    return the_list


def filter_by_args(url, args):
    """
    this function gets a dictionary of keys and value and finds all pages that matches these results

    :param args: dict
    :return: return all pages....
    """

    format_args = urllib.urlencode(args, doseq=True)
    api_request = requests.get(f"{url}/?{format_args}").text
    page_json = json.loads(api_request)
    return get_all_pages_info(page_json, -1)
