from classifier_helpers import *
from data_builder import login_to_reddit
import praw

def is_troll_comment(training_data, text):
    frame = combine_full_data(training_data)
    prediction = use_pipeline(frame, 'bernoulli', [text])[0]
    probability = use_pipeline_prob(frame, 'bernoulli', [text])[0][1]
    if probability > 0.95 and prediction == 1:
        return True
    else:
        return False

def trolliness(training_data, link):
    r = login_to_reddit()
    thread = r.get_submission(link)

    thread_comments = []

    for comment in praw.helpers.flatten_tree(thread.comments):
        thread_comments.append(comment.body)

    trolls = 0
    count = 0
    for comment in thread_comments:
        count += 1
        if is_troll_comment(training_data, comment):
            trolls += 1

    troll_percent = float(trolls)/float(count)

    if thread.link_flair_text in ["Humour", "Shitpost"] and troll_percent < 0.5:
        troll_percent += 0.5

    return troll_percent