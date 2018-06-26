"""This module provides the Legend class."""
import matplotlib


class Legend(object):
    """Document here."""

    def __init__(self):
        """Constructor."""
        self.legend_order = []
        self.sort_overrides = {}
        self.default_fontsize = 16

    def add_dataset(self, label, visible_label=None, is_stack=False, sort_as=None):
        """Document here."""
        label = [label, ""][label is None] + ["@{0}".format(visible_label), ""][visible_label is None]
        legend_text = ["", "stack:"][is_stack] + label
        if legend_text is not None and legend_text != "" and legend_text not in self.legend_order:
            self.legend_order.append(legend_text)
        if sort_as is not None:
            self.sort_overrides[sort_as] = legend_text

    def draw(self, x, y, axes, anchor_to, fontsize):
        """Draw the legend at (x, y) on the chosen axes."""
        transform = axes.transAxes
        handles, labels = self.__get_legend_handles_labels(axes)
        _legend = axes.legend(handles, labels, numpoints=1, loc=anchor_to, bbox_to_anchor=(x, y), bbox_transform=transform, borderpad=0, borderaxespad=0, columnspacing=0)
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
           Apply any provided label-sorting overrides."""
        # Remove duplicates
        handles, labels, seen = [], [], set()
        old_handles, old_labels = axes.get_legend_handles_labels()
        for handle, label in zip(old_handles, old_labels):
            visible_label = label if label.find("@") == -1 else label.split("@")[1]
            if visible_label not in seen:
                seen.add(visible_label)
                labels.append(visible_label)
                if isinstance(handle, matplotlib.patches.Polygon):
                    proxy_artist = matplotlib.pyplot.Line2D([0], [0], color=handle.properties()["edgecolor"], linestyle=handle.properties()["linestyle"])
                    handles.append(proxy_artist)
                elif isinstance(handle, matplotlib.patches.Ellipse):
                    line = matplotlib.pyplot.Line2D([0], [0], color=handle.properties()["edgecolor"], linestyle=handle.properties()["linestyle"])
                    rectangle = matplotlib.pyplot.Rectangle((0, 0), 0, 0, facecolor=handle.properties()["facecolor"])
                    handles.append((rectangle, line))
                else:
                    handles.append(handle)
        # Pre-sort legend order for stacks, which need reversing
        stack_labels = list(reversed([label.replace("stack:", "") for label in self.legend_order if "stack:" in label]))
        stack_indices = [idx for idx, label in enumerate(self.legend_order) if "stack:" in label]
        for idx, label in zip(stack_indices, stack_labels):
            self.legend_order[idx] = label
        # Sort list of labels
        sorted_labels, sorted_handles = [], []
        for label in self.legend_order:
            idx_label = [i for i, x in enumerate(labels) if x == label]
            if idx_label:
                sorted_labels.append(labels.pop(idx_label[0]))
                sorted_handles.append(handles.pop(idx_label[0]))
        # Append non-mATLASplotlib labels
        for label, handle in zip(labels, handles):
            sorted_labels.append(label)
            sorted_handles.append(handle)
        # Apply sort overrides
        for override in sorted(self.sort_overrides.keys(), reverse=True):
            idx_label = [i for i, x in enumerate(sorted_labels) if x == self.sort_overrides[override]]
            if idx_label:
                sorted_labels.insert(0, sorted_labels.pop(idx_label[0]))
                sorted_handles.insert(0, sorted_handles.pop(idx_label[0]))
        return sorted_handles, sorted_labels
