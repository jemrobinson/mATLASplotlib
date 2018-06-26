import logging
import sys
import matplotlib

# Set default matplotlib backend
matplotlib.use("pdf")

import canvases

__all__ = ["canvases"]

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

