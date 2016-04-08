import random
import re


class Markov(object):

    def __init__(self, filename):
        self.words = self.file_to_words(filename)
        self.starters = []
        self.temp_db = {}
        self.db = {}
        self.build_db(self.words)

    def caps(self, word):
        if word.isupper() and word != 'I':
            word = word.lower()
        elif word[0].isupper():
            word = word.lower().capitalize()
        else:
            word = word.lower()
        return word

    def file_to_words(self, filename):
        with open(filename, 'r') as f:
            words = [self.caps(w) for w in re.findall(r"[\w']+|[.,!?;]",
                    f.read())]
            return words

    def temp_mapping(self, head, tail):
        while len(head) > 0:
            key = tuple(head)
            if key in self.temp_db:
                if tail in self.temp_db[key]:
                    self.temp_db[key][tail] += 1.0
                else:
                    self.temp_db[key][tail] = 1.0
            else:
                self.temp_db[key] = {}
                self.temp_db[key][tail] = 1.0
            head = head[1:]

    def build_db(self, words, length=1):
        self.starters.append(words[0])
        for i in range(1, len(words) - 1):
            if i <= length:
                head = words[:i + 1]
            else:
                head = words[i - length + 1:i + 1]
            tail = words[i + 1]
            if head[-1] in '.' and tail not in '.,!?;':
                self.starters.append(tail)
            self.temp_mapping(head, tail)
        for s, e in self.temp_db.iteritems():
            total = sum(e.values())
            self.db[s] = dict([(k, v / total) for k, v in e.iteritems()])

    def next(self, previous):
        sum = 0.0
        r = ''
        index = random.random()
        while tuple(previous) not in self.db:
            previous.pop(0)
        for k, v in self.db[tuple(previous)].iteritems():
            sum += v
            if sum >= index and r == '':
                r = k
        return r

    def gen(self, length=1):
        current = random.choice(self.starters)
        gave = current.capitalize()
        previous = [current]
        while current not in '.':
            current = self.next(previous)
            previous.append(current)
            if len(previous) > length:
                previous.pop(0)
            if current not in '.,!?;':
                gave += ' '
            gave += current
        return gave


if __name__ == '__main__':
    import sys
    m = Markov(sys.argv[1])
    print m.gen()
