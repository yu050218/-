from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(50), nullable=False)
    phonetic = Column(String(100))
    meaning = Column(String(200), nullable=False)
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard


class TestRecord(Base):
    __tablename__ = 'test_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    test_date = Column(DateTime(timezone=True), server_default=func.now())
    correct_count = Column(Integer, nullable=False)
    total_count = Column(Integer, nullable=False)
    vocabulary_size = Column(Integer, nullable=False)
    level = Column(String(20), nullable=False)