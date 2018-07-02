import matplotlib
import numpy as np
import mATLASplotlib


def test_line_constructor():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line")
        lines = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)]
        assert len(lines) == 1
        _x, _y = lines[0].get_data()
        assert np.array_equal(_x, [0, 1, 2])
        assert np.array_equal(_y, [5, 10, 12])


def test_line_colour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line", colour="red")
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_color() == "red"


def test_line_label():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line", label="Testing")
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_label() == "Testing"


def test_line_linestyle():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line", linestyle="dotted")
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_linestyle() == ":"


def test_line_linewidth():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line", linewidth=20)
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_linewidth() == 20


def test_line_marker():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line", marker="o")
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_marker() == "o"


def test_line_smooth():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5], [5, 10, 12, 13], None, style="smooth line")
        lines = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)]
        assert len(lines) == 1
        _x, _y = lines[0].get_data()
        assert len(_x) == len(_y) == 40
        assert min(_x) == 0
        assert max(_x) == 3
        assert min(_y) == 5
        assert max(_y) == 13


def test_line_stepped():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5], [5, 10, 12, 13], None, style="stepped line")
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_drawstyle() == "steps-pre"
