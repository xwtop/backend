# Campus Portal Flask Backend

基于 Flask 的校园门户后端，实现了完整的 RBAC 权限管理系统。

## 环境要求

- Python 3.11+
- MySQL 5.7+ 或 MySQL 8.0+

## 技术栈

- Flask 3.1.0
- Flask-SQLAlchemy 3.1.1

- Flask-CORS 5.0.0
- PyJWT 2.9.0
- Marshmallow 3.21.3
- PyMySQL 1.1.1
- bcrypt 4.2.0
- python-dotenv 1.0.1

## 项目结构

```
backend/
├── app/
│   ├── api/              # API 路由
│   │   ├── auth_api.py       # 认证相关接口
│   │   ├── user_api.py       # 用户管理接口
│   │   ├── role_api.py       # 角色管理接口
│   │   └── permission_api.py # 权限管理接口
│   ├── models/           # 数据模型
│   │   ├── base_model.py     # 基础模型类
│   │   ├── sys_user.py       # 用户模型
│   │   ├── sys_role.py       # 角色模型
│   │   ├── sys_permission.py # 权限模型
│   │   ├── sys_user_role.py # 用户角色关联模型
│   │   ├── sys_role_permission.py # 角色权限关联模型
│   │   └── __init__.py      # 模型导出
│   ├── schemas/          # 数据验证和序列化
│   │   ├── auth_schema.py   # 认证相关 Schema
│   │   ├── user_schema.py   # 用户相关 Schema
│   │   ├── role_schema.py   # 角色相关 Schema
│   │   ├── permission_schema.py # 权限相关 Schema
│   │   └── __init__.py     # Schema 导出
│   ├── services/         # 业务逻辑
│   │   ├── auth_service.py
│   │   ├── sys_user_service.py
│   │   ├── sys_role_service.py
│   │   └── sys_permission_service.py
│   ├── utils/            # 工具函数
│   │   ├── jwt_helper.py  # JWT 工具
│   │   └── password_helper.py  # 密码加密工具
│   ├── middleware/       # 中间件
│   │   └── auth.py       # 认证中间件
│   ├── extensions.py     # Flask 扩展初始化
│   ├── blueprints.py     # 蓝图注册
│   └── __init__.py       # Flask 应用工厂
├── migrations/          # 数据库迁移文件
├── config.py             # 配置文件
├── requirements.txt      # 依赖包
├── run.py               # 启动文件
├── cli.py               # CLI 命令
├── init_data.py         # 初始化数据脚本
└── .env.example         # 环境变量示例
```

## RBAC 权限模型

### 实体关系

- **SysUser（用户）**: 存储用户基本信息
- **SysRole（角色）**: 存储角色信息
- **SysPermission（权限）**: 存储权限信息
- **SysUserRole（用户-角色关联）**: 多对多关系
- **SysRolePermission（角色-权限关联）**: 多对多关系

### 权限设计

- **用户**: username（学号）, password, real_name, email, phone, avatar, gender, birthday, introduction, status
- **角色**: code, name, sort, remark, status
- **权限**: code, name, resource, action, type（API/MENU/BUTTON）, remark, status

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env .env
```

编辑 `.env` 文件，配置数据库连接信息：

```env
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/campus_portal?charset=utf8mb4
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 3. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE campus_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```


### 5. 启动服务

```bash
python run.py
```

服务将在 `http://localhost:5000` 启动。

### CLI 命令

```bash
# 创建数据库表
flask init_db

# 删除数据库表
flask drop_db
```

## API 接口

### 认证接口

#### 用户登录
```
POST /v1/auth/login
Content-Type: application/json

{
  "username": "学号",
  "password": "密码"
}

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "accessToken": "JWT Token",
    "realName": "真实姓名",
    "role": ["角色名称列表"]
  }
}
```

#### 用户注册
```
POST /v1/auth/register
Content-Type: application/json

{
  "username": "学号",
  "password": "密码",
  "realName": "真实姓名",
  "email": "邮箱",
  "emailCode": "邮箱验证码"
}
```

#### 用户登出
```
POST /v1/auth/logout
Authorization: Bearer {token}
```

### 用户管理接口

#### 新增用户
```
POST /v1/sysUser/add
Authorization: Bearer {token}
Content-Type: application/json

{
  "username": "学号",
  "password": "密码",
  "realName": "真实姓名",
  "email": "邮箱",
  "phone": "手机号",
  "avatar": "头像URL",
  "gender": 1,
  "birthday": "2000-01-01T00:00:00",
  "introduction": "个人简介",
  "status": 1,
  "roleIds": [1, 2]
}
```

