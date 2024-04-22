"""Define QR code related operations for FastAPI application."""

import logging

from fastapi import APIRouter, HTTPException, Response, status

from .qrcode_generator import QRCode

logger = logging.getLogger(__name__)

qrcode_router = APIRouter(prefix="/qrcode", tags=["QR Codes"])


@qrcode_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={201: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def create_qrcode(content: str) -> Response:
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
    logger.debug("Received request to generate QR code with content: %s", content)

    try:
        qr_code = QRCode(content)
    except ValueError as error:
        logger.error("Invalid content received %s", content, exc_info=True)
        raise HTTPException(status_code=400, detail=str(error))

    try:
        qr_byte_stream = qr_code.make()
    except Exception:
        logger.critical(
            "An unknown error happened while creating QR Code", exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred while generating QR code. "
            "Please try again or contact administration.",
        )

    return Response(
        status_code=201, content=qr_byte_stream.getvalue(), media_type="image/png"
    )
