from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QWidget

from .styles import DefaultStyles

class PaginationWidget(QWidget):
    next = Signal()
    previous = Signal()

    def __init__(self, is_first = False, is_last = False):
        super().__init__()

        self.setStyleSheet(DefaultStyles.button)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.previous_next_layout = QHBoxLayout()
        self.layout.addLayout(self.previous_next_layout)

        self.previous_button = QPushButton()
        self.previous_button.setText('Poprzednie')
        self.previous_button.clicked.connect(self.on_previous)
        self.previous_next_layout.addWidget(self.previous_button)

        self.next_button = QPushButton()
        self.next_button.setText('Następne')
        self.next_button.clicked.connect(self.on_next)
        self.previous_next_layout.addWidget(self.next_button)

        self.next_unsolved_button = NextUnsolvedQuestionButton()
        self.layout.addWidget(self.next_unsolved_button)

        if  is_first:
            self.previous_button.hide()
        if  is_last:
            self.next_button.hide()

    def on_next(self):
        self.next.emit()

    def on_previous(self):
        self.previous.emit()

    def set_is_first(self, is_first):
        if is_first:
            self.previous_button.hide()
        else:
            self.previous_button.show()

    def set_is_last(self, is_last):
        if is_last:
            self.next_button.hide()
        else:
            self.next_button.show()


class NextUnsolvedQuestionButton(QPushButton):
    next_unsolved = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText('Następne nierozwiązane')
        self.setStyleSheet(DefaultStyles.button)
        self.clicked.connect(self.on_click)

    def on_click(self):
        self.next_unsolved.emit()