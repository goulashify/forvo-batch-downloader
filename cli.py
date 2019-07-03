#!/usr/bin/env python3
from argparse import ArgumentParser
import os.path
import requests

# TODO(danigu): language param does not work!
LANGUAGE_ID = 118

def main():
    args = parse_args()
    words = read_delimited_wordlist(args.file)[args.offset:]
    print(f'👌  Read {len(words)} words, continuing to download pronunciations.')

    for word in words:
        link = fetch_pronounciation_download_url(word, LANGUAGE_ID, args.key)
        if (link == None):
            print(f"⚠️ The requested word {word} is not found, will be skipped.")
            continue
        
        download_word(link, word, args.dest)

def parse_args():
    """
    Reads all command line arguments.
    """
    parser = ArgumentParser(description='Command line utility to download batch pronounciations from Forvo.')
    parser.add_argument('--key', type=str, required=True, help='API key, obtained from https://api.forvo.com.')
    parser.add_argument('--lang', type=str, required=True, help='ISO 639-1 language code, !THIS DOES NOT WORK!, read readme.')
    parser.add_argument('--dest', type=str, required=True, help='The folder where the requested words will be downloaded.')
    parser.add_argument('--offset', type=int, default=0, help='The non-profit forvo plan has a request limit of 500 a day, use this to chip off the beginning of the wordlist and continue the work from there.')
    parser.add_argument('file', type=str, help='A newline separated file which the words should be read from, example:\n\tik\n\tje\n\tverloofd')
    
    return parser.parse_args()

def read_delimited_wordlist(file: str) -> [str]:
    """
    Reads and parses the wordlist.
    """
    assert os.path.exists(file), f"The path provided for the wordlist doesn't seem to exist: \"{file}\", could you double check please?"
    return open(file, 'r').read().splitlines()

def fetch_pronounciation_download_url(word: str, lang_id: int, api_key:str) -> str:
    """
    Fetches the download URL for the mp3 file containing the top rated pronunciation of word, returns None if word not found.
    """
    # Get the best rated pronunciation for this word, check response.
    req = requests.get(f"https://apifree.forvo.com/action/word-pronunciations/format/json/word/{word}/id_lang_speak/{lang_id}/id_order/rate-desc/limit/1/key/{api_key}/")
    assert req.status_code == 200, f"The request for word {word} came out with a response of {req.status_code}: {req.text}"
    
    # Parse response, check if a pronunciation is found, if not, go to the next word.
    res = req.json()
    if len(res['items']) == 0:
        return None

    # In case it's found, we return it.
    return res['items'][0]['pathmp3']

def download_word(link:str, word:str, destination_folder: str):
    """
    Downloads {link}, into {destination_folder}/{word}.mp3.
    """
    p = os.path.join(destination_folder, f"{word}.mp3")
    r = requests.get(link)
    assert r.status_code == 200, f"The download link for {word}: \"{link}\" returned a non-200 response: {r.status_code}: {r.text}"

    with open(p, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

    print(f"👌  Wrote {p}")

if __name__ == "__main__":
    main()