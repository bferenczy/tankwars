from numpy import tan
import pygame 
from main_menu import MainMenu
from scores import Scores
from new_game_menu import NewGameMenu
from ui_elements import *
from constants import Scenes
import sys


from controller.game_controller import GameController


pygame.init()
fps = pygame.time.Clock()
screen = pygame.display.set_mode([640, 480])
screen.fill([255,255,255])

scene = Scenes.MAIN
mainMenu = MainMenu(screen, fps)
newMenu = NewGameMenu(screen, fps)
scores = Scores(screen, fps)

def main():
    global scene, result
    while True:
        if scene is Scenes.MAIN:
            scene = mainMenu.run()
            print(newMenu.state)
        if scene is Scenes.NEW:
            scene = newMenu.run()
        if scene is Scenes.SCORES:
            scene = scores.run()
        if scene is Scenes.GAME:
            controller = GameController(screen, newMenu.state)
            scene, result = controller.run()
            from pprint import pprint
            pprint(result)


if __name__ == "__main__":
    main()
