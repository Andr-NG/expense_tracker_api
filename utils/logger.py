import logging

# Create a logger with a name specific to your project
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a handler and a formatter (console/file handler as needed)
handler = logging.FileHandler(filename="my_logs.log", mode="a")
formatter = logging.Formatter(
    fmt="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]",
    datefmt="%d/%m/%Y %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Avoid duplicating logs
logger.propagate = False