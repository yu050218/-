import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import User
from werkzeug.security import generate_password_hash

# 创建SQLite数据库引擎
engine = create_engine('sqlite:///database/vocab.db', echo=True)
Session = sessionmaker(bind=engine)

# 连接数据库
session = Session()

# 检查是否已经存在管理员用户
admin_user = session.query(User).filter_by(username='admin').first()

if not admin_user:
    # 创建管理员用户
    password_hash = generate_password_hash('admin123')
    new_admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=password_hash,
        is_admin=1
    )
    session.add(new_admin)
    session.commit()
    print("Admin user created successfully")
else:
    # 更新现有用户为管理员
    admin_user.is_admin = 1
    session.commit()
    print("Admin user updated successfully")

# 关闭会话
session.close()
