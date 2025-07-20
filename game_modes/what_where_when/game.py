from game_modes.what_where_when.enums import (
    WWWBlitzQuestionCounter,
    WWWGameStatusEnum,
    WWWRoundModeEnum,
    WWWSuperBlitzQuestionCounter,
)


class WWWGame:
    """Класс с параметрами игры в ЧГК."""

    def __init__(
        self,
        status: WWWGameStatusEnum = WWWGameStatusEnum.READY,
        round_mode: WWWRoundModeEnum = WWWRoundModeEnum.REGULAR,
    ) -> None:
        self.status: WWWGameStatusEnum = status
        self.round_mode: WWWRoundModeEnum = round_mode
        self.current_blitz_question: WWWBlitzQuestionCounter | None = None
        self.current_super_blitz_question: WWWSuperBlitzQuestionCounter | None = None
        self.enable_time_to_provide_answers: bool = True
