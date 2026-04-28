from flask_restful import Resource, reqparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import TestRecord, WrongWord
from utils.jwt_utils import verify_token
from utils.excel_reader import get_assessment_words, get_distractors
from flask import request
import random
from datetime import datetime
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 从 api 目录向上两级到达项目根目录
project_root = os.path.dirname(os.path.dirname(current_dir))
# 构建数据库文件路径
database_path = os.path.join(project_root, 'database', 'vocab.db')

engine = create_engine(f'sqlite:///{database_path}')
Session = sessionmaker(bind=engine)

# 测试会话管理
test_sessions = {}


class TestStart(Resource):
    def post(self):
        try:
            # 打印请求信息
            print(f"Request method: {request.method}")
            print(f"Request headers: {dict(request.headers)}")
            print(f"Request data: {request.data}")
            print(f"Request json: {request.json}")

            # 直接从request.json获取数据，而不是使用reqparse
            # 允许空JSON对象
            if request.json is None:
                return {'message': 'No JSON data provided'}, 400

            # 生成测试会话ID
            session_id = str(random.randint(100000, 999999))

            # 获取测评单词列表
            print("Loading assessment words...")
            assessment_words = get_assessment_words()
            print(f"Loaded {len(assessment_words)} assessment words")
            if not assessment_words:
                return {'message': 'No words available for testing'}, 500

            # 初始化测试会话
            test_sessions[session_id] = {
                'total_questions': 50,
                'current_question': 0,
                'correct_count': 0,
                'answers': [],
                'consecutive_wrong': 0,
                'total_wrong': 0,
                'assessment_words': assessment_words,
                'word_index': 0
            }

            # 获取第一个问题
            print("Generating first question...")
            question = generate_question(assessment_words[0])
            print(f"Generated question: {question['word']}")
            # 存储第一个问题到会话数据中
            test_sessions[session_id]['current_question_data'] = question

            return {
                'session_id': session_id,
                'question': question,
                'current_question': 1,
                'total_questions': 50
            }, 200
        except Exception as e:
            print(f"Error in TestStart: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'message': f'Internal server error: {str(e)}'}, 500


class TestSubmit(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True, help='Session ID is required')
        parser.add_argument('word', required=True, help='Word is required')
        parser.add_argument('answer', required=True, help='Answer is required')  # option index or 'unknown'
        args = parser.parse_args()

        session_id = args['session_id']
        word = args['word']
        answer = args['answer']

        # 检查会话是否存在
        if session_id not in test_sessions:
            return {'message': 'Invalid session ID'}, 400

        session_data = test_sessions[session_id]
        session_data['current_question'] += 1

        # 检查答案是否正确
        is_correct = False
        if answer != 'unknown':
            # 从会话中获取当前问题的正确答案
            current_question = session_data.get('current_question_data')
            if current_question:
                is_correct = int(answer) == current_question['correct_index']
                if is_correct:
                    session_data['correct_count'] += 1
                    session_data['consecutive_wrong'] = 0
                    # 如果用户答对，且已登录，更新错题本
                    auth_header = request.headers.get('Authorization')
                    if auth_header:
                        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
                        user_id = verify_token(token)
                        if user_id:
                            session = Session()
                            # 检查错题是否已经存在
                            existing_wrong_word = session.query(WrongWord).filter_by(
                                user_id=user_id,
                                word=current_question['word']
                            ).first()
                            if existing_wrong_word:
                                # 如果错题已存在，增加正确次数
                                existing_wrong_word.correct_count += 1
                                existing_wrong_word.last_correct_date = datetime.now()
                                # 如果答对次数达到10次，从错题本中移除
                                if existing_wrong_word.correct_count >= 10:
                                    session.delete(existing_wrong_word)
                                session.commit()
                            session.close()
                else:
                    session_data['consecutive_wrong'] += 1
                    session_data['total_wrong'] += 1
                    # 如果用户答错，且已登录，将错题添加到错题本
                    auth_header = request.headers.get('Authorization')
                    if auth_header:
                        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
                        user_id = verify_token(token)
                        if user_id:
                            session = Session()
                            # 检查错题是否已经存在
                            existing_wrong_word = session.query(WrongWord).filter_by(
                                user_id=user_id,
                                word=current_question['word']
                            ).first()
                            if existing_wrong_word:
                                # 如果错题已存在，增加错误次数
                                existing_wrong_word.wrong_count += 1
                                existing_wrong_word.last_wrong_date = datetime.now()
                            else:
                                # 如果错题不存在，添加新记录
                                wrong_word = WrongWord(
                                    user_id=user_id,
                                    word=current_question['word'],
                                    phonetic=current_question['phonetic'],
                                    meaning=current_question['options'][current_question['correct_index']],
                                    difficulty='medium',  # 暂时设置为中等难度
                                    wrong_count=1,
                                    correct_count=0,
                                    last_wrong_date=datetime.now(),
                                    last_correct_date=datetime.now()
                                )
                                session.add(wrong_word)
                            session.commit()
                            session.close()
        else:
            # 用户选择了"不认识"
            session_data['consecutive_wrong'] += 1
            session_data['total_wrong'] += 1
            # 如果用户选择"不认识"，且已登录，将该单词添加到错题本
            auth_header = request.headers.get('Authorization')
            if auth_header:
                token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
                user_id = verify_token(token)
                if user_id:
                    current_question = session_data.get('current_question_data')
                    if current_question:
                        session = Session()
                        # 检查错题是否已经存在
                        existing_wrong_word = session.query(WrongWord).filter_by(
                            user_id=user_id,
                            word=current_question['word']
                        ).first()
                        if existing_wrong_word:
                            # 如果错题已存在，增加错误次数
                            existing_wrong_word.wrong_count += 1
                            existing_wrong_word.last_wrong_date = datetime.now()
                        else:
                            # 如果错题不存在，添加新记录
                            wrong_word = WrongWord(
                                user_id=user_id,
                                word=current_question['word'],
                                phonetic=current_question['phonetic'],
                                meaning=current_question['options'][current_question['correct_index']],
                                difficulty='medium',  # 暂时设置为中等难度
                                wrong_count=1,
                                last_wrong_date=datetime.now()
                            )
                            session.add(wrong_word)
                        session.commit()
                        session.close()

        session_data['answers'].append({'word': word, 'correct': is_correct, 'answer': answer})

        # 检查结束条件
        if (
            session_data['current_question'] >= 50 or  # 完成50个单词
            session_data['consecutive_wrong'] >= 4 or  # 连续答错4个
            session_data['total_wrong'] >= 7  # 累计答错7个
        ):
            # 测试完成，计算词汇量和水平
            result = calculate_assessment_result(session_data)
            
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
                        total_count=session_data['current_question'],
                        vocabulary_size=result['vocabulary_size'],
                        level=result['level']
                    )
                    session.add(test_record)
                    session.commit()
                    session.close()

            # 删除会话
            del test_sessions[session_id]

            # 打印返回结果，以便调试
            print(f"Test completed. Result: {result}")
            
            return {
                'result': result
            }, 200
        else:
            # 获取下一个问题
            session_data['word_index'] += 1
            if session_data['word_index'] < len(session_data['assessment_words']):
                next_word = session_data['assessment_words'][session_data['word_index']]
                question = generate_question(next_word)
                session_data['current_question_data'] = question

                return {
                    'question': question,
                    'current_question': session_data['current_question'],
                    'total_questions': 50,
                    'is_correct': is_correct,
                    'total_wrong': session_data['total_wrong'],
                    'consecutive_wrong': session_data['consecutive_wrong']
                }, 200
            else:
                # 单词列表用完了，结束测试
                result = calculate_assessment_result(session_data)
                
                # 保存测试记录（如果用户已登录）
                auth_header = request.headers.get('Authorization')
                print(f"Auth header: {auth_header}")
                if auth_header:
                    try:
                        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
                        print(f"Token: {token}")
                        user_id = verify_token(token)
                        print(f"User ID: {user_id}")
                        if user_id:
                            session = Session()
                            test_record = TestRecord(
                                user_id=user_id,
                                correct_count=session_data['correct_count'],
                                total_count=session_data['current_question'],
                                vocabulary_size=result['vocabulary_size'],
                                level=result['level']
                            )
                            session.add(test_record)
                            session.commit()
                            print(f"Test record saved for user {user_id}")
                            session.close()
                        else:
                            print("Invalid user ID from token")
                    except Exception as e:
                        print(f"Error saving test record: {e}")
                else:
                    print("No authorization header found")

                # 删除会话
                del test_sessions[session_id]

                return {
                    'result': result
                }, 200