#### 修改用户
```
PUT /v1/sysUser/{id}/update
Authorization: Bearer {token}
Content-Type: application/json

{
  "username": "学号",
  "realName": "真实姓名",
  "email": "邮箱",
  "roleIds": [1, 2]
}
```

#### 删除用户
```
DELETE /v1/sysUser/{ids}/delete
Authorization: Bearer {token}
```

#### 获取用户详情
```
GET /v1/sysUser/{id}/form
Authorization: Bearer {token}
```

#### 分页查询用户
```
POST /v1/sysUser/page
Authorization: Bearer {token}
Content-Type: application/json

{
  "page": 1,
  "pageSize": 10,
  "username": "学号（可选）",
  "realName": "姓名（可选）",
  "email": "邮箱（可选）",
  "status": 1
}

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "items": [...],
    "page": 1,
    "pageSize": 10
  }
}
```

### 角色管理接口

#### 新增角色
```
POST /v1/sysRole/add
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "角色编码",
  "name": "角色名称",
  "sort": 1,
  "remark": "备注",
  "status": 1,
  "permissionIds": [1, 2, 3]
}
```

#### 修改角色
```
PUT /v1/sysRole/{id}/update
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "角色编码",
  "name": "角色名称",
  "permissionIds": [1, 2, 3]
}
```

#### 删除角色
```
DELETE /v1/sysRole/{ids}/delete
Authorization: Bearer {token}
```

#### 获取角色详情
```
GET /v1/sysRole/{id}/form
Authorization: Bearer {token}
```

#### 分页查询角色
```
POST /v1/sysRole/page
Authorization: Bearer {token}
Content-Type: application/json

{
  "page": 1,
  "pageSize": 10,
  "code": "角色编码（可选）",
  "name": "角色名称（可选）",
  "status": 1
}
```

### 权限管理接口

#### 新增权限
```
POST /v1/sysPermission/add
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "权限编码",
  "name": "权限名称",
  "resource": "资源标识",
  "action": "操作",
  "type": "API",
  "remark": "备注",
  "status": 1
}
```

#### 修改权限
```
PUT /v1/sysPermission/{id}/update
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "权限编码",
  "name": "权限名称",
  "type": "API"
}
```

#### 删除权限
```
DELETE /v1/sysPermission/{ids}/delete
Authorization: Bearer {token}
```

#### 获取权限详情
```
GET /v1/sysPermission/{id}/form
Authorization: Bearer {token}
```

#### 分页查询权限
```
POST /v1/sysPermission/page
Authorization: Bearer {token}
Content-Type: application/json

{
  "page": 1,
  "pageSize": 10,
  "code": "权限编码（可选）",
  "name": "权限名称（可选）",
  "type": "API",
  "status": 1
}
```

## 认证和授权

### JWT Token

所有需要认证的接口都需要在请求头中携带 JWT Token：

```
Authorization: Bearer {token}
```

### 权限装饰器

使用 `@token_required` 装饰器保护需要认证的接口：

```python
from app.middleware.auth import token_required

@user_bp.route('/add', methods=['POST'])
@token_required
def save_sys_user():
    pass
```

使用 `@permission_required` 装饰器检查特定权限：

```python
from app.middleware.auth import token_required, permission_required

@user_bp.route('/add', methods=['POST'])
@token_required
@permission_required('user:add')
def save_sys_user():
    pass
```

## 默认数据

初始化脚本会创建以下默认数据：

### 角色

- **ADMIN（管理员）**: 拥有所有权限
- **STUDENT（学生）**: 默认角色，新注册用户自动分配

### 权限

- user:view, user:add, user:update, user:delete
- role:view, role:add, role:update, role:delete
- permission:view, permission:add, permission:update, permission:delete

## 配置

在 `config.py` 中配置：

```python
SECRET_KEY = 'your-secret-key'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/campus_portal?charset=utf8mb4'
JWT_SECRET_KEY = 'your-jwt-secret-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
CORS_ORIGINS = ['http://localhost:5173']
```

### 数据库配置

默认使用 MySQL 数据库，请确保：

1. MySQL 服务已启动
2. 已创建数据库 `campus_portal`
3. 数据库用户名和密码正确

如需修改数据库连接信息，请修改 `config.py` 中的 `SQLALCHEMY_DATABASE_URI`。

## 注意事项

1. 生产环境请修改 `SECRET_KEY` 和 `JWT_SECRET_KEY`
2. 确保 MySQL 数据库已正确配置
3. 密码使用 bcrypt 加密存储
4. 所有删除操作都是逻辑删除（deleted=1）
