from dataclasses import dataclass


@dataclass(frozen=True)
class UserImageEntry:
    name: str
    image: list
