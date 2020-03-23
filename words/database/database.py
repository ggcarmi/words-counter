from ..extensions import db


def save_to_db(frequencies_dict):
    db.mset(frequencies_dict)


def get_from_db(key):
    try:
        return db.get(key)
    except Exception as e:
        print(e)


def reset_db():
    db.flushdb()


def save_to_db_iteratively(frequencies_dict):
    try:
        with db.pipeline() as pipe: # transction=True
            for key, value in frequencies_dict.items():
                pipe.hincrby(key=key, amount=value)
            pipe.execute()

    except Exception as e:
        print()

    finally:
        print()
