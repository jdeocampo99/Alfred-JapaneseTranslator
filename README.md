# Alfred-JapaneseTranslator

This is an Alfred workflow which translates between English and Japanese, has in-depth vocabulary lookups, and generates verb conjugations for a given verb. I made this to aid in studying Japanese as I found myself often
double checking a sentence I was saying on the internet quite often. Through this workflow, you can do it much faster. 

Sentence translation is performed through Alfred's built in system where the user may provide a query and it redirects them through their default browser. Vocabulary 
look-ups were made possible by Jisho.org's API and allows for quick and easy viewing of definitions within Alfred. Verb conjugations were implemented through 
Web Scraping via Beautiful Soup 4 using Reverso.net's verb conjugation portion of their website.

This app was made using Python2 and is currently test on and works for Alfred 4.

## **[DOWNLOAD](https://github.com/JustinDeOcampo/Alfred-JapaneseTranslator/releases/download/v1.0.0/Japanese-Translator.alfredworkflow)**

## DEMO

![jpv demo](https://media.giphy.com/media/jslTiSzo3k129SiAdL/giphy.gif)
![jpc demo](https://media.giphy.com/media/YSwEfXD7Y7JuWCYSYE/giphy.gif)
![jte demo](https://media.giphy.com/media/iIYp2v1eESRX9pVzAq/giphy.gif)
## Commands:
- `jpv` -> "Japanese Vocabulary". Type in any english or japanese word to receive Japanese definitions.

- `jpc` -> "Japanese Conjugation". Type in any verb in Japanese and it will return a list of the possible conjugations.
  
  NOTE: `jpc` does not handle plugging in english verbs. Only Japanese verbs, though you can type them using the english alphabet or using kana.
  
- `jte` -> "Japanese to English". Type in any sentence in Japanese in order to filter your query through google translate.

- `etj` -> English to Japanese". Type in any english sentence to filter your query through google translate.

- `Enter` -> You can press the enter key on any query you make to be redirected to either Jisho.org, Reverso.net, or translate.google.com.

## Updates:
This is currently version 1.0.0. Alfred will periodically check for updates to this workflow every two weeks and prompt for installation if there is one.

## Credit:
This wouldn't be possible with out [Alfred](https://www.alfredapp.com). Quite possibly one of my favorite productivity apps on mac.

Thank you to [Jisho.org](https://jisho.org) for their huge dictionary of words and their API which made searching queries much faster. 

Thanks to [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for offering such a great tool for web scraping.

This workflow uses the [Alfred-Workflow](https://github.com/deanishe/alfred-workflow) library, licensed under The MIT License.

Inspired by [Jisho-Alfred](https://github.com/janclarin/jisho-alfred) which is a really good workflow that uses the same Jisho API to do essentially the same thing,
I just wanted to add the extra functionality described above. 

