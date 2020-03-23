from flask_restful import Resource
from flask import Response, request


class WordApi(Resource):
    def get(self, word):
        return f"GET word: {word}"


class WordsApi(Resource):
    def post(self):
        body = request.get_json()
        return "POST word"