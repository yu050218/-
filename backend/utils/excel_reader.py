import pandas as pd
import os
import random

# 读取excel文件中的词汇数据
def load_words_from_excel():
    words = []
    # 遍历所有excel文件
    # 获取当前文件的目录，然后构造正确的文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建项目根目录路径
    # 从 utils 目录向上两级到达项目根目录
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # 构建数据库文件路径
    database_dir = os.path.join(project_root, 'database')
    
    excel_files = [
        os.path.join(database_dir, '京师小学考纲.xlsx'),
        os.path.join(database_dir, '京师初中考纲.xlsx'),
        os.path.join(database_dir, '京师高中考纲.xlsx')
    ]
    
    # 学段映射
    level_map = {
        '京师小学考纲.xlsx': 'primary',
        '京师初中考纲.xlsx': 'middle',
        '京师高中考纲.xlsx': 'high'
    }
    
    for file_path in excel_files:
        if os.path.exists(file_path):
            try:
                # 读取excel文件
                df = pd.read_excel(file_path)
                # 获取学段
                file_name = os.path.basename(file_path)
                level = level_map.get(file_name, 'primary')
                
                # 尝试不同的列名，因为Excel文件可能使用不同的列名
                for _, row in df.iterrows():
                    # 尝试不同的列名
                    word = row.get('word', '') or row.get('单词', '') or row.get('Word', '') or row.get('词汇', '')
                    phonetic = row.get('phonetic', '') or row.get('音标', '') or row.get('Phonetic', '')
                    meaning = row.get('meaning', '') or row.get('释义', '') or row.get('Meaning', '') or row.get('译文', '')
                    
                    # 根据单词在文件中的位置分配难度级别
                    # 假设每个考纲文件中的单词是按难度递增排列的
                    total_rows = len(df)
                    row_index = df.index.get_loc(_)
                    if row_index < total_rows * 0.33:
                        difficulty = f"{level}_1"
                    elif row_index < total_rows * 0.66:
                        difficulty = f"{level}_2"
                    else:
                        difficulty = f"{level}_3"
                    
                    word_data = {
                        'word': word,
                        'phonetic': phonetic,
                        'meaning': meaning,
                        'difficulty': difficulty,
                        'level': level
                    }
                    if word_data['word'] and word_data['meaning']:
                        words.append(word_data)
            except Exception as e:
                print(f"读取文件 {file_path} 时出错: {str(e)}")
                import traceback
                traceback.print_exc()
    
    return words

# 根据难度获取词汇
def get_words_by_difficulty(difficulty):
    words = load_words_from_excel()
    return [word for word in words if word['difficulty'] == difficulty]

# 根据学段和难度级别获取词汇
def get_words_by_level_and_difficulty(level, difficulty):
    words = load_words_from_excel()
    return [word for word in words if word['level'] == level and word['difficulty'].endswith(f"_{difficulty}")]

# 获取随机词汇作为迷惑选项
def get_distractors(correct_word, count=5):
    words = load_words_from_excel()
    # 过滤掉正确答案
    distractors = [word for word in words if word['word'] != correct_word]
    # 随机选择count个
    return random.sample(distractors, min(count, len(distractors)))

# 获取测评单词列表
def get_assessment_words():
    # 单词分布：小学1级4个，小学2级6个，小学3级6个；初中1级6个，初中2级6个，初中3级6个；高中1级6个，高中2级6个，高中3级4个
    word_distribution = {
        'primary_1': 4,
        'primary_2': 6,
        'primary_3': 6,
        'middle_1': 6,
        'middle_2': 6,
        'middle_3': 6,
        'high_1': 6,
        'high_2': 6,
        'high_3': 4
    }
    
    words = load_words_from_excel()
    assessment_words = []
    
    # 按照顺序获取单词
    for difficulty, count in word_distribution.items():
        # 过滤出对应难度的单词
        level_words = [word for word in words if word['difficulty'] == difficulty]
        # 随机选择指定数量的单词
        if len(level_words) >= count:
            selected_words = random.sample(level_words, count)
        else:
            # 如果单词数量不足，全部选择
            selected_words = level_words
        assessment_words.extend(selected_words)
    
    return assessment_words