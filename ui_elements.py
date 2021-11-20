from abc import ABC, abstractmethod
import pygame
from enum import Enum

from pygame.event import Event

from constants import BLACK

pygame.init()

# CONSTANTS
C_BLACK = [90, 54, 28]
C_WHITE = [255, 236, 228]
C_TRANSPARENT = [248, 214, 196]
C_HOVER =  [122, 86, 69]

TXT_BODY = pygame.font.SysFont('Impact', 20)
TXT_TITLE = pygame.font.SysFont('Impact', 26)
TXT_HEADING2 = pygame.font.SysFont('Impact', 30)
TXT_HEADING1 = pygame.font.SysFont('Impact', 36)
TXT_DISPLAY =  pygame.font.SysFont('Impact', 60)

SOUND_CLICK = pygame.mixer.Sound("sound/click.wav")
SOUND_HOVER = pygame.mixer.Sound("sound/btn_hover.wav")

class EventResponse(Enum):
    NONE = 0
    CLICKED = 1
    KEYPRESS = 2

# ALL UI ELEMENTS SHOULD IMPLEMENT THIS
class UIElement(ABC):

    def __init__(self, screen) -> None:
        self.screen = screen

    @abstractmethod
    def draw(self):
        return


    @abstractmethod
    def handleEvent(self):
        return

class Button(UIElement):
    def __init__(self, screen, rect, text) -> None:
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.text = text
        self.currently_hovered = False
    
    def draw(self):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)

        color = C_BLACK
        if hover:
            color = C_HOVER
            if not self.currently_hovered:
                pygame.mixer.Sound.play(SOUND_HOVER)
            self.currently_hovered = True
        else:
            self.currently_hovered = False

        color = (C_HOVER if hover else C_BLACK)
        pygame.draw.rect(self.screen, color, self.rect)
        text = TXT_TITLE.render(self.text.upper(), True, C_WHITE)
        offset = (self.rect.w - text.get_width()) / 2
        self.screen.blit(text, [self.rect.x + offset, self.rect.y+4])


    def handleEvent(self, event) -> EventResponse:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                pygame.mixer.Sound.play(SOUND_CLICK)
                return EventResponse.CLICKED

class InputField(ABC):

    def __init__(self, screen, rect, label) -> None:
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.active = False
        self.text = ''
        self.txt_surface = TXT_BODY.render(self.text, True, C_WHITE)
        self.label = label

    def draw(self):
        pygame.draw.rect(self.screen, C_BLACK, self.rect)
        self.screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+7))
        label = TXT_BODY.render((self.label + ':').upper(), True, C_BLACK)
        self.screen.blit(label, (self.rect.x, self.rect.y-25))

    def text(self) -> str:
        return self.text

    def handleEvent(self, event) -> EventResponse:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                pygame.mixer.Sound.play(SOUND_CLICK)
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.txt_surface.get_width() < self.rect.w-20:
                        self.text += event.unicode.upper()
                self.txt_surface = TXT_BODY.render(self.text, True, C_WHITE)
                pygame.mixer.Sound.play(SOUND_HOVER)
                return EventResponse.KEYPRESS
        
        return EventResponse.NONE


class Switch(ABC):

    def __init__(self, screen, rect, options, label) -> None:
        self.screen = screen
        self.state = True
        self.rect = pygame.Rect(rect)
        self.inner = pygame.Rect([self.rect.x + 4, self.rect.y + 4, self.rect.w-8, self.rect.h-8])
        self.options = options
        self.label = label

    def handleEvent(self, event) -> EventResponse:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                    self.state = not self.state
                    pygame.mixer.Sound.play(SOUND_CLICK)
                    return EventResponse.CLICKED
        return EventResponse.NONE
                             

    def draw(self):
        pygame.draw.rect(self.screen, C_BLACK, self.rect)
        pygame.draw.rect(self.screen, C_TRANSPARENT, self.inner)
        label = TXT_BODY.render((self.label + ':').upper(), True, C_BLACK)
        self.screen.blit(label, (self.rect.x, self.rect.y-25))

        if self.state is True:
            pygame.draw.rect(self.screen, C_BLACK, [self.rect.x, self.rect.y, self.rect.w /2, self.rect.h])
            first = TXT_BODY.render(self.options[0].upper(), True, C_WHITE)
            second = TXT_BODY.render(self.options[1].upper(), True, C_BLACK)

            half = self.rect.w/2
            text_width = first.get_width()
            offset = (half - text_width) /2
            
            self.screen.blit(first, (self.rect.x+offset, self.rect.y+7))

            text_width = second.get_width()
            offset = (half - text_width) /2

            self.screen.blit(second, (self.rect.x + half + offset, self.rect.y+7))

        if self.state is False:
            half = self.rect.w/2
            pygame.draw.rect(self.screen, C_BLACK, [self.rect.x + half, self.rect.y, half, self.rect.h])

            first = TXT_BODY.render(self.options[0].upper(), True, C_BLACK)
            second = TXT_BODY.render(self.options[1].upper(), True, C_WHITE)

            text_width = first.get_width()
            offset = (half - text_width) /2            
            self.screen.blit(first, (self.rect.x+offset, self.rect.y+7))

            text_width = second.get_width()
            offset = (half - text_width) /2
            self.screen.blit(second, (self.rect.x + half + offset, self.rect.y+7))

class Smoke:
    def __init__(self, screen) -> None:
        self.image = pygame.image.load("img/smoke_seamless.png")
        self.rect_A = self.image.get_rect()
        self.rect_B = self.image.get_rect()
        self.rect_B[0] += 1280
        self.pos = [0,0]
        self.screen = screen
    
    def draw(self):
        self.rect_A[0] -= 1
        self.rect_B[0] -= 1
        if self.rect_A[0] <= -1280:
            self.rect_A[0] = 1280
        
        if self.rect_B[0] < -1280:
            self.rect_B[0] = 1280

        self.screen.blit(self.image, self.rect_A)
        self.screen.blit(self.image, self.rect_B)

class Background:
    def __init__(self, screen, image) -> None:
        self.screen = screen
        self.image = image
    
    def draw(self):
        self.screen.fill([255, 255, 255])
        bg = pygame.image.load(self.image)
        rect = bg.get_rect()
        rect.left, rect.top = 0, 0
        self.screen.blit(bg, rect)
