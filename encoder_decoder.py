from logging import Logger

import cv2
import numpy
import numpy as np

import my_logger

logger: Logger = my_logger.get_console_logger(__name__)


class EncoderDecoder:

    @staticmethod
    def _message_to_binary(message) -> str:
        logger.debug(f"Message: {message}")
        binary_message: str = str()
        if type(message) == str:
            binary_message = ''.join([format(ord(i), "08b") for i in message])
        elif type(message) == bytes or type(message) == np.ndarray:
            binary_message = ''.join([format(i, "08b") for i in message])
        elif type(message) == int or type(message) == np.uint8:
            binary_message = format(message, "08b")
        else:
            raise TypeError("Input type not supported")
        logger.debug(f"type: {type(message)},binary_message: {binary_message}")
        return binary_message

    @staticmethod
    def encode(image: numpy.ndarray, secret_message: str) -> numpy.ndarray:
        logger.info(f"Encoding {secret_message} into:\n{image}")
        DELIMITER: str = "#####"

        # calculate the maximum bytes to encode
        image_bytes: int = image.shape[0] * image.shape[1] * 3
        logger.debug(f"Maximum bytes to encode:{image_bytes}")

        # Check if the number of bytes to encode is less than the maximum bytes in the image
        if len(secret_message) > image_bytes:
            logger.error(
                f"Error encountered insufficient bytes. Secret message is {len(secret_message)} bytes, but the image is {image_bytes} bytes.")
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

        secret_message += DELIMITER

        # Convert the cover image to a 1D numpy array
        image_1d: numpy.ndarray = image.flatten()

        secret_message_bin: str = EncoderDecoder._message_to_binary(secret_message)
        data_to_hide_len: int = len(secret_message_bin)

        # Modify the least significant bit of each pixel to store the secret message
        for pixel_index in range(data_to_hide_len):
            image_1d[pixel_index] = (image_1d[pixel_index] & 254) | int(secret_message_bin[pixel_index])

        # Reshape the modified 1D array to the original shape of the cover image
        stego_img: numpy.ndarray = np.reshape(image_1d, image.shape)

        logger.info(f"The encoded image:\n{stego_img}")
        return stego_img

    @staticmethod
    def decode(image: numpy.ndarray) -> str:
        pass


