import requests

from urllib.parse import urlparse
import os

from words.commons import words_parser_common as common
from words.commons import words_parser_parallel as parallel
from ..database import database


def parse_text(data):
    if type(data) != str:
        return {"bad request": "data is not a string"}, 400
    words_frequencies = common.parse_text(data)
    database.save_to_db(words_frequencies)
    return {"success": "saved words from text"}, 201


def parse_url(data):
    try:
        url = urlparse(data)
        if not all([url.scheme, url.netloc, url.path]):
            return {"bad request": "invalid url"}, 400

        response = requests.get(url.geturl())
        response.raise_for_status()
        words_frequencies = common.parse_text(response.text)
        database.save_to_db(words_frequencies)
        return {"success": "saved words from url"}, 201
    except requests.HTTPError as http_err:
        return {"HTTP error": "cannot open the given url"}, http_err.response.status_code


def parse_file(data):
    file_exist = os.path.exists(data)
    read_access = os.access(os.path.dirname(data), os.R_OK)
    if not all([file_exist, read_access]):
        return {"bad request": "cannot read file or file does not exist"}, 400
    words_frequencies = parallel.read_file_in_parallel(file_name=data)
    database.save_to_db(words_frequencies)
    return {"success": "saved words from file"}, 201
