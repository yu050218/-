import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Word, Base
from utils.excel_reader import load_words_from_excel

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 从 utils 目录向上两级到达项目根目录
project_root = os.path.dirname(os.path.dirname(current_dir))
# 构建数据库文件路径
database_path = os.path.join(project_root, 'database', 'vocab.db')

# 创建SQLite数据库引擎
engine = create_engine(f'sqlite:///{database_path}', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# 创建表（如果不存在）
Base.metadata.create_all(engine)

# 先清空现有数据
session.query(Word).delete()
session.commit()
print("已清空现有单词数据")

# 从Excel文件加载单词
words = load_words_from_excel()
print(f"从Excel文件读取到 {len(words)} 个单词")

# 插入数据
for word_data in words:
    word = Word(
        word=word_data['word'],
        phonetic=word_data['phonetic'],
        meaning=word_data['meaning'],
        difficulty=word_data['difficulty']
    )
    session.add(word)

session.commit()
session.close()

print(f"成功导入 {len(words)} 个单词到数据库！")
