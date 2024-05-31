from sqlalchemy import Boolean, String, Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from db import Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, unique=True, index=True)
    lastname = Column(String, unique=True, index=True)

    scores = relationship("Score", back_populates="student")


class Scores(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String, unique=True, index=True)
    score = Column(Integer, unique=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))

    student = relationship("Student", back_populates="scores")

