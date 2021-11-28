import pygame
from ui_elements import *
from constants import Scenes
import sys
# initializing the constructor 
pygame.init()

class Controls:
    def __init__(self, screen, fps: pygame.time.Clock) -> None:
        self.running = False
        self.screen = screen
        self.fps = fps

    def run(self) -> str:
        self.running = True
        bg = Background(self.screen, "img/bg.png")
        btn_back = Button(self.screen, [248, 410, 140, 40], "Back")
        title = Text(self.screen, "Controls", [0, 22], size=36, align=Align.CENTER, decorate=True)

        change_angle = Text(self.screen, "Change Angle:", [0, 140], size=20, align=Align.CENTER)
        vertical_arrows = Text(self.screen, "Up and Down arrow keys", [0, 160], size=26, align=Align.CENTER)

        change_strength = Text(self.screen, "Change Strength:", [0, 230], size=20, align=Align.CENTER)
        horizontal_arrows = Text(self.screen, "Left and Right arrow keys", [0, 250], size=26, align=Align.CENTER)



        smoke = Smoke(self.screen)

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if btn_back.handleEvent(event) is EventResponse.CLICKED:
                    return Scenes.MAIN

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw stuff
            bg.draw()
            title.draw()
            change_angle.draw()
            vertical_arrows.draw()
            change_strength.draw()
            horizontal_arrows.draw()

            btn_back.draw()
            smoke.draw()

            # For displaying all elements
            pygame.display.update()
            self.fps.tick(60)

