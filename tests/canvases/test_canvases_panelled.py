import os
import matplotlib
import numpy as np
import pytest
import mATLASplotlib

def test_panelled_constructor():
    with mATLASplotlib.canvases.Panelled() as canvas:
        assert canvas.figure.get_figheight() == 8.0
        assert canvas.figure.get_figwidth() == 6.0


def test_panelled_constructor_n_panels():
    with mATLASplotlib.canvases.Panelled(n_panels=5) as canvas:
        assert canvas.n_panels == 5
        assert len([c for c in canvas.figure.get_children() if isinstance(c, matplotlib.axes._axes.Axes)]) == 6


def test_panelled_axis_labels():
    with mATLASplotlib.canvases.Panelled() as canvas:
        for axis, label in zip(["x", "y"], ["xlabel", "ylabel"]):
            canvas.set_axis_label(axis, label)
            assert canvas.get_axis_label(axis) == label


def test_panelled_axis_labels_unknown():
    with pytest.raises(ValueError):
        with mATLASplotlib.canvases.Panelled() as canvas:
            canvas.set_axis_label("imaginary", "test")
    with pytest.raises(ValueError):
        with mATLASplotlib.canvases.Panelled() as canvas:
            canvas.get_axis_label("imaginary")


def test_panelled_axis_ranges():
    with mATLASplotlib.canvases.Panelled() as canvas:
        for axis, ax_range in zip(["x", "y_plot1", "y_plot0"], [(5, 10), [0, 100], [0, 2]]):
            canvas.set_axis_range(axis, ax_range)
            assert np.array_equal(canvas.get_axis_range(axis), ax_range)
            canvas.set_axis_min(axis, 3)
            assert np.array_equal(canvas.get_axis_range(axis), (3, ax_range[1]))
            canvas.set_axis_max(axis, 7)
            assert np.array_equal(canvas.get_axis_range(axis), [3, 7])
        canvas.save("blank_test_output")
        assert os.path.isfile("blank_test_output.pdf")
        os.remove("blank_test_output.pdf")


def test_panelled_axis_ranges_unknown():
    with mATLASplotlib.canvases.Panelled() as canvas:
        with pytest.raises(ValueError):
            canvas.set_axis_range("imaginary", (0, 5))
        with pytest.raises(ValueError):
            canvas.set_axis_min("imaginary", 0)
        with pytest.raises(ValueError):
            canvas.set_axis_max("imaginary", 5)


def test_panelled_tick_ndp():
    with mATLASplotlib.canvases.Panelled() as canvas:
        for axis, ax_range in zip(["x", "y_plot0"], [(5, 10), [0, 100]]):
            canvas.set_axis_range(axis, ax_range)
            canvas.set_axis_tick_ndp(axis, 2)
            assert axis in canvas.axis_tick_ndps
            assert canvas.axis_tick_ndps[axis] == 2
        canvas.save("blank_test_output")
        assert os.path.isfile("blank_test_output.pdf")
        os.remove("blank_test_output.pdf")


def test_panelled_plot_dataset():
    with mATLASplotlib.canvases.Panelled() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line")
        assert "x" in canvas.axis_ranges.keys()


def test_panelled_plot_dataset_in_panel():
    with mATLASplotlib.canvases.Panelled() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line", axes="plot1")
        assert "x" in canvas.axis_ranges.keys()


def test_panelled_set_axis_ticks():
    with mATLASplotlib.canvases.Panelled(n_panels=3) as canvas:
        canvas.set_axis_ticks("x", [1, 2, 3])
        assert np.array_equal(canvas.subplots["plot0"].xaxis.get_major_locator()(), [1, 2, 3])
        assert np.array_equal(canvas.subplots["plot1"].xaxis.get_major_locator()(), [1, 2, 3])
        assert np.array_equal(canvas.subplots["plot2"].xaxis.get_major_locator()(), [1, 2, 3])
        canvas.set_axis_ticks("y_plot0", [4, 5, 6])
        canvas.set_axis_range("y_plot0", (0, 10))
        assert np.array_equal(canvas.subplots["plot0"].yaxis.get_major_locator()(), [4, 5, 6])
        with pytest.raises(ValueError):
            canvas.set_axis_ticks("imaginary", [0.8, 1.0, 1.2])


def test_panelled_title():
    with mATLASplotlib.canvases.Panelled() as canvas:
        canvas.set_title("title")
        title_text = [c for c in canvas.subplots["top"].get_children() if isinstance(c, matplotlib.text.Text)][0]
        assert title_text.get_text() == "title"


def test_panelled_plot_datasets_legends():
    with mATLASplotlib.canvases.Panelled(n_panels=4) as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line", colour="red", axes="plot0", label="red")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [12, 10, 5], None, style="line", colour="blue", axes="plot1", label="blue")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [3, 5, 7], None, style="line", colour="green", axes="plot2", label="green")
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [9, 8, 6], None, style="line", colour="orange", axes="plot3", label="orange")
        canvas.add_legend(0.1, 0.1, axes="top")
        canvas.add_legend(0.1, 0.1, axes="plot0")
        legend_element = [c for c in canvas.subplots["top"].get_children() if isinstance(c, matplotlib.legend.Legend)][0]
        assert len(legend_element.get_texts()) == 4
        texts = [t.get_text() for t in legend_element.get_texts()]
        assert np.array_equal(texts, ["red", "blue", "green", "orange"])
