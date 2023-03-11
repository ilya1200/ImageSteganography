import json
from logging import Logger
from typing import List, Dict
import my_logger
from base_directory import base_directory
from storage.user_image_entry import UserImageEntry

logger: Logger = my_logger.get_console_logger(__name__)


class UserImagesStorage:
    STORAGE_PATH: str = f"{base_directory}/storage/user_images.json"

    @staticmethod
    def _read() -> Dict[str, List]:
        content:  Dict[str, List] = {}
        with open(UserImagesStorage.STORAGE_PATH, 'r') as openfile:
            content = json.load(openfile)
        logger.debug(f"Read the content of {UserImagesStorage.STORAGE_PATH}. The are {len(content)} entries")
        return content

    @staticmethod
    def _write(user_image_entries: Dict[str, List]) -> Dict[str, List]:
        with open(UserImagesStorage.STORAGE_PATH, "w") as outfile:
            json.dump(user_image_entries, outfile)
        logger.debug(f"Wrote {len(user_image_entries)} images to {UserImagesStorage.STORAGE_PATH}")
        return user_image_entries

    @staticmethod
    def length() -> int:
        length: int = len(UserImagesStorage.as_list())
        logger.info(f"{length=}")
        return length

    @staticmethod
    def as_list() -> List[UserImageEntry]:
        user_images_dict: Dict[str, List] = UserImagesStorage._read()
        user_images: List[UserImageEntry] = list()
        for name, image in user_images_dict.items():
            user_images.append(UserImageEntry(name, image))
        user_images.sort(key=lambda user_image: user_image.name)
        logger.info(f"There are {len(user_images)} images stored. Here are some of them:\n{ [user_image_entry.name for user_image_entry in user_images[:10]] }")
        return user_images

    @staticmethod
    def read_user_image(image_name: str) -> UserImageEntry | None:
        user_images_dict: Dict[str, List] = UserImagesStorage._read()
        if image_name not in user_images_dict:
            logger.warning(f"Image with name: {image_name} not found in the storage.")
            return None
        user_image_entry: UserImageEntry = UserImageEntry(name=image_name, image=user_images_dict[image_name])
        logger.info(f"Got the image {image_name} from the storage.")
        return user_image_entry

    @staticmethod
    def is_image_in_storage(image_name: str) -> bool:
        user_images: Dict[str, List] = UserImagesStorage._read()
        is_in_storage: bool = image_name in user_images
        logger.info(f"The image with name: {image_name} is in storage: {is_in_storage}")
        return is_in_storage

    @staticmethod
    def write_user_image(user_image_entry: UserImageEntry) -> UserImageEntry:
        updated_user_images_dict: Dict[str, List] = UserImagesStorage._read()
        updated_user_images_dict[user_image_entry.name] = user_image_entry.image
        UserImagesStorage._write(updated_user_images_dict)
        logger.info(f"Added or updated the image: {user_image_entry.name} in storage")
        return user_image_entry

    @staticmethod
    def delete_user_image(image_name: str) -> UserImageEntry | None:
        if not UserImagesStorage.is_image_in_storage(image_name):
            logger.warning(f"Failed to delete image with name {image_name}, it is not in the storage.")
            return None
        user_images_dict: Dict[str, List] = UserImagesStorage._read()
        user_images_entry: UserImageEntry = UserImageEntry(name=image_name, image=user_images_dict[image_name])
        del user_images_dict[image_name]
        UserImagesStorage._write(user_images_dict)
        logger.info(f"Deleted user image with name: {image_name}")
        return user_images_entry

    @staticmethod
    def reset():
        UserImagesStorage._write(dict())
        actual_len: int = UserImagesStorage.length()
        if actual_len > 0:
            error_msg: str = f"Failed to delete all data in the storage. There are {actual_len} remaining items in {UserImagesStorage.STORAGE_PATH}"
            logger.error(error_msg)
            raise Exception(error_msg)
        logger.info("Storage was reset")



