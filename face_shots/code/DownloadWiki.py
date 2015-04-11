import os
import urllib2
import sys
import thread

__author__ = 'jmorales'


def download(path, url):
    with open(path, 'w') as f:
        try:
            print path
            f.write(urllib2.urlopen(url).read())
        except Exception as e:
            print 'Could not download {}: {}'.format(url, e)


if __name__ == "__main__":
    urls = {}
    with open('names.txt') as f:
        urls = dict(map(lambda name: (name.strip(), 'http://en.wikipedia.org/wiki/' + name.replace(' ', '_')), f))

    for name in urls:
        file_path = 'wiki2\\' + name
        if os.path.isfile(file_path): continue

        download(file_path, urls[name])




