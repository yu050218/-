from flask_restful import Resource, reqparse
from utils.jwt_utils import verify_token
from utils.excel_reader import load_words_from_excel
from flask import request
import random
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import WrongWord
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

# 匹配队列，存储用户ID和加入时间
match_queue = []
# 活跃对战
active_matches = {}
# 匹配超时时间（秒）
MATCH_TIMEOUT = 10


class PKMatch(Resource):
    def post(self):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        # 检查用户是否已在队列中，如果在则移除
        match_queue[:] = [item for item in match_queue if item['user_id'] != user_id]

        # 检查用户是否已在活跃对战中，如果在则移除旧的对战
        for match_id, match in list(active_matches.items()):
            if match['player1'] == user_id or match['player2'] == user_id:
                print(f"Removing stale match {match_id} for user {user_id}")
                del active_matches[match_id]

        # 清理超时的队列项
        self.cleanup_timeout_queue()

        # 检查是否有其他用户在队列中
        if match_queue:
            # 匹配成功，创建对战
            other_user = match_queue.pop(0)
            player1 = other_user['user_id']
            player2 = user_id
            print(f"Match found between {player1} and {player2}")

            # 生成对战ID
            match_id = str(random.randint(100000, 999999))

            # 加载词汇数据
            words = load_words_from_excel()
            if not words:
                return {'message': 'No words available for PK'}, 500

            # 初始化对战
            active_matches[match_id] = {
                'player1': player1,
                'player2': player2,
                'score1': 0,
                'score2': 0,
                'time1': 0,  # 玩家1总用时
                'time2': 0,  # 玩家2/AI总用时
                'current_round': 0,
                'max_rounds': 10,
                'status': 'active',  # active, finished
                'words': words,
                'current_word': None,
                'is_ai_match': False
            }

            # 生成第一个问题
            question = generate_pk_question(words)
            active_matches[match_id]['current_word'] = question

            return {
                'message': 'Match found',
                'match_id': match_id,
                'opponent_id': player2 if user_id == player1 else player1,
                'question': question,
                'time1': 0,
                'time2': 0
            }, 200
        else:
            # 没有其他用户，安排人机对战
            print(f"No opponents found, creating AI match for user {user_id}")

            # 生成对战ID
            match_id = str(random.randint(100000, 999999))

            # 加载词汇数据
            words = load_words_from_excel()
            if not words:
                return {'message': 'No words available for PK'}, 500

            # 初始化对战
            active_matches[match_id] = {
                'player1': user_id,
                'player2': 'AI',  # AI对手
                'score1': 0,
                'score2': 0,
                'time1': 0,  # 玩家总用时
                'time2': 0,  # AI总用时
                'current_round': 0,
                'max_rounds': 10,
                'status': 'active',  # active, finished
                'words': words,
                'current_word': None,
                'is_ai_match': True
            }

            # 生成第一个问题
            question = generate_pk_question(words)
            active_matches[match_id]['current_word'] = question

            return {
                'message': 'No opponents found, matched with AI',
                'match_id': match_id,
                'opponent_id': 'AI',
                'question': question,
                'time1': 0,
                'time2': 0
            }, 200

    def cleanup_timeout_queue(self):
        """清理超时的队列项"""
        current_time = time.time()
        global match_queue
        match_queue = [item for item in match_queue if current_time - item['join_time'] < MATCH_TIMEOUT]

    def put(self):
        print("=== PKMatch.put called ===")
        print(f"Request method: {request.method}")
        print(f"Request path: {request.path}")
        data = request.get_json() or {}
        print(f"Request data: {data}")
        
        match_id = data.get('match_id')
        action = data.get('action')
        answer = data.get('answer')
        time_spent = data.get('time_spent', 0)

        print(f"Parsed params - match_id: {match_id}, action: {action}, answer: {answer}, time_spent: {time_spent}")

        if not match_id:
            return {'message': 'Match ID is required'}, 400
        
        if not action:
            return {'message': 'Action is required'}, 400

        # 如果是离开操作，先获取用户ID
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401
        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        # 处理离开操作
        if action == 'leave':
            # 从队列中移除
            match_queue[:] = [item for item in match_queue if item['user_id'] != user_id]

            # 从活跃对战中移除
            for mid, match in list(active_matches.items()):
                if match['player1'] == user_id or match['player2'] == user_id:
                    del active_matches[mid]
                    return {'message': 'Match left'}, 200

            return {'message': 'No active match found'}, 200

        # 检查对战是否存在
        if match_id not in active_matches:
            return {'message': 'Match not found'}, 404

        match = active_matches[match_id]

        if action == 'submit':
            # 检查用户是否是对战的参与者
            if user_id != match['player1']:
                return {'message': 'You are not a participant in this match'}, 403

            print(f"=== Submit action received ===")
            print(f"match_id: {match_id}")
            print(f"answer: {answer}")
            print(f"time_spent: {time_spent}")
            print(f"is_ai_match: {match.get('is_ai_match')}")
            print(f"current time1: {match['time1']}")
            print(f"current time2: {match['time2']}")

            # 处理提交答案（answer 和 time_spent 已从请求体获取）
            is_correct = False
            if answer != 'unknown':
                is_correct = int(answer) == match['current_word']['correct_index']

            # 更新用户用时
            match['time1'] += time_spent

            # 如果用户答错，将错题添加到错题本
            if not is_correct:
                session = Session()
                # 检查错题是否已经存在
                existing_wrong_word = session.query(WrongWord).filter_by(
                    user_id=user_id,
                    word=match['current_word']['word']
                ).first()
                if existing_wrong_word:
                    # 如果错题已存在，增加错误次数
                    existing_wrong_word.wrong_count += 1
                    existing_wrong_word.last_wrong_date = datetime.now()
                else:
                    # 如果错题不存在，添加新记录
                    wrong_word = WrongWord(
                        user_id=user_id,
                        word=match['current_word']['word'],
                        phonetic=match['current_word']['phonetic'],
                        meaning=match['current_word']['options'][match['current_word']['correct_index']],
                        difficulty='medium',  # 暂时设置为中等难度
                        wrong_count=1,
                        last_wrong_date=datetime.now()
                    )
                    session.add(wrong_word)
                session.commit()
                session.close()

            # 更新得分
            if is_correct:
                match['score1'] += 1

            # AI对手的回答
            if match['is_ai_match']:
                # AI有80%的概率答对
                ai_correct = random.random() < 0.8
                if ai_correct:
                    match['score2'] += 1
                # AI用时（随机1-3秒）
                ai_time = random.randint(1, 3)
                match['time2'] += ai_time
                print(f"AI time added: {ai_time}, total AI time: {match['time2']}")

            match['current_round'] += 1

            # 检查是否结束
            if match['current_round'] >= match['max_rounds']:
                match['status'] = 'finished'
                
                # 判定胜负：先比较得分，得分相同则比较用时
                if match['score1'] > match['score2']:
                    winner = match['player1']
                elif match['score2'] > match['score1']:
                    winner = match['player2']
                else:
                    # 得分相同，用时较短的获胜
                    if match['time1'] < match['time2']:
                        winner = match['player1']
                    elif match['time2'] < match['time1']:
                        winner = match['player2']
                    else:
                        winner = None  # 完全平局
                
                return {
                    'status': 'finished',
                    'score1': match['score1'],
                    'score2': match['score2'],
                    'time1': match['time1'],
                    'time2': match['time2'],
                    'winner': winner,
                    'is_ai_match': match['is_ai_match']
                }, 200
            else:
                # 生成下一个问题
                question = generate_pk_question(match['words'])
                match['current_word'] = question
                return {
                    'status': 'active',
                    'current_round': match['current_round'],
                    'score1': match['score1'],
                    'score2': match['score2'],
                    'time2': match['time2'],
                    'question': question,
                    'is_correct': is_correct
                }, 200
        else:
            return {'message': 'Invalid action'}, 400




class PKStatus(Resource):
    def get(self, match_id):
        # 检查对战是否存在
        if match_id not in active_matches:
            return {'message': 'Match not found'}, 404

        match = active_matches[match_id]
        return {
            'match_id': match_id,
            'player1': match['player1'],
            'player2': match['player2'],
            'score1': match['score1'],
            'score2': match['score2'],
            'time1': match['time1'],
            'time2': match['time2'],
            'current_round': match['current_round'],
            'max_rounds': match['max_rounds'],
            'status': match['status'],
            'current_word': match.get('current_word')
        }, 200


def generate_pk_question(words):
    # 随机选择一个单词作为正确答案
    correct_word = random.choice(words)

    # 获取迷惑选项
    distractors = get_distractors(correct_word['word'])

    # 构建选项列表
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

def get_distractors(correct_word, count=3):
    words = load_words_from_excel()
    # 过滤掉正确答案
    distractors = [word for word in words if word['word'] != correct_word]
    # 随机选择count个
    return random.sample(distractors, min(count, len(distractors)))
