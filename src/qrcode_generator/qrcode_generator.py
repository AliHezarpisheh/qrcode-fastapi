"""A module for generating QR codes."""

import io

import segno


class QRCode:
    """A class representing a QR code generator."""

    def __init__(self, content: str) -> None:
        """
        Initialize a QRCode instance.

        Parameters
        ----------
        content : str
            The content for which the QR code will be generated.
        """
        self.content = content

    def make(self, scale: int = 10, border: int = 1) -> io.BytesIO:
        """
        Generate a QR code.

        Parameters
        ----------
        scale : int, optional
            The size of each module in pixels. Default is 10.
        border : int, optional
            The size of the white border around the QR code in modules. Default is 1.

        Returns
        -------
        io.BytesIO
            A byte stream containing the PNG representation of the QR code.
        """
        qr = segno.make(content=self.content)

        byte_stream = io.BytesIO()
        qr.save(byte_stream, kind="png", scale=scale, border=border)

        # Reset the stream pointer to the beginning before reading the data.
        byte_stream.seek(0)
        return byte_stream
