import json

def load_json_into_array(filename):
    with open(filename) as f:
        raw_text = f.read().replace('\n', '')
        return json.loads(raw_text)

def write_to_data_file(filename, data):
    wr = open(filename, 'w')
    wr.write(data)
    wr.close

def add_to_data(comment, classification):
    comment_classifications = load_json_into_array("troll_training_data.json")['comments']
    comment_classifications.append({"text": comment, "class": classification})
    write_to_data_file("troll_training_data.json", json.dumps({"comments": comment_classifications}))

def flip(x):
	if x == 1:
	    return 0
	else:
	    return 1