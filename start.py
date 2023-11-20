import sys

from icecream import ic
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base

from components.models import Base, PureQuestions, UserAnswers
from components.questionManager import QuestionManager
from components.questionWidget import QuestionWidget
from components.userAnswersManager import UserAnswersManager
from components.widgets import PaginationWidget


def setup_database():
    engine = create_engine('sqlite:///extraction/kpp.db')
    Base.metadata.create_all(engine)
    return engine


def main():
    app = QApplication(sys.argv)
    db_engine = setup_database()

    class AppWindow(QMainWindow):
        question: QuestionWidget

        def __init__(self, db_engine, model, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.db_engine = db_engine
            Session = sessionmaker(bind=db_engine)
            self.session = Session()
            self.user_answer_manager = UserAnswersManager(UserAnswers, self.session, self.db_engine)
            self.question_manager = QuestionManager(self.session, model,self.user_answer_manager)
            self.init_ui()

        def init_ui(self):
            self.init_app_layout()

            self.question = self.question_manager.get_curr()
            self.app_layout.addWidget(self.question)

            self.init_pagination()

        def init_app_layout(self):
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)

            self.app_layout = QVBoxLayout()
            self.central_widget.setLayout(self.app_layout)

        def init_pagination(self):
            self.pagination_widget = PaginationWidget(
                is_first=True)
            self.pagination_widget.next.connect(self.on_next)
            self.pagination_widget.previous.connect(self.on_previous)
            self.app_layout.addWidget(self.pagination_widget)

        def update_ui(self, new_question_widget: QuestionWidget):
            self.question.hide()
            self.app_layout.replaceWidget(self.question, new_question_widget)
            self.question = new_question_widget

            self.pagination_widget.set_is_first(self.question.is_first)

            ic(self.user_answer_manager.get_highest_answered_index())

        def closeEvent(self, event):
            self.session.flush()
            self.session.close_all()
            self.user_answer_manager.save_answers()

            super().closeEvent(event)

        def on_next(self):
            question = self.question_manager.get_next()
            self.update_ui(question)

        def on_previous(self):
            question = self.question_manager.get_previous()
            self.update_ui(question)

        def flush_session(self):
            self.session.flush()

        def on_next_unsolved(self):
            pass

    window = AppWindow(db_engine, PureQuestions)
    window.show()
    app.exec()
    


if __name__ == '__main__':
    main()
