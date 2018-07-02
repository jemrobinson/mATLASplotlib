import os
import matplotlib
import pytest
import mATLASplotlib


def test_base_close():
    n_initial = len(matplotlib.pyplot.get_fignums())
    canvas = mATLASplotlib.canvases.base_canvas.BaseCanvas()
    assert len(matplotlib.pyplot.get_fignums()) == n_initial + 1
    canvas.close()
    assert len(matplotlib.pyplot.get_fignums()) == n_initial


def test_base_set_axis_label():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            for axis, label in zip(["x", "y"], ["xlabel", "ylabel"]):
                canvas.set_axis_label(axis, label)


def test_base_set_axis_max():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            canvas.set_axis_max("x", 10)


def test_base_set_axis_min():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            canvas.set_axis_min("x", 0)


def test_base_set_axis_range():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            canvas.set_axis_range("x", (0, 10))


def test_base_set_axis_ticks():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            canvas.set_axis_ticks("x", [1, 2, 3])


def test_base_set_axis_log():
    with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
        canvas.set_axis_log("x")
        assert canvas.log_type == "x"


def test_base_set_title():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            canvas.set_title("title")


def test_base_apply_axis_limits():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            canvas._apply_axis_limits()


def test_base_apply_final_formatting():
    with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
        canvas._apply_final_formatting()
        canvas.save("blank_test_output")
        assert os.path.isfile("blank_test_output.pdf")
        os.remove("blank_test_output.pdf")


def test_base_get_axis_label():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            canvas.get_axis_label("x")


def test_base_get_axis_range():
    with pytest.raises(ValueError):
        with mATLASplotlib.canvases.base_canvas.BaseCanvas() as canvas:
            canvas.get_axis_range("x")
