from base_canvas import BaseCanvas


class Simple(BaseCanvas):
    '''Simple canvas with standard ATLAS setup'''

    def __init__(self, n_pixels=(600, 600), axis_dimensions=[0.15, 0.1, 0.8, 0.85], **kwargs):
        super(Simple, self).__init__(n_pixels, **kwargs)
        self.plots['main'] = self.figure.add_axes(axis_dimensions)

    def add_plottable(self, plottable, axes='main', **kwargs):
        super(Simple, self).add_plottable(plottable, axes, **kwargs)
        if 'x' not in self.axis_ranges:
            self.set_axis_range('x', self.plots[axes].get_xlim())
        if 'y' not in self.axis_ranges:
            self.set_axis_range('y', self.plots[axes].get_ylim())

    def apply_plot_formatting(self):
        super(Simple, self).apply_plot_formatting()
        if 'x' in self.axis_ranges:
            self.plots['main'].set_xlim(self.axis_ranges['x'])
        if 'y' in self.axis_ranges:
            self.plots['main'].set_ylim(self.axis_ranges['y'])

    # Provide defaults for inherited methods
    def draw_ATLAS_text(self, x, y, axes='main', **kwargs):
        super(Simple, self).draw_ATLAS_text(x, y, axes=axes, **kwargs)

    def draw_legend(self, x, y, axes='main', **kwargs):
        super(Simple, self).draw_legend(x, y, axes=axes, **kwargs)

    def draw_luminosity_text(self, x, y, luminosity_value, axes='main', **kwargs):
        super(Simple, self).draw_luminosity_text(x, y, luminosity_value, axes=axes, **kwargs)

    def draw_text(self, x, y, extra_value, axes='main', **kwargs):
        super(Simple, self).draw_text(x, y, extra_value, axes=axes, **kwargs)

    # Axis labels
    def get_axis_label(self, axis_name):
        if axis_name == 'x':
            return self.plots['main'].get_xlabel()
        elif axis_name == 'y':
            return self.plots['main'].get_ylabel()
        else:
            raise ValueError('axis {0} not recognised by {1}'.format(axis_name, type(self)))

    def set_axis_label(self, axis_name, axis_label):
        if axis_name == 'x':
            self.plots['main'].set_xlabel(axis_label, size=16, position=(1.0, 0.0), va='top', ha='right')
        elif axis_name == 'y':
            self.plots['main'].set_ylabel(axis_label, size=16)
            self.plots['main'].yaxis.get_label().set_ha('right')
            self.plots['main'].yaxis.set_label_coords(-0.13, 1.0)
        else:
            raise ValueError('axis {0} not recognised by {1}'.format(axis_name, type(self)))

    def set_axis_labels(self, x_axis_label, y_axis_label):
        self.set_axis_label('x', x_axis_label)
        self.set_axis_label('y', y_axis_label)

    # Axis ranges
    def set_axis_range(self, axis_name, axis_range):
        if axis_name == 'x':
            self.axis_ranges['x'] = axis_range
        elif axis_name == 'y':
            self.axis_ranges['y'] = axis_range
        else:
            raise ValueError('axis {0} not recognised by {1}'.format(axis_name, type(self)))

    def set_axis_ranges(self, x_axis_range, y_axis_range):
        self.set_axis_range('x', x_axis_range)
        self.set_axis_range('y', y_axis_range)

    # Plot title
    def set_title(self, title):
        self.plots['main'].set_title(title)
