import os
from logging import Logger
from typing import List, Dict
import urllib.request
import cv2
import numpy
from dotenv import load_dotenv
from omegaconf import OmegaConf
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from base_directory import base_directory
from encoder_decoder import EncoderDecoder
import my_logger
from urllib.error import HTTPError

load_dotenv()
SLACK_APP_TOKEN: str = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN: str = os.environ["SLACK_BOT_TOKEN"]

logger: Logger = my_logger.get_console_logger(__name__)
app: App = App(token=SLACK_BOT_TOKEN, name="Joke Bot")
cfg = OmegaConf.load(f"{base_directory}/config/config.yaml")

# Set the channel ID where you want to listen for file uploads
watch_channel_id = cfg.slack_bot.channel_id
BOT_ID = os.environ["BOT_ID"]

enciphered_files: List[Dict] = list()

files_storage: Dict[str, Dict] = dict()


@app.event("app_mention")
def handle_app_mention(event, say):
    text: str = event["text"]
    channel: str = event["channel"]
    logger.info(f"Got app_mention event from channel: {channel}")

    files_in_message: List[Dict] = event["files"]
    say(f"You mentioned me in <#{channel}>: '{text}'")
    if not (channel == watch_channel_id and len(text.split()) == 2 and len(files_in_message) == 1):
        logger.warning("Message should start with the app mention then the text to encode, also only one image should "
                       "be attached")
        return

    file: dict = files_in_message[0]
    image: numpy.ndarray

    try:
        logger.info(f"Reading the image from url: {file['url_private_download']}")
        with urllib.request.urlopen(file["url_private_download"]) as url:
            # read image as an numpy array
            image = numpy.asarray(bytearray(url.read()), dtype="uint8")
            logger.debug("Read the image")

            # Check that the image was read correctly
            if image.shape == (0,):
                raise ValueError("Image could not be read from URL")

            # Decode the NumPy array as an image using OpenCV
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            logger.debug("Decoded the image")
    except urllib.error.HTTPError as e:
        logger.error("HTTP error: %s", e)
    except ValueError as e:
        logger.error("Error reading image from URL: %s", e)
    except Exception as e:
        logger.error("Error reading image from URL: %s", e)

    secret_message: str = text.split()[1]
    stego_img: numpy.ndarray = EncoderDecoder.encode(image, secret_message)
    logger.debug(f"Encoded the message: {secret_message} into the image.")

    files_storage[file["name"]] = {"file_name": file["name"], "file": file, "stego_img": stego_img}
    say("Message encoded successfully.\nTo decode the message, use the /decipher command with the file_name to "
        "retrieve the secret message.")


@app.command("/decipher")
def handle_command(ack, respond, command):
    ack(f"Received command: {command['text']}")
    channel_id: str = command["channel_id"]
    text: str = command["text"].strip()
    if not (channel_id == watch_channel_id):
        logger.debug(f"Got /decipher command in unexpected channel: {channel_id}. Should be used in channel: {channel_id}")
        respond(f"To decipher and image, use /decipher command in channel: {watch_channel_id}")
        return
    if not text:
        logger.debug(f"File names to decipher are missing")
        respond(f"File name to decode is missing")
        return
    if not files_storage:
        logger.debug("files_storage is empty")
        respond("No file were encoded..")
        return

    files_to_decode: List[str] = text.split()

    for file_name in files_to_decode:
        if file_name not in files_storage:
            logger.warning(f"Did not find a file with name: {file_name} in {str(list(files_storage.keys()))}")
            respond(f"Did not find a file with name: {file_name} in {str(list(files_storage.keys()))}")
        else:
            logger.debug(f"Found a file with name: {file_name} in {str(list(files_storage.keys()))}")
            secret_message: str = EncoderDecoder.decode(files_storage[file_name]["stego_image"])
            logger.info(f"Deciphered the secret message from: {file_name}")
            respond(f"The secret message in {file_name} is {secret_message}")
    logger.info("/decipher command complete")


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
