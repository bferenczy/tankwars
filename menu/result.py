import pygame
from ui_elements import *
from constants import Scenes
from data.scoresdb import ScoresDB
import sys
# initializing the constructor 
pygame.init()

class Result:
    def __init__(self, screen, fps: pygame.time.Clock, result) -> None:
        self.running = False
        self.scoresdb = ScoresDB()
        self.screen = screen
        self.fps = fps
        self.result = result
        self._setWinnerLoser()
        self._saveResultToDB()

    def _saveResultToDB(self):
        self.scoresdb.save_player_result(self.winner, True)
        self.scoresdb.save_player_result(self.loser, False)


    def _setWinnerLoser(self):
        for player in self.result:
            if player['winner']:
                self.winner = player['name']
            else:
                self.loser = player['name']
   

    def run(self) -> str:
        self.running = True

        pygame.mixer.init()
        pygame.mixer.music.load("sound/victory_bg.wav")
        pygame.mixer.music.play(-1)

        bg = Background(self.screen, "img/bg.png")
        btn_rematch = Button(self.screen, [168, 410, 140, 40], "Rematch")
        btn_menu = Button(self.screen, [328, 410, 140, 40], "Menu")
        
        txt_winner = Text(self.screen, text='Winner:', color=C_BLACK, pos=[0,100], size=40, align=Align.CENTER)
        txt_winning_player = Text(self.screen, text=self.winner, pos=[0, 140], size=60, decorate=True, align=Align.CENTER)

        txt_loser = Text(self.screen, text="Loser:", pos = [0, 250], size=20, align=Align.CENTER)
        txt_loser_player = Text(self.screen, text=self.loser, pos = [0, 270], size=20, align=Align.CENTER)

        smoke = Smoke(self.screen)

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if btn_rematch.handleEvent(event) is EventResponse.CLICKED:
                    pygame.mixer.music.stop()
                    return Scenes.GAME
                if btn_menu.handleEvent(event) is EventResponse.CLICKED:
                    pygame.mixer.music.stop()
                    return Scenes.MAIN

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw stuff
            bg.draw()
            txt_winner.draw()
            txt_winning_player.draw()
            txt_loser.draw()
            txt_loser_player.draw()
            btn_menu.draw()
            btn_rematch.draw()
            smoke.draw()

            # For displaying all elements
            pygame.display.update()
            self.fps.tick(60)

