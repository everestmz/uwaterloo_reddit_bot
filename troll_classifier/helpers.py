import json

def load_json_into_array(filename):
    with open(filename) as f:
        raw_text = f.read().replace('\n', '')
        return json.loads(raw_text)

def write_to_data_file(filename, data):
    wr = open(filename, 'w')
    wr.write(data)
    wr.close