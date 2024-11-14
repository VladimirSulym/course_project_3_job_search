import logging
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

LOG_FORMAT = logging.Formatter("%(name)s / %(funcName)s / %(levelname)s: %(message)s")
LOG_LEVEL = logging.CRITICAL

FAVORITES_EMPLOYERS = [
    "10702342",
    "9000954",
    "5153079",
    "3268375",
    "5438665",
    "11587345",
    "657041",
    "9463756",
    "11568862",
    "3506633",
]
