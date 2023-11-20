from typing import List, Union


from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel,QVBoxLayout

from .answerWidget import AnswerWidget
from .styles import DefaultStyles



class QuestionWidget(QWidget):
    answered = Signal(int)

    def __init__(self, question: str, answers: List[str], true_answer: int, user_answer: Union[None, int] = None, is_first=False):
        super().__init__()

        self.is_answered = True if user_answer else False
        self.true_answer = true_answer
        self.is_first = is_first

        # I don`t now why I need this type declaration to get autosuggestion
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        self.question = QLabel(question)
        self.question.setStyleSheet(DefaultStyles.label)
        self.layout.addWidget(self.question)

        self.init_answers(answers, true_answer, user_answer)

    def init_answers(self, answers: List[str], true_answer: int, user_answer: Union[None, int] = None):
        self.answers = [AnswerWidget(answer, index)
                        for index, answer in enumerate(answers)]
        for answer in self.answers:
            self.layout.addWidget(answer)

        for answer in self.answers:
            answer.released.connect(self.on_answer)

        if user_answer:
            self.show_answer(user_answer)

    def show_answer(self, index: int):
        self.answers[self.true_answer].setStyleSheet(
            DefaultStyles.text_edit_true)

        if index != self.true_answer:
            self.answers[index].setStyleSheet(
                DefaultStyles.text_edit_wrong)

    def on_answer(self, index: int):
        if not self.is_answered:
            self.answered.emit(index)
            self.is_answered = True
            self.show_answer(index)
