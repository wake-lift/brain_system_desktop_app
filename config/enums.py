from core.enums import StrLabelEnum


class SoundFilesEnum(StrLabelEnum):
    """All available sound patterns with paths to files and human readable labels."""

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

    """All available game types."""
    BRAIN_RING = 'brain_ring', 'Брейн-ринг'
    WWW = 'what_where_when', 'Что-Где-Когда'
    ERUDITE = 'erudite', 'Эрудитка'
