import json

def load_json_into_array(filename):
    with open(filename) as f:
        raw_text = f.read().replace('\n', '')
        return json.loads(raw_text)

def flip(x):
	if x == 1:
	    return 0
	else:
	    return 1