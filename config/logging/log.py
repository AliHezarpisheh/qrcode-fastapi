"""Provides functions for setting up logging configurations based on a TOML file.

It includes functionality for reading the TOML configuration, validating and creating
directories for log files, and configuring the logging system using the provided
configuration.

Internal Dependencies:
    - .utils.funcs.read_toml: A function to read a TOML file and return its content.
    - .utils.funcs.validate_and_create_dirs: A function to validate and create
      directories for log files specified in the logging configuration.

Usage Example:
    from log_setup import setup_logging
    setup_logging(logging_config_path=Path("logging_.toml"))
"""

import logging.config
import logging.handlers
from pathlib import Path

from ..helper.funcs import read_toml, validate_and_create_dirs


def setup_logging(logging_config_path: Path) -> None:
    """Set up the logging configurations."""
    logging_config = read_toml(path=logging_config_path)
    # Check or Create the dirs of log files specified in the config.
    handlers = logging_config.get("handlers", None)
    validate_and_create_dirs(handlers=handlers)
    logging.config.dictConfig(logging_config)
