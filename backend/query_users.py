import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import User, TestRecord

# 创建数据库引擎
engine = create_engine('sqlite:///database/vocab.db')
Session = sessionmaker(bind=engine)
session = Session()

# 查询所有用户
users = session.query(User).all()

print("=== 用户列表 ===")
for user in users:
    print(f"ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 创建时间: {user.created_at}")
    
    # 查询该用户的测试记录
    records = session.query(TestRecord).filter_by(user_id=user.id).order_by(TestRecord.test_date.desc()).all()
    if records:
        print("  测试记录:")
        for record in records:
            print(f"    ID: {record.id}, 测试日期: {record.test_date}, 答对: {record.correct_count}, 总题数: {record.total_count}, 词汇量: {record.vocabulary_size}, 等级: {record.level}")
    else:
        print("  无测试记录")
    print()

session.close()