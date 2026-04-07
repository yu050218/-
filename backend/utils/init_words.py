import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Word

# 创建SQLite数据库引擎
engine = create_engine('sqlite:///../database/vocab.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# 初始单词数据
words_data = [
    # 简单难度
    {'word': 'apple', 'phonetic': '/ˈæpl/', 'meaning': '苹果', 'difficulty': 'easy'},
    {'word': 'banana', 'phonetic': '/bəˈnɑːnə/', 'meaning': '香蕉', 'difficulty': 'easy'},
    {'word': 'cat', 'phonetic': '/kæt/', 'meaning': '猫', 'difficulty': 'easy'},
    {'word': 'dog', 'phonetic': '/dɒɡ/', 'meaning': '狗', 'difficulty': 'easy'},
    {'word': 'egg', 'phonetic': '/eɡ/', 'meaning': '鸡蛋', 'difficulty': 'easy'},
    # 中等难度
    {'word': 'computer', 'phonetic': '/kəmˈpjuːtə/', 'meaning': '电脑', 'difficulty': 'medium'},
    {'word': 'database', 'phonetic': '/ˈdeɪtəbeɪs/', 'meaning': '数据库', 'difficulty': 'medium'},
    {'word': 'internet', 'phonetic': '/ˈɪntənet/', 'meaning': '互联网', 'difficulty': 'medium'},
    {'word': 'programming', 'phonetic': '/ˈprəʊɡræmɪŋ/', 'meaning': '编程', 'difficulty': 'medium'},
    {'word': 'algorithm', 'phonetic': '/ˈælɡərɪðəm/', 'meaning': '算法', 'difficulty': 'medium'},
    # 困难难度
    {'word': 'neural', 'phonetic': '/ˈnjʊərəl/', 'meaning': '神经的', 'difficulty': 'hard'},
    {'word': 'artificial', 'phonetic': '/ˌɑːtɪˈfɪʃl/', 'meaning': '人工的', 'difficulty': 'hard'},
    {'word': 'intelligence', 'phonetic': '/ɪnˈtelɪdʒəns/', 'meaning': '智能', 'difficulty': 'hard'},
    {'word': 'machine', 'phonetic': '/məˈʃiːn/', 'meaning': '机器', 'difficulty': 'hard'},
    {'word': 'learning', 'phonetic': '/ˈlɜːnɪŋ/', 'meaning': '学习', 'difficulty': 'hard'}
]

# 插入数据
for word_data in words_data:
    word = Word(**word_data)
    session.add(word)

session.commit()
session.close()

print('Words initialized successfully!')