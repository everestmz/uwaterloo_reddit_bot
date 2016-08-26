from tools.helpers import login_to_reddit, praw

def hot_post_stream(threads, count):
    reddit = login_to_reddit()
    comment_classifications = []
    hot_submissions = reddit.get_subreddit('uwaterloo').get_top_from_all()

    threads_to_add = []
    for post in hot_submissions:

        if len(threads_to_add) > count:
            break

        if post.id in threads:
            continue
        else:
            threads_to_add.append(post.id)
            print len(threads_to_add)

        for comment in praw.helpers.flatten_tree(post.comments):

            if not hasattr(comment, 'body'):
                continue

            comment_classifications.append({"text": comment.body, "class": comment.score})

    return {"threads": threads_to_add, "data": comment_classifications}

def cherry_pick_thread(link, threads):
    r = login_to_reddit()
    comment_classifications = []
    threads_to_add = []

    thread = r.get_submission(link)

    if thread.id in threads:
        return {"threads": [], "data": []}
    elif thread.id not in threads_to_add:
        threads_to_add.append(thread.id)

    for c in praw.helpers.flatten_tree(thread.comments):
        if not hasattr(c, 'body'):
            continue

        comment_classifications.append({"text": c.body, "class": c.score})

    return {"threads": threads_to_add, "data": comment_classifications}

def generate(count, threads):
    reddit = login_to_reddit()
    comment_classifications = []
    threads_to_add = []

    for c in praw.helpers.comment_stream(reddit, 'uwaterloo'):
        print len(comment_classifications)
        if len(comment_classifications) == count:
            break

        if c.submission.id in threads:
            continue
        elif c.submission.id not in threads_to_add:
            threads_to_add.append(c.submission.id)

        comment_classifications.append({"text": c.body, "class": c.score})

    return {"threads": threads_to_add, "data": comment_classifications}