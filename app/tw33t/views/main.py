import logging

# from flask import g, Markup
from flask import (Blueprint, render_template, make_response, redirect, url_for, abort, request, Response)
from tw33t import app
from twitter import Twitter, OAuth, TwitterResponse
import os
from flask import jsonify
import werkzeug.exceptions


consumer_key = os.environ.get('CONSUMER_KEY', 'pWjUmsX3bJbEHTiWYoGZsVj2M')
consumer_secret = os.environ.get('CONSUMER_SECRET', '0qquXOTeyVeqdpMK9dNLK5MtfuSCz1HG3m6TVcwqeDM7NH8E2S')

POOL_TIME = 1
logging.FileHandler


from logging.config import dictConfig


dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
            'simpleformatter': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
    },
    'filters': {
        'search_filter': {
          "name": "search"
        }
    },
    'handlers':
    {
        'search_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename' : 'search.log',
            'filters': ['search_filter'],
            'level': 'INFO',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simpleformatter',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'search': {
            'level': 'INFO',
            'handlers': ['search_handler']
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
})

search_logger = logging.getLogger('search')
root_logger = logging.getLogger('root')


def get_body(self, environ=None, scope=None):
    return f'{self.description or ""}'


werkzeug.exceptions.HTTPException.get_body = get_body


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/api/tweet", methods=['GET'])
def tweet_search():

    user = request.args.get('user', default='')
    if not user:
        abort(400, 'User is required')
    try:

        twitter = Twitter(auth=OAuth('', '', consumer_key, consumer_secret))
        statuses = twitter.statuses.user_timeline(screen_name=user, count=3)

        result = []
        for status in statuses:
            result.append({
                'createdAt': status['created_at'],
                'text':  status['text'],
                'userImageProfile': status['user']['profile_image_url'],
            })

        search_logger.info(result)
        return jsonify(result)
    except Exception:
        root_logger.exception('Error while searching Name: {}'.format(user))
        abort(500, 'Something went wrong while processing')




'''

Introduce a "Get tweets" route for the client and log relevant info from each search into a file.

'''