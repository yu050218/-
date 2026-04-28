import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, inspect

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 从 backend 目录向上一级到达项目根目录
project_root = os.path.dirname(current_dir)
# 构建数据库文件路径
database_path = os.path.join(project_root, 'database', 'vocab.db')

print(f"数据库路径: {database_path}")
print(f"数据库文件存在: {os.path.exists(database_path)}")

# 创建SQLite数据库引擎
engine = create_engine(f'sqlite:///{database_path}')

# 创建inspector来检查数据库结构
inspector = inspect(engine)

# 获取所有表名
tables = inspector.get_table_names()
print(f"\n数据库中的表: {tables}")

# 检查用户表结构
if 'users' in tables:
    columns = inspector.get_columns('users')
    print("\n用户表结构:")
    for col in columns:
        print(f"  {col['name']}: {col['type']}")
else:
    print("\n用户表不存在！")

# 检查单词表结构
if 'words' in tables:
    columns = inspector.get_columns('words')
    print("\n单词表结构:")
    for col in columns:
        print(f"  {col['name']}: {col['type']}")
    
    # 统计单词数量
    with engine.connect() as conn:
        result = conn.execute('SELECT COUNT(*) FROM words')
        count = result.scalar()
        print(f"\n单词数量: {count}")
else:
    print("\n单词表不存在！")
