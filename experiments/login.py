import asyncio

from rich.align import Align
from rich.box import DOUBLE
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from textual import events
from textual.app import App
from textual.reactive import Reactive
from textual.views import GridView
from textual.widget import Widget
from textual.widgets import Button, ButtonPressed

from db import check_user, create_users_table, register_user


class InputText(Widget):

    title: Reactive[RenderableType] = Reactive("")
    content: Reactive[RenderableType] = Reactive("")
    mouse_over: Reactive[RenderableType] = Reactive(False)

    def __init__(self, title: str):
        super().__init__(title)
        self.title = title

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False

    def on_key(self, event: events.Key) -> None:
        if self.mouse_over == True:
            if event.key == "ctrl+h":
                self.content = self.content[:-1]
            else:
                self.content += event.key

    def validate_title(self, value) -> None:
        try:
            return value.lower()
        except (AttributeError, TypeError):
            raise AssertionError("title attribute should be a string.")

    def render(self) -> RenderableType:
        renderable = None
        if self.title.lower() == "password":
            renderable = "".join(map(lambda char: "*", self.content))
        else:
            renderable = Align.left(Text(self.content, style="bold"))
        return Panel(
            renderable,
            title="",
            title_align="center",
            height=3,
            style="bold white on rgb(50,57,50)",
            border_style=Style(color="green"),
            box=DOUBLE,
        )


class LoginGrid(GridView):
    username: Reactive[RenderableType] = Reactive("")
    password: Reactive[RenderableType] = Reactive("")

    async def on_mount(self) -> None:
        # define input fields
        self.username = InputText("username")
        self.password = InputText("password")
        self.grid.set_align("center", "center")
        self.grid.set_gap(1, 1)
        # Create rows / columns / areas
        self.grid.add_column("column", repeat=2, size=40)
        self.grid.add_row("row", repeat=3, size=3)
        # Place out widgets in to the layout
        button_style = "bold red on white"
        label_style = "bold white on rgb(60,60,60)"
        username_label = Button(
            label="username", name="username_label", style=label_style
        )
        password_label = Button(
            label="password", name="password_label", style=label_style
        )
        self.grid.add_widget(username_label)
        self.grid.add_widget(self.username)
        self.grid.add_widget(password_label)
        self.grid.add_widget(self.password)
        self.grid.add_widget(
            Button(label="register", name="register", style=button_style)
        )
        self.grid.add_widget(Button(label="login", name="login", style=button_style))


class MainApp(App):
    username: Reactive[RenderableType] = Reactive("")
    password: Reactive[RenderableType] = Reactive("")

    async def handle_button_pressed(self, message: ButtonPressed) -> None:
        """A message sent by the submit button"""
        assert isinstance(message.sender, Button)
        button_name = message.sender.name
        self.username = self.login_grid.username.content
        self.password = self.login_grid.password.content
        if button_name == "login":
            # clear widgets
            self.view.layout.docks.clear()
            self.view.widgets.clear()
            if len(self.username) == 0 or len(self.password) == 0:
                # add new widget
                await self.view.dock(
                    Button(
                        label="Please enter a valid username and password!",
                        style="bold white on rgb(50,57,50)",
                    )
                )
                await asyncio.sleep(2)
                # clear widgets
                self.view.layout.docks.clear()
                self.view.widgets.clear()
                # redraw back the grid
                await self.view.dock(self.login_grid)
            elif check_user(self.username, self.password):
                # clear widgets
                self.view.layout.docks.clear()
                self.view.widgets.clear()
                # add new widget
                await self.view.dock(
                    Button(
                        label=f"Weclome back {self.username}!",
                        style="bold white on rgb(50,57,50)",
                    )
                )
            else:
                # clear widgets
                self.view.layout.docks.clear()
                self.view.widgets.clear()
                # add new widget
                await self.view.dock(
                    Button(
                        label="Invalid Credentials!",
                        style="bold white on rgb(50,57,50)",
                    )
                )
                await asyncio.sleep(2)
                # clear widgets
                self.view.layout.docks.clear()
                self.view.widgets.clear()
                # redraw back the grid
                await self.view.dock(self.login_grid)
        elif button_name == "register":
            result = None
            self.view.layout.docks.clear()
            self.view.widgets.clear()
            if len(self.username) == 0 or len(self.password) == 0:
                # add new widget
                await self.view.dock(
                    Button(
                        label="Please enter a valid username and password!",
                        style="bold white on rgb(50,57,50)",
                    )
                )
                await asyncio.sleep(2)
                # clear widgets
                self.view.layout.docks.clear()
                self.view.widgets.clear()
                # redraw back the grid
                await self.view.dock(self.login_grid)
            else:
                result = register_user(self.username, self.password)
            if result:
                # add new widget
                await self.view.dock(
                    Button(
                        label="User Registered Successfully!",
                        style="bold white on rgb(50,57,50)",
                    )
                )
                await asyncio.sleep(2)
                # clear widgets
                self.view.layout.docks.clear()
                self.view.widgets.clear()
                # redraw back the grid
                await self.view.dock(self.login_grid)
            elif not result and len(self.username) > 0:
                # add new widget
                await self.view.dock(
                    Button(
                        label="Username Already Exists!",
                        style="bold white on rgb(50,57,50)",
                    )
                )
                await asyncio.sleep(2)
                # clear widgets
                self.view.layout.docks.clear()
                self.view.widgets.clear()
                # redraw back the grid
                await self.view.dock(self.login_grid)

    async def on_mount(self) -> None:
        create_users_table()
        self.login_grid = LoginGrid()
        await self.view.dock(self.login_grid)


if __name__ == "__main__":
    MainApp.run(log="textual.log")
