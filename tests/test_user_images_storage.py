import json
from typing import List
from base_directory import base_directory
from storage.user_image_entry import UserImageEntry
from storage.user_images_storage import UserImagesStorage


class TestUserImagesStorage:

    def setup_class(self):
        UserImagesStorage.STORAGE_PATH = f"{base_directory}/storage/user_images_testing.json"
        with open(UserImagesStorage.STORAGE_PATH, "w") as outfile:
            json.dump(dict(), outfile)

    def test_reset(self):
        uie_name: str = "aaa"
        img: list = [[[111, 112, 113], [121, 144, 221], [0, 255, 70], [17, 222, 37]],
                     [[55, 66, 77], [52, 16, 17], [5, 6, 7], [60, 70, 80]]]

        uie: UserImageEntry = UserImagesStorage.write_user_image(UserImageEntry("aaa", img))
        assert uie.name == uie_name
        assert UserImagesStorage.is_image_in_storage(uie.name)

        UserImagesStorage.reset()
        assert UserImagesStorage.length() == 0

    def test_write_user_image(self):
        a_name: str = "aaa"
        a_img: list = [[[111, 112, 113], [121, 144, 221], [0, 255, 70], [17, 222, 37]],
                       [[55, 66, 77], [52, 16, 17], [5, 6, 7], [60, 70, 80]]]
        empty_img: list = list()
        UserImagesStorage.delete_user_image(a_name)

        # add new image
        uie: UserImageEntry = UserImagesStorage.write_user_image(UserImageEntry(a_name, a_img))
        assert UserImagesStorage.is_image_in_storage(uie.name)
        assert uie.name == a_name

        # update an existing image
        uie = UserImagesStorage.write_user_image(UserImageEntry(a_name, empty_img))
        assert UserImagesStorage.is_image_in_storage(uie.name)
        assert uie.name == a_name
        assert len(uie.image) == 0

    def delete_user_image(self):
        a_name: str = "aaa"
        a_img: list = [[[111, 112, 113], [121, 144, 221], [0, 255, 70], [17, 222, 37]],
                       [[55, 66, 77], [52, 16, 17], [5, 6, 7], [60, 70, 80]]]
        b_name: str = "bbb"
        b_img: list = []

        # add new images
        uie_a: UserImageEntry = UserImagesStorage.write_user_image(UserImageEntry(a_name, a_img))
        uie_b: UserImageEntry = UserImagesStorage.write_user_image(UserImageEntry(b_name, b_img))

        assert UserImagesStorage.is_image_in_storage(uie_a.name) is True
        assert uie_a.name == a_name

        assert UserImagesStorage.is_image_in_storage(uie_b.name) is True
        assert uie_b.name == b_name

        # delete the images
        UserImagesStorage.delete_user_image(a_name)
        assert UserImagesStorage.is_image_in_storage(a_name) is False

        UserImagesStorage.delete_user_image(b_name)
        assert UserImagesStorage.is_image_in_storage(b_name) is False

    def test_as_list(self):
        a_name: str = "aaa"
        a_img: list = [111, 112, 113]

        UserImagesStorage.reset()

        # add new image
        uie_a: UserImageEntry = UserImagesStorage.write_user_image(UserImageEntry(a_name, a_img))
        assert UserImagesStorage.is_image_in_storage(uie_a.name) is True
        assert uie_a.name == a_name

        images: List[UserImageEntry] = UserImagesStorage.as_list()
        assert len(images) == 1

        assert images[0].name == a_name
        assert images[0].image == a_img

    def test_length(self):
        a_name: str = "aaa"
        a_img: list = [111, 112, 113]

        UserImagesStorage.reset()

        # add new image
        uie_a: UserImageEntry = UserImagesStorage.write_user_image(UserImageEntry(a_name, a_img))
        assert UserImagesStorage.is_image_in_storage(uie_a.name) is True
        assert uie_a.name == a_name

        assert UserImagesStorage.length() == 1
