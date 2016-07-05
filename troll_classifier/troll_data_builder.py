import praw, os, json
import helpers
from helpers import add_to_data, flip
from troll_classifier import use_pipeline, combine_full_data

def print_comment_thread(child, r):
    parent = r.get_info(thing_id=child.parent_id)
    if not type(parent) == praw.objects.Submission:
        print parent.body
        print "----------------------------NEXT-----------------------------"
        if not parent.is_root:
            print_comment_thread(parent, r)

def login_to_reddit():
    reddit = praw.Reddit(user_agent='uw_reddit_ai')
    reddit.login('uw_reddit_bot', os.environ['UWATERLOO_REDDIT_KEY'], disable_warning=True)
    return reddit

def cherry_pick_thread(reddit):
    print "Link to thread"
    link = raw_input("> ")
    thread = reddit.get_submission(link)

    threads = helpers.load_json_into_array("threads.json")['threads']
    comment_classifications = helpers.load_json_into_array("troll_training_data.json")['comments']

    if thread.id in threads:
        exit(0)
    else:
        threads.append(thread.id)

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

    helpers.write_to_data_file("threads.json", json.dumps({"threads": threads}))
    helpers.write_to_data_file("troll_training_data.json", json.dumps({"comments": comment_classifications}))

def new_comment_loop(reddit):
    for c in praw.helpers.comment_stream(reddit, 'uwaterloo', limit=100):
        data = combine_full_data()

        print "-----------------------------"

        result = use_pipeline(data, [c.body])

        print_comment_thread(c, reddit)
        print c.body

        if result[0] == 1:
            print "Troll"
        else:
            print "Not Troll"

        print "Correct?"
        add = raw_input("[y/n] > ")

        if add == "y":
            add_to_data(c.body, int(result[0]))
        else:
            add_to_data(c.body, flip(int(result[0])))

def get_hot_post_comments(reddit, count):
    hot_submissions = reddit.get_subreddit('uwaterloo').get_hot(limit=count)

    threads = helpers.load_json_into_array("threads.json")['threads']
    comment_classifications = helpers.load_json_into_array("troll_training_data.json")['comments']

    for post in hot_submissions:

        if post.id in threads:
            continue

        print "NEW POST::Cancel data collection?[y/n]"
        result = raw_input("> ")
        if result == "y":
            break

        threads.append(post.id)

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

    helpers.write_to_data_file("threads.json", json.dumps({"threads": threads}))
    helpers.write_to_data_file("troll_training_data.json", json.dumps({"comments": comment_classifications}))

def main():
    reddit = login_to_reddit()
    #cherry_pick_thread(reddit)
    #get_hot_post_comments(reddit, 20)
    new_comment_loop(reddit)

if __name__ == "__main__":
    main()
