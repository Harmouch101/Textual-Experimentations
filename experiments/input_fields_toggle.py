from rich.align import Align
from rich.box import DOUBLE
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from textual import events
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button, ButtonPressed


class InputText(Widget):

    title: Reactive[RenderableType] = Reactive("")
    content: Reactive[RenderableType] = Reactive("")

    def __init__(self, title: str):
        super().__init__(title)
        self.title = title

    def on_key(self, event: events.Key) -> None:
        if event.key != "ctrl+i":
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
            title=self.title,
            title_align="center",
            height=3,
            style="bold white on rgb(50,57,50)",
            border_style=Style(color="green"),
            box=DOUBLE,
        )


class MainApp(App):
    username: Reactive[RenderableType] = Reactive("")
    password: Reactive[RenderableType] = Reactive("")
    current_index: Reactive[RenderableType] = Reactive(-1)

    async def on_load(self, event: events.Load) -> None:
        await self.bind("ctrl+i", "toggle_focus", show=False)

    def handle_button_pressed(self, message: ButtonPressed) -> None:
        """A message sent by the submit button"""
        assert isinstance(message.sender, Button)
        button_name = message.sender.name
        if button_name == "login":
            self.username = self.username_field.content
            self.password = self.password_field.content
            # Query the username and password

    async def on_mount(self) -> None:
        self.login_button = Button(label="login", name="login")
        self.username_field = InputText("username")
        self.password_field = InputText("password")

        await self.view.dock(self.login_button, edge="bottom", size=3)
        await self.view.dock(self.username_field, edge="left", size=50)
        await self.view.dock(self.password_field, edge="left", size=50)

        self.widgets: list = ["username_field", "password_field"]

    async def action_toggle_focus(self) -> None:
        """Set focus to the current widget"""
        widget: str = "username_field"
        if self.current_index in [-1, 1]:
            self.current_index = 0
            widget = self.widgets[self.current_index]
        else:
            self.current_index = 1
            widget = self.widgets[self.current_index]
        await getattr(self, widget).focus()


if __name__ == "__main__":
    MainApp.run(log="textual.log")
