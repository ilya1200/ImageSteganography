import pytest

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