import os
from logging import Logger

import cv2
import numpy
import requests
from requests import Response

import my_logger

logger: Logger = my_logger.get_console_logger(__name__)


def get_image_from_slack_url(image_url_in_slack: str) -> numpy.ndarray:
    """

    :param image_url_in_slack: url to image from Slack
    :return: A 3-d array that represents an RGB image
    """
    # Download the file using requests
    response: Response = requests.get(image_url_in_slack,
                                      headers={"Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}"})
    response.raise_for_status()

    # Create a NumPy array from the byte string
    img_array: numpy.ndarray = numpy.frombuffer(response.content, dtype=numpy.uint8)

    # Reshape the array to the desired dimensions
    image: numpy.ndarray = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Convert the color format from BGR to RGB
    image: numpy.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image
