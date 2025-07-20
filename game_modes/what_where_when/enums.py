from enum import StrEnum
from core.enums import StrLabelEnum


class WWWGameStatusEnum(StrLabelEnum):
    """Возможные статусы раунда (ЧГК)."""

    READY = 'Ready to start/resume timer', 'Готов'
    COUNTDOWN_STARTED = 'Timer started', 'Начат обратный отсчет'
    TIME_IS_OUT = 'Time is out', 'Время вышло'
    PROVIDE_ANSWERS_COUNTDOWN_STARTED = 'Timer to provide answers started', 'Время сдавать ответы!'


class WWWRoundModeEnum(StrLabelEnum):
    """Виды раундов (ЧГК)."""

    REGULAR = 'Regular', 'Стандартный раунд'
    BLITZ = 'Blitz', 'Блиц'
    SUPER_BLITZ = 'Super_blitz', 'Суперблиц'


class WWWBlitzQuestionCounter(StrEnum):
    """Номер вопроса в блиц-раунде (ЧГК)."""

    FIRST = 'вопрос #1'
    SECOND = 'вопрос #2'


class WWWSuperBlitzQuestionCounter(StrEnum):
    """Номер вопроса в суперблиц-раунде (ЧГК)."""

    FIRST = 'вопрос #1'
    SECOND = 'вопрос #2'
    THIRD = 'вопрос #3'
