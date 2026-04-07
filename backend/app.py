from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

# 导入路由
from api.user import UserRegister, UserLogin, UserProfile
from api.test import TestStart, TestSubmit, TestRecord
from api.pk import PKMatch, PKStatus

# 注册路由
api.add_resource(UserRegister, '/api/register')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserProfile, '/api/profile')
api.add_resource(TestStart, '/api/test/start')
api.add_resource(TestSubmit, '/api/test/submit')
api.add_resource(TestRecord, '/api/test/record')
api.add_resource(PKMatch, '/api/pk/match')
api.add_resource(PKStatus, '/api/pk/status/<match_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)