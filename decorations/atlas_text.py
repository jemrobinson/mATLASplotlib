class ATLAS_text(object):
    def __init__(self, plot_type=None):
        self.plot_type = plot_type
        self.default_fontsize = 17

    def draw(self, x, y, axes, ha, va, fontsize):
        transform = axes.transAxes
        fontsize = [fontsize, self.default_fontsize][fontsize==None]
        if self.plot_type is None:
            axes.text(x, y, "ATLAS", style="italic", fontsize=fontsize, fontweight="bold", ha=ha, va=va, transform=transform)
        else:
            # Plot invisible text to get bounding box
            style_args = {"fontsize":fontsize, "ha":ha, "va":va, "transform":transform}
            if ha == "left":  # draw ATLAS first and then align other text to it
                invisible_ATLAS_text = axes.text(x, y, "ATLASI", alpha=0, style="italic", fontweight="bold", **style_args)
                bounding_box = invisible_ATLAS_text.get_window_extent(renderer=self.__get_renderer(axes)).transformed(transform.inverted())
                visible_ATLAS_text = axes.text(x, y, "ATLAS", style="italic", fontweight="bold", **style_args)
                axes.text(bounding_box.max[0], y, self.plot_type, **style_args)
            elif ha == "right":  # draw other text first and then align ATLAS to it
                visible_normal_text = axes.text(x, y, " {}".format(self.plot_type), **style_args)
                bounding_box = visible_normal_text.get_window_extent(renderer=self.__get_renderer(axes)).transformed(transform.inverted())
                axes.text(bounding_box.min[0], y, "ATLAS", style="italic", fontweight="bold", **style_args)
            else:
                raise NotImplementedError("Alignment {} not recognised!".format(ha))

    def __get_renderer(self, axes):
        # axes.get_figure() was self.figure
        if hasattr(axes.get_figure().canvas, "get_renderer"):
            # Some backends, such as TkAgg, have the get_renderer method, which makes this easy.
            renderer = axes.get_figure().canvas.get_renderer()
        else:
            # Other backends do not have the get_renderer method, so we have a work
            # around to find the renderer.  Print the figure to a temporary file
            # object, and then grab the renderer that was used.
            import io
            axes.get_figure().canvas.print_pdf(io.BytesIO())
            renderer = axes.get_figure()._cachedRenderer
        return renderer
