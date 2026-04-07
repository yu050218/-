# English Vocabulary Proficiency Assessment Tool

A web-based English vocabulary assessment and learning system supporting vocabulary size testing, proficiency level evaluation, and online PvP practice.

## Features

- **User Management**: User registration, login, and profile management
- **Vocabulary Testing**: Online vocabulary proficiency assessment with test history tracking
- **Vocabulary Size Estimation**: Estimate user vocabulary size based on answer accuracy
- **Proficiency Level Assessment**: Map vocabulary size to standard CEFR levels (A1-C2)
- **PvP System**: Support for one-on-one vocabulary battle challenges
- **JWT Authentication**: Secure user authentication

## Technology Stack

### Backend
- Python Flask
- SQLAlchemy ORM
- PyJWT Token Authentication
- SQLite Database

### Frontend
- Vue 3
- Vue Router
- Pinia State Management
- Vite Build Tool

## Project Structure

```
├── backend/              # Backend service
│   ├── api/             # API endpoints
│   │   ├── pk.py        # PvP-related endpoints
│   │   ├── test.py      # Test-related endpoints
│   │   └── user.py      # User-related endpoints
│   ├── models/          # Data models
│   │   └── models.py    # User, Word, TestRecord models
│   ├── utils/          # Utility functions
│   │   ├── jwt_utils.py # JWT token utilities
│   │   ├── db_init.py  # Database initialization
│   │   └── init_words.py # Vocabulary data initialization
│   ├── app.py          # Flask application entry point
│   └── requirements.txt # Dependency list
│
├── frontend/            # Frontend application
│   ├── src/
│   │   ├── views/     # Page views
│   │   ├── stores/   # State management
│   │   ├── router/   # Routing configuration
│   │   ├── App.vue  # Root component
│   │   └── main.js  # Entry file
│   ├── index.html     # HTML template
│   ├── package.json # Dependency configuration
│   └── vite.config.js # Vite configuration
│
└── database/
    └── vocab.db       # SQLite database
```

## Quick Start

### Start Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend service runs by default at `http://localhost:5000`

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs by default at `http://localhost:5173`

## API Endpoints

### User Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/user/register | User registration |
| POST | /api/user/login | User login |
| GET | /api/user/profile | Retrieve user profile |
| PUT | /api/user/profile | Update user profile |

### Test Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/test/start | Start a vocabulary test |
| POST | /api/test/submit | Submit test answers |
| GET | /api/test/record | Retrieve test records |

### PvP Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/pk/match | Create or join a PvP match |
| GET | /api/pk/status/:match_id | Check match status |

## Vocabulary Level Reference

| Vocabulary Size | CEFR Level |
|-----------------|------------|
| 0-500 | A1 |
| 500-1500 | A2 |
| 1500-2500 | B1 |
| 2500-3500 | B2 |
| 3500-5000 | C1 |
| 5000+ | C2 |

## License

MIT License