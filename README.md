# anangrybot

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
`<training_file>` | File for use in building the n-gram cache.
`[<n>]` | Number of sentences to generate.

### Todo

- [ ] bot needs to reconnect on disconnect (and so many retries)
- [x] ~~needs to be restructured and ability to accept a range for length of generated sentence~~
- [x] ~~maybe just write the generator in Go completely?~~
- [x] ~~better handling of missing key~~
