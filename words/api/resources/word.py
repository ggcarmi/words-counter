from flask_restful import Resource
from flask import request

from ...database import database
from words.api.word_service import parse_file, parse_url, parse_text


class WordApi(Resource):

    def get(self, word):
        frequncies = database.get_from_db(word)
        if frequncies is None:
            return f"GET word: {word}. not found in the DB"
        return f"GET word: {word}. frequencies: {frequncies}"


class WordsApi(Resource):
    def post(self):
        body = request.get_json()
        input_type, data = body.get('input_type', None), body.get('data', None)

        if data is None:
            return "data error"

        input_types = {
            "text": parse_text,
            "url": parse_url,
            "file": parse_file
        }

        if input_type not in input_types:
            return "error, unsupported input type, please use: text, url, file"

        return input_types.get(input_type)(data)


