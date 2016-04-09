"""
Usage:
    tweet.py [options] <config>

Options:
    -h --help  Show this screen.
    -n --new  Create template config file.
"""

from docopt import docopt
from markov import Markov
from twitter import Api
from ConfigParser import ConfigParser


def create_config(filename):
    conf = ConfigParser(allow_no_value=True)
    conf.add_section('twitter')
    conf.add_section('markov')
    conf.set('twitter', 'consumer_key', 'key')
    conf.set('twitter', 'consumer_secret', 'secret')
    conf.set('markov', 'training_file', '/path/to/training.txt')
    conf.set('markov', 'ngram_length', value=2)
    conf.set('markov', 'word_limit', -1)
    f = open(filename, 'w')
    conf.write(f)
    f.close()


def load_config(filename):
    f = open(filename, 'r')
    conf = ConfigParser()
    conf.readfp(f)
# TODO: finish


def generate(filename):
    pass


def tweet(config):
    pass


if __name__ == '__main__':
    args = docopt(__doc__)
    new = args['--new']
    filename = args['<config>']
    if new:
        import sys
        create_config(filename)
        sys.exit(0)
    config = load_config(filename)
    # tweet(config)
