import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

# 创建SQLite数据库引擎
engine = create_engine('sqlite:///database/vocab.db', echo=True)

# 连接数据库
with engine.connect() as conn:
    # 检查 users 表是否已经有 is_admin 字段
    result = conn.execute(text("PRAGMA table_info('users')")).fetchall()
    has_admin_column = any(column[1] == 'is_admin' for column in result)
    
    if not has_admin_column:
        # 添加 is_admin 字段
        conn.execute(text("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0"))
        print("Added is_admin column to users table")
    else:
        print("is_admin column already exists")
    
    # 提交事务
    conn.commit()
