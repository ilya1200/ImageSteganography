import logging
from omegaconf import OmegaConf


def get_console_logger(logger_name: str, log_level=logging.DEBUG) -> logging.Logger:
    """
    Return a logger that outputs log messages to the console.

    :param logger_name: The name of the logger.
    :param log_level: The logging level of the logger. Default is DEBUG.
    :return: The logger object.
    """
    cfg = OmegaConf.load("config/config.yaml")

    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # create console handler and set level to log_level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # create formatter
    formatter = logging.Formatter(cfg.utils.logging_format)

    # add formatter to console handler
    console_handler.setFormatter(formatter)

    # add console handler to logger
    logger.addHandler(console_handler)

    return logger


l = get_console_logger(__name__)
l.debug("ssfaf")
