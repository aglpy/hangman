import os
import re
import random

from art import tprint as preprint

tprint = lambda x: preprint(x, font='advenger')
screen_limit = 13

def get_word_len(texts, max_len):
    # Return the length of the word or an empty string for random length
    word_len = input(texts.get('word_len'))
    
    # Check and get a correct length, integer between 1 and max language word length
    while word_len != '' and (type(word_len) is not int or not 0 < word_len <= max_len):
        try:
            word_len = int(word_len)
        except:
            word_len = input(texts.get('len_no_int'))
        else:
            if word_len <= 0:
                word_len = input(texts.get('invalid_len'))
            elif word_len > max_len:
                word_len = input(texts.get('large_len'))

    return word_len

def get_random_word(word_len, words):
    # Return a random word based on word length given
    if word_len == '':
        elegible_words = []
        for pack in words.values():
            elegible_words += pack
    else:
        elegible_words = words.get(str(word_len))
    
    return random.choice(elegible_words)

def get_upper_lines(word):
    # Return 4 strings to print the word with the ñ symbol
    regular = re.sub('[^ñ]', 9*' ' ,word)
    first = regular.replace('ñ', '   ##  ##')
    second = regular.replace('ñ', ' ##  ##  ')
    third = len(word)*9*' '
    return first[1:], second[1:], third[1:], word.replace('ñ', 'n') # Delete first character because tprint start with letter

def get_under_line(word):
    # Return the line under the word
    line = re.sub('[^_]', 9*' ' , word).replace('_', ' ####### ')
    return line[1:], word.replace('_', ' ')



def print_word(word):
    # Print the word given in a screen to fit it correctly and add the ñ symbol (not supported by library)
    if len(word) > screen_limit:
        for i in range(0, len(word), screen_limit):
            print_word(word[i:i + screen_limit])
    else:
        first, second, third, format_word = get_upper_lines(word)
        underline, format_word = get_under_line(format_word)
        print(first)
        print(second)
        print(third)
        tprint(format_word)
        print(underline)
        

def play(texts, players, words):
    os.system('cls')

    max_len = max(map(int, words.keys()))
    word_len = get_word_len(texts, max_len)
    word = get_random_word(word_len, words)
