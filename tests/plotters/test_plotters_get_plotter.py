import pytest
import mATLASplotlib


def test_get_plotter_bar():
    rv = mATLASplotlib.plotters.get_plotter("bar")
    assert isinstance(rv, mATLASplotlib.plotters.bar_chart.BarChart)


def test_get_plotter_binned_band():
    rv = mATLASplotlib.plotters.get_plotter("binned band")
    assert isinstance(rv, mATLASplotlib.plotters.binned_band.BinnedBand)


def test_get_plotter_coloured_2D():
    rv = mATLASplotlib.plotters.get_plotter("coloured 2D")
    assert isinstance(rv, mATLASplotlib.plotters.coloured_2D.Coloured2D)


def test_get_plotter_line():
    rv = mATLASplotlib.plotters.get_plotter("line")
    assert isinstance(rv, mATLASplotlib.plotters.line.Line)


def test_get_plotter_scatter():
    rv = mATLASplotlib.plotters.get_plotter("scatter")
    assert isinstance(rv, mATLASplotlib.plotters.scatter.Scatter)


def test_get_plotter_stack():
    rv = mATLASplotlib.plotters.get_plotter("stack")
    assert isinstance(rv, mATLASplotlib.plotters.stack.Stack)


def test_get_plotter_None():
    with pytest.raises(ValueError):
        mATLASplotlib.plotters.get_plotter(None)


def test_get_plotter_non_existant():
    with pytest.raises(NotImplementedError):
        mATLASplotlib.plotters.get_plotter("Dummy")


