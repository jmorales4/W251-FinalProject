import os

__author__ = 'jmorales'

import web

# Default route
urls = (
    '/', 'main.page',
    '/content', 'content.page',
    '/tweets', 'tweets.page',
    '/videos', 'videos.page'
)

# web.py objects
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
