import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

REDIS_DATABASE_URI = os.getenv("DATABASE_URI")

