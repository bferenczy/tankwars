import pygame 
from ui_elements import *
from constants import Scenes
import sys
  
# initializing the constructor 
pygame.init() 
pygame.mixer.init()

class MainMenu:
    def __init__(self, screen, fps: pygame.time.Clock) -> None:
        self.screen = screen
        self.running = False
        self.fps = fps

    def run(self) -> Scenes:
        self.running = True 
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("sound/main_theme.wav")
            pygame.mixer.music.play(-1)

        bg = Background(self.screen, "img/bg.png")
        smoke = Smoke(self.screen)
        
        title = Text(self.screen, "Tank Wars", pos=[0, 22], size=60, decorate=True, align=Align.CENTER)

        btn_new_game = Button(self.screen, [248, 134, 160, 40], "New Game")
        btn_scores = Button(self.screen, [248, 185, 160, 40], "Scores")
        btn_controls = Button(self.screen, [248, 236, 160, 40], "Controls")
        btn_quit = Button(self.screen, [248, 287, 160, 40], "Quit")

        while self.running: 
            # Handle events
            for event in pygame.event.get():
                resp = btn_new_game.handleEvent(event)
                if resp is EventResponse.CLICKED:
                    return Scenes.NEW

                if btn_controls.handleEvent(event) is EventResponse.CLICKED:
                    return Scenes.CONTROLS

                if btn_scores.handleEvent(event) is EventResponse.CLICKED:
                    return Scenes.SCORES

                if btn_quit.handleEvent(event) is EventResponse.CLICKED:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            # Draw stuff
            bg.draw()
            title.draw()
            btn_new_game.draw()
            btn_scores.draw()
            btn_controls.draw()
            btn_quit.draw()
            smoke.draw()

            # For displaying all elements
            pygame.display.update()
            self.fps.tick(60)

        return Scenes.MAIN
