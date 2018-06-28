"""mATLASplotlib is a package to produce plots with matplotlib which meet the ATLAS style guidelines."""

import logging
import sys
import matplotlib_wrapper
import canvases

__all__ = ["canvases", "matplotlib_wrapper"]

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
