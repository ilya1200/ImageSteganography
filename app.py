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
    logger.info(f"Got app_mention event from channel: {channel}, text: {text}")

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

            # use imdecode function
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            logger.debug("Decoded the image")
    except Exception as e:
        logger.error("Error reading image from URL: %s", e)

    secret_message: str = text.split()[1]
    stego_img: numpy.ndarray = EncoderDecoder.encode(image, secret_message)
    logger.debug(f"Encoded the message: {secret_message} into the image.")

    files_storage[file["name"]] = {"file_name": file["name"], "file": file, "secret_message": secret_message,
                                   "stego_img": stego_img}
    say("Message encoded. Use the /decipher command with the file_name to retrieve the secret message.")


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
