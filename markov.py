"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    key = choice([key for key in chains.keys() if key[0][0].isupper()])
    words = [key[0], key[1]]
    char_length = len(words[0]) + len(words[1]) + 2

    while key in chains:

        word = choice(chains[key])
        char_length = char_length + len(word) + 1
        if char_length > 140:
            key = tuple(words[-3:-1])
            try:
                words[-1] = choice([val for val in chains[key] if val[-1] in ".?!"])
            except IndexError:
                words[-1] = words[-1][:-3] + "..."
            break

        words.append(word)
        key = (key[1], word)

    return " ".join(words)


def tweet(chains):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    user_entry = ''
    while user_entry.lower() != 'q':
        status = api.PostUpdate(make_text(chains))
        print status.text
        print "Num of characters: {}".format(len(status.text))
        print ""
        user_entry = raw_input("Enter to tweet again [q to quit] > ")


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# Your task is to write a new function tweet, that will take chains as input
tweet(chains)
