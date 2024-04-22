"""Test module for QRCode class."""

import io
from typing import Any

import pytest
from PIL import Image

from src.qrcode_generator import QRCode


@pytest.mark.smoke
@pytest.mark.parametrize(
    "content",
    [
        "1234567890",
        "Testing QR codes",
        "Lorem ipsum dolor sit amet",
        "https://www.example.com",
        "42 is the answer",
        "Segno QR code generator",
    ],
)
def test_qr_code_make(content: str) -> None:
    """
    Test generating a QR code image.

    Parameters
    ----------
    content : str
        The content to encode in the QR code.

    Returns
    -------
    None
    """
    qr_code = QRCode(content)

    qr_bytes = qr_code.make()
    assert isinstance(qr_bytes, io.BytesIO)

    img = Image.open(qr_bytes)
    assert img.format == "PNG"


@pytest.mark.exception
@pytest.mark.parametrize(
    "content",
    [
        None,
        12,
        True,
        11.12,
        ["content"],
        {"key": "content"},
    ],
)
def test_invalid_qr_code_content_type(content: Any) -> None:
    """
    Test invalid content types for QR code generation.

    Parameters
    ----------
    content : Any
        The content to encode in the QR code.

    Returns
    -------
    None
    """
    with pytest.raises(AssertionError, match="content should be of type `str`"):
        QRCode(content)


@pytest.mark.exception
@pytest.mark.parametrize(
    "content",
    [
        "Hello, World!",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Special characters: @#&()[]",
        "https://www.example.com/path/to/page?query=string",
        "ASCII art: \n _\n( )\n( (_/\\_)\n \n",
        "Math equation: ∫(x^2 + 2x + 1) dx from 0 to 1",
        "Emoji 😀🚀🎉",
        "Café au lait",
        "Unicode characters: 𝒳² + 𝒴² = 𝒵²",
    ],
)
def test_invalid_qr_code_content_characters(content: str) -> None:
    """
    Test invalid characters in QR code content.

    Parameters
    ----------
    content : str
        The content to encode in the QR code.

    Returns
    -------
    None
    """
    with pytest.raises(ValueError, match="content contains invalid characters"):
        QRCode(content)


@pytest.mark.exception
def test_empty_str_qr_code_content() -> None:
    """
    Test generating a QR code with empty string content.

    Returns
    -------
    None
    """
    empty_string = ""
    with pytest.raises(ValueError, match="content cannot be an empty string"):
        QRCode(empty_string)


@pytest.mark.exception
@pytest.mark.parametrize("content_length", [301, 400, 500])
def test_max_length_qr_code_content(content_length: int) -> None:
    """
    Test generating a QR code with content exceeding maximum length.

    Parameters
    ----------
    content_length : int
        The length of the content to generate.

    Returns
    -------
    None
    """
    invalid_content = "a" * content_length
    with pytest.raises(ValueError, match="content length should not exceed"):
        QRCode(invalid_content)
