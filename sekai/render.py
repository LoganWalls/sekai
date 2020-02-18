from asciimatics.screen import Screen

from .state import State

__all__ = ["Renderer", "UnicodeRenderer", "AsciimaticsRenderer"]


class Renderer:
    def render_state(self, state: State, **kwargs):
        pass


class UnicodeRenderer(Renderer):
    def render_state(self, state: State, empty_display: str = "　", **kwargs):
        line = '－' * (2 * (state.n_columns - 1))
        result = [line]
        for y in range(state.n_rows):
            row = []
            for x in range(state.n_columns):
                o = state.objects.get(x, y)
                row.append(o.display if o else empty_display)
            result.append(f"|{'|'.join(row)}|")
            result.append(line)
        return "\n".join(result)


class AsciimaticsRenderer(Renderer):
    def render_state(self, state: State, screen: Screen = None, **kwargs):
        screen.clear()
        for t, (x, y) in state.tiles:
            # x * 2 to accommodate double-width characters
            if t.display:
                screen.print_at(t.display, x * 2, y)
        for o, (x, y) in state.objects:
            if o.display:
                screen.print_at(o.display, x * 2, y)
        screen.refresh()
