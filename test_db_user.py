import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from backend.models.models import User, Base

# 获取数据库路径
project_root = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(project_root, 'database', 'vocab.db')

print(f"数据库路径: {database_path}")
print(f"数据库文件存在: {os.path.exists(database_path)}")

# 创建SQLite数据库引擎
engine = create_engine(f'sqlite:///{database_path}')
Session = sessionmaker(bind=engine)
session = Session()

try:
    # 测试创建用户
    username = 'testuser_db'
    email = 'test_db@example.com'
    password = 'password123'
    
    print(f"\n尝试创建用户: {username}")
    
    # 检查用户名是否已存在
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print(f"用户已存在: {username}")
        session.close()
        sys.exit(0)
    
    # 创建新用户
    password_hash = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    
    session.add(new_user)
    session.commit()
    print(f"用户创建成功! 用户ID: {new_user.id}")
    
    # 验证用户是否创建成功
    created_user = session.query(User).filter_by(username=username).first()
    if created_user:
        print(f"验证成功! 用户名: {created_user.username}, 邮箱: {created_user.email}")
    
    session.close()
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    session.close()
