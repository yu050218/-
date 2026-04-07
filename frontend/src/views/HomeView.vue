<template>
  <div class="home">
    <h1>词汇评估工具</h1>
    <div class="features">
      <div class="feature-card">
        <h2>词汇测试</h2>
        <p>测试你的词汇量，获得详细的评估报告</p>
        <router-link to="/test" class="btn">开始测试</router-link>
      </div>
      <div class="feature-card">
        <h2>单词PK对战</h2>
        <p>与其他用户实时对战，检验你的词汇水平</p>
        <router-link to="/pk" class="btn">开始对战</router-link>
      </div>
      <div class="feature-card">
        <h2>个人中心</h2>
        <p>查看你的测试历史和个人资料</p>
        <router-link to="/profile" class="btn">进入中心</router-link>
      </div>
    </div>
    <div class="auth-buttons">
      <router-link to="/login" class="btn">登录</router-link>
      <router-link to="/register" class="btn">注册</router-link>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
  padding: 40px 0;
}

.home h1 {
  font-size: 36px;
  margin-bottom: 40px;
  color: #333;
}

.features {
  display: flex;
  justify-content: space-around;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.feature-card {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  margin: 10px;
}

.feature-card h2 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #333;
}

.feature-card p {
  margin-bottom: 20px;
  color: #666;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #45a049;
}

.auth-buttons {
  margin-top: 20px;
}

.auth-buttons .btn {
  margin: 0 10px;
}
</style>