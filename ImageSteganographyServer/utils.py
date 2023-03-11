from logging import Logger

import requests

import my_logger

logger: Logger = my_logger.get_console_logger(__name__)


def down_load_image(path_to_store_image: str, image_url: str) -> str:
    # Send an HTTP GET request to the image URL
    response = requests.get(image_url)

    # Check that the response was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the response (the image data)
        image_data = response.content
        # Write the image data to a file
        with open(path_to_store_image, "wb") as f:
            f.write(image_data)
    else:
        # Print an error message if the response was not successful
        logger.error(f"Error downloading image: {response.status_code}")
        raise Exception(f"Error downloading image: {response.status_code}")
    return path_to_store_image
