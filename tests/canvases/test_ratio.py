import os
import numpy as np
import mATLASplotlib


def test_ratio_constructor():
    with mATLASplotlib.canvases.Ratio() as canvas:
        # Default shape should be square
        assert canvas.figure.get_figheight() == 6.0
        assert canvas.figure.get_figwidth() == 6.0
        # Subplot should be main
        assert canvas.main_subplot == "top"


def test_ratio_constructor_shape():
    with mATLASplotlib.canvases.Ratio(shape="landscape") as canvas:
        # Default shape should be square
        assert canvas.figure.get_figheight() == 6.0
        assert canvas.figure.get_figwidth() == 8.0


def test_ratio_constructor_log_type_x():
    with mATLASplotlib.canvases.Ratio(log_type="x") as canvas:
        assert "x" in canvas.log_type


def test_ratio_constructor_log_type_y():
    with mATLASplotlib.canvases.Ratio(log_type="y") as canvas:
        assert "y" in canvas.log_type


def test_ratio_constructor_log_type_xy():
    with mATLASplotlib.canvases.Ratio(log_type="xy") as canvas:
        assert "x" in canvas.log_type
        assert "y" in canvas.log_type


def test_ratio_constructor_log_x_force_label_pos():
    with mATLASplotlib.canvases.Ratio(log_type="x", log_x_force_label_pos=[1, 2, 4]) as canvas:
        assert canvas.log_x_force_label_pos == [1, 2, 4]


def test_ratio_constructor_x_tick_labels():
    with mATLASplotlib.canvases.Ratio(x_tick_labels=["A", "B", "C"]) as canvas:
        assert canvas.x_tick_labels == ["A", "B", "C"]


def test_ratio_constructor_x_tick_label_size():
    with mATLASplotlib.canvases.Ratio(x_tick_label_size=20) as canvas:
        assert canvas.x_tick_label_size == 20


def test_ratio_constructor_y_tick_labels():
    with mATLASplotlib.canvases.Ratio(y_tick_labels=["A", "B", "C"]) as canvas:
        assert canvas.y_tick_labels == ["A", "B", "C"]


def test_ratio_constructor_y_tick_label_size():
    with mATLASplotlib.canvases.Ratio(y_tick_label_size=20) as canvas:
        assert canvas.y_tick_label_size == 20


def test_ratio_axis_labels():
    with mATLASplotlib.canvases.Ratio() as canvas:
        for axis, label in zip(["x", "y"], ["xlabel", "ylabel"]):
            canvas.set_axis_label(axis, label)
            assert canvas.get_axis_label(axis) == label


def test_ratio_axis_ranges():
    with mATLASplotlib.canvases.Ratio() as canvas:
        for axis, ax_range in zip(["x", "y"], [(5, 10), [0, 100]]):
            # Test set_axis_range()
            canvas.set_axis_range(axis, ax_range)
            assert np.array_equal(canvas.get_axis_range(axis), ax_range)
            # Test set_axis_min() with a tuple
            canvas.set_axis_min(axis, 3)
            assert np.array_equal(
                canvas.get_axis_range(axis), (3, ax_range[1]))
            # Test set_axis_max() with a list
            canvas.set_axis_max(axis, 7)
            assert np.array_equal(canvas.get_axis_range(axis), [3, 7])


def test_ratio_save():
    # Test pdf output
    with mATLASplotlib.canvases.Ratio() as canvas:
        canvas.save("blank_test_output")
        assert os.path.isfile("blank_test_output.pdf")
        os.remove("blank_test_output.pdf")
    # Test png output
    with mATLASplotlib.canvases.Ratio() as canvas:
        canvas.save("blank_test_output", extension="png")
        assert os.path.isfile("blank_test_output.png")
        os.remove("blank_test_output.png")
    # Test eps output
    with mATLASplotlib.canvases.Ratio() as canvas:
        canvas.save("blank_test_output", extension="eps")
        assert os.path.isfile("blank_test_output.eps")
        os.remove("blank_test_output.eps")


def test_ratio_plot_dataset():
    with mATLASplotlib.canvases.Ratio() as canvas:
        assert canvas.axis_ranges.keys() == ["y_ratio"]
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [5, 10, 12], None, style="line")
        assert "x" in canvas.axis_ranges.keys()
        assert "y" in canvas.axis_ranges.keys()
        assert "y_ratio" in canvas.axis_ranges.keys()
