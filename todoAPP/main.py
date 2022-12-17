import flet
from flet import (
    Page, 
    TextField, 
    Checkbox, 
    FloatingActionButton, 
    icons, 
    Row, 
    Column, 
    theme,
    UserControl,
    IconButton,
    Tabs,
    Tab
)

class Task(UserControl):

    def __init__(self, task_name, task_delete, task_status_change):
        super().__init__()
        self.completed = False
        self.task_status_change = task_status_change
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=False, 
            label=self.task_name,
            on_change = self.status_changed
            )
        self.edit_name = TextField(expand=True)

        self.display_view = Row(
            alignment = "spaceBetween",
            vertical_alignment = "center", 
            controls = [
                self.display_task,
                Row(
                    spacing = 0,
                    controls = [
                        IconButton(
                            icon = icons.CREATE_OUTLINED,
                            tooltip = "Edit",
                            on_click = self.edit_clicked,
                        ),
                        IconButton(
                            icon = icons.DELETE_OUTLINE,
                            tooltip = "Delete",
                            on_click = self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible = False,
            alignment = "spaceBetween",
            vertical_alignment = "center", 
            controls=[
                self.edit_name,
                FloatingActionButton(
                    icon= icons.DONE_OUTLINE,
                    on_click=self.save_clicked,
                ),
            ],
        )

        return Column(controls=[self.display_view, self.edit_view])

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)        


class TodoApp(UserControl):

    def build(self):
        self.tasks = []
        self.new_task = TextField(hint_text="Que voulez-vous faire ?", expand = True)
        self.tasks = Column()

        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")],
        )

        view = Column(
            width = 600,
            controls=[
                Row(
                    controls = [
                        self.new_task,
                        FloatingActionButton(icon = icons.ADD, on_click=self.add_clicked)
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                    ],
                ),
            ],
        )

        return view


    
    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
        super().update()

    def tabs_changed(self, e):
        self.update()

    def task_status_change(self, task):
        self.update()

    def add_clicked(self, e):
        # self.task_view.controls.append(Checkbox(label=self.new_task.value))
        task = Task(self.new_task.value, self.task_delete, self.task_status_change)
        self.tasks.controls.append(task)
        self.new_task.value=""
        self.update()
    
    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()


def main(page : Page) :
    page.title = "Todo Day"
    page.theme = theme.Theme(color_scheme_seed="blue")
    page.horizontal_alignment = "center"

    todo = TodoApp()
    page.add(todo)

flet.app(target=main)