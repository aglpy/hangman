import os

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

def play(texts, players, words):
    os.system('cls')

    max_len = max(map(int, words.keys()))
    word_len = get_word_len(texts, max_len)
