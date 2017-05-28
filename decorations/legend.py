import matplotlib


class Legend(object):
    """Document here."""

    def __init__(self):
        """Constructor."""
        self.legend_order = []
        self.default_fontsize = 16

    def add_dataset(self, label, visible_label=None, is_stack=False):
        """Document here."""
        legend_text = ["", "stack:"][is_stack] + label
        if legend_text is not None and legend_text is not "" and legend_text not in self.legend_order:
            self.legend_order.append(legend_text)

    def draw(self, x, y, axes, anchor_to, fontsize):
        """Document here."""
        if axes is None: axes = self.default_axes
        transform = axes.transAxes
        handles, labels = self.__get_legend_handles_labels(axes)
        _legend = axes.legend(handles, labels, numpoints=1, loc=anchor_to, bbox_to_anchor=(x, y), bbox_transform=transform, borderpad=0, borderaxespad=0, columnspacing=0)
        _legend.get_frame().set_linewidth(0)
        _legend.get_frame().set_alpha(0.0)
        fontsize = [fontsize, self.default_fontsize][fontsize is None]
        matplotlib.pyplot.setp(_legend.get_texts(), fontsize=fontsize)
        [text.set_va("bottom") for text in _legend.get_texts()]

    def __get_legend_handles_labels(self, axes):
        """Document here."""
        # Remove duplicates
        handles, labels, seen = [], [], set()
        old_handles, old_labels = axes.get_legend_handles_labels()
        for handle, label in zip(old_handles, old_labels):
            visible_label = label if label.find("@") == -1 else label.split("@")[1]
            if visible_label not in seen:
                seen.add(visible_label)
                labels.append(visible_label)
                # if isinstance(handle, Polygon):
                if isinstance(handle, matplotlib.patches.Polygon):
                    # import matplotlib.pyplot as pyplot
                    # proxy_artist = pyplot.Line2D([0], [0], color=handle.properties()["edgecolor"], linestyle=handle.properties()["linestyle"])
                    proxy_artist = matplotlib.pyplot.Line2D([0], [0], color=handle.properties()["edgecolor"], linestyle=handle.properties()["linestyle"])
                    handles.append(proxy_artist)
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
            if len(idx_label) > 0:
                sorted_labels.append(labels.pop(idx_label[0]))
                sorted_handles.append(handles.pop(idx_label[0]))
        # Append non-mATLASplotlib labels
        for label, handle in zip(labels, handles):
            sorted_labels.append(label)
            sorted_handles.append(handle)
        return sorted_handles, sorted_labels
