import cv2
import numpy as np
import types


class EncoderDecoder:

    @staticmethod
    def _message_to_binary(message):
        if type(message) == str:
            return ''.join([format(ord(i), "08b") for i in message])
        elif type(message) == bytes or type(message) == np.ndarray:
            return ''.join([format(i, "08b") for i in message])
        elif type(message) == int or type(message) == np.uint8:
            return format(message, "08b")
        else:
            raise TypeError("Input type not supported")

    @staticmethod
    def encode(image, secret_message: str):
        pass

    @staticmethod
    def decode(image) -> str:
        pass
