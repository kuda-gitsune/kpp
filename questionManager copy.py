from collections import defaultdict
from icecream import ic
from PySide6.QtCore import Signal
from typing import Generator

from .models import PureQuestions
from .questionWidget import QuestionWidget


def fetch_questions_in_chunks(session, model: PureQuestions, chunk_size: int = 1) -> Generator[PureQuestions, None, None]:
    try:
        # Query the database in chunks
        for chunk in session.query(model).yield_per(chunk_size):
            yield chunk
    except Exception as e:
        print(f"#TODO Unexpected error occurred in fetch_question: {e}")
    finally:
        pass
        # session.close()


class QuestionManager():
    NOT_FETCHED = 'not_fetched'
    SUCCESS = 'sucess'
    OUT_RANGE = 'out_range'
    FETCH_ERR = 'fetch_err'
    ALL_FETCHED = 'all_fetched'

    curr_question: QuestionWidget

    set_end = Signal()

    def __init__(self, session, model: PureQuestions):
        self.answers = defaultdict(lambda: None)
        self.questions_data = []
        self.curr_index = -1
        self.curr_length = 0
        self.session = session

        self.fetcher = fetch_questions_in_chunks(session, model, chunk_size=25)
        self.get_next()

    def create_new_question(self, db_result: PureQuestions, user_answer=None, is_first=False):
        answer2index = {a: index for index,
                        a in enumerate(['A', 'B', 'C', 'D', 'E'])}

        new_question = QuestionWidget(db_result.Q, [
            db_result.A, db_result.B, db_result.C, db_result.D, db_result.E], answer2index[db_result.answer], is_first=is_first, user_answer=user_answer)
        new_question.answered.connect(self.save_answer)

        self.curr_question = new_question

        return new_question

    def fetch_create_first_question(self):

        result = next(self.fetcher)
        self.create_new_question(result, is_first=True)

    def get_curr(self) -> QuestionWidget:
        return self.curr_question

    def get_next(self):
        """Sprawdza czy jesteśmy na obecnym końcu i sprawdza czy są możliwe dalsze i wykonuje ewentualne pobranie """
        answer2index = {a: index for index,
                        a in enumerate(['A', 'B', 'C', 'D', 'E'])}

        if self.curr_index == self.curr_length - 1:
            try:
                result = next(self.fetcher)

            except StopIteration:
                self.set_end.emit()
                print("Koniec pytań")

            finally:
                self.questions_data.append(result)
                self.curr_length = len(self.questions_data)

                new_question = self.create_new_question(result)
                self.curr_index += 1
                return new_question


        else:
            self.curr_index += 1

            new_question = self.create_new_question(
                        self.questions_data[self.curr_index], user_answer=self.answers[self.curr_index])
            self.curr_question = new_question

            return new_question

    def get_previous(self):
        if self.curr_index == 0:
            raise IndexError(
                'You can not get previous question when you at first question')

        self.curr_index = self.curr_index - 1
        ic(self.curr_index)
        is_first = True if self.curr_index == 0 else False

        new_question = self.create_new_question(
            self.questions_data[self.curr_index], user_answer=self.answers[self.curr_index], is_first=is_first)
        self.curr_question = new_question

        return new_question

    def save_answer(self, answer_index: int):
        self.answers[self.curr_index] = answer_index
        ic(self.answers)
