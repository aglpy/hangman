from src import intro_screen, game

def main():
    texts, players, words = intro_screen.launch()
    input(texts.get('start_game'))
    game.play(texts, players, words)

if __name__ == '__main__':
    main()