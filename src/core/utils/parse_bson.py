from json import loads, dumps
from bson import json_util

def parse_bson_single(bson):
    bson_string = dumps(bson, sort_keys=True, indent=4, default=json_util.default)
    bson_json = loads(bson_string)
    return bson_json

def parse_bson_list(bson_array):
    return [parse_bson_single(bson) for bson in bson_array]

def parse_bson(bson):
    if not bson: return None
    is_single_bson = isinstance(bson, dict)
    if(is_single_bson):
        return parse_bson_single(bson)
    else:
        return parse_bson_list(bson)