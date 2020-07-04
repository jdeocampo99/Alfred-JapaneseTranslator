#!/usr/bin/python
# encoding: utf-8

import sys


# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3, web

API_URL = 'http://jisho.org/api/v1/search/words'


def fetch_results(query):
    """Fetches query search results from Jisho.org API.
    Args:
        query: A string representing the search query for Jisho.org.
    Returns:
        An array of JSON results from Jisho.org based on search query.
    """

    params = dict(keyword=query)
    request = web.get(API_URL, params)

    # Throw an error if request failed.
    request.raise_for_status()

    # Parse response as JSON and extract results.
    response = request.json()

    return response['data']


def english_def_formatter(senses):
    """Formats the english definitions into a list separated by commas

    Args:
        senses (array with dict elements): an array of english definitions for a given vocabulary word
    Returns:
        formatted_definitions (string): a string containing formatted english definitions
    """
    # iterate through each item in senses, and grab the english definitions
    eng_def_list = []
    for sense in senses:
        if 'english_definitions' in sense:
            # iterate through each english definition in a english_definitions, and add it to a list
            for i in range(0, len(sense['english_definitions'])):
                eng_def_list.append(sense['english_definitions'][i])
    return ', '.join(eng_def_list)


def add_vocab_item(wf, vocab):
    """Parses the JSON parameter to loop through vocab results. Adds the workflow item when parsed.
    Args:
        wf: workflow object
        vocab: A dict of information for a single japanese vocabulary result
    """

    # storing japanese reading tuple in an array
    vocabulary = vocab['japanese']

    # grabs first japanese word + reading. most common reading
    word_reading = vocabulary[0]

    # kanji reading stored in a string
    reading = word_reading['reading']

    # senses contains a list of items, where each item contains english_definitions inside it
    senses = vocab['senses']

    # storing english definitions in a string
    formatted_english_defs = english_def_formatter(senses)

    # vocab is only kana
    if 'reading' in word_reading and 'word' not in word_reading:
        title = word_reading['reading']
        subtitle = formatted_english_defs
    # vocab has at least one kanji in it
    else:
        title = word_reading['word']
        subtitle = reading + u' | ' + formatted_english_defs

    # create the workflow item
    wf.add_item(title=title, subtitle=subtitle, arg=title, valid=True)


def main(wf):

    # If the user has typed a word, store the query
    if len(wf.args):
        query = wf.args[0]

    else:
        None

    try:
        # if user types input, fetch the API page for that word
        if len(query):
            result = fetch_results(query)

            # if the vocab word exists in the API, add each item to an alfred item
            if result:
                # limit results to 25
                for i in range(0, min(len(result), 25)):
                    add_vocab_item(wf, result[i])
            # if vocab word doesnt exist in dictionary, then display error message
            else:
                error_msg = "No results found for '%s'" % (query)
                wf.add_item(error_msg, arg=query, valid=True)

    except:
        error_msg = "There was an issue retrieving Jisho results"
        wf.add_item(error_msg, valid=True)

    # Send output to Alfred. You can only call this once.
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
