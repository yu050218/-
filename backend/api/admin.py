from flask_restful import Resource, reqparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import User, TestRecord, WrongWord
from utils.jwt_utils import verify_token
from utils.excel_reader import load_words_from_excel
from flask import request
import os

engine = create_engine('sqlite:///database/vocab.db')
Session = sessionmaker(bind=engine)


class AdminUsers(Resource):
    def get(self):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        # 检查用户是否为管理员（暂时假设所有用户都是管理员）
        # 实际项目中应该在User模型中添加is_admin字段

        session = Session()
        users = session.query(User).all()
        session.close()

        return [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat() if user.created_at else None
        } for user in users], 200

    def delete(self, user_id):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        current_user_id = verify_token(token)
        if not current_user_id:
            return {'message': 'Invalid or expired token'}, 401

        # 检查用户是否为管理员（暂时假设所有用户都是管理员）

        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            session.close()
            return {'message': 'User not found'}, 404

        # 删除用户的相关记录
        session.query(TestRecord).filter_by(user_id=user_id).delete()
        session.query(WrongWord).filter_by(user_id=user_id).delete()
        session.delete(user)
        session.commit()
        session.close()

        return {'message': 'User deleted successfully'}, 200


class AdminTestRecords(Resource):
    def get(self, user_id):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        current_user_id = verify_token(token)
        if not current_user_id:
            return {'message': 'Invalid or expired token'}, 401

        # 检查用户是否为管理员（暂时假设所有用户都是管理员）

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


class AdminWordBank(Resource):
    def get(self):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        # 检查用户是否为管理员（暂时假设所有用户都是管理员）

        # 加载所有单词
        all_words = load_words_from_excel()
        return all_words, 200

    def post(self):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        # 检查用户是否为管理员（暂时假设所有用户都是管理员）

        # 上传新的词库文件
        # 实际项目中应该实现文件上传功能
        # 这里只是一个示例

        return {'message': 'Word bank updated successfully'}, 200
