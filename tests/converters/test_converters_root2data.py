import array
import numpy as np
import pytest
import ROOT
import mATLASplotlib

def test_root2data_constructor_TF1():
    root_object = ROOT.TF1("TF1", "sin(x)/x", 0.0, 10.0)
    ds = mATLASplotlib.converters.Dataset(root_object)
    # Dimensions should be x and y
    assert ds.get_dimensions() == ["x", "y"]
    # The x points should be spaced along the range 0.0 to 10.0
    assert np.array_equal(ds.x_points, np.linspace(0.0, 10.0, num=1000, endpoint=True))
    # There should be 1000 y points
    assert len(ds.y_points) == 1000
    # There should be 1000 points altogether
    assert ds.nPoints == 1000


def test_root2data_constructor_TGraph():
    x, y = [0, 1, 2], [0, 1, 4]
    root_object = ROOT.TGraph(3, array.array("d", x), array.array("d", y))
    ds = mATLASplotlib.converters.Dataset(root_object)
    # Dimensions should be x and y
    assert ds.get_dimensions() == ["x", "y"]
    # x points should be recentred such that the x-errors are symmetric
    assert np.array_equal(ds.x_points, np.array([0.0, 1.0, 2.0]))
    # y points should be 0, 1, 4
    assert np.array_equal(ds.y_points, np.array([0.0, 1.0, 4.0]))
    # x error pairs should all be (0.4, 0.6)
    assert np.array_equal(ds.x_error_pairs, np.array([(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]))
    # y error pairs should all be as specified
    assert np.array_equal(ds.y_error_pairs, np.array([(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]))
    # There should be 3 points altogether
    assert ds.nPoints == 3

def test_root2data_constructor_TGraphAsymmErrors():
    x, y = [0, 1, 2], [0, 1, 4]
    exl, exh = [0.5, 0.5, 0.5], [0.5, 0.5, 0.5]
    eyl, eyh = [0.0, 1.0, 2.0], [1.0, 2.0, 3.0]
    root_object = ROOT.TGraphAsymmErrors(3, array.array("d", x), array.array("d", y),
                                         array.array("d", exl), array.array("d", exh),
                                         array.array("d", eyl), array.array("d", eyh))
    ds = mATLASplotlib.converters.Dataset(root_object)
    # Dimensions should be x and y
    assert ds.get_dimensions() == ["x", "y"]
    # x points should be recentred such that the x-errors are symmetric
    assert np.array_equal(ds.x_points, np.array([0.0, 1.0, 2.0]))
    # y points should be 0, 1, 4
    assert np.array_equal(ds.y_points, np.array([0.0, 1.0, 4.0]))
    # x error pairs should all be (0.4, 0.6)
    assert np.array_equal(ds.x_error_pairs, np.array([(0.5, 0.5), (0.5, 0.5), (0.5, 0.5)]))
    # y error pairs should all be as specified
    assert np.array_equal(ds.y_error_pairs, np.array([(0.0, 1.0), (1.0, 2.0), (2.0, 3.0)]))
    # There should be 3 points altogether
    assert ds.nPoints == 3

def test_root2data_constructor_TGraphErrors():
    x, y = [0, 1, 2], [0, 1, 4]
    ex = [0.5, 0.5, 0.5]
    ey = [0.0, 1.0, 2.0]
    root_object = ROOT.TGraphErrors(3, array.array("d", x), array.array("d", y),
                                        array.array("d", ex), array.array("d", ey))
    ds = mATLASplotlib.converters.Dataset(root_object)
    # Dimensions should be x and y
    assert ds.get_dimensions() == ["x", "y"]
    # x points should be recentred such that the x-errors are symmetric
    assert np.array_equal(ds.x_points, np.array([0.0, 1.0, 2.0]))
    # y points should be 0, 1, 4
    assert np.array_equal(ds.y_points, np.array([0.0, 1.0, 4.0]))
    # x error pairs should all be (0.4, 0.6)
    assert np.array_equal(ds.x_error_pairs, np.array([(0.5, 0.5), (0.5, 0.5), (0.5, 0.5)]))
    # y error pairs should all be as specified
    assert np.array_equal(ds.y_error_pairs, np.array([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]))
    # There should be 3 points altogether
    assert ds.nPoints == 3

def test_root2data_constructor_TH1D():
    root_object = ROOT.TH1D("TH1D", "TH1D", 3, -0.5, 2.5)
    for _x in range(3):
        root_object.Fill(_x)
    ds = mATLASplotlib.converters.Dataset(root_object)
    # Dimensions should be x and y
    assert ds.get_dimensions() == ["x", "y"]
    # x points should be 0, 1, 2
    assert np.array_equal(ds.x_points, np.array([0.0, 1.0, 2.0]))
    # y points should be 1, 1, 1
    assert np.array_equal(ds.y_points, np.array([1.0, 1.0, 1.0]))
    # x error pairs should all be 0.5
    assert np.array_equal(ds.x_error_pairs, np.array([(0.5, 0.5), (0.5, 0.5), (0.5, 0.5)]))
    # y error pairs should all be 1
    assert np.array_equal(ds.y_error_pairs, np.array([(1.0, 1.0), (1.0, 1.0), (1.0, 1.0)]))
    # There should be 3 points altogether
    assert ds.nPoints == 3


def test_root2data_constructor_TH2D():
    root_object = ROOT.TH2D("TH2D", "TH2D", 3, -0.5, 2.5, 3, -0.5, 2.5)
    for _x in range(3):
        for _y in range(3):
            root_object.Fill(_x, _y)
    ds = mATLASplotlib.converters.Dataset(root_object)
    # Dimensions should be x, y and z
    assert ds.get_dimensions() == ["x", "y", "z"]
    # x points should be [0.0, 1.0, 2.0]
    assert np.array_equal(ds.x_points, np.array([0.0, 1.0, 2.0]))
    # y points should be [0.0, 1.0, 2.0]
    assert np.array_equal(ds.y_points, np.array([0.0, 1.0, 2.0]))
    # z points should be [8, 27, 64]
    assert np.array_equal(ds.z_points, np.array([1., 1., 1., 1., 1., 1., 1., 1., 1.]))
    # x error pairs should all be zero
    assert np.array_equal(ds.x_error_pairs, np.array([(0.5, 0.5), (0.5, 0.5), (0.5, 0.5)]))
    # y error pairs should all be zero
    assert np.array_equal(ds.y_error_pairs, np.array([(0.5, 0.5), (0.5, 0.5), (0.5, 0.5)]))
    # There should be 9 points altogether
    assert ds.nPoints == 9


def test_root2data_constructor_TObject():
    with pytest.raises(ValueError):
        root_object = ROOT.TObject()
        mATLASplotlib.converters.Dataset(root_object)


def test_root2data_canvas_plot_TF1():
    root_object = ROOT.TF1("TF1", "sin(x)/x", 0.0, 10.0)
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset(root_object, style="line", colour="red")


def test_root2data_zero_removal():
    x, y = [0, 1, 2], [0, 1, 4]
    root_object = ROOT.TGraph(3, array.array("d", x), array.array("d", y))
    ds = mATLASplotlib.converters.Dataset(root_object, remove_zeros=True)
    assert ds.get_dimensions() == ["x", "y"]
    assert np.array_equal(ds.x_points, np.array([1.0, 2.0]))
    assert np.array_equal(ds.y_points, np.array([1.0, 4.0]))
    assert np.array_equal(ds.x_error_pairs, np.array([(0.0, 0.0), (0.0, 0.0)]))
    assert np.array_equal(ds.y_error_pairs, np.array([(0.0, 0.0), (0.0, 0.0)]))
    assert ds.nPoints == 2
