import numpy as np
import pytest
from mATLASplotlib.converters import Dataset

def test_constructor_x_y():
    ds = Dataset([1, 2, 3], [4, 9, 16])
    # Dimensions should be x and y
    assert(ds.get_dimensions() == ["x", "y"])
    # x points should be 1, 2, 3
    assert(np.array_equal(ds.x_points,np.array([1, 2, 3])))
    # y points should be 4, 9, 16
    assert(np.array_equal(ds.y_points,np.array([4, 9, 16])))
    # x error pairs should all be zero
    assert(np.array_equal(ds.x_error_pairs,np.array([(0, 0), (0, 0), (0, 0)])))
    # y error pairs should all be zero
    assert(np.array_equal(ds.y_error_pairs,np.array([(0, 0), (0, 0), (0, 0)])))


def test_constructor_x_y_with_symmetric_x_errors():
    ds = Dataset([4, 5, 6], [1, 2, 3], [4, 9, 16], None)
    # Dimensions should be x and y
    assert(ds.get_dimensions() == ["x", "y"])
    # x points should be 1, 2, 3
    assert(np.array_equal(ds.x_points,np.array([4, 5, 6])))
    # y points should be 4, 9, 16
    assert(np.array_equal(ds.y_points,np.array([4, 9, 16])))
    # x errors should be pairs based on the input errors
    assert(np.array_equal(ds.x_error_pairs,np.array([(1, 1), (2, 2), (3, 3)])))
    # y error pairs should all be zero
    assert(np.array_equal(ds.y_error_pairs,np.array([(0, 0), (0, 0), (0, 0)])))


def test_constructor_x_y_with_symmetric_x_and_y_errors():
    ds = Dataset([4, 5, 6], [1, 2, 3], [4, 9, 16], [3, 2, 1])
    # Dimensions should be x and y
    assert(ds.get_dimensions() == ["x", "y"])
    # x points should be 1, 2, 3
    assert(np.array_equal(ds.x_points,np.array([4, 5, 6])))
    # y points should be 4, 9, 16
    assert(np.array_equal(ds.y_points,np.array([4, 9, 16])))
    # x errors should be pairs based on the input errors
    assert(np.array_equal(ds.x_error_pairs,np.array([(1, 1), (2, 2), (3, 3)])))
    # y error should be pairs based on the input errors
    assert(np.array_equal(ds.y_error_pairs,np.array([(3, 3), (2, 2), (1, 1)])))


def test_constructor_x_y_with_asymmetric_x_errors():
    ds = Dataset([4, 5, 6], [(1, 2), (2, 3), (3, 4)], [4, 9, 16], None)
    # Dimensions should be x and y
    assert(ds.get_dimensions() == ["x", "y"])
    # x points should be 1, 2, 3
    assert(np.array_equal(ds.x_points,np.array([4, 5, 6])))
    # y points should be 4, 9, 16
    assert(np.array_equal(ds.y_points,np.array([4, 9, 16])))
    # x errors should be the input errors
    assert(np.array_equal(ds.x_error_pairs,np.array([(1, 2), (2, 3), (3, 4)])))
    # y error pairs should all be zero
    assert(np.array_equal(ds.y_error_pairs,np.array([(0, 0), (0, 0), (0, 0)])))


def test_constructor_x_y_with_asymmetric_x_and_y_errors():
    ds = Dataset([4, 5, 6], [(1, 2), (2, 3), (3, 4)], [4, 9, 16], [(3, 2), (2, 1), (1, 0)])
    # Dimensions should be x and y
    assert(ds.get_dimensions() == ["x", "y"])
    # x points should be 1, 2, 3
    assert(np.array_equal(ds.x_points,np.array([4, 5, 6])))
    # y points should be 4, 9, 16
    assert(np.array_equal(ds.y_points,np.array([4, 9, 16])))
    # x errors should be the input errors
    assert(np.array_equal(ds.x_error_pairs,np.array([(1, 2), (2, 3), (3, 4)])))
    # y errors should be the input errors
    assert(np.array_equal(ds.y_error_pairs,np.array([(3, 2), (2, 1), (1, 0)])))


def test_constructor_x_y_with_non_matching_inputs():
    with pytest.raises(AssertionError) as e_info:
        ds = Dataset([1, 2, 3], [4, 9, 16, 25])
