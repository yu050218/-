import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

# 创建SQLite数据库引擎
engine = create_engine('sqlite:///database/vocab.db', echo=True)

# 连接数据库
with engine.connect() as conn:
    # 检查 wrong_words 表是否已经有 correct_count 字段
    result = conn.execute(text("PRAGMA table_info('wrong_words')")).fetchall()
    has_correct_count = any(column[1] == 'correct_count' for column in result)
    has_last_correct_date = any(column[1] == 'last_correct_date' for column in result)
    
    if not has_correct_count:
        # 添加 correct_count 字段
        conn.execute(text("ALTER TABLE wrong_words ADD COLUMN correct_count INTEGER DEFAULT 0"))
        print("Added correct_count column to wrong_words table")
    else:
        print("correct_count column already exists")
    
    if not has_last_correct_date:
        # 添加 last_correct_date 字段（先添加字段，不设置默认值）
        conn.execute(text("ALTER TABLE wrong_words ADD COLUMN last_correct_date DATETIME"))
        # 然后更新所有记录的默认值
        conn.execute(text("UPDATE wrong_words SET last_correct_date = CURRENT_TIMESTAMP"))
        print("Added last_correct_date column to wrong_words table")
    else:
        print("last_correct_date column already exists")
    
    # 提交事务
    conn.commit()
