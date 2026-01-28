-- base 数据库建表脚本（系统表，sys_前缀）
-- 用户表
CREATE TABLE IF NOT EXISTS sys_user
(
    id           VARCHAR(64) PRIMARY KEY COMMENT '主键ID',
    username     VARCHAR(64)  NOT NULL UNIQUE COMMENT '学号',
    password     VARCHAR(255) NOT NULL COMMENT '密码哈希',
    real_name    VARCHAR(64) COMMENT '真实姓名',
    email        VARCHAR(128) COMMENT '邮箱',
    phone        VARCHAR(32) COMMENT '手机号',
    avatar       VARCHAR(255) COMMENT '头像URL',
    gender       TINYINT  DEFAULT 0 COMMENT '性别（0-未知，1-男，2-女）',
    birthday     DATE COMMENT '生日',
    introduction TEXT COMMENT '个人简介',
    status       TINYINT  DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    create_by    VARCHAR(64)   DEFAULT 0,
    create_time  DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_by    VARCHAR(64)   DEFAULT 0,
    update_time  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted      TINYINT  DEFAULT 0 COMMENT '逻辑删除（0未删除，1已删除）'
) COMMENT ='系统用户表';

-- 角色表
CREATE TABLE IF NOT EXISTS sys_role
(
    id          VARCHAR(64) PRIMARY KEY COMMENT '主键ID',
    code        VARCHAR(64) NOT NULL UNIQUE COMMENT '角色编码',
    name        VARCHAR(64) NOT NULL COMMENT '角色名称',
    sort        INT      DEFAULT 0 COMMENT '显示顺序',
    remark      VARCHAR(255) COMMENT '备注',
    status      INT      DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    create_by   VARCHAR(64)   DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_by   VARCHAR(64)   DEFAULT 0,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted     TINYINT  DEFAULT 0 COMMENT '逻辑删除（0未删除，1已删除）'
) COMMENT ='角色表';

-- 权限表
CREATE TABLE IF NOT EXISTS sys_permission
(
    id          VARCHAR(64) PRIMARY KEY COMMENT '主键ID',
    code        VARCHAR(64) NOT NULL UNIQUE COMMENT '权限编码',
    name        VARCHAR(64) NOT NULL COMMENT '权限名称',
    resource    VARCHAR(255) COMMENT '资源标识',
    action      VARCHAR(32) COMMENT '操作',
    type        VARCHAR(32) COMMENT '类型（API/MENU/BUTTON）',
    remark      VARCHAR(255) COMMENT '备注',
    status      INT      DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    create_by   VARCHAR(64)   DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_by   VARCHAR(64)   DEFAULT 0,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted     TINYINT  DEFAULT 0 COMMENT '逻辑删除（0未删除，1已删除）'
) COMMENT ='权限表';

-- 用户角色关联表
CREATE TABLE IF NOT EXISTS sys_user_role
(
    id          VARCHAR(64) PRIMARY KEY COMMENT '主键ID',
    user_id     VARCHAR(64) NOT NULL COMMENT '用户ID',
    role_id     VARCHAR(64) NOT NULL COMMENT '角色ID',
    create_by   VARCHAR(64)   DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_by   VARCHAR(64)   DEFAULT 0,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted     TINYINT  DEFAULT 0 COMMENT '逻辑删除（0未删除，1已删除）'
) COMMENT ='用户角色关联表';

-- 角色权限关联表
CREATE TABLE IF NOT EXISTS sys_role_permission
(
    id            VARCHAR(64) PRIMARY KEY COMMENT '主键ID',
    role_id       VARCHAR(64) NOT NULL COMMENT '角色ID',
    permission_id VARCHAR(64) NOT NULL COMMENT '权限ID',
    create_by     VARCHAR(64)   DEFAULT 0,
    create_time   DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_by     VARCHAR(64)   DEFAULT 0,
    update_time   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted       TINYINT  DEFAULT 0 COMMENT '逻辑删除（0未删除，1已删除）'
) COMMENT ='角色权限关联表';

-- 内容分类表
CREATE TABLE IF NOT EXISTS content_category
(
    id           VARCHAR(64) PRIMARY KEY COMMENT '主键ID',
    parent_id    VARCHAR(64)  DEFAULT NULL COMMENT '父分类ID（NULL表示顶级分类）',
    name         VARCHAR(64)  NOT NULL COMMENT '分类名称',
    code         VARCHAR(64)  NOT NULL UNIQUE COMMENT '分类编码（唯一标识）',
    sort         INT      DEFAULT 0 COMMENT '排序（数字越小越靠前）',
    status       TINYINT  DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    remark       VARCHAR(255) COMMENT '备注',
    create_by    VARCHAR(64)   DEFAULT 0 COMMENT '创建人',
    create_time  DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_by    VARCHAR(64)   DEFAULT 0 COMMENT '更新人',
    update_time  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted      TINYINT  DEFAULT 0 COMMENT '逻辑删除（0未删除，1已删除）'
) COMMENT ='内容分类表';
