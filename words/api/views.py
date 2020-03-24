from flask import Blueprint
from flask_restful import Api

from .resources.word import WordApi, WordsApi


words_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(words_blueprint)


api.add_resource(WordApi, "/words/<word>")
api.add_resource(WordsApi, "/words")


