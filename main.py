import pygame
from game import ProgrammingGame

def main():
    pygame.init()
    game = ProgrammingGame()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
