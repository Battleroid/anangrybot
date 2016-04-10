"""
Usage:
    markov.py [options] <training_file> [<n>]

Options:
    -h --help  Show this screen.
    -l --length=<len>  Set n-gram length [default: 2].
    --limit=<lim>  Total number of words max per sentence.
"""

from collections import defaultdict
from collections import Counter
from random import randrange
from random import choice
from itertools import izip
from itertools import islice
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from lxml import html
from docopt import docopt
import string


class Markov(object):

    def __init__(self, filename, limit=None, length=2):
        self.limit = limit
        self.length = length
        self.db = self.create_db(filename)

    def create_db(self, filename):
        with open(filename, 'r') as f:
            text = f.read()
        text = html.document_fromstring(text).text_content()

        db = defaultdict(Counter)
        for sentence in sent_tokenize(text):
            if sentence.isupper():
                continue
            words = [None] + word_tokenize(sentence) + [None]
            grams = izip(*[words[i:] for i in range(self.length + 1)])
            for group in grams:
                gram = group[:self.length]
                word = group[self.length]
                db[gram][word] += 1

        return db

    def gen(self):
        starters = [w for w in self.db.keys() if w[0] is None]
        seed = choice(starters)
        sentence = list(seed[1:])
        current = seed
        while True:
            next_word = self.get_word(self.db[current])
            if (self.limit and len(sentence) >= self.limit) or not next_word:
                return ''.join(' ' + w if not w.startswith("'") and w not in
                               string.punctuation else w for w in
                               sentence).strip()
            sentence.append(next_word)
            current = tuple(sentence[- self.length:])

    def get_word(self, freq):
        ridx = randrange(sum(freq.values()))
        return next(islice(freq.elements(), ridx, None))


if __name__ == '__main__':
    args = docopt(__doc__)
    limit = int(args['--limit']) if args['--limit'] else None
    length = int(args['--length'])
    filename = args['<training_file>']
    times = int(args['<n>']) if args['<n>'] else 1
    m = Markov(filename, limit=limit, length=length)
    for _ in range(times):
        print m.gen()
