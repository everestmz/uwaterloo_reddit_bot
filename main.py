from troll_comments.classifier import is_troll_comment
from troll_comments.data_builder import combine_full_data
from tools.helpers import load_json_into_array
from tools.s3 import fetch_file_from_bucket

#fetch_file_from_bucket('uw-bot-troll-classification', 'comments/data.json', 'comments.json')

data = load_json_into_array("comments.json")['comments']
#
# print_metrics(data)

# raw_text = None
#
# stopwords = load_json_into_array("troll_comments/stopwords.json")['stopwords']
#
# with open("comments.json") as f:
#     raw_text = f.read().replace('}, {', '')
#     raw_text = raw_text.replace('"text":', '')
#     raw_text = raw_text.replace(', "class": ', '')
#     raw_text = raw_text.replace('0', '')
#     raw_text = raw_text.replace('1', '')
#     raw_text = raw_text.replace('"', '')
#     raw_text = raw_text.replace('}', '')
#     raw_text = raw_text.replace('{', '')
#     raw_text = raw_text.replace(']', '')
#     raw_text = raw_text.replace('!', '')
#     raw_text = raw_text.replace('\'', '')
#     raw_text = raw_text.replace('?', '')
#     raw_text = raw_text.replace(':', '')
#     raw_text = raw_text.replace(';', '')
#     raw_text = raw_text.replace('\\n', '')
#     raw_text = raw_text.replace('\\n', '')
#
# wordcount = {}
#
# for word in raw_text.split(" "):
#     if word not in wordcount:
#         wordcount[word] = 1
#     else:
#         wordcount[word] += 1
#
# a = []
#
# for k,v in wordcount.items():
#     a.append([k, v])
#
# for i in sorted(a, key=lambda x: x[1]):
#     if str(i[0]) not in stopwords:
#         print i

examples = [
    'DISRUPTIVE',
    "You're a fgt",
    "I'm gay",
    "It's all fun and games until someone is",
    "dank memes br0",
    "It's just a frantic karma grab after the first panino variation was posted.",
    "HERE COME DAT BOI O SHIT WADDUP",
    "im sorry",
    "Hey I'm gonna go do some homework"
]

for e in examples:
    print e + " : " + str(is_troll_comment(data, e))