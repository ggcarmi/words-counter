import logging

from ..extensions import db


logger = logging.getLogger("words.sub")


def get_from_db(key):
    try:
        return db.get(key)
    except Exception as e:
        logger.debug(f"failed get from db {e}")


def save_to_db(frequencies_dict):
    try:
        with db.pipeline() as pipe:
            for key, value in frequencies_dict.items():
                pipe.incrby(name=key, amount=value)
            pipe.execute()

    except Exception as e:
        logger.debug(f"failed save to db {e}")


def save_to_db_at_once(frequencies_dict):
    db.mset(frequencies_dict)



