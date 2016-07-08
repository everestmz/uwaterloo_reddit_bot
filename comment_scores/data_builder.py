import praw, os

def login_to_reddit():
    reddit = praw.Reddit(user_agent='uw_reddit_ai')
    reddit.login('uw_reddit_bot', os.environ['UWATERLOO_REDDIT_KEY'], disable_warning=True)
    return reddit

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