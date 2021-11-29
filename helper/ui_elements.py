from abc import ABC, abstractmethod
import pygame
from enum import Enum

pygame.init()

# CONSTANTS
C_BLACK = [90, 54, 28]
C_WHITE = [255, 236, 228]
C_TRANSPARENT = [248, 214, 196]
C_HOVER = [122, 86, 69]
C_HEALTH = [255, 80, 0]
C_STRENGTH = [255, 184, 0]

TXT_BODY = pygame.font.SysFont('Impact', 20)
TXT_TITLE = pygame.font.SysFont('Impact', 26)
TXT_HEADING2 = pygame.font.SysFont('Impact', 30)
TXT_HEADING1 = pygame.font.SysFont('Impact', 36)
TXT_DISPLAY = pygame.font.SysFont('Impact', 60)

SOUND_CLICK = pygame.mixer.Sound("sound/click.wav")
SOUND_HOVER = pygame.mixer.Sound("sound/btn_hover.wav")


class Align(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2


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
    def handleEvent(self, event):
        return


class Button(UIElement):
    def __init__(self, screen, rect, text) -> None:
        super().__init__(screen)
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.text = text
        self.currently_hovered = False

    def draw(self):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)

        if hover:
            if not self.currently_hovered:
                pygame.mixer.Sound.play(SOUND_HOVER)
            self.currently_hovered = True
        else:
            self.currently_hovered = False

        color = (C_HOVER if hover else C_BLACK)
        pygame.draw.rect(self.screen, color, self.rect)
        text = TXT_TITLE.render(self.text.upper(), True, C_WHITE)
        offset = (self.rect.w - text.get_width()) / 2
        self.screen.blit(text, [self.rect.x + offset, self.rect.y + 4])

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
        self.screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 7))
        label = TXT_BODY.render((self.label + ':').upper(), True, C_BLACK)
        self.screen.blit(label, (self.rect.x, self.rect.y - 25))

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
                    if self.txt_surface.get_width() < self.rect.w - 20:
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
        self.inner = pygame.Rect([self.rect.x + 4, self.rect.y + 4, self.rect.w - 8, self.rect.h - 8])
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
        self.screen.blit(label, (self.rect.x, self.rect.y - 25))

        if self.state is True:
            pygame.draw.rect(self.screen, C_BLACK, [self.rect.x, self.rect.y, self.rect.w / 2, self.rect.h])
            first = TXT_BODY.render(self.options[0].upper(), True, C_WHITE)
            second = TXT_BODY.render(self.options[1].upper(), True, C_BLACK)

            half = self.rect.w / 2
            text_width = first.get_width()
            offset = (half - text_width) / 2

            self.screen.blit(first, (self.rect.x + offset, self.rect.y + 7))

            text_width = second.get_width()
            offset = (half - text_width) / 2

            self.screen.blit(second, (self.rect.x + half + offset, self.rect.y + 7))

        if self.state is False:
            half = self.rect.w / 2
            pygame.draw.rect(self.screen, C_BLACK, [self.rect.x + half, self.rect.y, half, self.rect.h])

            first = TXT_BODY.render(self.options[0].upper(), True, C_BLACK)
            second = TXT_BODY.render(self.options[1].upper(), True, C_WHITE)

            text_width = first.get_width()
            offset = (half - text_width) / 2
            self.screen.blit(first, (self.rect.x + offset, self.rect.y + 7))

            text_width = second.get_width()
            offset = (half - text_width) / 2
            self.screen.blit(second, (self.rect.x + half + offset, self.rect.y + 7))


class ProgressBar(ABC):

    def __init__(self, screen, rect, alignment=Align.LEFT, color=C_HEALTH) -> None:
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.status = 1
        self.alignment = alignment
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, C_BLACK, self.rect)
        if self.alignment is Align.LEFT:
            pygame.draw.rect(self.screen, self.color,
                             [self.rect.x + 3, self.rect.y + 3, (self.rect.w - 6) * self.status, self.rect.h - 6])
        if self.alignment is Align.RIGHT:
            starting_pos = (self.rect.x + self.rect.w - 3) - (self.rect.w - 6) * self.status
            pygame.draw.rect(self.screen, self.color,
                             [starting_pos, self.rect.y + 3, (self.rect.w - 6) * self.status, self.rect.h - 6])

    def set_status(self, status):
        self.status = status

    def handleEvent(self):
        pass


class Text(ABC):
    def __init__(self, screen, text, pos=[0, 0], size=20, color=C_BLACK, align=Align.LEFT, decorate=False) -> None:
        super().__init__()
        self.screen = screen
        self.text = text.upper()
        self.pos = pos
        self.size = size
        self.color = color
        self.alignment = align
        self.decorate = decorate
        self.font = pygame.font.SysFont('Impact', self.size)
        self.render = self.font.render(self.text, True, self.color)

    def draw(self):
        pos = self.pos
        if self.alignment is Align.LEFT:
            pos = self.pos
        if self.alignment is Align.RIGHT:
            pos = [self.pos[0] - self.render.get_width(), self.pos[1]]
        if self.alignment is Align.CENTER:
            pos = [320 - self.render.get_width() / 2, self.pos[1]]

        if self.decorate:
            pos, rect1, rect2 = self.__getDecoration(pos)
            self.screen.blit(self.render, pos)
            pygame.draw.rect(self.screen, self.color, rect1)
            pygame.draw.rect(self.screen, self.color, rect2)
        else:
            self.screen.blit(self.render, pos)

    def __getDecoration(self, pos):
        scale = self.size / 40
        dec_width = 13 * scale
        dec_height = 5 * scale
        gap = 5 * scale

        if self.alignment is Align.LEFT:
            pos = [pos[0] + (dec_width + gap), pos[1]]
        if self.alignment is Align.RIGHT:
            pos = [pos[0] - (dec_width + gap), pos[1]]

        rect1_pos = [pos[0] - (dec_width + gap), pos[1] + (self.render.get_height() / 2) - round(dec_height / 2) + 1]
        rect2_pos = [pos[0] + self.render.get_width() + gap,
                     pos[1] + (self.render.get_height() / 2) - round(dec_height / 2) + 1]

        rect1 = pygame.Rect([rect1_pos[0], rect1_pos[1], dec_width, dec_height])
        rect2 = pygame.Rect([rect2_pos[0], rect2_pos[1], dec_width, dec_height])
        return [pos, rect1, rect2]

    def handleEvent(self):
        pass


class Smoke:
    def __init__(self, screen) -> None:
        self.image = pygame.image.load("img/smoke_seamless.png")
        self.rect_A = self.image.get_rect()
        self.rect_B = self.image.get_rect()
        self.rect_B[0] += 1280
        self.pos = [0, 0]
        self.screen = screen

    def draw(self):
        if self.rect_A[0] <= -1280:
            self.rect_A[0] = 1280
            self.rect_B[0] = 0
        elif self.rect_B[0] < -1280:
            self.rect_B[0] = 1280
            self.rect_A[0] = 0
        else:
            self.rect_A[0] -= 1
            self.rect_B[0] -= 1

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
