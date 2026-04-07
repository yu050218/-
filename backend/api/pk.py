from flask_restful import Resource, reqparse
from utils.jwt_utils import verify_token
from flask import request
import random

# 匹配队列
match_queue = []
# 活跃对战
active_matches = {}


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

        # 检查用户是否已在队列中
        if user_id in match_queue:
            return {'message': 'You are already in the match queue'}, 400

        # 将用户加入匹配队列
        match_queue.append(user_id)

        # 检查是否有其他用户在队列中
        if len(match_queue) >= 2:
            # 匹配成功，创建对战
            player1 = match_queue.pop(0)
            player2 = match_queue.pop(0)

            # 生成对战ID
            match_id = str(random.randint(100000, 999999))

            # 初始化对战
            active_matches[match_id] = {
                'player1': player1,
                'player2': player2,
                'score1': 0,
                'score2': 0,
                'current_round': 0,
                'max_rounds': 10,
                'status': 'active'  # active, finished
            }

            return {
                'message': 'Match found',
                'match_id': match_id,
                'opponent_id': player2 if user_id == player1 else player1
            }, 200
        else:
            return {'message': 'Waiting for opponent...'}, 202

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('match_id', required=True, help='Match ID is required')
        parser.add_argument('action', required=True, help='Action is required')  # join, leave, submit
        parser.add_argument('answer', required=False)  # true or false
        args = parser.parse_args()

        match_id = args['match_id']
        action = args['action']

        # 检查对战是否存在
        if match_id not in active_matches:
            return {'message': 'Match not found'}, 404

        match = active_matches[match_id]

        if action == 'submit':
            # 处理提交答案
            answer = args['answer'] == 'true'
            # 简单的得分逻辑
            if answer:
                # 假设当前玩家是player1
                match['score1'] += 1
            match['current_round'] += 1

            # 检查是否结束
            if match['current_round'] >= match['max_rounds']:
                match['status'] = 'finished'
                winner = match['player1'] if match['score1'] > match['score2'] else match['player2']
                return {
                    'status': 'finished',
                    'score1': match['score1'],
                    'score2': match['score2'],
                    'winner': winner
                }, 200
            else:
                return {
                    'status': 'active',
                    'current_round': match['current_round'],
                    'score1': match['score1'],
                    'score2': match['score2']
                }, 200
        elif action == 'leave':
            # 处理离开对战
            del active_matches[match_id]
            return {'message': 'Match left'}, 200
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
            'current_round': match['current_round'],
            'max_rounds': match['max_rounds'],
            'status': match['status']
        }, 200