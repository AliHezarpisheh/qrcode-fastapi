"""Define QR code related operations for FastAPI application."""

from fastapi import APIRouter, Response

from .qrcode_generator import QRCode

qrcode_router = APIRouter(prefix="/qrcode", tags=["QR Codes"])


@qrcode_router.post(
    "/",
    status_code=201,
    responses={201: {"content": {"image/png": {}}}},
    response_class=Response,
)
def create_qrcode(content: str) -> Response:
    """
    Create a QR code image from the provided content.

    Parameters
    ----------
    content : str
        The content to be encoded into the QR code.

    Returns
    -------
    Response
        A FastAPI Response object containing the generated QR code image as PNG.
    """
    qr_code = QRCode(content)
    qr_byte_stream = qr_code.make()
    return Response(content=qr_byte_stream.getvalue(), media_type="image/png")
