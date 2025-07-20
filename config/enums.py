from core.enums import StrLabelEnum


class SoundFileEnum(StrLabelEnum):
    """Доступные звуковые файлы с человекочитаемыми названиями."""

    OPENING = 'chgk_opening.mp3', 'Начало игры (заглавная тема)'
    WHIPPING_TOP = 'chgk_whipping_top.mp3', 'Волчок (мелодия)'
    BLACK_BOX = 'chgk_black_box.mp3', 'Черный ящик (мелодия)'
    CORRECT_ANSWER = 'chgk_correct_ans_music.mp3', 'Правильный ответ (мелодия)'
    INCORRECT_ANSWER = 'chgk_incorrect_ans_music.mp3', 'Неправильный ответ (мелодия)'
    WINNER_ANNOUNCE = 'chgk_winner_announce.mp3', 'Объявление победителя (мелодия)'
    PAUSE = 'chgk_pause.mp3', 'Пауза в игре (мелодия)'
    GONG_01 = 'chgk_gong_01.mp3', 'Гонг 1'
    GONG_02 = 'chgk_gong_02.mp3', 'Гонг 2'
    TIMER_START_STOP = 'chgk_timer_start_stop.mp3', 'Таймер: старт/стоп'
    TIMER_10_SEC_LEFT = 'chgk_timer_10_sec_left.mp3', 'Таймер: осталось 10 секунд'
    BRAIN_TIMER_START_END = 'brain_ring_timer_start_stop_1174.66_hz.mp3', 'Брейн-ринг: старт / время вышло'
    BRAIN_TIMER_CLOSE_TO_END = 'brain_ring_timer_close_to_end_1174.66_hz.mp3', 'Брейн-ринг: время на исходе'
    BRAIN_PLAYER_BUTTON_PRESSED = 'brain_ring_player_button_pressed_830.61_hz.mp3', 'Брейн-ринг: кнопка игрока нажата'
    BRAIN_PLAYER_FALSE_START = 'brain_ring_false_start_523.25_hz.mp3', 'Брейн-ринг: фальстарт'


class GameTypeEnum(StrLabelEnum):
    """Доступные режимы игры."""

    BRAIN_RING = 'brain_ring', 'Брейн-ринг'
    WWW = 'what_where_when', 'Что-Где-Когда'
    ERUDITE = 'erudite', 'Эрудитка'


