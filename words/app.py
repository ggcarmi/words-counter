from flask import Flask

import logging
import sys

from words.api.views import words_blueprint


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("words")
    app.config.from_object("words.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_logger(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(words_blueprint)


def configure_logger(app):
    if not app.logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    create_app().run()
