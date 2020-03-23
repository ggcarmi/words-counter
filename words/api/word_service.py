import requests
from requests import HTTPError

from urllib.parse import urlparse
import os

from words.commons import words_parser_common as common
from words.commons import words_parser_parallel as parallel
from ..database import db


def parse_text(data):
    if type(data) != str:
        return "data not a sring"
    words_frequencies = common.get_words_frequencies(data)
    db.save_to_db(words_frequencies)
    return f"parsed text, dict len: {len(words_frequencies)}"


def parse_url(data):
    try:
        url = urlparse(data)
        if not all([url.scheme, url.netloc, url.path]):
            return "bad url"
        response = requests.get(url.geturl())
        response.raise_for_status()
        words_frequencies = common.get_words_frequencies(response.text)
        db.save_to_db(words_frequencies)
        return "saved words from url"
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6


def parse_file(data):
    file_exist = os.path.exists(data)
    read_access = os.access(os.path.dirname(data), os.R_OK)
    if not all([file_exist, read_access]):
        return "error, cannot read file or file does not exist"

    words_frequencies = parallel.read_file_in_parallel(file_name=data)
    db.save_to_db(words_frequencies)
    return "words from text file saved to db"
