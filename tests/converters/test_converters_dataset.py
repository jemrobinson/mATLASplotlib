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
    # There should be 3 points altogether
    assert(ds.nPoints == 3)


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
    # There should be 3 points altogether
    assert(ds.nPoints == 3)


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
    # There should be 3 points altogether
    assert(ds.nPoints == 3)


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
    # There should be 3 points altogether
    assert(ds.nPoints == 3)


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
    # There should be 3 points altogether
    assert(ds.nPoints == 3)


def test_constructor_x_y_with_non_matching_inputs():
    with pytest.raises(AssertionError) as e_info:
        ds = Dataset([1, 2, 3], [4, 9, 16, 25])


def test_constructor_x_y_z():
    x, y = [2, 3, 4], [4, 9, 16]
    z = [_x * _y for _x in x for _y in y]
    ds = Dataset(x, y, z)
    # Dimensions should be x and y
    assert(ds.get_dimensions() == ["x", "y", "z"])
    # x points should be [1, 2, 3]
    assert(np.array_equal(ds.x_points,np.array([2, 3, 4])))
    # y points should be [4, 9, 16]
    assert(np.array_equal(ds.y_points,np.array([4, 9, 16])))
    # z points should be [8, 27, 64]
    assert(np.array_equal(ds.z_points,np.array([8, 18, 32, 12, 27, 48, 16, 36, 64])))
    # There should be 9 points altogether
    assert(ds.nPoints == 9)

def test_constructor_x_y_z_with_symmetric_x_errors():
    x, y = [2, 3, 4], [4, 9, 16]
    z = [_x * _y for _x in x for _y in y]
    ds = Dataset(x, [1, 2, 3], y, None, z, None)
    # Dimensions should be x and y
    assert(ds.get_dimensions() == ["x", "y", "z"])
    # x points should be [1, 2, 3]
    assert(np.array_equal(ds.x_points,np.array([2, 3, 4])))
    # y points should be [4, 9, 16]
    assert(np.array_equal(ds.y_points,np.array([4, 9, 16])))
    # z points should be [8, 27, 64]
    assert(np.array_equal(ds.z_points,np.array([8, 18, 32, 12, 27, 48, 16, 36, 64])))
    # x errors should be pairs based on the input errors
    assert(np.array_equal(ds.x_error_pairs,np.array([(1, 1), (2, 2), (3, 3)])))
    # There should be 9 points altogether
    assert(ds.nPoints == 9)
