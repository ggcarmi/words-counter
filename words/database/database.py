from ..extensions import db


def get_from_db(key):
    try:
        return db.get(key)
    except Exception as e:
        print(e)


def reset_db():
    db.flushdb()


def save_to_db(frequencies_dict):
    try:
        with db.pipeline() as pipe:
            for key, value in frequencies_dict.items():
                pipe.incrby(name=key, amount=value)
            pipe.execute()

    except Exception as e:
        print(e)

    finally:
        print()


def save_to_db_at_once(frequencies_dict):
    db.mset(frequencies_dict)



