

# 英语词汇水平评估工具

一个基于 Web 的英语词汇能力评估与学习系统，支持词汇量测试、词汇等级评估以及在线对战练习。

## 功能特性

- **用户管理**：用户注册、登录、个人信息管理
- **词汇测试**：在线词汇能力评估，记录测试历史
- **词汇量估算**：根据答题正确率估算用户词汇量
- **等级评估**：将词汇量映射为标准等级（A1-C2）
- **对战系统**：支持一对一词汇对战 PK
- **JWT 认证**：安全的用户身份验证

## 技术栈

### 后端
- Python Flask
- SQLAlchemy ORM
- PyJWT 令牌认证
- SQLite 数据库

### 前端
- Vue 3
- Vue Router
- Pinia 状态管理
- Vite 构建工具

## 项目结构

```
├── backend/              # 后端服务
│   ├── api/             # API 接口
│   │   ├── pk.py        # 对战相关接口
│   │   ├── test.py      # 测试相关接口
│   │   └── user.py      # 用户相关接口
│   ├── models/          # 数据模型
│   │   └── models.py     # User, Word, TestRecord 模型
│   ├── utils/          # 工具函数
│   │   ├── jwt_utils.py # JWT 令牌工具
│   │   ├── db_init.py  # 数据库初始化
│   │   └── init_words.py # 词汇数据初始化
│   ├── app.py          # Flask 应用入口
│   └── requirements.txt # 依赖列表
│
├── frontend/            # 前端应用
│   ├── src/
│   │   ├── views/     # 页面视图
│   │   ├── stores/   # 状态管理
│   │   ├── router/   # 路由配置
│   │   ├── App.vue  # 根组件
│   │   └── main.js  # 入口文件
│   ├── index.html     # HTML 模板
│   ├── package.json # 依赖配置
│   └── vite.config.js # Vite 配置
│
└── database/
    └── vocab.db       # SQLite 数据库
```

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端服务默认运行在 `http://localhost:5000`

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 `http://localhost:5173`

## API 接口

### 用户接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/user/register | 用户注册 |
| POST | /api/user/login | 用户登录 |
| GET | /api/user/profile | 获取个人信息 |
| PUT | /api/user/profile | 更新个人信息 |

### 测试接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/test/start | 开始测试 |
| POST | /api/test/submit | 提交答案 |
| GET | /api/test/record | 获取测试记录 |

### 对战接口

| 方法 | 路径 |说明 |
|------|------|------|
| POST | /api/pk/match | 创建/加入对战 |
| GET | /api/pk/status/:match_id | 查看对战状态 |

## 词汇等级参考

| 词汇量 | CEFR 等级 |
|--------|-----------|
| 0-500 | A1 |
| 500-1500 | A2 |
| 1500-2500 | B1 |
| 2500-3500 | B2 |
| 3500-5000 | C1 |
| 5000+ | C2 |

## 许可证

MIT License