class ColorSchemaEnum(StrLabelEnum):
    """Цвета, используемые в программе и виджетах."""

    RED = '#FF0000', 'Базовый цвет красной кнопки (игрока)'
    GREEN = '#008000', 'Базовый цвет зеленой кнопки (игрока)'
    BLUE = '#0000FF', 'Базовый цвет синей кнопки (игрока)'
    YELLOW = '#FFFF00', 'Базовый цвет желтой кнопки (игрока)'
    WHITE = '#FFFFFF', 'Базовый цвет белой кнопки (игрока)'
    BLACK = '#000000', 'Базовый цвет черной кнопки (игрока)'

    DEFAULT_SCALABLE_LABEL = '#17202a', 'Дефолтный цвет текстового лейбла'

    BRAIN_GAME_WIDGET_BACKGROUND = '#122560', 'Цвет основного фона игрового виджета брейн-ринга'
    BRAIN_PLAYER_NAME_LABEL = '#FFFFFF', 'Цвет названия игрока на игровом виджете (брейн-ринг)'
    BRAIN_NOT_FIRST_PLAYER_NAME_LABEL = '#778899', 'Цвет названия не первого игрока на игровом виджете (брейн-ринг)'
    BRAIN_PLAYER_TIME_LABEL = '#FFFFFF', 'Цвет времени игрока на игровом виджете (брейн-ринг)'
    BRAIN_NOT_FIRST_PLAYER_TIME_LABEL = '#778899', 'Цвет времени не первого игрока на игровом виджете (брейн-ринг)'
    BRAIN_RING_GAME_TIMER_INITIAL = '#000000', 'Исходный цвет времени на игровом виджете (брейн-ринг)'
    BRAIN_RING_GAME_TIMER_START = '#2C97FF', 'Цвет времени на игровом виджете (брейн-ринг) после старта таймера'
    BRAIN_RING_GAME_TIMER_5_SEC_LEFT = '#FF9900', 'Цвет времени на игровом виджете (брейн-ринг) (осталось < 5 сек)'
    BRAIN_RING_GAME_TIMER_RUN_OUT = '#E4002A', 'Цвет времени на игровом виджете (брейн-ринг) при истечении таймера'
    BRAIN_RING_MODERATOR_TIMER_INITIAL = '#000000', 'Исходный цвет времени на виджете ведущего (брейн-ринг)'
    BRAIN_RING_MODERATOR_TIMER_START = '#2C97FF', 'Цвет времени виджете ведущего (брейн-ринг) после старта таймера'
    BRAIN_RING_MODERATOR_TIMER_5_SEC_LEFT = '#CC6432', 'Цвет времени виджете ведущего (брейн-ринг) (осталось < 5 сек)'
    BRAIN_RING_MODERATOR_TIMER_RUN_OUT = '#CC0000', 'Цвет времени виджете ведущего (брейн-ринг) при истечении таймера'

    WWW_GAME_WIDGET_BACKGROUND = '#122560', 'Цвет основного фона игрового виджета ЧГК'
    WWW_ROUND_STATUS_LABEL = '#B0C4DE', 'Цвет информации о статусе раунда на игровом виджете (ЧГК)'
    WWW_GAME_TIMER_INITIAL = '#2C97FF', 'Исходный цвет времени на игровом виджете (ЧГК)'
    WWW_GAME_TIMER_START = '#2C97FF', 'Цвет времени на игровом виджете (ЧГК) после старта таймера'
    WWW_GAME_TIMER_10_SEC_LEFT = '#D27E00', 'Цвет времени на игровом виджете (ЧГК) (осталось < 10 сек)'
    WWW_GAME_TIMER_RUN_OUT = '#E4002A', 'Цвет времени на игровом виджете (ЧГК) при истечении таймера'
    WWW_GAME_TIMER_PROVIDE_ANSWERS = '#BF1D02', 'Цвет времени на игровом виджете (ЧГК) (время на сбор ответов)'
    WWW_MODERATOR_TIMER_INITIAL = '#000000', 'Исходный цвет времени на виджете ведущего (ЧГК)'
    WWW_MODERATOR_TIMER_10_SEC_LEFT = '#D27E00', 'Цвет времени виджете ведущего (ЧГК) (осталось < 10 сек)'
    WWW_MODERATOR_TIMER_PROVIDE_ANSWERS = '#BF1D02', 'Цвет времени виджете ведущего (ЧГК) (время на сбор ответов)'

    ERUDITE_GAME_WIDGET_BACKGROUND = '#122560', 'Цвет основного фона игрового виджета эрудитки'
    ERUDITE_PLAYER_NAME_LABEL = '#FFFFFF', 'Цвет названия игрока на игровом виджете (эрудитка)'
    ERUDITE_NOT_FIRST_PLAYER_NAME_LABEL = '#778899', 'Цвет названия не первого игрока на игровом виджете (эрудитка)'
    ERUDITE_PLAYER_TIME_LABEL = '#FFFFFF', 'Цвет времени игрока на игровом виджете (эрудитка)'
    ERUDITE_NOT_FIRST_PLAYER_TIME_LABEL = '#778899', 'Цвет времени не первого игрока на игровом виджете (эрудитка)'
    ERUDITE_GAME_TIMER_INITIAL = '#000000', 'Исходный цвет времени на игровом виджете (эрудитка)'
    ERUDITE_GAME_TIMER_START = '#2C97FF', 'Цвет времени на игровом виджете (эрудитка) после старта таймера'
    ERUDITE_GAME_TIMER_5_SEC_LEFT = '#FF9900', 'Цвет времени на игровом виджете (эрудитка) (осталось < 5 сек)'
    ERUDITE_GAME_TIMER_RUN_OUT = '#E4002A', 'Цвет времени на игровом виджете (эрудитка) при истечении таймера'
    ERUDITE_MODERATOR_TIMER_INITIAL = '#000000', 'Исходный цвет времени на виджете ведущего (эрудитка)'
    ERUDITE_MODERATOR_TIMER_START = '#2C97FF', 'Цвет времени виджете ведущего (эрудитка) после старта таймера'
    ERUDITE_MODERATOR_TIMER_5_SEC_LEFT = '#CC6432', 'Цвет времени виджете ведущего (эрудитка) (осталось < 5 сек)'
    ERUDITE_MODERATOR_TIMER_RUN_OUT = '#CC0000', 'Цвет времени виджете ведущего (эрудитка) при истечении таймера'
