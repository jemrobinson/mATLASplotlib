"""This module provides the ``Legend`` class."""
import matplotlib


class Legend(object):
    """Class for controlling plot legends."""

    def __init__(self):
        """Initialise legend ordering and default fontsize."""
        self.legend_order = []
        self.sort_overrides = {}
        self.default_fontsize = 16

    def add_dataset(self, label, is_stack=False, sort_as=None):
        """Add a dataset to the legend.

        :param label: label that will appear in the legend
        :type label: str
        :param is_stack: if this is a stack plot it needs to be stored in reverse order
        :type is_stack: bool
        :param sort_as: override the default first-in-first-out sorting, and sort using this text instead
        :type sort_as: str
        """
        legend_text = ("stack:" if is_stack else "") + (label if label is not None else "")
        if legend_text is not None and legend_text != "" and legend_text not in self.legend_order:
            self.legend_order.append(legend_text)
        if sort_as is not None:
            self.sort_overrides[sort_as] = legend_text

    def plot(self, x, y, axes, anchor_to, fontsize, use_axes=False):
        """Plot the legend at (x, y) on the chosen axes.

        :param x: x-position of legend
        :type x: float
        :param y: y-position of legend
        :type y: float
        :param axes: axes to plot on
        :type axes: str
        :param anchor_to: which corner to anchor the (x, y) to
        :type anchor_to: str
        :param fontsize: fontsize of legend contents
        :type fontsize: float
        :param use_axes: get handles and labels from all axes in list
        :type use_axes: list[matplotlib.axes.Axes]
        """
        transform = axes.transAxes
        if use_axes:
            handles, labels = zip(*[self.__get_legend_handles_labels(subplot) for subplot in use_axes])
            handles, labels = sum(handles, []), sum(labels, [])
        else:
            handles, labels = self.__get_legend_handles_labels(axes)
        _legend = axes.legend(handles, labels, numpoints=1, loc=anchor_to, bbox_to_anchor=(x, y),
                              bbox_transform=transform, borderpad=0, borderaxespad=0, columnspacing=0)
        _legend.get_frame().set_linewidth(0)
        _legend.get_frame().set_alpha(0.0)
        fontsize = self.default_fontsize if fontsize is None else fontsize
        matplotlib.pyplot.setp(_legend.get_texts(), fontsize=fontsize)
        for text in _legend.get_texts():
            text.set_va("bottom")

    def __get_legend_handles_labels(self, axes):
        """Get legend handles and labels for the current axes.

        Start from the matplotlib get_legend_handles_labels() function.
        Add proxy artists as appropriate (for multi-component handles).
        Reverse the order for stacks (so that the highest one has the highest label).
        Apply any provided label-sorting overrides.

        :param axes: axes to plot on
        :type axes: str
        """
        # Remove duplicates
        handles, labels = [], []
        for handle, label in zip(*axes.get_legend_handles_labels()):
            if label not in labels:
                labels.append(label)
                if isinstance(handle, matplotlib.patches.Ellipse):
                    handles.append((matplotlib.patches.Rectangle((0, 0), 0, 0, facecolor=handle.properties()["facecolor"]),
                                    matplotlib.lines.Line2D([0], [0], color=handle.properties()["edgecolor"], linestyle=handle.properties()["linestyle"])))
                else:
                    handles.append(handle)
        # Pre-sort legend order for stacks, which need reversing
        stack_labels = list(reversed([label.replace("stack:", "") for label in self.legend_order if "stack:" in label]))
        stack_indices = [idx for idx, label in enumerate(self.legend_order) if "stack:" in label]
        for idx, label in zip(stack_indices, stack_labels):
            self.legend_order[idx] = label
        # Sort list of labels
        sorted_labels, sorted_handles = [], []
        for label in [l for l in self.legend_order if l in labels]:
            idx = labels.index(label)
            sorted_handles.append(handles.pop(idx))
            sorted_labels.append(labels.pop(idx))
        # Append non-mATLASplotlib labels
        for handle, label in zip(handles, labels):
            sorted_handles.append(handle)
            sorted_labels.append(label)
        # Apply sort overrides
        for override in sorted(self.sort_overrides.keys(), reverse=True):
            idx = [i for i, x in enumerate(sorted_labels) if x == self.sort_overrides[override]]
            if idx:
                sorted_labels.insert(0, sorted_labels.pop(idx[0]))
                sorted_handles.insert(0, sorted_handles.pop(idx[0]))
        return sorted_handles, sorted_labels
