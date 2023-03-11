import os
from logging import Logger
from typing import List, Dict
import cv2
import numpy
from dotenv import load_dotenv
from omegaconf import OmegaConf
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import my_logger
from ImageSteganographyServer import utils
from ImageSteganographyServer.image_steganography_server import ImageSteganographyServer
from base_directory import base_directory
from ImageSteganographyServer.encoder_decoder import EncoderDecoder
from ImageSteganographyServer.storage.user_image_entry import UserImageEntry

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
    image_path: str = utils.down_load_image(f"{base_directory}/ImageSteganographyServer/images/{file['name']}", file['url_private_download'])
    image: numpy.ndarray = cv2.imread(image_path)
    os.remove(image_path)

    secret_message: str = text.split()[1]
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
        logger.debug(f"Got /decipher command in unexpected channel: {channel_id}. Should be used in channel: {channel_id}")
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
