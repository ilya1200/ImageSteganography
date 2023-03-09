from logging import Logger

import numpy
import numpy as np

import my_logger

logger: Logger = my_logger.get_console_logger(__name__)


class EncoderDecoder:
    END_OF_MESSAGE_DELIMITER: str = "#####"

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

        # calculate the maximum bytes to encode
        image_bytes: int = image.shape[0] * image.shape[1] * 3
        logger.debug(f"Maximum bytes to encode:{image_bytes}")

        # Check if the number of bytes to encode is less than the maximum bytes in the image
        if len(secret_message) > image_bytes:
            logger.error(
                f"Error encountered insufficient bytes. Secret message is {len(secret_message)} bytes, but the image is {image_bytes} bytes.")
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

        secret_message += EncoderDecoder.END_OF_MESSAGE_DELIMITER

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
        logger.info(f"Decoding the image:\n{image}")
        hidden_data: str = ''

        # Extract LSB from color in each pixel
        for row in image:
            for pixel in row:
                for value in pixel:
                    hidden_data += bin(value)[-1]

        decoded_data: str = ''
        for i in range(0, len(hidden_data), 8):
            decoded_data += chr(int(hidden_data[i:i + 8], 2))

        if EncoderDecoder.END_OF_MESSAGE_DELIMITER in decoded_data:
            decoded_data = decoded_data.split(EncoderDecoder.END_OF_MESSAGE_DELIMITER)[0]
        else:
            logger.warning(f"The end of message delimiter: {EncoderDecoder.END_OF_MESSAGE_DELIMITER} not found in the decoded data.")

        logger.info(f"Decoded data:{decoded_data}")
        return decoded_data


