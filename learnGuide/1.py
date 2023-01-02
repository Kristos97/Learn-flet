import flet
from flet import Page, Text

def main(page : Page):
    page.title = "My First App with Flet"

    txt = Text(value="Hello world !" )
    page.controls.append(txt)
    page.update()
    return True
flet.app(target=main)