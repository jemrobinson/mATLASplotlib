import matplotlib
import numpy as np
import mATLASplotlib

def test_binned_band_constructor():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band")
        polycollections = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.PolyCollection)]
        assert len(polycollections) == 1


def test_binned_band_alpha():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band", alpha=0.5)
        pc = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.PolyCollection)][0]
        assert pc.get_alpha() == 0.5


def test_binned_band_colour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band", colour="red")
        pc = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.PolyCollection)][0]
        assert np.array_equal(pc.get_facecolor()[0], [1, 0, 0, 1])


def test_binned_band_hatch():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band", hatch="x")
        pc = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.PolyCollection)][0]
        assert pc.get_hatch() == "x"


def test_binned_band_hatchcolour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band", hatchcolour="red", hatch="x")
        pc = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.PolyCollection)][0]
        assert np.array_equal(pc.get_edgecolor()[0], [1, 0, 0, 1])


def test_binned_band_central_line_linecolour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line", linecolour="red")
        central_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.LineCollection)][0]
        assert np.array_equal(central_line.get_color()[0], [1, 0, 0, 1])


def test_binned_band_central_line_stepped_linecolour():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line", linecolour="red")
        central_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert central_line.get_color()[0] == "r"


def test_binned_band_central_line_linestyle():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line", linestyle="dotted")
        central_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.LineCollection)][0]
        ls_tuple = central_line.get_linestyle()[0] # offset, (on, off)
        assert ls_tuple[0] == 0
        assert ls_tuple[1][1] > ls_tuple[1][0]


def test_binned_band_central_line_stepped_linestyle():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line stepped", linestyle="dotted")
        central_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert central_line.get_linestyle() == ":"


def test_binned_band_central_line_linewidth():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line", linewidth=5)
        central_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.LineCollection)][0]
        assert central_line.get_linewidth() == 5


def test_binned_band_central_line_stepped_linewidth():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line stepped", linewidth=5)
        central_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert central_line.get_linewidth() == 5


def test_binned_band_label():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band", label="Testing")
        proxy = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)][0]
        assert proxy.get_label() == "Testing"


def test_binned_band_central_line_label():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line", label="Testing")
        proxy = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Ellipse)][0]
        assert proxy.get_label() == "Testing"


def test_binned_band_central_line_stepped_label():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line stepped", label="Testing")
        proxy = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Ellipse)][0]
        assert proxy.get_label() == "Testing"
