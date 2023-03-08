import os

base_directory: str = os.getenv("BASE_DIRECTORY")
if base_directory is None:
    base_directory = os.path.dirname(os.path.realpath(__file__))
