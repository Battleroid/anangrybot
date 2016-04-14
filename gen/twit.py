"""
Make a one off tweet from text generated via markov chain generator.

Usage:
    twit.py [options] <config>

Options:
    -h --help  Show this screen.
    -n --new   Create new config at location.
"""

from ConfigParser import ConfigParser
from docopt import docopt
from markov import Markov
import tweepy


def new_config(loc='config.cfg'):
    conf = ConfigParser(allow_no_value=True)
    conf.add_section('twitter')
    conf.set('twitter', 'consumer_key', 'key')
    conf.set('twitter', 'consumer_secret', 'secret')
    conf.set('twitter', 'access_token', 'token')
    conf.set('twitter', 'access_secret', 'secret')
    conf.add_section('markov')
    conf.set('markov', 'corpus', 'stuff.txt')
    conf.set('markov', 'pickled', value=False)
    f = open(loc, 'w')
    conf.write(f)
    f.close()


def load_config(loc='config.cfg'):
    conf = ConfigParser()
    conf.read(loc)
    return conf


def main(params):
    consumer_key = params.get('twitter', 'consumer_key')
    consumer_secret = params.get('twitter', 'consumer_secret')
    access_token = params.get('twitter', 'access_token')
    access_token_secret = params.get('twitter', 'access_secret')

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    corpus = params.get('markov', 'corpus')
    is_pickled = params.getboolean('markov', 'pickled')
    m = Markov(corpus)
    if is_pickled:
        m.load_db()
    else:
        m.make_db()

    text = m.gen(climit=140)
    api.update_status(text)


if __name__ == '__main__':
    args = docopt(__doc__)
    conf = args['<config>']
    new = args['--new']
    if new:
        new_config(conf)
        import sys
        sys.exit(0)
    params = load_config(conf)
    main(params)
