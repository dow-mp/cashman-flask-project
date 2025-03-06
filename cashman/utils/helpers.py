import json

def convert_bytes_to_json(func):
    res = func()
    bytes = res.data
    json_res = json.loads(bytes.decode("utf-8"))
    return json_res

def loop_to_sum(list, key):
    sum_total = 0.0
    for item in list:
        sum_total += item[key]
    return sum_total