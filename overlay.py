########################################################################
#                            Python overlay                            #
#                      19.03.2022 create MrBonjur                      #
#                      Libraries: pywin32, pygame                      #
#                    Doesn't work in full screen mode                  #
#                         Tested on python 3.9                         #
#                       https://github.com/MrBonjur                    #
########################################################################

# pip install pywin32, pygame
from win32gui import GetWindowText, GetForegroundWindow
import win32gui
import sys
import os


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''  # hide text "Hello from the pygame community"
import pygame

pygame.init()


class Vector:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Figure:
    def __init__(self, vector, color):
        self.vector = vector
        self.color = color


class Rectangle(Figure):
    def __init__(self, vector, color):
        super().__init__(vector, color)
        self.type = "Rectangle"


class Circle(Figure):
    def __init__(self, vector, color, thickness, radius):
        super().__init__(vector, color)
        self.type = "Circle"
        self.thickness = thickness
        self.radius = radius


class Line(Figure):
    def __init__(self, vector, color, thickness):
        super().__init__(vector, color)
        self.type = "Line"
        self.thickness = thickness


class Text(Figure):
    def __init__(self, vector, color, text, font_object):
        super().__init__(vector, color)
        self.type = "Text"
        self.text = text
        self.font_object = font_object


def win_enum_handler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd) != "":
            print(win32gui.GetWindowText(hwnd))


def get_list_windows():
    win32gui.EnumWindows(win_enum_handler, None)


class Overlay:
    def __init__(self, window_title, fps=None, always_update=True):
        self.window_title = window_title
        self.figuresToDraw = []
        self.fps = fps
        self.always_update = always_update
        self.targetHwnd = win32gui.FindWindow(None, self.window_title)

        if not self.targetHwnd:
            sys.exit(f"Window not found: {self.window_title}")

        # get monitor size
        self.window_width = pygame.display.Info().current_w
        self.window_height = pygame.display.Info().current_w

        # fix black flashing (start point)
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(self.window_width) + "," + str(self.window_height)

        self.is_updated = False  # for init (only always_update=False)
        self.targetRect = self.get_target_window_rect()

        self.old_rect_x = self.targetRect.x
        self.old_rect_y = self.targetRect.y
        self.old_rect_width = self.targetRect.width
        self.old_rect_height = self.targetRect.height

        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        self.hWnd = pygame.display.get_wm_info()['window']
        self.WindowLong = win32gui.GetWindowLong(self.hWnd, -20)
        win32gui.SetWindowLong(self.hWnd, -20, 0x16 | 0x00080000)
        win32gui.SetLayeredWindowAttributes(self.hWnd, 1, 0, 0x00000001)
        win32gui.BringWindowToTop(self.hWnd)
        win32gui.SetWindowPos(self.hWnd, -1, 0, 0, 0, 0, 2 | 1)

    def get_target_window_rect(self):
        rect = win32gui.GetWindowRect(self.targetHwnd)
        x = rect[0] + 10  # pygame draw bug
        y = rect[1] + 10
        width = rect[2] - rect[0] - 20
        height = rect[3] - rect[1] - 20
        return Vector(x, y, width, height)

    def accept(self):
        win32gui.SetWindowPos(self.hWnd, -1, self.targetRect.x, self.targetRect.y, 0, 0, 2 | 1)
        pygame.event.get()  # fix crash pygame
        self.targetRect = self.get_target_window_rect()

        win32gui.MoveWindow(self.hWnd,
                            self.targetRect.x,
                            self.targetRect.y,
                            self.targetRect.width,
                            self.targetRect.height,
                            True)

        self.screen.fill((1, 0, 0))

        for figure in self.figuresToDraw:
            if figure.type == "Rectangle":
                rect = pygame.Rect(figure.vector.x, figure.vector.y, figure.vector.width, figure.vector.height)
                pygame.draw.rect(surface=self.screen,
                                 color=figure.color,
                                 rect=rect)
            elif figure.type == "Circle":
                pygame.draw.circle(surface=self.screen,
                                   color=figure.color,
                                   center=(figure.vector.x, figure.vector.y),
                                   radius=figure.radius,
                                   width=figure.thickness)
            elif figure.type == "Line":
                pygame.draw.line(surface=self.screen,
                                 color=figure.color,
                                 start_pos=(figure.vector.x, figure.vector.y),
                                 end_pos=(figure.vector.width, figure.vector.height),
                                 width=figure.thickness)
            elif figure.type == "Text":
                self.screen.blit(source=figure.font_object.render(figure.text, 1, figure.color),
                                 dest=(figure.vector.x, figure.vector.y))

        # for low pc init elements
        if not self.is_updated:
            pygame.display.update()
            focused_window = GetWindowText(GetForegroundWindow())
            if focused_window == self.window_title:
                for i in range(len(self.figuresToDraw) + 1):  # time for draw all element
                    pygame.display.update()
                    self.is_updated = True

        # instant update for normal pc
        if self.always_update:
            pygame.display.update()

        if self.fps:  # if fps != None
            pygame.time.Clock().tick(self.fps)

        # low pc mode (sorry for the shit code. class != class)
        if self.old_rect_x != self.targetRect.x or \
                self.old_rect_y != self.targetRect.y or \
                self.old_rect_width != self.targetRect.width or \
                self.old_rect_height != self.targetRect.height and not self.always_update:

            pygame.display.update()
            self.old_rect_x = self.targetRect.x
            self.old_rect_y = self.targetRect.y
            self.old_rect_width = self.targetRect.width
            self.old_rect_height = self.targetRect.height

        self.figuresToDraw = []

    def draw(self, figure: str, vector: Vector, color, thickness=None, radius=None, text=None, font_object=None):
        focused_window = GetWindowText(GetForegroundWindow())
        if focused_window == self.window_title:
            if figure == "fillRect":
                self.figuresToDraw.append(Rectangle(vector, color))
            elif figure == "Circle":
                self.figuresToDraw.append(Circle(vector, color, thickness, radius))
            elif figure == "Line":
                self.figuresToDraw.append(Line(vector, color, thickness))
            elif figure == "Text":
                self.figuresToDraw.append(Text(vector, color, text, font_object))


def get_font(size, name="Calibri", bold=False, italic=False):
    return pygame.font.SysFont(name=name, size=size, bold=bold, italic=italic)
