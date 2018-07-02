""" This module provides the ``Dataset`` class."""
import numpy as np
from root2data import root2data


class Dataset(object):
    """Container for plottable datasets."""

    def __init__(self, *args, **kwargs):
        """Constructor - specify values and error pair separately for each dimension.

        Arguments will be interpreted as the dataset to be plotted.

        :Examples:
            * x vs y : __init__([1,2,3], [4,9,16])
            * x vs y with y_errors : __init__([1,2,3], None, [4,9,16], [2,3,4])
            * z values at each (x, y) point : __init__([1, 2], [3, 4], [3, 4, 6, 8])

        :Positional Arguments:
            * **args**: (*ROOT.TObject*, *iterable*, *numpy array*) -- plottable information which is used to build a ``Dataset``

        :Keyword Arguments:
            * **x_values**: (*iterable*) -- list of points along the x-axis
            * **x_error_pairs**: (*iterable*) -- list of error pairs along the x-axis
            * **y_values**: (*iterable*) -- list of points along the y-axis
            * **y_error_pairs**: (*iterable*) -- list of error pairs along the y-axis
            * **z_values**: (*iterable*) -- list of points along the z-axis
            * **z_error_pairs**: (*iterable*) -- list of error pairs along the z-axis

        :raises AssertionError: arguments are not correctly sized
        :raises ValueError: arguments cannot be interpreted
        """
        self._data = {}
        self.nPoints = 0

        # Assume that an existing dataset or a ROOT object has been passed
        if len(args) == 1:
            if root2data.valid_input(args[0]):
                self.__from_ROOT(args[0], **kwargs)
            else:
                self.__from_dataset(args[0])

        # Assume that x, y values have been passed
        elif len(args) == 2:
            self.__from_xy_values(args[0], args[1])

        # Assume that x, y, z values have been passed
        elif len(args) == 3:
            self.__from_xyz_values(args[0], args[1], args[2])

        # Assume that x, y values with errors have been passed
        elif len(args) == 4:
            self.__from_xy_values_errors(args[0], args[1], args[2], args[3])

        # Assume that x, y values with errors and z values
        elif len(args) == 5:
            self.__from_xyz_values_errors(args[0], args[1], args[2], args[3], args[4], None)

        # Assume that x, y, z values with errors have been passed
        elif len(args) == 6:
            self.__from_xyz_values_errors(args[0], args[1], args[2], args[3], args[4], args[5])

        # Assume that keyworded lists have been passed in
        else:
            self.__from_keywords(**kwargs)

        # Add metainformation and validate
        if "x" in self.get_dimensions() and "y" in self.get_dimensions():
            self.__add_xy_dimensions()
        if not self.get_dimensions():
            raise ValueError("Attempt to initialise plottable {0} without providing data!".format(type(self)))

    def construct_2D_bin_list(self, axes="xy"):
        """Construct full set of bins when treating x and y as two sides of a 2D plot.

        :return: array of x and y bin centers that cover every (x, y) combination
        :rtype: [np.array, np.array]
        :raises ValueError: unsupported axes argument
        """
        if axes == "xy":
            bin_centres = np.meshgrid(getattr(self, "x_points"), getattr(self, "y_points"), indexing="xy")
        else:
            raise ValueError("Attempted to construct 2D bin list for {0} axes. Only 'xy' is currently supported.".format(axes))
        return [bin_centre.ravel() for bin_centre in bin_centres]

    def get_dimensions(self):
        """Get a list of dimension names.

        :return: list of dimension names
        :rtype: list(str)
        """
        return sorted(self._data.keys())

    def __from_dataset(self, input_dataset):
        """Construct from an existing dataset or a ROOT object.

        :param input_dataset: dataset
        :type input_dataset: Dataset

        :raises AssertionError: arguments are not correctly sized
        """
        if not isinstance(input_dataset, Dataset):
            raise AssertionError("Failed to interpret argument as an existing dataset")
        if hasattr(input_dataset, "x_points"):
            self.__add_dimension("x", input_dataset.x_points, input_dataset.x_error_pairs)
        if hasattr(input_dataset, "y_points"):
            self.__add_dimension("y", input_dataset.y_points, input_dataset.y_error_pairs)
        if hasattr(input_dataset, "z_points"):
            self.__add_dimension("z", input_dataset.z_points, input_dataset.z_error_pairs)
        self.nPoints = input_dataset.nPoints

    def __from_ROOT(self, input_object, **kwargs):
        """Construct from an existing ROOT object.

        :param input_object: ROOT object
        :type input_object: ROOT.TObject
        """
        data = root2data(input_object, remove_zeros=kwargs.pop("remove_zeros", False))
        for dimension in ["x", "y", "z"]:
            if hasattr(data, "{0}_values".format(dimension)) and getattr(data, "{0}_values".format(dimension)) is not None:
                self.__add_dimension(dimension, getattr(data, "{0}_values".format(dimension)), getattr(data, "{0}_error_pairs".format(dimension)))
        self.nPoints = data.nPoints

    def __from_xy_values(self, x, y):
        """Construct from x, y values.

        :param x: x values
        :type x: list
        :param y: y values
        :type y: list

        :raises AssertionError: arguments are not correctly sized
        """
        if len(x) != len(y):
            raise AssertionError("Failed to interpret arguments as 'x' and 'y' points since they differ in size")
        self.__add_dimension("x", x, None)
        self.__add_dimension("y", y, None)
        self.nPoints = len(self._data["x"])

    def __from_xyz_values(self, x, y, z):
        """Construct from x, y, z values.

        :param x: x values
        :type x: list
        :param y: y values
        :type y: list
        :param z: z values
        :type z: list

        :raises AssertionError: arguments are not correctly sized
        """
        if len(x) * len(y) != len(z):
            raise AssertionError("Failed to interpret arguments as 'x' and 'y' bins with 'z' values since they differ in size")
        self.__add_dimension("x", x, None)
        self.__add_dimension("y", y, None)
        self.__add_dimension("z", z, None)
        self.nPoints = len(self._data["z"])

    def __from_xy_values_errors(self, x, x_err, y, y_err):
        """Construct from x, y values with errors.

        :param x: x values
        :type x: list
        :param x_err: x errors
        :type x_err: list
        :param y: y values
        :type y: list
        :param y_err: y errors
        :type y_err: list

        :raises AssertionError: arguments are not correctly sized
        """
        if len(x) != len(y):
            raise AssertionError("Failed to interpret arguments as 'x' and 'y' points with errors since they differ in size")
        self.__add_dimension("x", x, x_err)
        self.__add_dimension("y", y, y_err)
        self.nPoints = len(self._data["x"])

    def __from_xyz_values_errors(self, x, x_err, y, y_err, z, z_err):
        """Construct from x, y, z values with errors.

        :param x: x values
        :type x: list
        :param x_err: x errors
        :type x_err: list
        :param y: y values
        :type y: list
        :param y_err: y errors
        :type y_err: list
        :param z: z values
        :type z: list
        :param z_err: z errors
        :type z_err: list

        :raises AssertionError: arguments are not correctly sized
        """
        if len(x) * len(y) != len(z):
            raise AssertionError("Failed to interpret arguments as 'x' and 'y' bins with 'z' values since they differ in size")
        self.__add_dimension("x", x, x_err)
        self.__add_dimension("y", y, y_err)
        self.__add_dimension("z", z, z_err)
        self.nPoints = len(self._data["z"])

    def __from_keywords(self, **kwargs):
        """Construct an array of points with an error pair in each direction.

        :Keyword Arguments:
            * **x_values** (*list*) -- x values
            * **x_error_pairs** (*list*) -- x error pairs
            * **y_values** (*list*) -- y values
            * **y_error_pairs** (*list*) -- y error pairs
            * **z_values** (*list*) -- z values
            * **z_error_pairs** (*list*) -- z error pairs
        """
        if "x_values" in kwargs:
            self.__add_dimension("x", kwargs.pop("x_values"), kwargs.get("x_error_pairs", None))
            self.nPoints = len(self._data["x"])
        if "y_values" in kwargs:
            self.__add_dimension("y", kwargs.pop("y_values"), kwargs.get("y_error_pairs", None))
        if "z_values" in kwargs:
            self.__add_dimension("z", kwargs.pop("z_values"), kwargs.get("z_error_pairs", None))
            self.nPoints = len(self._data["z"])

    def __add_dimension(self, dimension, values, error_pairs):
        """Add a new dimension with appropriate methods.

        :param dimension: which axis dimension to add
        :type dimension: str
        :param values: values along this dimension
        :type values: list
        :param error_pairs: pairs of errors for each point
        :type error_pairs: list[tuple]
        """
        # Use zeros if no errors provided
        if error_pairs is None:
            error_pairs = [(0, 0)] * len(values)
        try:
            # If errors are paired, check that each pair has two elements
            for error_pair in error_pairs:
                if len(error_pair) != 2:
                    raise ValueError("Error pairs must be of size 2!")
        except TypeError:
            # Otherwise construct symmetric error pairs
            error_pairs = [(e, e) for e in error_pairs]
        # Check that the dimensions match
        if len(values) != len(error_pairs):
            raise ValueError("Number of error pairs must equal number of values!")
        # Register this dimension
        self._data[dimension] = np.array([[value, error_pair[0], error_pair[1]] for value, error_pair in zip(values, error_pairs)])
        # Add appropriate attributes
        setattr(self, "{0}_points".format(dimension), self.__get_points(dimension))
        setattr(self, "{0}_error_pairs".format(dimension), self.__get_error_pairs(dimension))
        setattr(self, "{0}_points_error_symmetrised".format(dimension), self.__get_points_error_symmetrised(dimension))
        setattr(self, "{0}_errors_symmetrised".format(dimension), self.__get_errors_symmetrised(dimension))
        setattr(self, "{0}_all_bin_edges".format(dimension), self.__get_all_bin_edges(dimension))
        setattr(self, "{0}_bin_edges".format(dimension), self.__get_bin_edges(dimension))
        setattr(self, "{0}_bin_widths".format(dimension), self.__get_bin_widths(dimension))
        setattr(self, "{0}_bin_low_edges".format(dimension), self.__get_bin_low_edges(dimension))
        setattr(self, "{0}_bin_high_edges".format(dimension), self.__get_bin_high_edges(dimension))

    def __add_xy_dimensions(self):
        """Add xy-appropriate methods."""
        setattr(self, "x_at_y_bin_edges", self.__get_x_at_y_bin_edges())
        setattr(self, "y_at_x_bin_edges", self.__get_y_at_x_bin_edges())
        setattr(self, "band_edges_x", self.__get_band_edges_x())
        setattr(self, "band_edges_y_low", self.__get_band_edges_y_low())
        setattr(self, "band_edges_y_high", self.__get_band_edges_y_high())

    def __get_points(self, dimension):
        """Return array of x/y/z points, constructing if necessary."""
        attr_name = "_{0}_points".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[0] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_error_pairs(self, dimension):
        """Return array of x/y/z points, constructing if necessary."""
        attr_name = "_{0}_error_pairs".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([[point[1], point[2]] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_points_error_symmetrised(self, dimension):
        """Return array of x/y/z points, constructing if necessary."""
        attr_name = "_{0}_points_error_symmetrised".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[0] + (point[2] - point[1]) / 2.0 for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_errors_symmetrised(self, dimension):
        """Return array of x/y/z points, constructing if necessary."""
        attr_name = "_{0}_errors_symmetrised".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([(point[1] + point[2]) / 2.0 for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_all_bin_edges(self, dimension):
        """Return array of all x/y/z bin edges, constructing if necessary."""
        attr_name = "_{0}_all_bin_edges".format(dimension)
        if not hasattr(self, attr_name):
            low_edges, high_edges = self.__get_bin_low_edges(dimension), self.__get_bin_high_edges(dimension)
            value = np.array(sum([[l, h] for l, h in zip(low_edges, high_edges)], []))
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_bin_edges(self, dimension):
        """Return array of x/y/z bin edges without duplicates, constructing if necessary."""
        attr_name = "_{0}_bin_edges".format(dimension)
        if not hasattr(self, attr_name):
            value = np.unique(getattr(self, "_{0}_all_bin_edges".format(dimension)))
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_bin_widths(self, dimension):
        """Return array of x/y/z bin widths, constructing if necessary."""
        attr_name = "_{0}_bin_widths".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[1] + point[2] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_bin_low_edges(self, dimension):
        """Return array of x/y/z bin low edges, constructing if necessary."""
        attr_name = "_{0}_bin_low_edges".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[0] - point[1] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_bin_high_edges(self, dimension):
        """Return array of x/y/z bin high edges, constructing if necessary."""
        attr_name = "_{0}_bin_high_edges".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[0] + point[2] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    def __get_x_at_y_bin_edges(self):
        """Return array of x at the bin edges of y bins, constructing if necessary."""
        if not hasattr(self, "_x_at_y_bin_edges"):
            setattr(self, "_x_at_y_bin_edges", np.array(sum([[x_point, x_point] for x_point in getattr(self, "x_points")], [])))
        return getattr(self, "_x_at_y_bin_edges")

    def __get_y_at_x_bin_edges(self):
        """Return array of y at the bin edges of x bins, constructing if necessary."""
        if not hasattr(self, "_y_at_x_bin_edges"):
            setattr(self, "_y_at_x_bin_edges", np.array(sum([[y_point, y_point] for y_point in getattr(self, "y_points")], [])))
        return getattr(self, "_y_at_x_bin_edges")

    def __get_band_edges_x(self):
        """Return array of x edges for fillable band, constructing if necessary."""
        if not hasattr(self, "_band_edges_x"):
            setattr(self, "_band_edges_x", np.array(sum([[point[0] - point[1], point[0] + point[2]] for point in self._data["x"]], [])))
        return getattr(self, "_band_edges_x")

    def __get_band_edges_y_low(self):
        """Return array of y minima for fillable band, constructing if necessary."""
        if not hasattr(self, "_band_edges_y_low"):
            setattr(self, "_band_edges_y_low", np.array(sum([[point[0] - point[1], point[0] - point[1]] for point in self._data["y"]], [])))
        return getattr(self, "_band_edges_y_low")

    def __get_band_edges_y_high(self):
        """Return array of y maxima for fillable band, constructing if necessary."""
        if not hasattr(self, "_band_edges_y_high"):
            setattr(self, "_band_edges_y_high", np.array(sum([[point[0] + point[2], point[0] + point[2]] for point in self._data["y"]], [])))
        return getattr(self, "_band_edges_y_high")
