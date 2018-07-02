import matplotlib
import numpy as np
import mATLASplotlib

def test_bar_chart_constructor():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [0.5, 0.5], [5, 10], None, style="bar")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        # Widths are increased by 0.004 to avoid zero-width gaps
        assert bars[0].get_width() == 1.004
        assert bars[0].get_height() == 5
        assert bars[1].get_width() == 1.004
        assert bars[1].get_height() == 10


def test_bar_chart_colour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [0.5, 0.5], [5, 10], None, style="bar", colour="red")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert np.array_equal(bars[0].get_facecolor(), [1, 0, 0, 1])


def test_bar_chart_edgecolour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [0.5, 0.5], [5, 10], None, style="bar", edgecolour="red")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert np.array_equal(bars[0].get_edgecolor(), [1, 0, 0, 1])


def test_bar_chart_edgewidth():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [0.5, 0.5], [5, 10], None, style="bar", edgecolour="red", edgewidth=20)
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert bars[0].get_linewidth() == 20

def test_bar_chart_label():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [0.5, 0.5], [5, 10], None, style="bar", label="Testing")
        labels = [c.get_label() for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert "Testing" in labels
