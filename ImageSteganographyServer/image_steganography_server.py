from ImageSteganographyServer.encoder_decoder import EncoderDecoder
from ImageSteganographyServer.storage.user_images_storage import UserImagesStorage


class ImageSteganographyServer:
    user_images_storage: UserImagesStorage = UserImagesStorage
    encoder_decoder: EncoderDecoder = EncoderDecoder
