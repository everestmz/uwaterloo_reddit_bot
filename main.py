import praw, os

reddit = praw.Reddit(user_agent='uw_reddit_bot')
reddit.login('uw_reddit_bot', os.environ['UWATERLOO_REDDIT_KEY'])

new_submissions = reddit.get_subreddit('uwaterloo').get_new(limit=10)