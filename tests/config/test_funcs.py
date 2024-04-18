"""Test cases and fixtures for the utility functions related to TOML file handling."""

import tempfile
from pathlib import Path
from typing import Any, Generator

import pytest

from config.helper.funcs import read_toml, validate_and_create_dirs


@pytest.fixture
def valid_sample_toml_content() -> str:
    """
    Fixture: Providing a sample TOML content as a string.

    Returns
    -------
    str
        Sample TOML content.
    """
    return 'key = "value"'


@pytest.fixture
def invalid_sample_toml_content() -> str:
    """
    Fixture: Providing a sample TOML content as a string.

    Returns
    -------
    str
        Sample TOML content.
    """
    return "invalid data for toml files."


@pytest.fixture
def valid_temp_toml_file_path(
    valid_sample_toml_content: str,
) -> Generator[Path, None, None]:
    """
    Fixture: Creating a temporary TOML file with the sample content and yielding Path.

    Parameters
    ----------
    valid_sample_toml_content : str
        Sample TOML content.

    Yields
    ------
    Generator[Path, None, None]
        Temporary TOML file path.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".toml") as file:
        file.write(valid_sample_toml_content.encode())
        file_path = Path(file.name)
    yield file_path
    file_path.unlink()


@pytest.fixture
def invalid_temp_toml_file_path(
    invalid_sample_toml_content: str,
) -> Generator[Path, None, None]:
    """
    Fixture: Creating a temporary TOML file with the sample content and yielding Path.

    Parameters
    ----------
    valid_sample_toml_content : str
        Sample TOML content.

    Yields
    ------
    Generator[Path, None, None]
        Temporary TOML file path.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".toml") as file:
        file.write(invalid_sample_toml_content.encode())
        file_path = Path(file.name)
    yield file_path
    file_path.unlink()


@pytest.fixture
def sample_handlers(tmp_path: Path) -> dict[str, Any]:
    """Fixture returning a sample dictionary of handlers with associated filenames."""
    handlers = {
        "handler1": {"filename": tmp_path / "path1/log.txt"},
        "handler2": {"filename": tmp_path / "path2/log.txt"},
        "handler3": {},
        "handler4": {"filename": tmp_path / "path1/log.txt"},
    }
    return handlers


def test_read_valid_toml_file(valid_temp_toml_file_path: Path) -> None:
    """
    Test case for checking if the read_toml function reads a valid TOML file correctly.

    Parameters
    ----------
    valid_temp_toml_file_path : Path
        Path to the temporary TOML file.
    """
    actual = read_toml(path=valid_temp_toml_file_path)
    expected = {"key": "value"}
    assert actual == expected, f"expected `{expected}` but got `{actual}`"


def test_read_invalid_toml_file(invalid_temp_toml_file_path: Path) -> None:
    """Test for read_toml handling syntax errors in specified TOML file."""
    with pytest.raises(SystemExit):
        read_toml(path=invalid_temp_toml_file_path)


def test_read_toml_file_not_found() -> None:
    """Test for read_toml handling case where specified TOML file is not found."""
    with pytest.raises(SystemExit):
        read_toml(Path("nonexistence_file.toml"))


def test_validate_and_create_dirs_with_path_manager(
    sample_handlers: dict[str, dict[str, str]],
) -> None:
    """Test the validate_and_create_dirs function with PathManager."""
    paths = validate_and_create_dirs(sample_handlers)
    for path in paths:
        assert path.parent.exists(), (
            "Expect that the parent of the paths to "
            "be created, but they are not created!"
        )
