# Forvo-downloader

This tool can be used as a command line utility to download pronunciations for your wordlist, for example, if you're building Anki decks.

## REQUIREMENTS

To get started, you'll need:

* Pipenv: `brew install pipenv`
* A Forvo key, get one [here](https://api.forvo.com/plans-and-pricing/)
* A newline delimited wordlist, see [provided example](docs/example_wordlist.txt)

## SYNOPSIS

Clone this repository, then:
* Install dependencies: `pipenv install`
* Given running rights: `chmod +x cli.py`
* Check out the help menu: `./cli.py -h`
* Simple example: `./cli.py --lang nl --dest ./pronunciations --key ugalabugala ./docs/example_wordlist.txt`

## LIMITATIONS

The language switch doesn't work yet, go visit the Forvo API [demo page](https://api.forvo.com/demo/), select the language you'd like, do a demo request, grab the language id from there (after `id_lang_speak` in the URL) and set the constant `LANGUAGE_ID` in the top of the file to it.