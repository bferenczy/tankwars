import pygame 
import main_menu
from ui_elements import *
from constants import Scenes
import sys
# initializing the constructor 
pygame.init() 

class Scores:
    def __init__(self, screen, fps: pygame.time.Clock) -> None:
        self.running = False
        self.screen = screen
        self.fps = fps
        self.table = [
            ["Zolika", 22, 112],
            ["Petike", 15, 34],
            ["Pistike", 9, 11],
            ["Irénke", 7, 5],
            ["Gabika", 5, 5],
            ["Marcika", 5, 7],
            ["Jancsika", 3, 5],
            ["Gusztika", 2, 1],
            ["Ferika", 1, 1],
            ["Jocika", 1, 2]
        ]
        
    def __draw_title(self):
        title = TXT_HEADING1.render('SCORES', True, C_BLACK)
        self.screen.blit(title, [264, 22])
        pygame.draw.rect(self.screen, C_BLACK, [240, 44, 13, 5])
        pygame.draw.rect(self.screen, C_BLACK, [387, 44, 13, 5])

    def __draw_header(self):
        hash = TXT_BODY.render('#', True, C_BLACK)
        name = TXT_BODY.render('NAME', True, C_BLACK)
        wins = TXT_BODY.render('WINS', True, C_BLACK)
        losses = TXT_BODY.render('LOSSES', True, C_BLACK)

        self.screen.blit(hash, [70, 100])
        self.screen.blit(name, [110, 100])
        self.screen.blit(wins, [300, 100])
        self.screen.blit(losses, [470, 100])
    
    def __draw_results(self):
        for idx, res in enumerate(self.table[:5]):
            rank = TXT_BODY.render(str(idx + 1) + '.', True, C_BLACK)
            name = TXT_BODY.render(res[0].upper(), True, C_BLACK)
            wins = TXT_BODY.render(str(res[1]), True, C_BLACK)
            losses = TXT_BODY.render(str(res[2]), True, C_BLACK)

            self.screen.blit(rank, [70, 130+idx*30])
            self.screen.blit(name, [110, 130+idx*30])
            self.screen.blit(wins, [300, 130+idx*30])
            self.screen.blit(losses, [470, 130+idx*30])
    
    def run(self) -> str:
        self.running = True

        bg = Background(self.screen, "img/bg.png")
        btn_back = Button(self.screen, [248, 410, 140, 40], "Back")

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
            self.__draw_title()
            self.__draw_header()
            self.__draw_results()
            btn_back.draw()
            smoke.draw()
            
            # For displaying all elements
            pygame.display.update()
            self.fps.tick(60)
