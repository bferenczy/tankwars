import pygame 
from ui_elements import *
from constants import Scenes
import sys
  
# initializing the constructor 
pygame.init() 

class MainMenu:
    def __init__(self, screen, fps: pygame.time.Clock) -> None:
        self.screen = screen
        self.running = False
        self.fps = fps

    def run(self) -> Scenes:
        self.running = True
        bg = Background(self.screen, "img/bg.png")
        smoke = Smoke(self.screen)
        
        title = Text(self.screen, "Tank Wars", pos=[0, 22], size=60, decorate=True, align=Align.CENTER)

        btn_new_game = Button(self.screen, [248, 134, 160, 40], "New Game")
        btn_scores = Button(self.screen, [248, 185, 160, 40], "Scores")
        btn_controls = Button(self.screen, [248, 236, 160, 40], "Controls")
        btn_quit = Button(self.screen, [248, 287, 160, 40], "Quit")

        health_p1 = ProgressBar(self.screen, [22, 25, 270, 10], Align.RIGHT, C_HEALTH)
        health_p1.set_status(0.7)
        strength_p1 = ProgressBar(self.screen, [192, 38, 100, 10], Align.RIGHT, C_STRENGTH)

        p1_name = Text(self.screen, "Lacika", pos=[22, 35])
        p2_name = Text(self.screen, "Onyetueueue Ossas", pos=[617, 35], align=Align.RIGHT)
        vs = Text(self.screen, "vs", pos=[0,21], align=Align.CENTER, size=26)

        health_p2 = ProgressBar(self.screen, [348, 25, 270, 10], Align.LEFT, C_HEALTH)
        health_p2.set_status(1)
        strength_p2 = ProgressBar(self.screen, [348, 38, 100, 10], Align.LEFT, C_STRENGTH)



        while self.running: 
            # Handle events
            for event in pygame.event.get():
                resp = btn_new_game.handleEvent(event)
                if resp is EventResponse.CLICKED:
                    return Scenes.NEW

                btn_controls.handleEvent(event)
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
            health_p1.draw()
            strength_p1.draw()
            p1_name.draw()
            p2_name.draw()
            vs.draw()
            health_p2.draw()
            strength_p2.draw()
            smoke.draw()
            
            # For displaying all elements
            pygame.display.update()
            self.fps.tick(60)
        
        return Scenes.MAIN
