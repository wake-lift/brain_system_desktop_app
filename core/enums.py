from enum import StrEnum
from typing import Self


class StrLabelEnum(StrEnum):
    def __new__(cls, value: str, label: str = None) -> Self:
        """Adds additional attribute "label" for each enum element."""
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    @classmethod
    def get_item_by_label(cls, label: str) -> Self | None:
        for member in cls:
            if member.label == label:
                return member
        return None
