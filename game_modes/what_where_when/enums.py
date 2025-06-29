from enum import StrEnum
from core.enums import StrLabelEnum


class WWWGameStatusEnum(StrLabelEnum):
    READY = 'Ready to start/resume timer', 'Готов'
    COUNTDOWN_STARTED = 'Timer started', 'Начат обратный отсчет'
    TIME_IS_OUT = 'TIME_IS_OUT', 'Время вышло'
    PROVIDE_ANSWERS_COUNTDOWN_STARTED = 'Timer to provide answers started', 'Время сдавать ответы'


class WWWRoundModeEnum(StrLabelEnum):
    REGULAR = 'Regular', 'Стандартный раунд'
    BLITZ = 'Blitz', 'Блиц'
    SUPER_BLITZ = 'Super_blitz', 'Суперблиц'


class WWWBlitzQuestionCounter(StrEnum):
    FIRST = 'Первый вопрос'
    SECOND = 'Второй вопрос'


class WWWSuperBlitzQuestionCounter(StrEnum):
    FIRST = 'Первый вопрос'
    SECOND = 'Второй вопрос'
    THIRD = 'Третий вопрос'
