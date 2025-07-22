from enum import StrEnum
from typing import Self


class StrLabelEnum(StrEnum):
    """Класс с дополнительным атрибутом "label" у каждого элемента."""

    def __new__(cls, value: str, label: str = None) -> Self:  # noqa: WPS110
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    @classmethod
    def get_item_by_label(cls, label: str) -> Self | None:
        """Возвращает элемент на основании его атрибута "label"."""
        for member in cls:
            if member.label == label:
                return member
        return None
