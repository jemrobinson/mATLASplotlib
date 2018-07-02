import matplotlib
import numpy as np
import mATLASplotlib


def test_legend():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter", label="Test")
        canvas.add_legend(0.5, 0.5)
        legend_element = canvas.subplots["main"].get_legend()
        assert isinstance(legend_element, matplotlib.legend.Legend)
        assert len(legend_element.get_texts()) == 1
        assert [t.get_text() for t in legend_element.get_texts()][0] == "Test"


def test_legend_sorting():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter", label="Test 1")
        canvas.plot_dataset([0, 1], [7, 12], style="scatter", label="Test 2", sort_as="A")
        canvas.add_legend(0.5, 0.5)
        legend_element = canvas.subplots["main"].get_legend()
        assert isinstance(legend_element, matplotlib.legend.Legend)
        assert len(legend_element.get_texts()) == 2
        texts = [t.get_text() for t in legend_element.get_texts()]
        assert np.array_equal(texts, ["Test 2", "Test 1"])


def test_legend_stack_sorting():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="stack", colour="blue", label="Test 1")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [4, 9, 16], [2, 3, 4], style="stack", colour="red", label="Test 2")
        canvas.add_legend(0.5, 0.5)
        legend_element = canvas.subplots["main"].get_legend()
        assert isinstance(legend_element, matplotlib.legend.Legend)
        assert len(legend_element.get_texts()) == 2
        texts = [t.get_text() for t in legend_element.get_texts()]
        assert np.array_equal(texts, ["Test 2", "Test 1"])


def test_legend_external():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter", label="Scatter 1")
        canvas.subplots["main"].plot([1,2,3], [1,2,3], "go-", label="Line 1", linewidth=2)
        canvas.add_legend(0.2, 0.9)
        legend_element = canvas.subplots["main"].get_legend()
        assert isinstance(legend_element, matplotlib.legend.Legend)
        assert len(legend_element.get_texts()) == 2
        texts = [t.get_text() for t in legend_element.get_texts()]
        assert np.array_equal(texts, ["Scatter 1", "Line 1"])

def test_legend_ellipse_proxy():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 3, 4], [1, 1, 1], style="binned band central line", linecolour="red", label="Testing")
        canvas.add_legend(0.2, 0.9)
        central_line = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.lines.Line2D)][0]
        assert central_line.get_color()[0] == "r"
