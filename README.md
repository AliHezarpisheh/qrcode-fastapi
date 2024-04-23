# FastAPI QR Code Generator

This FastAPI project allows you to dynamically generate QR codes by sending a POST request with the desired content.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AliHezarpisheh/qrcode-fastapi.git
    ```

2. Navigate to the project directory:

    ```bash
    cd qrcode-fastapi/
    ```

3. Install dependencies using [Poetry](https://python-poetry.org/) or [pip](https://pip.pypa.io/en/stable/):

    Using Poetry:
    ```bash
    poetry install
    ```

    Using pip (activate virtual environment if necessary):
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the FastAPI server using [Uvicorn](https://www.uvicorn.org/):

    ```bash
    uvicorn main:app
    ```

2. Once the server is running, you can make a POST request to `/qrcode` with the content parameter in the query string. For example:

    ```bash
    curl -X POST "http://localhost:8000/qrcode?content=https://example.com"
    ```

    This will generate a QR code with the content "https://example.com" and return the image.
