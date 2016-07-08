import praw
from tools.helpers import flip, login_to_reddit
from classifier_helpers import use_pipeline, combine_full_data, cross_validate
from tools.pipelines import TYPES as pipeline_types

def print_comment_thread(child, r):
    parent = r.get_info(thing_id=child.parent_id)
    if not type(parent) == praw.objects.Submission:
        print parent.body
        print "----------------------------NEXT-----------------------------"
        if not parent.is_root:
            print_comment_thread(parent, r)

def cherry_pick_thread(threads):
    reddit = login_to_reddit()
    threads_to_add = []
    comment_classifications = []

    print "Link to thread"
    link = raw_input("> ")
    thread = reddit.get_submission(link)

    if thread.id in threads:
        return {"threads": [], "data": []}
    elif thread.id not in threads_to_add:
        threads_to_add.append(thread.id)

    for comment in praw.helpers.flatten_tree(thread.comments):
        if not hasattr(comment, 'body'):
                continue

        print_comment_thread(comment, reddit)
        print comment.body

        result = raw_input("> ")

        if result == "1" or result == "0":
            comment_classifications.append({"text": comment.body, "class": int(result)})
        elif result == "finish":
            break

    return {"threads": threads_to_add, "data": comment_classifications}

def new_comment_loop(count, threads, rows):
    reddit = login_to_reddit()
    comment_classifications = []
    threads_to_add = []

    for c in praw.helpers.comment_stream(reddit, 'uwaterloo', limit=count):
        if c.submission.id in threads:
            continue
        elif c.submission.id not in threads_to_add:
            threads_to_add.append(c.submission.id)

        print "-----------------------------"

        result = use_pipeline(combine_full_data(rows), 'bernoulli', [c.body])

        print_comment_thread(c, reddit)
        print c.body

        if result[0] == 1:
            print "Troll"
        else:
            print "Not Troll"

        print "Correct?"
        add = raw_input("[y/n/x] > ")

        if add == "y":
            comment_classifications.append({"text": c.body, "class": int(result[0])})
        elif add == "x":
            break
        else:
            comment_classifications.append({"text": c.body, "class": flip(int(result[0]))})

    return {"threads": threads_to_add, "data": comment_classifications}

def get_hot_post_comments(count, threads):
    reddit = login_to_reddit()
    comment_classifications = []
    hot_submissions = reddit.get_subreddit('uwaterloo').get_hot(limit=count)

    threads_to_add = []

    for post in hot_submissions:

        if post.id in threads:
            continue

        print "NEW POST::Cancel data collection?[y/n]"
        result = raw_input("> ")
        if result == "y":
            break

        if post.id not in threads_to_add:
            threads_to_add.append(post.id)

        for comment in praw.helpers.flatten_tree(post.comments):

            if not hasattr(comment, 'body'):
                continue

            print_comment_thread(comment, reddit)
            print comment.body

            result = raw_input("> ")

            if result == "1" or result == "0":
                comment_classifications.append({"text": comment.body, "class": int(result)})
            elif result == "finish":
                break

    return {"threads": threads_to_add, "data": comment_classifications}

def classify_cmdline(data):
    comment_classifications = []

    while True:
        randomly_permuted_frame = combine_full_data(data)

        print "Type your phrase"
        phrase = raw_input("> ")

        result = use_pipeline(randomly_permuted_frame, 'bernoulli', [phrase])

        if result[0] == 1:
            print "Troll"
        else:
            print "Not Troll"

        print "Correct?"
        add = raw_input("[y/n/exit] > ")

        if add == "y":
            comment_classifications.append({"text": phrase, "class": int(result[0])})
        elif add == "exit":
            break
        else:
            comment_classifications.append({"text": phrase, "class": flip(int(result[0]))})

    return {"threads": [], "data": comment_classifications}

def print_metrics(data):
    frame = combine_full_data(data)

    for type in pipeline_types:
        print type

        testing = cross_validate(frame, type)

        print sum(testing['scores']) / len(testing['scores'])
        print testing['confusion']
        print "---------------------------"