import logging
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

LOG_FORMAT = logging.Formatter("%(name)s / %(funcName)s / %(levelname)s: %(message)s")
LOG_LEVEL = logging.DEBUG