class TestRecordResource(Resource):
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
            'test_date': record.test_date.isoformat() if record.test_date else None,
            'correct_count': record.correct_count,
            'total_count': record.total_count,
            'vocabulary_size': record.vocabulary_size,
            'level': record.level
        } for record in records], 200


class WrongWords(Resource):
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
        wrong_words = session.query(WrongWord).filter_by(user_id=user_id).order_by(WrongWord.last_wrong_date.desc()).all()
        session.close()

        return [{
            'id': word.id,
            'word': word.word,
            'phonetic': word.phonetic,
            'meaning': word.meaning,
            'difficulty': word.difficulty,
            'wrong_count': word.wrong_count,
            'correct_count': word.correct_count,
            'last_wrong_date': word.last_wrong_date.isoformat() if word.last_wrong_date else None,
            'last_correct_date': word.last_correct_date.isoformat() if word.last_correct_date else None
        } for word in wrong_words], 200
    
    def post(self):
        # 添加新的错题
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        data = request.get_json()
        if not data:
            return {'message': 'No JSON data provided'}, 400

        word = data.get('word')
        phonetic = data.get('phonetic')
        meaning = data.get('meaning')

        if not word or not meaning:
            return {'message': 'Word and meaning are required'}, 400

        session = Session()
        # 检查单词是否已经在错题本中
        existing_word = session.query(WrongWord).filter_by(
            user_id=user_id,
            word=word
        ).first()

        if existing_word:
            # 如果已存在，增加错误计数
            existing_word.wrong_count += 1
            existing_word.last_wrong_date = datetime.now()
        else:
            # 如果不存在，创建新的错题记录
            new_wrong_word = WrongWord(
                user_id=user_id,
                word=word,
                phonetic=phonetic or '',
                meaning=meaning,
                difficulty='unknown',
                wrong_count=1,
                correct_count=0,
                last_wrong_date=datetime.now()
            )
            session.add(new_wrong_word)

        session.commit()
        session.close()

        return {'message': 'Word added to wrong words successfully'}, 200


