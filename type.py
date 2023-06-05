import json

import yaml


def json_object(string_value):
    return json.loads(string_value)


def yaml_object(string_value):
    return yaml.safe_load(string_value)
