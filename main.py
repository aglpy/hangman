from src import intro_screen, game

def main():
    texts, players, words = intro_screen.launch()
    input(texts.get('start_game'))
    
    while True:
        game.play(texts, players, words)
        input(texts.get('play_again'))

if __name__ == '__main__':
    main()