from random import randint as random
from overlay import Overlay, Vector, get_font, get_list_windows

get_list_windows()  # print visible window list

# fps=0 - unlimited
# always_update=False - for low PC

window = Overlay(window_title="Без имени – Блокнот", fps=0, always_update=True)
# window = Overlay(window_title="NotePad - Untitled")


while True:
    window.draw(figure="Text",
                vector=Vector(10, 100, 0, 0),
                color=(0, 118, 254),
                text="O",
                font_object=get_font(name="Segoe UI", size=55, bold=True, italic=True))

    window.draw(figure="Text",
                vector=Vector(53, 100, 0, 0),
                color=(255, 255, 255),
                text="verlay v1.0",
                font_object=get_font(name="Segoe UI", size=55, bold=True, italic=True))

    window.draw(figure="Text",
                vector=Vector(10, 175, 0, 0),
                color=(255, 255, 255),
                text="https://github.com/MrBonjur",
                font_object=get_font(size=20))

    window.draw(figure="Line",
                vector=Vector(10, 210, 350, 210),
                color=(255, 255, 255),
                thickness=1)

    for i in range(2, 20, 5):
        window.draw(figure="Circle",
                    vector=Vector(400, 160, 0, 0),
                    color=(random(0, 255), random(0, 255), random(0, 255)),
                    radius=50 - i,
                    thickness=0)

    window.accept()  # accept and draw all elements
