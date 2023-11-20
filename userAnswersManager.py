from collections import defaultdict
from typing import List, Union

from icecream import ic
from sqlalchemy import inspect

from components.models import UserAnswers


class UserAnswersManager():

    def __init__(self, db_model: UserAnswers, session, db_engine):
        self.db_model = db_model
        self.session = session
        self.db_engine = db_engine

        self.answers: defaultdict[int, int] = defaultdict(lambda: None)
        self.highest_answered_index = -1
        self.fetch_answers()

    def fetch_answers(self):
        self.indices_fetched = set()

        try:
            # Query the database in chunks
            fetched_answers: List[UserAnswers] = self.session.query(
                self.db_model).all()
        except Exception as e:
            print(f"#TODO Unexpected error occurred in fetch_answers: {e}")
        finally:
            for row in fetched_answers:
                self.answers[row.question_index] = row.answer_index
                self.indices_fetched.add(row.question_index)
                self.set_highest_answered_index(row.question_index)

    def save_answers(self):
        insert_list = [{'question_index': kay, 'answer_index': value}
                       for kay, value in self.answers.items() if kay not in self.indices_fetched and value != None]
        if insert_list:
            try:
                with self.db_engine.connect() as connection:
                    connection.execute(
                        self.db_model.__table__.insert(),
                        insert_list)
                    connection.commit()
            except Exception as e:
                print(f"Error: {e}")

    def get_user_answer(self, index: int) -> Union[int, None]:
        return self.answers[index]

    def insert_user_answer(self, question_index: int, answer_index: int):
        self.answers[question_index] = answer_index
        self.set_highest_answered_index(question_index)

    def get_highest_answered_index(self):
        return self.highest_answered_index

    def set_highest_answered_index(self, index: int):
        self.highest_answered_index = max(index, self.highest_answered_index)
