# 用户认证模块测试文档

## 一、依赖安装

```bash
cd backend
pip install -r requirements.txt
```

## 二、启动服务

### 本地开发环境启动
```bash
cd backend
python app.py
```

服务将在 http://localhost:5000 启动

### 魔搭创空间环境启动

1. 设置环境变量（在魔搭创空间控制台）：
```
JWT_SECRET=your_secret_key_here
SERVER_PORT=8888
```

2. 启动服务：
```bash
python app.py
```

## 三、接口测试示例

### 1. 用户注册

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456",
    "email": "test@example.com"
  }'
```

预期响应：
```json
{
  "code": 200,
  "msg": "注册成功",
  "requestId": "req_xxx",
  "data": {
    "user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "username": "testuser"
  }
}
```

### 2. 用户登录

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456"
  }'
```

预期响应：
```json
{
  "code": 200,
  "msg": "登录成功",
  "requestId": "req_xxx",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400,
    "user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "username": "testuser"
  }
}
```

### 3. 获取用户信息（需要携带token）

```bash
# 将YOUR_TOKEN替换为登录时获取的token
curl -X GET http://localhost:5000/api/v1/auth/info \
  -H "Authorization: Bearer YOUR_TOKEN"
```

预期响应：
```json
{
  "code": 200,
  "msg": "success",
  "requestId": "req_xxx",
  "data": {
    "user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2026-01-23T20:30:00.000000",
    "updated_at": "2026-01-23T20:30:00.000000"
  }
}
```

### 4. 刷新Token

```bash
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_OLD_TOKEN"
  }'
```

预期响应：
```json
{
  "code": 200,
  "msg": "刷新成功",
  "requestId": "req_xxx",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400
  }
}
```

### 5. 测试鉴权中间件（访问需要鉴权的接口）

```bash
# 访问项目列表接口（需要token）
curl -X GET http://localhost:5000/api/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN"
```

如果token有效，将正常返回数据；如果token无效或缺失，将返回401错误。

## 四、错误码说明

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（token无效或过期） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 五、数据存储位置

用户数据保存在：`backend/data/users/users.json`

文件格式：
```json
{
  "users": [
    {
      "user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "username": "testuser",
      "password": "$2b$12$...",
      "email": "test@example.com",
      "created_at": "2026-01-23T20:30:00.000000",
      "updated_at": "2026-01-23T20:30:00.000000"
    }
  ]
}
```

## 六、注意事项

1. **魔搭创空间部署时**，务必在环境变量中配置 `JWT_SECRET`
2. **密码长度**：最少6位
3. **Token格式**：支持 `Bearer token` 和 `token` 两种格式
4. **Token过期时间**：默认24小时（86400秒）
5. **数据迁移**：当前使用JSON文件存储，后续需迁移到数据库时，只需修改 `utils/user_storage.py` 中标记了 `【TODO】` 的方法即可

## 七、PowerShell测试命令

如果使用PowerShell，请使用以下格式：

```powershell
# 注册
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/register" -Method POST -ContentType "application/json" -Body '{"username":"testuser","password":"123456","email":"test@example.com"}'

# 登录
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/login" -Method POST -ContentType "application/json" -Body '{"username":"testuser","password":"123456"}'
$token = $response.data.token

# 获取用户信息
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/info" -Method GET -Headers @{"Authorization"="Bearer $token"}
```
