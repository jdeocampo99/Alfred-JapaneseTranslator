#!/usr/bin/python
# encoding: utf-8

import sys

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3, web

__version__ = '1.0.0'

TENSES = [u'Present', u'Negative Present', u'Past', u'Negative Past', u'-te Form', u'Volitional', u'Potential', u'Negative Potential',
          u'Passive', u'Negative Passive', u'Causative', u'Negative Causative', u'Imperative', u'Negative Imperative',
          u'Conditional', u'Conditional (-tara）']


def clean_string(raw_query):
    """Cleans up query by removing white space and converting japanese input into romaji for url usage

    Args:
        query (string): a query written by the user
    """
    # Library which cleans up
    import pykakasi

    ### japanese conversion to romaji ####
    kakasi = pykakasi.kakasi()    # instantiating kakasi object
    kakasi.setMode("J", "a")      # Japanese to ascii
    kakasi.setMode("H", "a")      # Hiragana to ascii
    kakasi.setMode("K", "a")      # Katakana to ascii
    conv = kakasi.getConverter()  # initializing converter
    query = conv.do(raw_query)    # applying converter
    ######################################

    query = query.replace(' ', '')
    return query


def fetch_data(query):
    """Fetches data from URL specified by the user query

    Args:
        query (string): user inputted query
    Returns:
        reversoSoup (beautiful soup object): Formatted html of the page we are looking for
    """
    # importing beautiful soup
    from bs4 import BeautifulSoup, SoupStrainer

    # Building correct URL
    URL = u'https://conjugator.reverso.net/conjugation-japanese-verb-' + query + \
        u'.html'
    URL = URL.strip()
    # get page
    result = web.get(URL)
    # raise warning if failed to reach
    result.raise_for_status()
    # Soup Strainer to constrain scraping only to the html blocks with the conjugation inside it
    only_ruby = SoupStrainer("span", class_="ruby")
    # converting page to beautiful soup object
    reverso_soup = BeautifulSoup(
        result.text, 'html.parser', parse_only=only_ruby)

    return reverso_soup


def parse_data(soup_object, query):
    """Scrapes the web page for the appropriate verb conjugations and then places them in the appropriate alfred items

    Args:
        soup_object (BeautifulSoup): Soup Object containing all the html for a page given the japanese verb
        query (str) : query so that user can hit enter on any of the conjugations and be brought to the reverso.net page
    Returns:
        Prints out array of alfred objects containing the conjugations
    """

    # Scrape for class which contains the conjugations
    conjugations = soup_object.findAll("span", class_="ruby")
    # zipping the plain/formal conjugations into pairs [1,2],[3,4]...[n,n+1]
    paired_conjugations = zip(conjugations[1:], conjugations[2:])[::2]
    # destructuring the plain forms and polite forms into separate lists
    plain_forms, polite_forms = zip(*paired_conjugations)
    # Type conversion to lists
    plain_forms, polite_forms = list(plain_forms), list(polite_forms)

    # iterate through each pair of conjugations and make them into an alfred item
    for i in range(0, len(TENSES)):
        title = TENSES[i]
        # 'value' attribute in the HTML contains the conjugation
        subtitle = plain_forms[i].get('value') + u' | ' + \
            polite_forms[i].get('value')
        wf.add_item(title, subtitle, arg=query, valid=True)


def main(wf):

    # Reading in user args
    args = wf.args
    raw_query = args[0]

    # clean up string for query
    query = clean_string(raw_query)

    if wf.update_available:
        wf.add_item('A newer version of Japanese Translator Workflow is available. \
        Please hit enter to download and install the new version.', autocomplete='workflow:update')

    try:
        # Calling webscraper
        reverso_soup = fetch_data(query)
        # Scraping conjugations and adding them to alfred workflow
        parse_data(reverso_soup, query)

    except:
        error_msg = u'We couldn\'t find any matches. Please double check spelling'
        wf.add_item(error_msg)

    # Send output to Alfred. You can only call this once.
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3(libraries=['./lib'], update_settings={
        'github_slug': 'justindeocampo/Alfred-JapaneseTranslator',
        'version': __version__,
        'frequency': 14
    })
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
