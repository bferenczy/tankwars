import pygame 
import main_menu
from ui_elements import *
from constants import Scenes
import sys
# initializing the constructor 
pygame.init() 

class NewGameMenu:
    def __init__(self, screen, fps: pygame.time.Clock) -> None:
        self.running = False
        self.screen = screen
        self.fps = fps
        self.state = {
            "player1": '',
            "player2": 'Konrad',
            "AI": True,
            "p1_color": 'Red',
            "p2_color": 'Red'
        }
        
    def __draw_title(self):
        title_color = [90, 54, 28]
        title_font = pygame.font.SysFont('Impact', 36)
        title = title_font.render('NEW GAME', True, title_color)
        self.screen.blit(title, [245, 22])
        pygame.draw.rect(self.screen, title_color, [221, 44, 13, 5])
        pygame.draw.rect(self.screen, title_color, [406, 44, 13, 5])

    def __draw_texts(self):
        text_color = [90, 54, 28]
        player_font = pygame.font.SysFont('Impact', 30)
        player1 = player_font.render('PLAYER 1', True, text_color)
        player2 = player_font.render('PLAYER 2', True, text_color)
        self.screen.blit(player1, [80, 100])
        self.screen.blit(player2, [380, 100])
    
    def run(self) -> str:
        self.running = True

        bg = Background(self.screen, "img/bg.png")

        inp_player1_name = InputField(self.screen, [80, 180, 160, 40], "Name")
        sw_player1_color = Switch(self.screen, [80,255,160,40], ["Red", "Blue"], "Color")

        inp_player2_name = InputField(self.screen, [380, 180, 160, 40], "Name")
        sw_player2_mode = Switch(self.screen, [380, 255, 160, 40], ["AI", "Human"], "Mode")
        sw_player2_color = Switch(self.screen, [380,330,160,40], ["Red", "Blue"], "Color")

        btn_start = Button(self.screen, [328, 410, 140, 40], "Start")
        btn_back = Button(self.screen, [168, 410, 140, 40], "Back")

        smoke = Smoke(self.screen)

        while self.running: 
            # Handle events
            for event in pygame.event.get():
                if inp_player1_name.handleEvent(event) is EventResponse.KEYPRESS:
                    self.state["player1"] = inp_player1_name.text
                
                if inp_player2_name.handleEvent(event) is EventResponse.KEYPRESS:
                    self.state["player2"] = inp_player2_name.text

                if sw_player1_color.handleEvent(event) is EventResponse.CLICKED:
                    self.state["p1_color"] = ('Red' if sw_player1_color.state else 'Blue')
                
                if sw_player2_color.handleEvent(event) is EventResponse.CLICKED:
                    self.state["p2_color"] = ('Red' if sw_player2_color.state else 'Blue')

                if sw_player2_mode.handleEvent(event) is EventResponse.CLICKED:
                    self.state["AI"] = sw_player2_mode.state
                
                if btn_start.handleEvent(event) is EventResponse.CLICKED:
                    return Scenes.GAME

                if btn_back.handleEvent(event) is EventResponse.CLICKED:
                    return Scenes.MAIN

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Draw stuff
            bg.draw()
            self.__draw_title()
            self.__draw_texts()
            inp_player1_name.draw()
            inp_player2_name.draw()
            sw_player1_color.draw()
            sw_player2_color.draw()
            sw_player2_mode.draw()
            btn_start.draw()
            btn_back.draw()
            smoke.draw()
            
            
            
            # For displaying all elements
            pygame.display.update()
            self.fps.tick(60)
