import matplotlib
import numpy as np
import mATLASplotlib


def test_coloured_2D_constructor():
    x, ex = [0, 1, 2], [0.5, 0.5, 0.5]
    y, ey = [0, 1, 2], [0.5, 0.5, 0.5]
    z = [_x * _y for _x in x for _y in y]
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset(x, ex, y, ey, z, None, style="coloured 2D")
        axes = [c for c in canvas.figure.get_children() if isinstance(c, matplotlib.axes._axes.Axes)]
        assert len(axes) == 2
        assert np.array_equal(canvas.subplots["main"].get_xlim(), (-0.5, 2.5))
        assert np.array_equal(canvas.subplots["main"].get_ylim(), (-0.5, 2.5))


def test_coloured_2D_colour_map():
    x, ex = [1, 2, 3, 4], [0.5, 0.5, 0.5, 0.5]
    y, ey = [1, 2, 3, 4], [0.5, 0.5, 0.5, 0.5]
    z = [_x * _y for _x in x for _y in y]
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset(x, ex, y, ey, z, None, style="coloured 2D", colour_map="Blues")
        axes = [c for c in canvas.figure.get_children() if isinstance(c, matplotlib.axes._axes.Axes)]
        assert len(axes) == 2
        assert np.array_equal(canvas.subplots["main"].get_xlim(), (0.5, 4.5))
        assert np.array_equal(canvas.subplots["main"].get_ylim(), (0.5, 4.5))


def test_coloured_2D_with_key():
    x, ex = [1, 2, 3, 4], [0.5, 0.5, 0.5, 0.5]
    y, ey = [1, 2, 3, 4], [0.5, 0.5, 0.5, 0.5]
    z = [_x * _y for _x in x for _y in y]
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset(x, ex, y, ey, z, None, style="coloured 2D", with_key=False)
        axes = [c for c in canvas.figure.get_children() if isinstance(c, matplotlib.axes._axes.Axes)]
        assert len(axes) == 1
        assert np.array_equal(canvas.subplots["main"].get_xlim(), (0.5, 4.5))
        assert np.array_equal(canvas.subplots["main"].get_ylim(), (0.5, 4.5))
