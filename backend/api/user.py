from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import User
from utils.jwt_utils import generate_token, verify_token
from flask import request
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 从 api 目录向上两级到达项目根目录
project_root = os.path.dirname(os.path.dirname(current_dir))
# 构建数据库文件路径
database_path = os.path.join(project_root, 'database', 'vocab.db')

print(f"[DEBUG] Database path: {database_path}")
print(f"[DEBUG] Database exists: {os.path.exists(database_path)}")

engine = create_engine(f'sqlite:///{database_path}')
Session = sessionmaker(bind=engine)


class UserRegister(Resource):
    def post(self):
        print("[DEBUG] UserRegister POST called")
        print(f"[DEBUG] request.data: {request.data}")
        print(f"[DEBUG] request.content_type: {request.content_type}")
        
        try:
            # 使用 request.json 来获取 JSON 请求体
            data = request.json
            print(f"[DEBUG] request.json result: {data}")
            
            if data is None:
                print("[DEBUG] JSON data is None")
                return {'message': 'Invalid JSON data'}, 400

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            print(f"[DEBUG] Register attempt: username={username}, email={email}")

            if not username or not email or not password:
                return {'message': 'Username, email, and password are required'}, 400

            session = Session()
            print("[DEBUG] Session created")
            
            # 检查用户名是否已存在
            if session.query(User).filter_by(username=username).first():
                session.close()
                return {'message': 'Username already exists'}, 400
            # 检查邮箱是否已存在
            if session.query(User).filter_by(email=email).first():
                session.close()
                return {'message': 'Email already exists'}, 400

            # 创建新用户
            password_hash = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash
            )
            session.add(new_user)
            session.commit()
            session.close()

            print(f"[DEBUG] User registered successfully: {username}")
            return {'message': 'User registered successfully'}, 201
        except Exception as e:
            print(f"[DEBUG] Registration error: {e}")
            import traceback
            traceback.print_exc()
            return {'message': 'Internal Server Error'}, 500


class UserLogin(Resource):
    def post(self):
        try:
            # 使用 request.json 来获取 JSON 请求体
            data = request.json
            if data is None:
                return {'message': 'Invalid JSON data'}, 400

            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'message': 'Username and password are required'}, 400

            session = Session()
            user = session.query(User).filter_by(username=username).first()
            session.close()

            if not user or not check_password_hash(user.password_hash, password):
                return {'message': 'Invalid username or password'}, 401

            # 生成JWT令牌
            token = generate_token(user.id)
            return {'token': token, 'user_id': user.id, 'username': user.username, 'is_admin': user.is_admin}, 200
        except Exception as e:
            print(f"[DEBUG] Login error: {e}")
            import traceback
            traceback.print_exc()
            return {'message': 'Internal Server Error'}, 500


class UserProfile(Resource):
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
        user = session.query(User).filter_by(id=user_id).first()
        session.close()

        if not user:
            return {'message': 'User not found'}, 404

        print(f"[DEBUG] User data: id={user.id}, username={user.username}, email={user.email}, created_at={user.created_at}")
        try:
            created_at_str = user.created_at.isoformat() if user.created_at else None
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': created_at_str
            }, 200
        except Exception as e:
            print(f"[DEBUG] Error formatting user data: {e}")
            return {'message': 'Error formatting user data'}, 500

    def put(self):
        # 从请求头获取JWT令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is required'}, 401

        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else auth_header
        user_id = verify_token(token)
        if not user_id:
            return {'message': 'Invalid or expired token'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('email', required=False)
        parser.add_argument('password', required=False)
        args = parser.parse_args()

        session = Session()
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            session.close()
            return {'message': 'User not found'}, 404

        # 更新用户信息
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.password_hash = generate_password_hash(args['password'])

        session.commit()
        session.close()

        return {'message': 'Profile updated successfully'}, 200