import logging
import numpy as np
from scipy import interpolate

logger = logging.getLogger("mATLASplotlib.plotters")

class Line(object):
    """Plot as points in the x-y plane"""
    def __init__(self, plot_style):
        self.plot_style = plot_style

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        plot_args = {}
        plot_args["color"] = kwargs.pop("colour", "black")        # Default colour: black
        plot_args["label"] = kwargs.pop("label", None)            # Default label: None
        plot_args["linewidth"] = kwargs.pop("linewidth", 2)       # Default linewidth: 2
        plot_args["marker"] = kwargs.pop("marker", None)           # Default marker: dot

        if "stepped" in self.plot_style:
            axes.plot(dataset.x_all_bin_edges, dataset.y_at_x_bin_edges, drawstyle="stepped", **plot_args)
	
	if "join centres" in self.plot_style:
            axes.plot(dataset.x_points, dataset.y_points, **plot_args)

        if "smooth" in self.plot_style:
            print "x", dataset.x_all_bin_edges, len(dataset.x_all_bin_edges)
            print "y", dataset.y_at_x_bin_edges, len(dataset.y_at_x_bin_edges)


            # s=numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
            #   51     #print(len(s))
            #   52     if window == 'flat': #moving average
            #   53         w=numpy.ones(window_len,'d')
            #   54     else:
            #   55         w=eval('numpy.'+window+'(window_len)')
            #   56
            #   57     y=numpy.convolve(w/w.sum(),s,mode='valid')
            #   58     return y

            spline = interpolate.interp1d(dataset.x_all_bin_edges, dataset.y_at_x_bin_edges)#, kind="cubic")
            # # dataset.x_all_bin_edges = np.arange(0, 2*np.pi+np.pi/4, 2*np.pi/8)
            # dataset.y_at_x_bin_edges = np.sin(dataset.x_all_bin_edges)
            # spline = interpolate.UnivariateSpline(dataset.x_all_bin_edges, dataset.y_at_x_bin_edges)
            # # spline = interpolate.splrep(dataset.x_all_bin_edges, dataset.y_at_x_bin_edges, s=0)
            x_spline = np.linspace(min(dataset.x_all_bin_edges), max(dataset.x_all_bin_edges), 1*len(dataset.x_all_bin_edges))
            # print "x_spline", x_spline, len(x_spline)
            # # y_spline = interpolate.splev(x_spline, spline, der=0)
            y_spline = spline(x_spline)
            # print "y_spline", y_spline, len(y_spline)
            axes.plot(x_spline, y_spline, **plot_args)

    #def _smooth(x, window_size=3):
