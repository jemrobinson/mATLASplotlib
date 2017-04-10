import numpy as np
from root2data import root2data

class Dataset(object):
    """Container for plottable datasets"""
    # Constructor - specify values and error pair separately for each dimension
    # Example : x vs y : __init__( [1,2,3], [4,9,16] )
    # Example : x vs y with y_errors : __init__( [1,2,3], None, [4,9,16], [2,3,4] )
    def __init__(self, *args, **kwargs):
        self._data = {}
        # Check how the data has been provided
        if len(args) == 1 :
            # Check for ROOT input
            if root2data.valid_input(args[0]):
                data = root2data(args[0])
                if data.x_values is not None:
                    self._add_dimension("x", data.x_values, data.x_error_pairs)
                if data.y_values is not None:
                    self._add_dimension("y", data.y_values, data.y_error_pairs)
                if data.z_values is not None:
                    self._add_dimension("z", data.z_values, data.z_error_pairs)
        # Assume that x,y values have been passed
        elif len(args) == 2:
            self._add_dimension("x", args[0], None, **kwargs)
            self._add_dimension("y", args[1], None, **kwargs)
        # Assume that x,y,z values have been passed
        elif len(args) == 3:
            self._add_dimension("x", args[0], None, **kwargs)
            self._add_dimension("y", args[1], None, **kwargs)
            self._add_dimension("z", args[2], None, **kwargs)
        # Assume that x,y values with errors have been passed
        elif len(args) == 4:
            self._add_dimension("x", args[0], args[1], **kwargs)
            self._add_dimension("y", args[2], args[3], **kwargs)
        # Assume that x,y,z values with errors have been passed
        elif len(args) == 6:
            self._add_dimension("x", args[0], args[1], **kwargs)
            self._add_dimension("y", args[2], args[3], **kwargs)
            self._add_dimension("z", args[4], args[5], **kwargs)
        # Construct an array of points in N-dimensional space, with an error pair in each direction
        else:
            if "x_values" in kwargs:
                self._add_dimension("x", kwargs["x_values"], kwargs.get("x_error_pairs", None), **kwargs)
            if "y_values" in kwargs:
                self._add_dimension("y", kwargs["y_values"], kwargs.get("y_error_pairs", None), **kwargs)
            if "z_values" in kwargs:
                self._add_dimension("z", kwargs["z_values"], kwargs.get("z_error_pairs", None), **kwargs)
            for dimension in self.get_dimensions():
                assert(len(self._data[dimension]) == self.number_of_points())
        if "x" in self.get_dimensions() and "y" in self.get_dimensions():
            self._add_xy_dimensions()
        if len(self.get_dimensions()) == 0:
            raise RuntimeError("Attempt to initialise plottable {0} without providing data!".format(type(self)))



    # Add a new dimension with appropriate methods
    def _add_dimension(self, dimension, values, error_pairs):
        # Use zeros if no errors provided
        if error_pairs is None:
            error_pairs = [(0, 0)] * len(values)
        # Pair-up errors if only single errors are provided
        try:
            for error_pair in error_pairs:
                assert(len(error_pair) == 2)
        except TypeError:
            error_pairs = [(e, e) for e in error_pairs]
        assert(len(values) == len(error_pairs))
        try:
            self._data[dimension] = np.array([[value, error_pair[0], error_pair[1]] for value, error_pair in zip(values, error_pairs)])
        except IndexError:
            self._data[dimension] = np.array([[value, error, error] for value, error in zip(values, error_pairs)])
        setattr(self, "{0}_points".format(dimension), self.__get_points(dimension))
        setattr(self, "{0}_error_pairs".format(dimension), self.__get_error_pairs(dimension))
        setattr(self, "{0}_points_error_symmetrised".format(dimension), self.__get_points_error_symmetrised(dimension))
        setattr(self, "{0}_errors_symmetrised".format(dimension), self.__get_errors_symmetrised(dimension))
        setattr(self, "{0}_all_bin_edges".format(dimension), self.__get_all_bin_edges(dimension))
        setattr(self, "{0}_bin_edges".format(dimension), self.__get_bin_edges(dimension))
        setattr(self, "{0}_bin_widths".format(dimension), self.__get_bin_widths(dimension))
        setattr(self, "{0}_bin_low_edges".format(dimension), self.__get_bin_low_edges(dimension))
        setattr(self, "{0}_bin_high_edges".format(dimension), self.__get_bin_high_edges(dimension))

    # Add xy-appropriate methods
    def _add_xy_dimensions(self):
        setattr(self, "x_at_y_bin_edges", self.__get_x_at_y_bin_edges())
        setattr(self, "y_at_x_bin_edges", self.__get_y_at_x_bin_edges())
        setattr(self, "band_edges_x", self.__get_band_edges_x())
        setattr(self, "band_edges_y_low", self.__get_band_edges_y_low())
        setattr(self, "band_edges_y_high", self.__get_band_edges_y_high())

    # def number_of_points(self):
    #     return len(self._data[self.get_dimensions()[0]])

    def get_dimensions(self):
        return sorted(self._data.keys())


    # Construct expanded bin lists in x and y
    def unroll_bins(self, axes="xy"):
        if axes == "xy":
            bin_centres = np.meshgrid(self.x_points, self.y_points, indexing="xy")
        return [bin_centre.ravel() for bin_centre in bin_centres]

    # Return array of x/y/z points, constructing if necessary
    def __get_points(self, dimension):
        attr_name = "_{0}_points".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[0] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of x/y/z points, constructing if necessary
    def __get_error_pairs(self, dimension):
        attr_name = "_{0}_error_pairs".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([[point[1], point[2]] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of x/y/z points, constructing if necessary
    def __get_points_error_symmetrised(self, dimension):
        attr_name = "_{0}_points_error_symmetrised".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[0] + (point[2] - point[1]) / 2.0 for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of x/y/z points, constructing if necessary
    def __get_errors_symmetrised(self, dimension):
        attr_name = "_{0}_errors_symmetrised".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([(point[1] + point[2]) / 2.0 for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of all x/y/z bin edges, constructing if necessary
    def __get_all_bin_edges(self, dimension):
        attr_name = "_{0}_all_bin_edges".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array(sum([[low_edge, high_edge] for low_edge, high_edge in zip(self.__get_bin_low_edges(dimension), self.__get_bin_high_edges(dimension))], []))
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of x/y/z bin edges without duplicates, constructing if necessary
    def __get_bin_edges(self, dimension):
        attr_name = "_{0}_bin_edges".format(dimension)
        if not hasattr(self, attr_name):
            value = np.unique(getattr(self, "_{0}_all_bin_edges".format(dimension)))
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of x/y/z bin widths, constructing if necessary
    def __get_bin_widths(self, dimension):
        attr_name = "_{0}_bin_widths".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[1] + point[2] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of x/y/z bin low edges, constructing if necessary
    def __get_bin_low_edges(self, dimension):
        attr_name = "_{0}_bin_low_edges".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[0] - point[1] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of x/y/z bin high edges, constructing if necessary
    def __get_bin_high_edges(self, dimension):
        attr_name = "_{0}_bin_high_edges".format(dimension)
        if not hasattr(self, attr_name):
            value = np.array([point[0] + point[2] for point in self._data[dimension]])
            setattr(self, attr_name, value)
        return getattr(self, attr_name)

    # Return array of x at the bin edges of y bins, constructing if necessary
    def __get_x_at_y_bin_edges(self):
        if not hasattr(self, "_x_at_y_bin_edges"):
            self._x_at_y_bin_edges = np.array(sum([[x_point, x_point] for x_point in self.x_points], []))
        return self._x_at_y_bin_edges

    # Return array of y at the bin edges of x bins, constructing if necessary
    def __get_y_at_x_bin_edges(self):
        if not hasattr(self, "_y_at_x_bin_edges"):
            self._y_at_x_bin_edges = np.array(sum([[y_point, y_point] for y_point in self.y_points], []))
        return self._y_at_x_bin_edges

    # Return array of x edges for fillable band, constructing if necessary
    def __get_band_edges_x(self):
        if not hasattr(self, "_band_edges_x"):
            self._band_edges_x = np.array(sum([[point[0] - point[1], point[0] + point[2]] for point in self._data["x"]], []))
        return self._band_edges_x

    # Return array of y minima for fillable band, constructing if necessary
    def __get_band_edges_y_low(self):
        if not hasattr(self, "_band_edges_y_low"):
            self._band_edges_y_low = np.array(sum([[point[0] - point[1], point[0] - point[1]] for point in self._data["y"]], []))
        return self._band_edges_y_low

    # Return array of y maxima for fillable band, constructing if necessary
    def __get_band_edges_y_high(self):
        if not hasattr(self, "_band_edges_y_high"):
            self._band_edges_y_high = np.array(sum([[point[0] + point[2], point[0] + point[2]] for point in self._data["y"]], []))
        return self._band_edges_y_high
