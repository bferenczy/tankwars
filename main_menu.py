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

    def __draw_title(self):
        title_color = [90, 54, 28]
        title_font = pygame.font.SysFont('Impact', 60)
        title = title_font.render('TANK WARS', True, title_color)
        self.screen.blit(title, [182, 22])
        pygame.draw.rect(self.screen, title_color, [158, 58, 13, 5])
        pygame.draw.rect(self.screen, title_color, [460, 58, 13, 5])

    def run(self) -> Scenes:
        self.running = True
        bg = Background(self.screen, "img/bg.png")
        smoke = Smoke(self.screen)
        
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
            self.__draw_title()
            btn_new_game.draw()
            btn_scores.draw()
            btn_controls.draw()
            btn_quit.draw()
            smoke.draw()
            
            # For displaying all elements
            pygame.display.update()
            self.fps.tick(60)
        
        return Scenes.MAIN
