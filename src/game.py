import os
import re
import random
import time

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
        for pack in words.get('length').values():
            elegible_words += pack
    else:
        elegible_words = words.get('length').get(str(word_len))

    word = random.choice(elegible_words).upper()
    
    # Exclude words with rare characters
    #FIXME input file of words must be cleaned to avoid this code
    if any(c not in words.get('letters') for c in word.upper()):
        return get_random_word(word_len, words)

    return word

def get_upper_lines(word):
    # Return 4 strings to print the word with the ñ symbol
    regular = re.sub('[^Ñ]', 9*' ' ,word)
    first = regular.replace('Ñ', '   ##  ##')
    second = regular.replace('Ñ', ' ##  ##  ')
    third = len(word)*9*' '
    return first[1:], second[1:], third[1:], word.replace('Ñ', 'N') # Delete first character because tprint start with letter

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

def check_correct_input(c, valid):
    # Check if the input string is correct (letters are contained in valid string)
    return c != '' and all(x in valid for x in c)

def draw_fails(fails):
    # Draw the fails figure
    print('   |----' if fails >= 3 else '   |' if fails >= 2 else '')
    print('   |   |' if fails >= 4 else '   |' if fails >= 2 else '')
    print('   |   O' if fails >= 5 else '   |' if fails >= 2 else '')
    print('   |  /|\\' if fails >= 8 else'   |  /|' if fails >= 7 else '   |   |' if fails >= 6 else '   |' if fails >= 2 else '')
    print('   |  / \\' if fails == 10 else'   |  /' if fails >= 9 else '   |' if fails >= 2 else '')
    print('   |   ' if fails >= 2 else '')
    print('-------' if fails >= 1 else '')

def result_color(win):
    # Change console color if win or loose
    intermittence = True
    for i in range(8):
        if intermittence:
            if win:
                os.system('color af')
            else:
                os.system('color cf')
            time.sleep(0.5)
            intermittence = False
        else:
            os.system('color 0f')
            time.sleep(0.5)
            intermittence = True

def color_fail():
    # Perform red fail
    os.system('color 0c')
    time.sleep(0.3)
    os.system('color 0f')

def color_win():
    # Perform green check
    os.system('color 0a')
    time.sleep(0.3)
    os.system('color 0f')

def play(texts, players, words):
    os.system('cls')

    max_len = max(map(int, words.get('length').keys()))
    word_len = get_word_len(texts, max_len)
    word = get_random_word(word_len, words)

    max_fails = 10
    fails = 0
    guess_word = '_' * len(word)
    remaining_letters = list(words.get('letters'))
    used_letters = []
    random.shuffle(players)
    len_players = len(players)
    current_player = -1

    while guess_word != word:
        os.system('cls')
        
        current_player += 1

        print_word(guess_word)
        print(texts.get('remaining_letters') + ' '.join(remaining_letters))
        print(texts.get('used_letters') + ' '.join(used_letters) + '\n')

        draw_fails(fails)
        if fails == max_fails:
            break

        if len_players:
            print(texts.get('player_input') + players[current_player % len_players])
        
        c = input(texts.get('input')).upper()

        while not check_correct_input(c, words.get('letters')):
            c = input(texts.get('invalid_input')).upper()
        
        if len(c) > 1:
            if c == word:
                guess_word = c
            else:
                fails += 1
                color_fail()
        else:
            if c not in remaining_letters:
                fails += 1
                color_fail()
            else:
                remaining_letters.remove(c)
                used_letters.append(c)

                if c in word:   
                    color_win()  
                    guess_word = re.sub(f'[^{"".join(used_letters)}]', '_' , word)
                else:
                    fails += 1
                    color_fail()

    os.system('cls')
    print_word(guess_word)
    print(texts.get('remaining_letters') + ' '.join(remaining_letters))
    print(texts.get('used_letters') + ' '.join(used_letters) + '\n')
    if word == guess_word:
        result_color(True)
        if not len_players:
            print(texts.get('you_win'))
        else:
            print(players[current_player % len_players] + texts.get('player_win'))
    else:
        result_color(False)
        print(texts.get('game_over'))
        print(texts.get('reveal_word') + word)
    draw_fails(fails)

