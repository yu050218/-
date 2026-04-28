import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from models.models import Base

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 从 utils 目录向上两级到达项目根目录
project_root = os.path.dirname(os.path.dirname(current_dir))
# 构建数据库文件路径
database_path = os.path.join(project_root, 'database', 'vocab.db')

# 创建SQLite数据库引擎
engine = create_engine(f'sqlite:///{database_path}', echo=False)

# 创建所有表
Base.metadata.create_all(engine)

print(f"数据库表创建成功！数据库路径: {database_path}")
