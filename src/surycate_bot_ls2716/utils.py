import logging


# Define a function to get a logger
def get_logger(name: str) -> logging.Logger:
    """Return a logger with the given name."""
    # Create a logger
    logger = logging.getLogger(name)
    # Set the logging level
    logger.setLevel(logging.DEBUG)
    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s"
    )
    # Create a stream handler
    stream_handler = logging.StreamHandler()
    # Set the formatter
    stream_handler.setFormatter(formatter)
    # Add the stream handler to the logger
    logger.addHandler(stream_handler)
    # Return the logger
    return logger
