""" This module provides the ``root2data`` class."""
import numpy as np
import ROOT

# pylint: disable=no-member
# ROOT members are incorrectly flagged as not belonging to the package


class root2data(object):
    """Interpreter for ROOT objects."""

    def __init__(self, root_object, remove_zeros=False):
        """Extract x/y/z information from a ROOT object.

        :param root_object: ROOT input to interpret
        :type root_object: ROOT.TObject
        :param remove_zeros: whether to remove points with a value of 0
        :type remove_zeros: bool
        """
        self.x_values, self.x_error_pairs = None, None
        self.y_values, self.y_error_pairs = None, None
        self.z_values, self.z_error_pairs = None, None
        self.nPoints = 0
        # Initialise TH2 constructor
        if isinstance(root_object, ROOT.TH2):
            self.construct_from_TH2(root_object)
        # Initialise TH1 constructor
        elif isinstance(root_object, ROOT.TH1):
            self.construct_from_TH1(root_object)
        # Initialise TF1 constructor
        elif isinstance(root_object, ROOT.TF1):
            self.construct_from_TF1(root_object)
        # Initialise TGraphAsymmErrors constructor
        elif isinstance(root_object, ROOT.TGraphAsymmErrors):
            self.construct_from_TGraphAsymmErrors(root_object)
        # Initialise TGraphErrors constructor
        elif isinstance(root_object, ROOT.TGraphErrors):
            self.construct_from_TGraphErrors(root_object)
        # Initialise TGraph constructor
        elif isinstance(root_object, ROOT.TGraph):
            self.construct_from_TGraph(root_object)
        else:
            raise ValueError("{0}, of type {1}, is not a convertible ROOT object".format(root_object, type(root_object)))
        if remove_zeros:
            self.do_zero_removal()

    @staticmethod
    def valid_input(test_object):
        """Check that the input object is a valid ROOT TObject.

        :param test_object: input object to invesigate
        :type test_object: object
        :return: whether the input object is a ROOT TObject
        :rtype: bool
        """
        return isinstance(test_object, ROOT.TObject)

    def construct_from_TF1(self, input_TF1):
        """Read TF1 into x, y dimensions.

        :param input_TF1: input TF1
        :type input_TF1: ROOT.TF1
        """
        x_min, x_max = ROOT.Double(), ROOT.Double()
        input_TF1.GetRange(x_min, x_max)
        self.x_values = np.linspace(x_min, x_max, num=1000, endpoint=True)
        self.x_error_pairs = [[0, 0] for _ in range(len(self.x_values))]
        self.y_values = [input_TF1.Eval(x) for x in self.x_values]
        self.y_error_pairs = [[0, 0] for _ in range(len(self.y_values))]
        self.nPoints = len(self.x_values)

    def construct_from_TH1(self, input_TH1):
        """Read TH1 into x, y dimensions.

        :param input_TH1: input TH1
        :type input_TH1: ROOT.TH1
        """
        self.x_values = [input_TH1.GetXaxis().GetBinCenter(_bin) for _bin in range(1, input_TH1.GetNbinsX() + 1)]
        self.x_error_pairs = [[0.5 * input_TH1.GetXaxis().GetBinWidth(_bin)] * 2 for _bin in range(1, input_TH1.GetNbinsX() + 1)]
        self.y_values = [input_TH1.GetBinContent(_bin) for _bin in range(1, input_TH1.GetNbinsX() + 1)]
        self.y_error_pairs = [(input_TH1.GetBinErrorLow(_bin), input_TH1.GetBinErrorUp(_bin)) for _bin in range(1, input_TH1.GetNbinsX() + 1)]
        self.nPoints = len(self.x_values)

    def construct_from_TH2(self, input_TH2):
        """Read TH2 into x, y, z dimensions.

        :param input_TH2: input TH2
        :type input_TH2: ROOT.TH2
        """
        self.x_values = [input_TH2.GetXaxis().GetBinCenter(_bin) for _bin in range(1, input_TH2.GetNbinsX() + 1)]
        self.x_error_pairs = [[0.5 * input_TH2.GetXaxis().GetBinWidth(_bin)] * 2 for _bin in range(1, input_TH2.GetNbinsX() + 1)]
        self.y_values = [input_TH2.GetYaxis().GetBinCenter(_bin) for _bin in range(1, input_TH2.GetNbinsY() + 1)]
        self.y_error_pairs = [[0.5 * input_TH2.GetYaxis().GetBinWidth(_bin)] * 2 for _bin in range(1, input_TH2.GetNbinsY() + 1)]
        self.z_values, self.z_error_pairs = [], []
        x_bin_edges = [input_TH2.GetXaxis().GetBinLowEdge(_bin) for _bin in range(1, input_TH2.GetNbinsX() + 2)]
        y_bin_edges = [input_TH2.GetYaxis().GetBinLowEdge(_bin) for _bin in range(1, input_TH2.GetNbinsY() + 2)]
        ix_array, iy_array = np.meshgrid(range(1, len(x_bin_edges)), range(1, len(y_bin_edges)), indexing='xy')
        for ix, iy in zip(ix_array.ravel(), iy_array.ravel()):
            self.z_values.append(input_TH2.GetBinContent(ix, iy))
            self.z_error_pairs.append((input_TH2.GetBinErrorLow(ix, iy), input_TH2.GetBinErrorUp(ix, iy)))
        self.nPoints = len(self.z_values)

    def construct_from_TGraph(self, input_TGraph):
        """Read TGraph into x, y dimensions.

        :param input_TGraph: input TGraph
        :type input_TGraph: ROOT.TGraph
        """
        x, y = input_TGraph.GetX(), input_TGraph.GetY()
        self.x_values, self.x_error_pairs, self.y_values, self.y_error_pairs = [], [], [], []
        for ii in range(input_TGraph.GetN()):
            self.x_values.append(x[ii])
            self.x_error_pairs.append([0, 0])
            self.y_values.append(y[ii])
            self.y_error_pairs.append([0, 0])
        self.nPoints = len(self.x_values)

    def construct_from_TGraphErrors(self, input_TGraphErrors):
        """Read TGraphErrors into x, y dimensions.

        :param input_TGraphErrors: input TGraphErrors
        :type input_TGraphErrors: ROOT.TGraphErrors
        """
        x, x_errors = input_TGraphErrors.GetX(), input_TGraphErrors.GetEX()
        y, y_errors = input_TGraphErrors.GetY(), input_TGraphErrors.GetEY()
        self.x_values, self.x_error_pairs, self.y_values, self.y_error_pairs = [], [], [], []
        for ii in range(input_TGraphErrors.GetN()):
            self.x_values.append(x[ii])
            self.x_error_pairs.append([x_errors[ii]] * 2)
            self.y_values.append(y[ii])
            self.y_error_pairs.append([y_errors[ii]] * 2)
        self.nPoints = len(self.x_values)

    def construct_from_TGraphAsymmErrors(self, input_TGraphAsymmErrors):
        """Read TGraphErrors into x, y dimensions.

        :param input_TGraphAsymmErrors: input TGraphAsymmErrors
        :type input_TGraphAsymmErrors: ROOT.TGraphAsymmErrors
        """
        x, x_errors_low, x_errors_high = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEXlow(), input_TGraphAsymmErrors.GetEXhigh()
        y, y_errors_low, y_errors_high = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEYlow(), input_TGraphAsymmErrors.GetEYhigh()
        self.x_values, self.x_error_pairs, self.y_values, self.y_error_pairs = [], [], [], []
        for ii in range(input_TGraphAsymmErrors.GetN()):
            self.x_values.append(x[ii] + (x_errors_high[ii] - x_errors_low[ii]) / 2.0)
            self.x_error_pairs.append([(x_errors_high[ii] + x_errors_low[ii]) / 2.0] * 2)
            self.y_values.append(y[ii])
            self.y_error_pairs.append([y_errors_low[ii], y_errors_high[ii]])
        self.nPoints = len(self.x_values)

    def do_zero_removal(self):
        """Remove points with zero y-value."""
        def filter_by_list(input_list, filter_list):
            """Filter items according to a boolean filter.

            :param input_list: list to filter
            :type input_list: list
            :param filter_list: filter to apply. Booleans indicate whether each element should be retained.
            :type filter_list: list(bool)
            :return: filtered list (subset of the input list)
            :rtype: list
            """
            return [val for idx, val in zip(filter_list, input_list) if idx]
        indices_to_keep = [_y != 0 for _y in self.y_values]
        self.x_values = filter_by_list(self.x_values, indices_to_keep)
        self.x_error_pairs = filter_by_list(self.x_error_pairs, indices_to_keep)
        self.y_values = filter_by_list(self.y_values, indices_to_keep)
        self.y_error_pairs = filter_by_list(self.y_error_pairs, indices_to_keep)
        self.nPoints = len(self.x_values)
