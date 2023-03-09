from logging import Logger
import cv2
import numpy as np
import types
import my_logger

logger: Logger = my_logger.get_console_logger(__name__)


class EncoderDecoder:

    @staticmethod
    def _message_to_binary(message) -> str:
        logger.debug(f"Message: {message}")
        binary_message = None
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
    def encode(image, secret_message: str):
        pass

    @staticmethod
    def decode(image) -> str:
        pass
