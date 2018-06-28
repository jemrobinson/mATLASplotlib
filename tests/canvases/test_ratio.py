import os
import numpy as np
from mATLASplotlib import canvases

def test_constructor():
    canvas = canvases.Ratio()
    # Default shape should be square
    assert(canvas.figure.get_figheight() == 6.0)
    assert(canvas.figure.get_figwidth() == 6.0)
    # Subplot should be main
    assert(canvas.main_subplot == "top")
    canvas.close()

def test_constructor_shape():
    canvas = canvases.Ratio(shape="landscape")
    # Default shape should be square
    assert(canvas.figure.get_figheight() == 6.0)
    assert(canvas.figure.get_figwidth() == 8.0)
    canvas.close()

def test_constructor_log_type_x():
    canvas = canvases.Ratio(log_type="x")
    assert("x" in canvas.log_type)
    canvas.close()

def test_constructor_log_type_y():
    canvas = canvases.Ratio(log_type="y")
    assert("y" in canvas.log_type)
    canvas.close()

def test_constructor_log_type_xy():
    canvas = canvases.Ratio(log_type="xy")
    assert("x" in canvas.log_type)
    assert("y" in canvas.log_type)
    canvas.close()

def test_constructor_log_x_force_label_pos():
    canvas = canvases.Ratio(log_type="x", log_x_force_label_pos=[1, 2, 4])
    assert(canvas.log_x_force_label_pos == [1, 2, 4])
    canvas.close()

def test_constructor_x_tick_labels():
    canvas = canvases.Ratio(x_tick_labels=["A", "B", "C"])
    assert(canvas.x_tick_labels == ["A", "B", "C"])
    canvas.close()

def test_constructor_x_tick_label_size():
    canvas = canvases.Ratio(x_tick_label_size=20)
    assert(canvas.x_tick_label_size == 20)
    canvas.close()

def test_constructor_y_tick_labels():
    canvas = canvases.Ratio(y_tick_labels=["A", "B", "C"])
    assert(canvas.y_tick_labels == ["A", "B", "C"])
    canvas.close()

def test_constructor_y_tick_label_size():
    canvas = canvases.Ratio(y_tick_label_size=20)
    assert(canvas.y_tick_label_size == 20)
    canvas.close()

def test_axis_labels():
    canvas = canvases.Ratio()
    for axis, label in zip(["x", "y"], ["xlabel", "ylabel"]):
        canvas.set_axis_label(axis, label)
        assert(canvas.get_axis_label(axis) == label)
    canvas.close()

def test_axis_ranges():
    canvas = canvases.Ratio()
    for axis, ax_range in zip(["x", "y"], [(5, 10), [0, 100]]):
        # Test set_axis_range()
        canvas.set_axis_range(axis, ax_range)
        assert(np.array_equal(canvas.get_axis_range(axis), ax_range))
        # Test set_axis_min() with a tuple
        canvas.set_axis_min(axis, 3)
        assert(np.array_equal(canvas.get_axis_range(axis), (3, ax_range[1])))
        # Test set_axis_max() with a list
        canvas.set_axis_max(axis, 7)
        assert(np.array_equal(canvas.get_axis_range(axis), [3, 7]))
    canvas.close()

def test_save_to_file():
    # Test pdf output
    canvas = canvases.Ratio()
    canvas.save_to_file("blank_test_output")
    assert(os.path.isfile("blank_test_output.pdf"))
    os.remove("blank_test_output.pdf")
    # Test png output
    canvas = canvases.Ratio()
    canvas.save_to_file("blank_test_output", extension="png")
    assert(os.path.isfile("blank_test_output.png"))
    os.remove("blank_test_output.png")
    # Test eps output
    canvas = canvases.Ratio()
    canvas.save_to_file("blank_test_output", extension="eps")
    assert(os.path.isfile("blank_test_output.eps"))
    os.remove("blank_test_output.eps")


