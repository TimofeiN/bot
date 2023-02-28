from dataclasses import dataclass
from emoji import emojize


@dataclass(frozen=True)
class Messages:
    welcome: str = emojize('Hi! :victory_hand: \n'
                           'Write me smth. or press /help')

    back: str = emojize(':right_arrow_curving_left: back')
    confirm: str = emojize(':check_mark_button: confirm')


msg = Messages()
