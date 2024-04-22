"""A module for generating QR codes."""

import io

import segno


class QRCode:
    """A class representing a QR code generator."""

    CONTENT_MAX_LENGTH = 300
    CONTENT_VALID_CHARACHTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

    def __init__(self, content: str) -> None:
        """
        Initialize a QRCode instance.

        Parameters
        ----------
        content : str
            The content for which the QR code will be generated.
        """
        self.content = content

    @property
    def content(self) -> str:
        """
        Get the content of the QR code.

        Returns
        -------
        str
            The content for which the QR code will be generated.
        """
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        """
        Set the content of the QR code.

        Parameters
        ----------
        value : str
            The content for which the QR code will be generated.

        Raises
        ------
        ValueError
            If the content is an empty string or exceeds the maximum length.
        TypeError
            If the content contains invalid characters.
        """
        assert isinstance(value, str), "content should be of type `str`"

        if not value:
            raise ValueError("content cannot be an empty string")

        if len(value) > self.CONTENT_MAX_LENGTH:
            raise ValueError(
                f"content length should not exceed {self.CONTENT_MAX_LENGTH} characters"
            )

        if not set(value.upper()).issubset(set(self.CONTENT_VALID_CHARACHTERS)):
            raise ValueError("content contains invalid characters")

        self._content = value

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
