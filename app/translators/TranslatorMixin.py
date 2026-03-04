from typing import Protocol


class FromRuTranslatorMixin(Protocol):
    @staticmethod
    def from_ru_to_eng():
        """
        Перевод с русского на английский
        """
        pass

class FromEngTranslatorMixin(Protocol):
    @staticmethod
    def from_eng_to_ru():
        """
        Перевод с английского на русский
        """
        pass