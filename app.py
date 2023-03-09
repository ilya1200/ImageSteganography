import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()


def main():
    SLACK_APP_TOKEN: str = os.environ["SLACK_APP_TOKEN"]
    SLACK_BOT_TOKEN: str = os.environ["SLACK_BOT_TOKEN"]
    app = App(token=SLACK_BOT_TOKEN, name="ImageSteganography")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
