from troll_comments.data_builder import print_metrics
from tools.helpers import load_json_into_array
from tools.s3 import fetch_file_from_bucket

fetch_file_from_bucket('uw-bot-troll-classification', 'comments/data.json', 'comments.json')

data = load_json_into_array("comments.json")['comments']

print_metrics(data)