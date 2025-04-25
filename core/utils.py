import json


def is_json(str):
    try:
        json.loads(str)
        return True
    except json.decoder.JSONDecodeError:
        return False


