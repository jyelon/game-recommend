"Miscellaneous utility functions"

import urllib.request
import urllib.parse
import json

def jfetch(url):
    "Fetch the specified URL and parse the returned text as json"
    with urllib.request.urlopen(url) as url:
        jtree = json.loads(url.read().decode())
        return jtree

def jget(json, attrib):
    "Given a json dict, fetch the specified attribute"
    if type(json) is not dict:
        raise KeyError(f'json does not contain attribute "{attrib}"')
    value = json.get(attrib)
    if value is None:
        raise KeyError(f'json does not contain attribute "{attrib}"')
    return value

def PrettyJson(json):
    "A reasonably concise representation of the json tree that shows at least the top level"
    if type(json) == list:
        return '[ %d items ]' % len(json)
    elif type(json) == dict:
        parts = []
        for k, v in json.items():
            if type(v) is list or type(v) is dict:
                parts.append(f'{repr(k)}')
            elif type(v) is str and len(v) > 40:
                parts.append(f'{repr(k)}')
            else:
                parts.append(f'{repr(k)}:{repr(v)}')
        joined = ', '.join(parts)
        return '{' + joined + '}'
    else:
        return repr(json)

def PrettyPrintJson(json):
    "Prints a reasonably concise representation of the json tree that shows at least the top level"
    print(PrettyJson(json))

def pp(json):
    "Prints a reasonably concise representation of the json tree that shows at least the top level"
    print(PrettyJson(json))

