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

# 创建SQLite数据库引擎
engine = create_engine(f'sqlite:///{database_path}')
Session = sessionmaker(bind=engine)
session = Session()

try:
    # 检查是否已有管理员
    admin_user = session.query(User).filter_by(username='admin').first()
    if admin_user:
        print("管理员账户已存在，更新密码...")
        admin_user.password_hash = generate_password_hash('admin123')
    else:
        print("创建管理员账户...")
        # 创建管理员用户
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=1
        )
        session.add(admin_user)
    
    session.commit()
    print("管理员账户创建/更新成功！")
    print(f"用户名: admin")
    print(f"密码: admin123")
    print(f"邮箱: admin@example.com")
    
    # 创建一个普通用户作为测试
    test_user = session.query(User).filter_by(username='testuser').first()
    if not test_user:
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('test123'),
            is_admin=0
        )
        session.add(test_user)
        session.commit()
        print("\n测试用户创建成功！")
        print(f"用户名: testuser")
        print(f"密码: test123")
    
    session.close()
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    session.close()