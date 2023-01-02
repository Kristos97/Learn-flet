import flet
from flet import Page, Text, Row, Column

from time import sleep

def main(page : Page):
    page.title = "My First App with Flet"

    L=[]
    page.add(
        Column(controls=L)
    )
    

    for i in range(10):
        sleep(1)
        print(i)
        L.append(Text(value=f"Day{i}"))
        page.update()
        sleep(1)
    
flet.app(target=main)