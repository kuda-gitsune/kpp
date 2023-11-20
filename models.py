from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PureQuestions(Base):
    __tablename__ = 'pure'
    nr = Column(Integer, primary_key=True)
    Q = Column(String)
    A = Column(String)
    B = Column(String)
    C = Column(String)
    D = Column(String)
    E = Column(String)
    answer = Column(String)

class UserAnswers(Base):
    __tablename__ = 'user_answers'
    question_index = Column(Integer, unique=True, primary_key=True)
    answer_index = Column(Integer)
