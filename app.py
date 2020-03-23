from flask import Flask
from words.api.views import words_blueprint
from words.extensions import db


def create_app(testing=False):
    """Application factory, used to create application
    """
    app = Flask("words")
    app.config.from_object("words.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    """configure flask extensions
    """
    # db.init_db(app)
    pass


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(words_blueprint)


if __name__ == '__main__':
    create_app().run()
