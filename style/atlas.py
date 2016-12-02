import logging
import matplotlib
import rootpy.plotting


def set_atlas():
    """
    Definition:
    -----------
            Set the plotting style to ATLAS-style and then point this function to
            "None" so that it can only be called once. Should be called on import.

    Args:
    -----------
            None
    """
    logger = logging.getLogger("mATLASplotlib.style")
    logger.info("Setting ATLAS style")

    # Start from rootpy ATLAS style
    rootpy.plotting.set_style("ATLAS", mpl=True)
    # Set general options
    matplotlib.use('PDF')
    matplotlib.rcParams["figure.figsize"] = (6, 6)
    # Force Helvetica in mathmode
    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["font.sans-serif"] = "Helvetica"
    matplotlib.rcParams["mathtext.fontset"] = "custom"
    # matplotlib.rcParams["mathtext.default"] = "regular"
    matplotlib.rcParams["mathtext.default"] = "sf"
    # matplotlib.rcParams['mathtext.cal'] = "cursive"
    matplotlib.rcParams["mathtext.bf"] = "sans:bold"
    matplotlib.rcParams["mathtext.it"] = "sans:italic"
    matplotlib.rcParams["mathtext.rm"] = "serif"
    # matplotlib.rcParams['mathtext.sf'] = "sans"
    matplotlib.rcParams["mathtext.tt"] = "sans"
    # matplotlib.rcParams['mathtext.fallback_to_cm'] = True
    set_atlas.func_code = (lambda: None).func_code
