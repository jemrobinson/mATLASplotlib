import matplotlib
import numpy as np
import mATLASplotlib

def test_stack_constructor():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="stack")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="stack", colour="red")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert len(bars) == 7
        assert bars[0].get_width() == 1.004
        assert bars[0].get_height() == 2
        assert bars[1].get_width() == 1.004
        assert bars[1].get_height() == 3
        assert bars[3].get_width() == 1.004
        assert bars[3].get_height() == 4
        assert bars[4].get_width() == 1.004
        assert bars[4].get_height() == 9

def test_stack_colour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="stack", colour="blue")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="stack", colour="red")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert np.array_equal(bars[0].get_facecolor(), [0, 0, 1, 1])
        assert np.array_equal(bars[4].get_facecolor(), [1, 0, 0, 1])


def test_stack_hatch():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="stack", colour="blue", hatch="x")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="stack", colour="red")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert bars[0].get_hatch() == "x"


def test_stack_hatchcolour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="stack", colour="blue", hatch="x", hatchcolour="#00ff00")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="stack", colour="red")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert bars[0].get_hatch() == "x"
        assert np.array_equal(bars[0].get_facecolor(), [0, 0, 1, 1])
        assert np.array_equal(bars[0].get_edgecolor(), [0, 1, 0, 1])


def test_stack_label():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="stack", colour="blue", label="Testing")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="stack", colour="red")
        assert "Testing" in canvas.subplots["main"].get_legend_handles_labels()[1]


def test_stack_outlinewidth():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="stack", colour="blue", hatch="x", hatchcolour="#00ff00", outlinewidth=20)
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="stack", colour="red")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        assert bars[0].get_linewidth() == 20

