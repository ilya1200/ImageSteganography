import os
from logging import Logger
from typing import List, Dict
import cv2
import numpy
import requests
from dotenv import load_dotenv
from omegaconf import OmegaConf
from requests import Response
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import SlackResponse

import my_logger
from ImageSteganographyServer import utils
from ImageSteganographyServer.image_steganography_server import ImageSteganographyServer
from base_directory import base_directory
from ImageSteganographyServer.encoder_decoder import EncoderDecoder
from ImageSteganographyServer.storage.user_image_entry import UserImageEntry
from PIL import Image
from io import BytesIO

load_dotenv()
SLACK_APP_TOKEN: str = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN: str = os.environ["SLACK_BOT_TOKEN"]

logger: Logger = my_logger.get_console_logger(__name__)
app: App = App(token=SLACK_BOT_TOKEN, name="ImageSteganography")
cfg = OmegaConf.load(f"{base_directory}/config/config.yaml")

# Set the channel ID where you want to listen for file uploads
watch_channel_id = cfg.slack_bot.channel_id
BOT_ID = os.environ["BOT_ID"]


@app.event("app_mention")
def handle_app_mention(event, say):
    logger.info(f"Got app_mention event")
    text: str = event["text"]
    channel: str = event["channel"]

    say(f"You mentioned me in <#{channel}>: '{text}'")
    text = text.strip()
    if not channel == watch_channel_id:
        logger.debug(f"The event is not form the defined channel {watch_channel_id}, but actually from {channel=}")
        return

    args: List[str] = text.split()
    if BOT_ID not in args[0]:
        error_msg: str = "The bot should be mentioned first and then a message to encrypt"
        logger.error(error_msg)
        say(error_msg)
        return

    if len(args[1:]) < 1:
        error_msg: str = "The message to encrypt is missing"
        logger.error(error_msg)
        say(error_msg)
        return

    if "files" not in event:
        error_msg: str = "No file attached to the request"
        logger.error(error_msg)
        say(error_msg)
        return
    files_in_message: List[Dict] = event["files"]

    if len(files_in_message) > 1:
        error_msg: str = f"Expected only one file to be attached, but got {len(files_in_message)}"
        logger.warning(error_msg)
        say(error_msg)
        return

    secret_message: str = args[1:]
    file: dict = files_in_message[0]
    say(f"Encrypting the message {secret_message} into image {file['name']}")

    file_id: str = file["id"]

    file_info: SlackResponse = app.client.files_info(file=file_id)

    # Extract the URL to download the file
    download_url: str = file_info["file"]["url_private"]

    # Download the file using requests
    response: Response = requests.get(download_url, headers={"Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}"})
    response.raise_for_status()

    # Create a NumPy array from the byte string
    img_array: numpy.ndarray = numpy.frombuffer(response.content, dtype=numpy.uint8)

    # Reshape the array to the desired dimensions
    image: numpy.ndarray = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Convert the color format from BGR to RGB
    image: numpy.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    stego_img: numpy.ndarray = EncoderDecoder.encode(image, secret_message)
    logger.debug(f"Encoded the message: {secret_message} into the image.")

    user_image_entry: UserImageEntry = UserImageEntry(name=file["name"], image=stego_img.tolist())
    ImageSteganographyServer.user_images_storage.write_user_image(user_image_entry)
    say(f"Message {secret_message} encoded successfully into image {user_image_entry.name}.\n"
        f"To decode the message, use the decipher command with the file_name to"
        "retrieve the secret message.")


@app.command("/decipher")
def handle_command(ack, respond, command):
    ack(f"Received decipher command with args: {command['text']}")
    logger.info(f"Received decipher command with args: {command['text']}")

    channel_id: str = command["channel_id"]
    text: str = command["text"].strip()
    if not (channel_id == watch_channel_id):
        logger.debug(
            f"Got /decipher command in unexpected channel: {channel_id}. Should be used in channel: {channel_id}")
        respond(f"To decipher an image, use decipher command in channel: {watch_channel_id}")
        return
    if not text:
        logger.debug(f"File names to decipher are missing")
        respond(f"File name to decode is missing")
        return
    if ImageSteganographyServer.user_images_storage.is_empty():
        logger.debug("files_storage is empty")
        respond("No file were encoded..")
        return

    files_to_decode: List[str] = text.split()

    for file_name in files_to_decode:
        uie: UserImageEntry = ImageSteganographyServer.user_images_storage.read_user_image(file_name)
        if not ImageSteganographyServer.user_images_storage.is_image_in_storage(file_name):
            error_msg: str = f"Did not find a file with name: {file_name} in the storage"
            logger.warning(error_msg)
            respond(error_msg)
        else:
            logger.debug(f"Found a file with name: {file_name} in the storage")
            secret_message: str = EncoderDecoder.decode(numpy.array(uie.image))
            logger.info(f"Deciphered the secret message from: {file_name}")
            respond(f"The secret message in {file_name} is {secret_message}")
    logger.info("/decipher command complete")


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
