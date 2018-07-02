import pytest
import mATLASplotlib

def test_base_add_to_axes():
    with pytest.raises(NotImplementedError):
        with mATLASplotlib.canvases.Simple() as canvas:
            ds = mATLASplotlib.converters.Dataset([0, 1], [0.5, 0.5], [5, 10], None)
            plotter = mATLASplotlib.plotters.base_plotter.BasePlotter(plot_style="dummy")
            plotter.add_to_axes(canvas.subplots["main"], ds)
