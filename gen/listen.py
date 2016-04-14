"""
Start listener for markov replies or use of hashtag(s). Using the listed terms
for tracking. The list of tracked terms is comma delimited.

Usage:
    listen.py [options] <config> <track>

Options:
    -h --help  Show this screen.
    -n --new   Create new config at location.
"""

from twit import new_config, load_config
from docopt import docopt
from markov import Markov
import tweepy


class Listener(tweepy.StreamListener):

    def __init__(self, markov, is_pickled, api=None):
        super(Listener, self).__init__(api)
        self.markov = markov
        self.is_pickled = is_pickled

    def on_status(self, status):
        user = status.author.screen_name

        # save data if not pickled, quick solution for 'learning'
        if not self.is_pickled:
            print 'Saving to {}: {}'.format(self.markov.training, status.text)
            f = open(self.markov.training, 'a')
            f.write('\n' + status.text)

        try:
            message = '@' + user + ' '
            message += self.markov.gen(climit=140 - len(message))
            self.api.update_status(message[:140])
            print 'Sent: "' + message + '" to ' + user
        except tweepy.error.RateLimitError, e:
            print e

    def on_error(self, status_code):
        print 'Given status code ' + str(status_code)
        return True

    def on_timeout(self):
        print 'Timed out'
        return True


def main(params, tracklist):
    # twitter info
    consumer_key = params.get('twitter', 'consumer_key')
    consumer_secret = params.get('twitter', 'consumer_secret')
    access_token = params.get('twitter', 'access_token')
    access_token_secret = params.get('twitter', 'access_secret')

    # auth & api
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # markov
    corpus = params.get('markov', 'corpus')
    is_pickled = params.getboolean('markov', 'pickled')
    m = Markov(corpus)
    if is_pickled:
        m.load_db()
    else:
        m.make_db()

    # listener
    print 'Starting listener for "{}"...'.format(', '.join(tracklist))
    listener = Listener(m, is_pickled, api=api)
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=tracklist)

if __name__ == '__main__':
    args = docopt(__doc__)
    conf = args['<config>']
    tracklist = args['<track>'].split(',')
    new = args['--new']
    if new:
        new_config(conf)
        import sys
        sys.exit(0)
    params = load_config(conf)
    main(params, tracklist)
