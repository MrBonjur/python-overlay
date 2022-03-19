# Python game overlay

#### Not working in full screen. Supported items: Rectangle, Circle, Line, Text.
![output](https://user-images.githubusercontent.com/55990897/159128522-649a1c0b-cddd-454d-b81b-1def27a55d47.gif)



## Very easy example:
```
from overlay import Overlay, Vector, get_font

window = Overlay(window_title="NotePad - Untitled")  # target window
font = get_font(name="Segoe UI", size=55)  # init font

while True:
    # draw text "Overlay"
    window.draw(figure="Text", vector=Vector(0, 100, 0, 0), color=(255, 255, 255), text="Overlay", font_object=font)
    # accept and draw all elements
    window.accept()
   
```

![изображение](https://user-images.githubusercontent.com/55990897/159128377-7576aa94-9c2e-4560-84de-f283a30c0ef9.png)
