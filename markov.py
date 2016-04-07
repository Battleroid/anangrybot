from itertools import izip
from random import choice


class Markov(object):

    EOS = ('.', '!', '?')

    def __init__(self, training_file, size=3):
        self.training_file = training_file
        self.lines = self.file_to_lines(self.training_file)
        self.database = dict()
        self._build_database(self.lines, size)

    def file_to_lines(self, fo):
        lines = open(fo, 'r').readlines()
        return lines

    def _build_database(self, lines, size=3):

        def ngrams(line, n=3):
            return izip(*[line[i:] for i in range(n)])

        for line in lines:
            line = line.split()
            for a, b, c in ngrams(line, size):
                state = (a, b)
                rest = c
                if state not in self.database:
                    self.database[state] = {}
                if rest not in self.database[state]:
                    self.database[state] = [rest]

    def generate(self):
        sentence = []
        seed = choice(self.database.keys())
        a, b = seed[0], seed[1]
        while True:
            try:
                c = choice(self.database[(a, b)])
            except KeyError:
                break
            sentence.append(c)
            if c[-1] in Markov.EOS:
                break
            a, b = b, c
        return ' '.join(sentence)
