import json

import yaml


def convert_from_string(convert_to, value, conversion_function_lookup=None):
    if conversion_function_lookup is None:
        conversion_function_lookup = {}
    if convert_to:
        if convert_to == 'int':
            value = int(value)
        elif convert_to == 'float':
            value = float(value)
        elif convert_to == 'json':
            value = json.loads(value)
        elif convert_to == 'yaml':
            value = yaml.safe_load(value)
        elif conversion_function_lookup and (convert_to in conversion_function_lookup):
            value = conversion_function_lookup[convert_to](value)
        else:  # elif convert_to == 'str':
            value = str(value)
    return str(value)


def replace_variables(string_to_replace, variables):
    result = string_to_replace

    while True:
        match_found = False
        for variable in variables:
            to_search = "${" + variable + "}"
            if to_search in result:
                result = result.replace(to_search, str(variables[variable]))
                match_found = True
        if not match_found:
            break

    return result
