"""This module provides the ``draw_ATLAS_text`` convenience function."""


def draw_ATLAS_text(axes, loc, align, plot_type=None, fontsize=17):
    """Draw ATLAS text on axes.

    :param axes: axes to plot on
    :type axes: str
    :param loc: x and y position of text
    :type loc: tuple(float)
    :param align: horizontal and vertical alignment of text
    :type align: tuple(str)
    :param plot_type: Internal/Preliminary/Work-In-Progress etc.
    :type plot_type: str
    :param fontsize: fontsize of legend contents
    :type fontsize: float
    """
    x, y = loc
    ha, va = align
    transform = axes.transAxes
    if plot_type is None:
        axes.text(x, y, "ATLAS", style="italic",
                  fontsize=fontsize, fontweight="bold",
                  ha=ha, va=va, transform=transform)
    else:
        # Plot invisible text to get bounding box
        style_args = {"fontsize": fontsize, "ha": ha, "va": va, "transform": transform}
        if ha == "left":  # draw ATLAS first and then align other text to it
            invisible_ATLAS_text = axes.text(x, y, "ATLASI", alpha=0, style="italic", fontweight="bold", **style_args)
            bounding_box = invisible_ATLAS_text.get_window_extent(renderer=__get_renderer(axes)).transformed(transform.inverted())
            axes.text(x, y, "ATLAS", style="italic", fontweight="bold", **style_args)
            axes.text(bounding_box.max[0], y, plot_type, **style_args)
        elif ha == "right":  # draw other text first and then align ATLAS to it
            visible_normal_text = axes.text(x, y, " {}".format(plot_type), **style_args)
            bounding_box = visible_normal_text.get_window_extent(renderer=__get_renderer(axes)).transformed(transform.inverted())
            axes.text(bounding_box.min[0], y, "ATLAS", style="italic", fontweight="bold", **style_args)
        else:
            raise NotImplementedError("Alignment {} not recognised!".format(ha))


def __get_renderer(axes):
    """Retrieve appropriate renderer.

    :param axes: matplotlib axes for which we want the renderer
    :type axes: matplotlib.axes.Axes
    """
    # pylint: disable=protected-access
    # For backends that do not support get_renderer() we have to use this workaround
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
