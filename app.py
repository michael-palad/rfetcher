from collections import namedtuple
from flask import Flask, render_template, request
import praw

app = Flask(__name__)

Post = namedtuple('Post', ['id', 'title', 'selftext', 'url', 'score', 'num_comments', 'subreddit'])

reddit = praw.Reddit(client_id='opqOO7Uavtxmeg',
                 client_secret='lXz6MRIK9AgagWlsKTTTxvCq-8o',
                 user_agent='firstscript by /u/lakara20')

def fetch_subreddit(subreddit_name, new_submissions=False):
    posts = []
    submissions = None
    limit = 30
    if new_submissions:
        submissions = reddit.subreddit(subreddit_name).new(limit=limit)
    else:
        submissions = reddit.subreddit(subreddit_name).hot(limit=limit)

    for submission in submissions:
        url = submission.url
        if 'reddit.com' in url or 'redd.it' in url:
            url = None
        posts.append(Post(id=submission.id, title=submission.title, selftext=submission.selftext, url=url,
                          score=submission.score, num_comments=submission.num_comments, subreddit=submission.subreddit))         
    return posts


def fetch_submission(id):
    submission = reddit.submission(id=id)
    post = Post(id=submission.id, title=submission.title, selftext=submission.selftext, url=submission.url,
                score=submission.score, num_comments=submission.num_comments, subreddit=submission.subreddit)
    submission.comments.replace_more(limit=0)
    top_level_comments = []
    for top_level_comment in submission.comments:
        comment = { 'body': top_level_comment.body,
                    'score': top_level_comment.score
        }
        if top_level_comment.author is not None:
            comment['author_name'] = top_level_comment.author.name
        top_level_comments.append(comment)

    top_level_comments.sort(key=lambda c : int(c['score']), reverse=True)
    return (post, top_level_comments)
    

@app.route('/')
def index():
    posts = []
    group_name = request.args.get('group', '')
    is_new = request.args.get('new', '0')
    if group_name:
        posts = fetch_subreddit(group_name.strip(), (is_new == '1'))
    return render_template('index.html', group_name=group_name, is_new=is_new, posts=posts)
  
  
@app.route('/submission/<string:id>')
def submission(id):
    post, comments = fetch_submission(id)
    return render_template('submission.html', group_name=post.subreddit, post=post, comments=comments,
                           referrer=request.referrer, comments_count=len(comments))
    

