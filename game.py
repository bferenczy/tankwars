from numpy import tan
import pygame 
from main_menu import MainMenu
from scores import Scores
from new_game_menu import NewGameMenu
from ui_elements import *
from constants import Scenes
import tankwars
import sys

pygame.init() 
fps = pygame.time.Clock()
screen = pygame.display.set_mode([640, 480]) 
screen.fill([255,255,255])

scene = Scenes.MAIN
mainMenu = MainMenu(screen, fps)
newMenu = NewGameMenu(screen, fps)
scores = Scores(screen, fps)

def main():
    global scene
    while True:
        if scene is Scenes.MAIN:
            scene = mainMenu.run()
            print(newMenu.state)
        if scene is Scenes.NEW:
            scene = newMenu.run()
        if scene is Scenes.SCORES:
            scene = scores.run()
        if scene is Scenes.GAME:
            # TODO: change tankwars to run the same way as the other scenes
            tankwars.main()
    


if __name__ == "__main__":
    main()
