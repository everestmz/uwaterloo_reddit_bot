import praw, os, json
import helpers

def print_comment_thread(child, r):
    parent = r.get_info(thing_id=child.parent_id)
    if not type(parent) == praw.objects.Submission:
        print parent.body
        print "----------------------------NEXT-----------------------------"
        if not parent.is_root:
            print_comment_thread(parent, r)

reddit = praw.Reddit(user_agent='uw_reddit_ai')
reddit.login('uw_reddit_bot', os.environ['UWATERLOO_REDDIT_KEY'], disable_warning=True)

hot_submissions = reddit.get_subreddit('uwaterloo').get_hot(limit=10)

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
