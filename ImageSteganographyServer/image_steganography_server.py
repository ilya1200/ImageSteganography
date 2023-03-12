from dataclasses import asdict
from logging import Logger
from typing import Dict, Any

import numpy

import my_logger
from ImageSteganographyServer.encoder_decoder import EncoderDecoder
from ImageSteganographyServer.storage.user_image_entry import UserImageEntry
from ImageSteganographyServer.storage.user_images_storage import UserImagesStorage

logger: Logger = my_logger.get_console_logger(__name__)


class ImageSteganographyServer:
    user_images_storage: UserImagesStorage = UserImagesStorage
    encoder_decoder: EncoderDecoder = EncoderDecoder

    @staticmethod
    def encipher(secret_message: str, image_name: str, image: numpy.ndarray) -> Dict[str, Any]:
        stego_img: numpy.ndarray = ImageSteganographyServer.encoder_decoder.encode(image, secret_message)
        logger.debug(f"Encoding the message: {secret_message} into the image {image_name}.")

        user_image_entry: UserImageEntry = ImageSteganographyServer.user_images_storage.write_user_image(
            UserImageEntry(name=image_name, image=stego_img.tolist()))
        logger.info(f"Encoded the message: {secret_message} into the image {user_image_entry.name}.")
        return asdict(user_image_entry)

    @staticmethod
    def decipher(image_name: str) -> str:
        uie: UserImageEntry = ImageSteganographyServer.user_images_storage.read_user_image(image_name)
        secret_message: str = ImageSteganographyServer.encoder_decoder.decode(numpy.array(uie.image))
        logger.debug(f"Deciphered the secret message from: {image_name}, {secret_message=}")
        return secret_message

