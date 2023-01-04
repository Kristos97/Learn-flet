import flet
from flet import Page, Text, Row, IconButton, icons

def main(page : Page):
    page.title = "Learn Flet 0.3"

    txt = Text(value="0")

    def def_add(e):
        txt.value = int(txt.value)+1
        page.update()

    def def_remove(e):
        txt.value = int(txt.value)-1
        page.update()

    page.add(
        Row(
            controls=[
                IconButton(icon=icons.REMOVE, on_click=def_remove),
                txt,
                IconButton(icon=icons.ADD, on_click=def_add),
            ],
            alignment="center"
        )
    )

    page.update()


flet.app(target=main)