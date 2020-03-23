from flask_restful import Resource
from flask import request, Response

from ...database import database
from words.api.word_service import parse_file, parse_url, parse_text


class WordApi(Resource):

    def get(self, word):
        frequncies = database.get_from_db(word)
        if frequncies is None:
            return Response(f"word: {word}, not found in the DB", status=404, mimetype='application/json')
        return Response(f"success: word: {word}, appeared: {int(frequncies)} times", status=200, mimetype='application/json')


class WordsApi(Resource):
    def post(self):
        body = request.get_json()
        input_type, data = body.get('input_type', None), body.get('data', None)

        if data is None:
            return Response("bad request: data value is empty", status=400, mimetype='application/json')

        input_types = {
            "text": parse_text,
            "url": parse_url,
            "file": parse_file
        }

        if input_type not in input_types:
            return Response("bad request: unsupported input type, please use: text, url, file", status=400, mimetype='application/json')

        return input_types.get(input_type)(data)


