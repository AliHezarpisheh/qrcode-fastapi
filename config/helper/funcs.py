"""
Configuration Utility Functions.

This module contains utility functions to facilitate the configuration processes in the
project. The functions provided here are designed to assist in various aspects of
configuration, enhancing the flexibility and maintainability of the project settings.

Usage
-----
These utility functions can be imported and used in the main configuration files to
streamline the setup and customization of project settings. Refer to each function's
documentation for specific details on usage and parameters.

Notes
-----
This module is designed for handling specific tasks related to TOML files and directory
creation in a logging setup.
"""

import sys
from pathlib import Path
from typing import Any

import tomlkit


def read_toml(path: Path) -> dict[str, Any]:
    """
    Read a TOML file and return its content as a dictionary.

    Parameters
    ----------
    path : Path
        The path to the TOML file.

    Returns
    -------
    dict
        The parsed content of the TOML file.
    """
    try:
        with path.open(mode="rb") as file:
            content = tomlkit.load(file)
        return content
    except FileNotFoundError:
        print(f"\n\033[91mThis path is unreachable: `{path}`!")
        sys.exit()
    except tomlkit.exceptions.ParseError:
        print(f"\n\033[91mSyntax Error in: `{path}`!")
        sys.exit()


def validate_and_create_dirs(handlers: dict[str, dict[str, Any]]) -> list[Path]:
    """
    Validate the configuration and create directories specified in handlers.

    Parameters
    ----------
    handlers : dict
        Dictionary containing logging handlers.

    Notes
    -----
    The function checks for the existence of directories specified
    in the 'filename' attribute of each handler in the configuration.
    If the directories do not exist, they are created.
    """
    paths = []
    for handler in handlers.values():
        handler_path = handler.get("filename", None)
        if handler_path is not None:
            path = Path(handler_path)
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                paths.append(path)
    return paths
