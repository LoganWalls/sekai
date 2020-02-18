from time import sleep

from asciimatics.screen import Screen

from .render import AsciimaticsRenderer, Renderer
from .state import State

__all__ = ["Engine", "AsciimaticsEngine", "EpisodeTerminated"]


class EpisodeTerminated(BaseException):
    pass


class Engine(object):
    def __init__(self, state: State, **kwargs):
        self.state: State = state
        self.renderer: Renderer = kwargs.get('renderer')

    def render(self, state: State):
        return self.renderer.render_state(state)

    def tick(self, state: State):
        for o, (x, y) in state.objects:
            o.tick(state, x, y)

    def run(self, wait_time: float = 0.5):
        while not self.state.terminal_state:
            try:
                self.tick(self.state)
            except EpisodeTerminated:
                self.state.terminal_state = True
            if self.renderer:
                self.render(self.state)
            sleep(wait_time)


class AsciimaticsEngine(Engine):

    def __init__(self, state: State, **kwargs):
        super().__init__(state, **kwargs)
        if not self.renderer:
            self.renderer = AsciimaticsRenderer()
        self.screen: Screen = None

    def render(self, state: State):
        self.renderer.render_state(state, screen=self.screen)

    def run(self, wait_time: float = 0.5):
        self.screen = Screen.open()
        self.screen.clear()
        try:
            while not self.state.terminal_state:
                try:
                    self.tick(self.state)
                except EpisodeTerminated:
                    self.state.terminal_state = True
                if self.renderer:
                    self.render(self.state)
                sleep(wait_time)
        finally:
            self.screen.close()
