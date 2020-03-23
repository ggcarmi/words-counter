import requests
from flask import Response
from requests import HTTPError

from urllib.parse import urlparse
import os

from words.commons import words_parser_common as common
from words.commons import words_parser_parallel as parallel
from ..database import database


def parse_text(data):
    if type(data) != str:
        return Response("{bad request': data is not a string}", status=400, mimetype='application/json')
    words_frequencies = common.get_words_frequencies(data)
    database.save_to_db(words_frequencies)
    return Response("{success: saved words from text}", status=201, mimetype='application/json')


def parse_url(data):
    try:
        url = urlparse(data)
        if not all([url.scheme, url.netloc, url.path]):
            return Response("{bad request': invalid url}", status=400, mimetype='application/json')

        response = requests.get(url.geturl())
        response.raise_for_status()
        words_frequencies = common.get_words_frequencies(response.text)
        database.save_to_db(words_frequencies)
        return Response("{success: saved words from url}", status=201, mimetype='application/json')
    except HTTPError as http_err:
        return Response(f"HTTP error occurred {http_err}", status=http_err.response.status_code, mimetype='application/json')
    except Exception as e:
        print(f'Other error occurred: {e}')


def parse_file(data):
    file_exist = os.path.exists(data)
    read_access = os.access(os.path.dirname(data), os.R_OK)
    if not all([file_exist, read_access]):
        return Response("{bad request: cannot read file or file does not exist}", status=400, mimetype='application/json')
    words_frequencies = parallel.read_file_in_parallel(file_name=data)
    database.save_to_db(words_frequencies)
    return Response("{success: saved words from file}", status=201, mimetype='application/json')
