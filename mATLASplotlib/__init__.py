import logging
import sys
import matplotlib

# Set default matplotlib backend - must be done before local imports
matplotlib.use("pdf")

import canvases
import converters
import decorations
import plotters
import style

__all__ = ["canvases"]

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

