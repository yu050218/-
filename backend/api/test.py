from flask_restful import Resource, reqparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Word, TestRecord
from utils.jwt_utils import verify_token
from flask import request
import random

engine = create_engine('sqlite:///../database/vocab.db')
Session = sessionmaker(bind=engine)

# 测试会话管理
test_sessions = {}


class TestStart(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('test_type', required=True, help='Test type is required')  # 30 or 50
        args = parser.parse_args()

        test_type = args['test_type']
        total_questions = 30 if test_type == '30' else 50

        # 生成测试会话ID
        session_id = str(random.randint(100000, 999999))

        # 初始化测试会话
        test_sessions[session_id] = {
            'total_questions': total_questions,
            'current_question': 0,
            'correct_count': 0,
            'answers': [],
            'difficulty': 'medium'
        }

        # 获取第一个问题
        session = Session()
        words = session.query(Word).filter_by(difficulty='medium').all()
        session.close()

        if not words:
            return {'message': 'No words available for testing'}, 500

        word = random.choice(words)

        return {
            'session_id': session_id,
            'question': {
                'id': word.id,
                'word': word.word,
                'phonetic': word.phonetic,
                'meaning': word.meaning
            },
            'current_question': 1,
            'total_questions': total_questions
        }, 200


class TestSubmit(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True, help='Session ID is required')
        parser.add_argument('word_id', required=True, help='Word ID is required')
        parser.add_argument('answer', required=True, help='Answer is required')  # true or false
        args = parser.parse_args()

        session_id = args['session_id']
        word_id = args['word_id']
        answer = args['answer'] == 'true'

        # 检查会话是否存在
        if session_id not in test_sessions:
            return {'message': 'Invalid session ID'}, 400

        session_data = test_sessions[session_id]
        session_data['current_question'] += 1

        # 检查答案是否正确
        session = Session()
        word = session.query(Word).filter_by(id=word_id).first()
        session.close()

        if not word:
            return {'message': 'Word not found'}, 404

        is_correct = answer
        if is_correct:
            session_data['correct_count'] += 1

        session_data['answers'].append({'word_id': word_id, 'correct': is_correct})

        # 调整难度
        if session_data['current_question'] <= session_data['total_questions']:
            correct_rate = session_data['correct_count'] / session_data['current_question']
            difficulty = adjust_difficulty(correct_rate)
            session_data['difficulty'] = difficulty

            # 获取下一个问题
            session = Session()
            words = session.query(Word).filter_by(difficulty=difficulty).all()
            session.close()

            if not words:
                return {'message': 'No words available for testing'}, 500

            word = random.choice(words)

            return {
                'question': {
                    'id': word.id,
                    'word': word.word,
                    'phonetic': word.phonetic,
                    'meaning': word.meaning
                },
                'current_question': session_data['current_question'],
                'total_questions': session_data['total_questions'],
                'is_correct': is_correct
            }, 200
        else:
            # 测试完成，计算词汇量
            correct_rate = session_data['correct_count'] / session_data['total_questions']
            vocabulary_size = estimate_vocabulary_size(correct_rate, session_data['difficulty'])
            level = get_vocabulary_level(vocabulary_size)

            # 保存测试记录（如果用户已登录）
            auth_header = request.headers.get('Authorization')
            if auth_header:
                token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
                user_id = verify_token(token)
                if user_id:
                    session = Session()
                    test_record = TestRecord(
                        user_id=user_id,
                        correct_count=session_data['correct_count'],
                        total_count=session_data['total_questions'],
                        vocabulary_size=vocabulary_size,
                        level=level
                    )
                    session.add(test_record)
                    session.commit()
                    session.close()

            # 删除会话
            del test_sessions[session_id]

            return {
                'result': {
                    'correct_count': session_data['correct_count'],
                    'total_count': session_data['total_questions'],
                    'correct_rate': correct_rate,
                    'vocabulary_size': vocabulary_size,
                    'level': level
                }
            }, 200


class TestRecord(Resource):
    def get(self):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        session = Session()
        records = session.query(TestRecord).filter_by(user_id=user_id).order_by(TestRecord.test_date.desc()).all()
        session.close()

        return [{
            'id': record.id,
            'test_date': record.test_date,
            'correct_count': record.correct_count,
            'total_count': record.total_count,
            'vocabulary_size': record.vocabulary_size,
            'level': record.level
        } for record in records], 200


def adjust_difficulty(correct_rate):
    if correct_rate > 0.7:
        return "hard"
    elif correct_rate < 0.4:
        return "easy"
    return "medium"


def estimate_vocabulary_size(correct_rate, difficulty):
    # 简单的词汇量估算逻辑
    base_size = {
        'easy': 1000,
        'medium': 3000,
        'hard': 6000
    }
    return int(base_size[difficulty] * (correct_rate * 1.5 + 0.5))


def get_vocabulary_level(vocabulary_size):
    if vocabulary_size < 1000:
        return "Beginner"
    elif vocabulary_size < 3000:
        return "Intermediate"
    elif vocabulary_size < 6000:
        return "Advanced"
    else:
        return "Expert"