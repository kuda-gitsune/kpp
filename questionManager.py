from collections import defaultdict
from dataclasses import dataclass
from functools import total_ordering
from icecream import ic
from PySide6.QtCore import Signal
from typing import Generator

from components.userAnswersManager import UserAnswersManager

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

    def __init__(self, session, model: PureQuestions, user_answer_manager: UserAnswersManager):
        self.answers = user_answer_manager
        self.questions_data = []
        self.new_questions_data: dict[QuestionData] = dict()
        self.curr_index = -1
        self.curr_length = 0
        self.session = session

        self.fetch_all_questions()
        ic(str(self.new_questions_data[1]))

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

    def fetch_all_questions(self):
        try:
            # Query the database in chunks
            for row in self.session.query(PureQuestions).all():
                question = QuestionData.from_db_row(row)
                self.new_questions_data[question.question_index] = question

        except Exception as e:
            print(f"#TODO Unexpected error occurred in fetch_question: {e}")
        finally:
            pass

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

                self.curr_index += 1
                new_question = self.create_new_question(
                    result, user_answer=self.answers.get_user_answer(self.curr_index))
                return new_question

        else:
            self.curr_index += 1

            new_question = self.create_new_question(
                self.questions_data[self.curr_index], user_answer=self.answers.get_user_answer(self.curr_index))
            self.curr_question = new_question

            return new_question

    def get_previous(self):
        if self.curr_index == 0:
            raise IndexError(
                'You can not get previous question when you at first question')

        self.curr_index = self.curr_index - 1
        is_first = True if self.curr_index == 0 else False

        new_question = self.create_new_question(
            self.questions_data[self.curr_index], user_answer=self.answers.get_user_answer(self.curr_index), is_first=is_first)
        self.curr_question = new_question

        return new_question

    def save_answer(self, answer_index: int):
        self.answers.insert_user_answer(self.curr_index, answer_index)

@dataclass(frozen=True)
@total_ordering
class QuestionData:
    question_index: int
    Q: str
    A: str
    B: str
    C: str
    D: str
    E: str

    @classmethod
    def from_db_row(cls, db_row: PureQuestions):
        return cls(question_index=db_row.nr, Q=db_row.Q, A=db_row.A, B=db_row.B, C=db_row.C, D=db_row.D, E=db_row.E)

    def __eq__(self, other):
        if not isinstance(other, QuestionData):
            return NotImplemented
        return self.question_index == other.question_index

    def __lt__(self, other):
        if not isinstance(other, QuestionData):
            return NotImplemented
        return self.question_index < other.question_index
