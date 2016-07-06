import json

def load_json_into_array(filename):
    with open(filename) as f:
        raw_text = f.read().replace('\n', '')
        return json.loads(raw_text)

def write_to_data_file(filename, data):
    wr = open(filename, 'w')
    wr.write(data)
    wr.close

def add_to_data(filename, parent_key, object):
    data = load_json_into_array(filename)[parent_key]
    data.append(object)
    write_to_data_file(filename, json.dumps({parent_key: data}))

def bulk_add_to_data(filename, parent_key, new_stuff):
    original = load_json_into_array(filename)[parent_key]
    final = original + new_stuff
    write_to_data_file(filename, json.dumps({parent_key: final}))