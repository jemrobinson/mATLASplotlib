import matplotlib
import numpy as np
import mATLASplotlib


def test_scatter_constructor():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter")
        lines = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)]
        assert len(lines) == 1
        _x, _y = lines[0].get_data()
        assert np.array_equal(_x, [0, 1, 2])
        assert np.array_equal(_y, [4, 9, 16])


def test_scatter_colour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter", colour="red")
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_color() == "red"


def test_scatter_label():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter", label="Testing")
        assert "Testing" in canvas.subplots["main"].get_legend_handles_labels()[1]


def test_scatter_join_centres_linestyle():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter join centres", linestyle="dashed")
        centre_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D) and c.get_linestyle() != "None"][0]
        assert centre_line.get_linestyle() == "--"
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter join centres", linestyle="dotted")
        centre_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D) and c.get_linestyle() != "None"][0]
        assert centre_line.get_linestyle() == ":"
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter join centres", linestyle="dashdot")
        centre_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D) and c.get_linestyle() != "None"][0]
        assert centre_line.get_linestyle() == "-."


def test_scatter_linewidth():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter", linewidth=20)
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_linewidth() == 20


def test_scatter_marker():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter", marker="o")
        line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert line.get_marker() == "o"


def test_scatter_join_centres():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter join centres")
        lines = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)]
        assert len(lines) == 2
        centre_line = [l for l in lines if l.get_linestyle() != 'None'][0]
        assert centre_line.get_linestyle() == "-"


def test_scatter_xerror():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter xerror")
        x_error_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.LineCollection)][0]
        x_error_bars = [path.vertices for path in x_error_line.get_paths()]
        assert np.array_equal(x_error_bars[0], [[-0.5, 4], [0.5, 4]])
        assert np.array_equal(x_error_bars[1], [[0.5, 9], [1.5, 9]])
        assert np.array_equal(x_error_bars[2], [[1.5, 16], [2.5, 16]])


def test_scatter_yerror():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter yerror")
        y_error_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.LineCollection)][0]
        y_error_bars = [path.vertices for path in y_error_line.get_paths()]
        assert np.array_equal(y_error_bars[0], [[0, 2], [0, 6]])
        assert np.array_equal(y_error_bars[1], [[1, 6], [1, 12]])
        assert np.array_equal(y_error_bars[2], [[2, 12], [2, 20]])


def test_scatter_yerror_with_error_bar_caps():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter yerror")
        n_children_no_caps = len(canvas.subplots["main"].get_children())
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="scatter yerror", with_error_bar_caps=True)
        assert len(canvas.subplots["main"].get_children()) == n_children_no_caps + 2
