import cv2
import numpy
import pytest
import os
from base_directory import base_directory
from encoder_decoder import EncoderDecoder


@pytest.mark.parametrize("secret_message", [
    "Hi",
    "hello world",
    255,
])
def test_message_to_binary(secret_message):
    binary_message: str = EncoderDecoder._message_to_binary(secret_message)
    assert type(binary_message) == str
    for char in binary_message:
        assert int(char) in (0, 1)


@pytest.mark.parametrize("image_path, secret_message", [
    (f"{base_directory}/images/balloons.png", "Hello"),
    (f"{base_directory}/images/squirrel.png", "World")
])
def test_decode(image_path: str, secret_message: str):
    image: numpy.ndarray = cv2.imread(image_path)
    stego_img: numpy.ndarray = EncoderDecoder.encode(image, secret_message)
    assert stego_img.size == image.size

    stego_img_path: str = f"{base_directory}/images/stego_{os.path.basename(image_path)}"
    cv2.imwrite(stego_img_path, stego_img)
    assert os.path.exists(stego_img_path) and os.path.isfile(stego_img_path)

    os.remove(stego_img_path)
    assert True
