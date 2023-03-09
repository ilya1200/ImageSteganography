import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()


def main():
    APP_NAME: str = "ImageSteganography"
    app = App(token=os.environ["SLACK_BOT_TOKEN"], name=APP_NAME)
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()


if __name__ == "__main__":
    main()
