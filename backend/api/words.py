from flask_restful import Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Word
from utils.jwt_utils import verify_token
from flask import request
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
database_path = os.path.join(project_root, 'database', 'vocab.db')

engine = create_engine(f'sqlite:///{database_path}')
Session = sessionmaker(bind=engine)


class WordList(Resource):
    def get(self):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        # 普通用户也可以访问词库
        session = Session()
        words = session.query(Word).all()
        session.close()

        return [{
            'word': word.word,
            'phonetic': word.phonetic,
            'meaning': word.meaning,
            'difficulty': word.difficulty
        } for word in words], 200
