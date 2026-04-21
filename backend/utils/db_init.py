import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from models.models import Base

# 创建SQLite数据库引擎
engine = create_engine('sqlite:///database/vocab.db', echo=True)

# 创建所有表
Base.metadata.create_all(engine)