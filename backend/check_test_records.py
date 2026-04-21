import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import TestRecord, User

# 创建数据库引擎
engine = create_engine('sqlite:///database/vocab.db')
Session = sessionmaker(bind=engine)
session = Session()

# 查询所有测试记录
records = session.query(TestRecord).order_by(TestRecord.test_date.desc()).all()

print("=== 测试记录列表 ===")
if records:
    for record in records:
        # 获取用户信息
        user = session.query(User).filter_by(id=record.user_id).first()
        username = user.username if user else "未知用户"
        
        print(f"ID: {record.id}, 用户: {username}, 测试日期: {record.test_date}, 答对: {record.correct_count}, 总题数: {record.total_count}, 词汇量: {record.vocabulary_size}, 等级: {record.level}")
else:
    print("无测试记录")

session.close()