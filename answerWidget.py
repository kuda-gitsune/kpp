import re

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel

from .styles import DefaultStyles


class AnswerWidget(QLabel):
    released = Signal(int)

    def __init__(self, text, index, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.setStyleSheet(DefaultStyles.text_edit_default)
        self.index = index

    def mouseReleaseEvent(self, event):
        self.released.emit(self.index)
        super().mouseReleaseEvent(event)

    def count_new_lines(self, text: str):
        new_line = r'\<br\>'
        return len(re.findall(new_line, text)) + 1