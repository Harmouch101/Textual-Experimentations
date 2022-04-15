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
            title=self.title,
            title_align="center",
            height=3,
            style="bold white on rgb(50,57,50)",
            border_style=Style(color="green"),
            box=DOUBLE,
        )


class MainApp(App):
    async def on_load(self) -> None:
        await self.bind("ctrl+c", "quit", "Quit")

    async def on_mount(self) -> None:
        await self.view.dock(InputText("user_name"), edge="left", size=50)
        await self.view.dock(InputText("password"), edge="left", size=50)


if __name__ == "__main__":
    MainApp.run()