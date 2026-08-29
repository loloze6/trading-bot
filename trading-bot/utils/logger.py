import logging
import os


def setup_logger(
    name: str, log_file: str = "logs/bot.log", level: int = logging.INFO, console: bool = False, mode: str = "w"
) -> logging.Logger:
    """
    Setup and return a logger instance with a file handler and console stream handler.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file. Default is 'logs/bot.log'.
        level (int): Logging level, e.g., logging.INFO, logging.DEBUG.
        console (bool): Whether to add a console stream handler.

    Returns:
        logging.Logger: Configured logger instance.
    """
    strategy_refinement = False  # ← Custom parameter to control logging behavior in strategies

    # Ensure the directory for the log file exists; create if it does not
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define log message format including timestamp, severity, logger name, and message
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",  # ← Custom date format
    )

    # Create or get logger instance by name
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Attach your custom parameter directly to the logger object
    logger.strategy_refinement = strategy_refinement

    # Add handlers only if not already configured to avoid duplicate logs
    if not logger.hasHandlers():
        # File handler logs messages to specified file, appending by default
        file_handler = logging.FileHandler(log_file, mode=mode, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Stream handler outputs logs to console
        if console:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

    return logger


# def setup_logger(name, log_file="logs/bot.log", level=logging.INFO):
#     formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

#     handler = logging.FileHandler(log_file, mode='w')
#     handler.setFormatter(formatter)

#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#     logger.addHandler(handler)

#     return logger
