# AnAngryBot

I use collected text from a channel on a Mumble server to train a Markov chain generator. My implementation isn't the best, but it is functional. I need more practice.

### Installation & Usage

1. Install requirements with `$ pip install -r requirements.txt`
2. You'll need _punkt_ and _words_ bundles for NLTK I believe (correct me if I'm wrong). So do...

    ```python
    >>> import nltk
    >>> nltk.download()
    ```

3. Follow the instructions from there to download the appropriate modules.
4. Get a text file full of sample stuff to train it on and run it: `$ python markov.py stuff.txt`

### Options & Arguments

Name | Description
---- | -----------
`-h --help` | Show this screen.
`-l --length=<len>` | Set n-gram length [default: 2].
`--limit=<lim>` | Total number of words max per sentence.
`--char=<lim>` | Maximum characters for generated sentence.
`-p --pickle` | Load training file as pickled data instead.
`-s --save <pickle>` | Save database as pickled data.
`-u --update <pickle>` | Update pickled database with given training file.
`-d` | Don't generate any sayings.
`<training_file>` | File for use in building the n-gram cache.
`[<n>]` | Number of sentences to generate.
