import pygame 
from main_menu import MainMenu
from result import Result
from scores import Scores
from new_game_menu import NewGameMenu
from ui_elements import *
from constants import Scenes
from controls import Controls
from controller.game_controller import GameController

pygame.init()
fps = pygame.time.Clock()
screen = pygame.display.set_mode([640, 480])
screen.fill([255,255,255])

scene = Scenes.MAIN
mainMenu = MainMenu(screen, fps)
newMenu = NewGameMenu(screen, fps)
scores = Scores(screen, fps)
controls = Controls(screen, fps)

def main():
    global scene, result
    while True:
        if scene is Scenes.MAIN:
            scene = mainMenu.run()
        if scene is Scenes.NEW:
            scene = newMenu.run()
        if scene is Scenes.SCORES:
            scene = scores.run()
        if scene is Scenes.GAME:
            pygame.mixer.music.stop()
            controller = GameController(screen, newMenu.state)
            scene, result = controller.run()
        if scene is Scenes.RESULT:
            pygame.mixer.music.stop()
            result = Result(screen, fps, result)
            scene = result.run()
        if scene is Scenes.CONTROLS:
            scene = controls.run()

if __name__ == "__main__":
    main()
