from collections import namedtuple
from flask import Flask, render_template, request
import praw

app = Flask(__name__)

Post = namedtuple('Post', ['title', 'selftext', 'url', 'score', 'num_comments'])


def fetch_subreddit(subreddit_name):
    reddit = praw.Reddit(client_id='opqOO7Uavtxmeg',
                     client_secret='lXz6MRIK9AgagWlsKTTTxvCq-8o',
                     user_agent='firstscript by /u/lakara20')
    posts = []
    for submission in reddit.subreddit(subreddit_name).hot(limit=15):
        url = submission.url
        if 'reddit.com' in url or 'redd.it' in url:
            url = None
        posts.append(Post(title=submission.title, selftext=submission.selftext, url=url,
                          score=submission.score, num_comments=submission.num_comments))         
    return posts
        

@app.route('/')
def index():
    posts = []
    group_name = request.args.get('group')
    if group_name:
        posts = fetch_subreddit(group_name.strip())
    return render_template('index.html', group_name=group_name, posts=posts)

