import json
from typing import List, Dict

from base_directory import base_directory
from storage.user_image_entry import UserImageEntry


class UserImagesStorage:
    STORAGE_PATH: str = f"{base_directory}/storage/user_images.json"

    @staticmethod
    def _read() -> Dict[str, List]:
        with open(UserImagesStorage.STORAGE_PATH, 'r') as openfile:
            return json.load(openfile)

    @staticmethod
    def _write(user_image_entries: Dict[str, List]) -> Dict[str, List]:
        with open(UserImagesStorage.STORAGE_PATH, "w") as outfile:
            json.dump(user_image_entries, outfile)
        return user_image_entries

    @staticmethod
    def length() -> int:
        return len(UserImagesStorage.as_list())

    @staticmethod
    def as_list() -> List[UserImageEntry]:
        user_images_dict: Dict[str, List] = UserImagesStorage._read()
        user_images: List[UserImageEntry] = list()
        for name, image in user_images_dict.items():
            user_images.append(UserImageEntry(name, image))
        user_images.sort(key=lambda user_image: user_image.name)
        return user_images

    @staticmethod
    def read_user_image(image_name: str) -> UserImageEntry | None:
        user_images_dict: Dict[str, List] = UserImagesStorage._read()
        if image_name not in user_images_dict:
            return None
        return UserImageEntry(name=image_name, image=user_images_dict[image_name])

    @staticmethod
    def is_image_in_storage(image_name) -> bool:
        user_images: Dict[str, List] = UserImagesStorage._read()
        return image_name in user_images

    @staticmethod
    def write_user_image(user_image_entry: UserImageEntry) -> UserImageEntry:
        updated_user_images_dict: Dict[str, List] = UserImagesStorage._read()
        updated_user_images_dict[user_image_entry.name] = user_image_entry.image
        UserImagesStorage._write(updated_user_images_dict)
        return user_image_entry

    @staticmethod
    def remove_user_image(image_name: str) -> UserImageEntry | None:
        if not UserImagesStorage.is_image_in_storage(image_name):
            return None
        user_images_dict: Dict[str, List] = UserImagesStorage._read()
        user_images_entry: UserImageEntry = UserImageEntry(name=image_name, image=user_images_dict[image_name])
        del user_images_dict[image_name]
        UserImagesStorage._write(user_images_dict)
        return user_images_entry

    @staticmethod
    def reset():
        UserImagesStorage._write(dict())
        actual_len: int = UserImagesStorage.length()
        if actual_len > 0:
            raise Exception(f"Failed to delete all data in the storage. There are {actual_len} items in {UserImagesStorage.STORAGE_PATH}")



