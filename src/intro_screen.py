import yaml
import json
import os

from art import tprint

# Supported languages, each language must have a lang text file in lang/ and a dictionary file in dicts/
langs = ['es', 'en']

def get_language(texts):
    # Ask for the language and return its code
    print(texts.get('switch_lang')) 
    new_lang = input()

    while new_lang not in langs:
        print(texts.get('unknown_lang') + ', '.join(langs))
        new_lang = input()

    return new_lang

def get_player_names():
    # Get the list of player names
    players = input().split(',')
    clean_players = list(map(lambda x: x.strip(), players)) # Names are cleaned of spaces
    return clean_players

def launch(lang='es', lang_selected=False):
    # Texts are loaded
    texts = yaml.safe_load(open(f'lang/{lang}.yaml', 'r', encoding='utf-8'))

    # Intro screen
    os.system('cls')
    tprint('DELICIOUS    PY')
    tprint('HANGMAN\nTOURNAMENT')
    print(f'{texts.get("author")}: aglpy')

    # Ask for language
    if not lang_selected:
        lang = get_language(texts)
        return launch(lang, True)

    # Ask for player names
    print(texts.get('wellcome'))
    players = get_player_names()
    
    # Words loaded
    words = json.load(open(f'dicts/{lang}.json', 'r', encoding='utf-8'))

    return texts, players, words
    