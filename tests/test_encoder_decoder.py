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


@pytest.mark.parametrize("image_path, secret_message", [
    (f"{base_directory}/images/balloons.png", "abc"),
    (f"{base_directory}/images/squirrel.png", "123456")
])
def test_encode_decode(image_path: str, secret_message: str):
    image: numpy.ndarray = cv2.imread(image_path)
    stego_img: numpy.ndarray = EncoderDecoder.encode(image, secret_message)
    assert stego_img.size == image.size

    decoded_data: str = EncoderDecoder.decode(stego_img)
    assert decoded_data == secret_message


@pytest.mark.parametrize("image, expected_capacity", [
    (numpy.array([[[111, 112, 113], [121, 144, 221], [0, 255, 70], [17, 222, 37]],
                  [[55, 66, 77], [52, 16, 17], [5, 6, 7], [60, 70, 80]]]), 3)
])
def test_calculate_lsb_encoding_capacity(image: numpy.ndarray, expected_capacity: int):
    actual_capacity: int = EncoderDecoder.calculate_lsb_encoding_capacity(image)
    assert actual_capacity == expected_capacity


@pytest.mark.parametrize("image", [
    None,
    numpy.array(17),
    numpy.array([1, 2, 3])
])
def test_negative_calculate_lsb_encoding_capacity(image: numpy.ndarray):
    with pytest.raises(ValueError) as ve:
        EncoderDecoder.calculate_lsb_encoding_capacity(image)
    if image is None:
        assert ve.value.args[0] == "Image should not be None"
    else:
        assert ve.value.args[0] == f"Image is not 3-d array, it's {image.ndim=}"

