"""Module containing test functions for QR code generation endpoint."""

from unittest import mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "content", ["QR123", "Generate QR code.", "007", "https://example.com", "Hello QR"]
)
def test_read_qr_code(content: str) -> None:
    """
    Test the QR code generation endpoint with valid content.

    Parameters
    ----------
    content : str
        The content to be encoded in the QR code.
    """
    response = client.post("/qrcode", params={"content": content})
    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert response.headers.get("content-type", None) == "image/png"


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
def test_read_qr_code_invalid_content_characters(content: str) -> None:
    """
    Test the QR code generation endpoint with invalid content.

    Parameters
    ----------
    content : str
        The content to be encoded in the QR code.
    """
    response = client.post("/qrcode", params={"content": content})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    assert response.json() == {"detail": "content contains invalid characters"}


def test_read_qr_code_empty_content_string() -> None:
    """Test the QR code generation endpoint with empty content string."""
    response = client.post("/qrcode", params={"content": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    assert response.json() == {"detail": "content cannot be an empty string"}


def test_read_qr_code_long_content() -> None:
    """Test the QR code generation endpoint with content exceeding maximum length."""
    long_content = "a" * 301
    response = client.post("/qrcode", params={"content": long_content})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    assert response.json() == {
        "detail": "content length should not exceed 300 characters"
    }


def test_read_qr_code_unexpected_error() -> None:
    """Test QR code generation endpoint with unexpected error during generation."""
    with mock.patch("src.routers.QRCode") as mocked_qrcode:
        mocked_qrcode_instance = mock.MagicMock()
        mocked_qrcode_instance.make.side_effect = Exception("Unknown Error")
        mocked_qrcode.return_value = mocked_qrcode_instance

        response = client.post("/qrcode", params={"content": "https://example.com"})
        assert (
            response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        ), response.text
        assert response.json() == {
            "detail": "Internal server error occurred while generating QR code. Please "
            "try again or contact administration."
        }
