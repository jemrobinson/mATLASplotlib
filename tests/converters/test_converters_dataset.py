import numpy as np
import pytest
from mATLASplotlib.converters import Dataset


def test_dataset_constructor_x_y():
    ds = Dataset([1, 2, 3], [4, 9, 16])
    assert ds.get_dimensions() == ["x", "y"]
    assert np.array_equal(ds.x_points, np.array([1, 2, 3]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.x_error_pairs, np.array([(0, 0), (0, 0), (0, 0)]))
    assert np.array_equal(ds.y_error_pairs, np.array([(0, 0), (0, 0), (0, 0)]))
    assert ds.nPoints == 3


def test_dataset_constructor_x_y_with_symmetric_x_errors():
    ds = Dataset([4, 5, 6], [1, 2, 3], [4, 9, 16], None)
    assert ds.get_dimensions() == ["x", "y"]
    assert np.array_equal(ds.x_points, np.array([4, 5, 6]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.x_error_pairs, np.array([(1, 1), (2, 2), (3, 3)]))
    assert np.array_equal(ds.y_error_pairs, np.array([(0, 0), (0, 0), (0, 0)]))
    assert ds.nPoints == 3


def test_dataset_constructor_x_y_with_symmetric_x_and_y_errors():
    ds = Dataset([4, 5, 6], [1, 2, 3], [4, 9, 16], [3, 2, 1])
    assert ds.get_dimensions() == ["x", "y"]
    assert np.array_equal(ds.x_points, np.array([4, 5, 6]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.x_error_pairs, np.array([(1, 1), (2, 2), (3, 3)]))
    assert np.array_equal(ds.y_error_pairs, np.array([(3, 3), (2, 2), (1, 1)]))
    assert ds.nPoints == 3


def test_dataset_constructor_x_y_with_asymmetric_x_errors():
    ds = Dataset([4, 5, 6], [(1, 2), (2, 3), (3, 4)], [4, 9, 16], None)
    assert ds.get_dimensions() == ["x", "y"]
    assert np.array_equal(ds.x_points, np.array([4, 5, 6]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.x_error_pairs, np.array([(1, 2), (2, 3), (3, 4)]))
    assert np.array_equal(ds.y_error_pairs, np.array([(0, 0), (0, 0), (0, 0)]))
    assert ds.nPoints == 3


def test_dataset_constructor_x_y_with_asymmetric_x_and_y_errors():
    ds = Dataset([4, 5, 6], [(1, 2), (2, 3), (3, 4)],
                 [4, 9, 16], [(3, 2), (2, 1), (1, 0)])
    assert ds.get_dimensions() == ["x", "y"]
    assert np.array_equal(ds.x_points, np.array([4, 5, 6]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.x_error_pairs, np.array([(1, 2), (2, 3), (3, 4)]))
    assert np.array_equal(ds.y_error_pairs, np.array([(3, 2), (2, 1), (1, 0)]))
    assert ds.nPoints == 3


def test_dataset_constructor_x_y_with_non_matching_inputs():
    with pytest.raises(AssertionError):
        Dataset([1, 2, 3], [4, 9, 16, 25])


def test_dataset_constructor_x_y_z():
    x, y = [2, 3, 4], [4, 9, 16]
    z = [_x * _y for _x in x for _y in y]
    ds = Dataset(x, y, z)
    assert ds.get_dimensions() == ["x", "y", "z"]
    assert np.array_equal(ds.x_points, np.array([2, 3, 4]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.z_points, np.array(
        [8, 18, 32, 12, 27, 48, 16, 36, 64]))
    assert ds.nPoints == 9


def test_dataset_constructor_x_y_z_without_z_errors():
    x, y = [2, 3, 4], [4, 9, 16]
    z = [_x * _y for _x in x for _y in y]
    ds = Dataset(x, [1, 2, 3], y, None, z)
    assert ds.get_dimensions() == ["x", "y", "z"]
    assert np.array_equal(ds.x_points, np.array([2, 3, 4]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.z_points, np.array([8, 18, 32, 12, 27, 48, 16, 36, 64]))
    assert np.array_equal(ds.x_error_pairs, np.array([(1, 1), (2, 2), (3, 3)]))
    assert ds.nPoints == 9


def test_dataset_constructor_x_y_z_with_symmetric_x_errors():
    x, y = [2, 3, 4], [4, 9, 16]
    z = [_x * _y for _x in x for _y in y]
    ds = Dataset(x, [1, 2, 3], y, None, z, None)
    assert ds.get_dimensions() == ["x", "y", "z"]
    assert np.array_equal(ds.x_points, np.array([2, 3, 4]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.z_points, np.array([8, 18, 32, 12, 27, 48, 16, 36, 64]))
    assert np.array_equal(ds.x_error_pairs, np.array([(1, 1), (2, 2), (3, 3)]))
    assert ds.nPoints == 9


def test_dataset_constructor_keywords():
    ds = Dataset(x_values=[2, 3, 4], y_values=[4, 9, 16], z_values=[8, 18, 32, 12, 27, 48, 16, 36, 64])
    assert ds.get_dimensions() == ["x", "y", "z"]
    assert np.array_equal(ds.x_points, np.array([2, 3, 4]))
    assert np.array_equal(ds.y_points, np.array([4, 9, 16]))
    assert np.array_equal(ds.z_points, np.array([8, 18, 32, 12, 27, 48, 16, 36, 64]))
    assert ds.nPoints == 9


def test_dataset_constructor_dataset():
    ds1 = Dataset([2, 3, 4], [1, 2, 3], [4, 9, 16], None, [8, 18, 32, 12, 27, 48, 16, 36, 64], None)
    ds2 = Dataset(ds1)
    assert np.array_equal(ds1.x_points, ds2.x_points)
    assert np.array_equal(ds1.x_error_pairs, ds2.x_error_pairs)
    assert np.array_equal(ds1.y_points, ds2.y_points)
    assert np.array_equal(ds1.y_error_pairs, ds2.y_error_pairs)
    assert np.array_equal(ds1.z_points, ds2.z_points)
    assert np.array_equal(ds1.z_error_pairs, ds2.z_error_pairs)


def test_dataset_constructor_invalid():
    with pytest.raises(ValueError):
        Dataset()
    with pytest.raises(AssertionError):
        Dataset(5)
    with pytest.raises(AssertionError):
        Dataset([1, 2, 3], [4, 5])
    with pytest.raises(AssertionError):
        Dataset([1, 2, 3], [4, 5], [7, 8, 9, 10, 11])
    with pytest.raises(AssertionError):
        Dataset([1, 2, 3], [1, 1, 1], [4, 5], [1, 1])
    with pytest.raises(ValueError):
        Dataset([4, 5, 6], [(1, 1), (2, 2, 2), (3, 3)], [4, 9, 16], [1, 2, 3])
    with pytest.raises(ValueError):
        Dataset([4, 5, 6], [1, 2, 3], [4, 9, 16], [1, 2])
    with pytest.raises(AssertionError):
        Dataset([4, 5, 6], [1, 2, 3], [4, 9], [1, 2], [1, 1, 1, 1, 1], None)


def test_dataset_construct_2D_bin_list_invalid():
    ds = Dataset([1, 2, 3], [4, 9, 16])
    with pytest.raises(ValueError):
        ds.construct_2D_bin_list("yz")