class ReviewSubmit(Resource):
    def post(self):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {'message': 'Authorization header is required'}, 401

            token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
            user_id = verify_token(token)
            if not user_id:
                return {'message': 'Invalid or expired token'}, 401

            data = request.get_json()
            if not data:
                return {'message': 'No JSON data provided'}, 400

            word = data.get('word')
            is_correct = data.get('is_correct')

            if word is None or is_correct is None:
                return {'message': 'Word and is_correct are required'}, 400

            session = Session()
            wrong_word = session.query(WrongWord).filter_by(
                user_id=user_id,
                word=word
            ).first()

            if wrong_word:
                if is_correct:
                    wrong_word.correct_count += 1
                    wrong_word.last_correct_date = datetime.now()
                    if wrong_word.correct_count >= 10:
                        session.delete(wrong_word)
                else:
                    wrong_word.wrong_count += 1
                    wrong_word.last_wrong_date = datetime.now()
                session.commit()
                session.close()
            else:
                session.close()
                return {'message': 'Word not found in wrong words'}, 404

            return {'message': 'Review answer submitted successfully'}, 200
        except Exception as e:
            print(f"Error in ReviewSubmit: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'message': f'Internal server error: {str(e)}'}, 500


def generate_question(correct_word):
    # 获取迷惑选项
    distractors = get_distractors(correct_word['word'])
    
    # 构建选项列表（只包含正确选项和5个迷惑选项）
    options = [correct_word['meaning']] + [d['meaning'] for d in distractors]
    
    # 随机打乱选项顺序
    random.shuffle(options)
    
    # 记录正确选项的索引
    correct_index = options.index(correct_word['meaning'])
    
    return {
        'word': correct_word['word'],
        'phonetic': correct_word['phonetic'],
        'options': options,
        'correct_index': correct_index
    }

def calculate_assessment_result(session_data):
    # 计算正确率
    correct_count = session_data['correct_count']
    total_count = session_data['current_question']
    correct_rate = correct_count / total_count if total_count > 0 else 0
    
    # 计算水平评估
    if correct_count <= 10:
        level = "入门级"
    elif correct_count <= 20:
        level = "小学水平"
    elif correct_count <= 30:
        level = "初中水平"
    elif correct_count <= 40:
        level = "高中水平"
    else:
        level = "优秀水平"
    
    # 计算词汇量
    # 假设各学段各难度级别的词汇量
    vocabulary_base = {
        'primary_1': 500,
        'primary_2': 1000,
        'primary_3': 1500,
        'middle_1': 2000,
        'middle_2': 3000,
        'middle_3': 4000,
        'high_1': 5000,
        'high_2': 6000,
        'high_3': 7000
    }
    
    # 计算各学段各难度的掌握率
    mastery_rates = {}
    for word in session_data['assessment_words'][:total_count]:
        difficulty = word['difficulty']
        if difficulty not in mastery_rates:
            mastery_rates[difficulty] = {'correct': 0, 'total': 0}
        mastery_rates[difficulty]['total'] += 1
    
    # 统计答对的单词
    for i, answer in enumerate(session_data['answers']):
        if i >= len(session_data['assessment_words']):
            break
        word = session_data['assessment_words'][i]
        difficulty = word['difficulty']
        if answer['correct']:
            mastery_rates[difficulty]['correct'] += 1
    
    # 计算词汇量
    total_vocabulary = 0
    for difficulty, stats in mastery_rates.items():
        if stats['total'] > 0:
            mastery_rate = stats['correct'] / stats['total']
            # 获取学段
            level = difficulty.split('_')[0]
            # 获取权重
            if level == 'primary':
                weight = 1.25
            else:
                weight = 1.1
            # 计算该难度的词汇量
            base_size = vocabulary_base.get(difficulty, 1000)
            total_vocabulary += base_size * mastery_rate * weight
    
    # 计算教育水平
    if total_vocabulary < 1000:
        education_level = "小学"
    elif total_vocabulary < 3000:
        education_level = "初中"
    elif total_vocabulary < 6000:
        education_level = "高中"
    else:
        education_level = "大学及以上"
    
    # 生成学习建议
    study_suggestions = get_study_suggestions(correct_count, total_vocabulary)
    
    return {
        'correct_count': correct_count,
        'total_count': total_count,
        'correct_rate': correct_rate,
        'vocabulary_size': int(total_vocabulary),
        'level': level,
        'education_level': education_level,
        'study_suggestions': study_suggestions
    }

def get_study_suggestions(correct_count, vocabulary_size):
    if correct_count <= 10:
        return [
            "建议从基础词汇开始学习",
            "重点掌握小学考纲中的核心词汇",
            "每天学习10-15个新单词",
            "多进行基础词汇的听力和口语练习"
        ]
    elif correct_count <= 20:
        return [
            "建议加强小学词汇的巩固",
            "开始学习初中考纲中的基础词汇",
            "每天学习15-20个新单词",
            "多进行简单的阅读练习"
        ]
    elif correct_count <= 30:
        return [
            "建议巩固初中词汇",
            "开始学习高中考纲中的基础词汇",
            "每天学习20-25个新单词",
            "多进行中等难度的阅读练习"
        ]
    elif correct_count <= 40:
        return [
            "建议巩固高中词汇",
            "开始学习大学英语基础词汇",
            "每天学习25-30个新单词",
            "多进行高级阅读和写作练习"
        ]
    else:
        return [
            "建议继续扩大词汇量",
            "重点学习专业词汇和学术词汇",
            "每天学习30-35个新单词",
            "多进行学术阅读和写作练习"
        ]
