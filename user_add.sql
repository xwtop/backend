-- 插入学生用户
INSERT INTO sys_user (id, username, password, real_name, email, phone, avatar, gender, birthday, introduction, status, create_by, create_time, update_by, update_time, deleted) VALUES
('2016200001000000001', '2100960301', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '张明华', '2100960301@example.edu.cn', '13812345601', NULL, 1, '2002-03-15', '我是学生张明华', 1, '', NOW(), '', NOW(), 0),
('2016200001000000002', '2100960302', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '李思雨', '2100960302@example.edu.cn', '13812345602', NULL, 2, '2002-05-20', '我是学生李思雨', 1, '', NOW(), '', NOW(), 0),
('2016200001000000003', '2100960303', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '王浩然', '2100960303@example.edu.cn', '13812345603', NULL, 1, '2002-01-08', '我是学生王浩然', 1, '', NOW(), '', NOW(), 0),
('2016200001000000004', '2100960304', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '陈晓婷', '2100960304@example.edu.cn', '13812345604', NULL, 2, '2002-07-12', '我是学生陈晓婷', 1, '', NOW(), '', NOW(), 0),
('2016200001000000005', '2100960305', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '刘子轩', '2100960305@example.edu.cn', '13812345605', NULL, 1, '2002-11-25', '我是学生刘子轩', 1, '', NOW(), '', NOW(), 0),
('2016200001000000006', '2100960306', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '赵雅琪', '2100960306@example.edu.cn', '13812345606', NULL, 2, '2002-09-03', '我是学生赵雅琪', 1, '', NOW(), '', NOW(), 0),
('2016200001000000007', '2100960307', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '孙伟杰', '2100960307@example.edu.cn', '13812345607', NULL, 1, '2002-04-18', '我是学生孙伟杰', 1, '', NOW(), '', NOW(), 0),
('2016200001000000008', '2100960308', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '周雨萱', '2100960308@example.edu.cn', '13812345608', NULL, 2, '2002-06-30', '我是学生周雨萱', 1, '', NOW(), '', NOW(), 0),
('2016200001000000009', '2100960309', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '吴俊杰', '2100960309@example.edu.cn', '13812345609', NULL, 1, '2002-02-14', '我是学生吴俊杰', 1, '', NOW(), '', NOW(), 0),
('2016200001000000010', '2100960310', '$2b$12$4JkgUwmSWaf1ATMVaLITXOh0.XIH/HGAHNEBcr4C2YyZJD8nrhkbe', '郑欣怡', '2100960310@example.edu.cn', '13812345610', NULL, 2, '2002-10-22', '我是学生郑欣怡', 1, '', NOW(), '', NOW(), 0);

-- 插入用户角色关联（STUDENT角色ID为2016141604301180928）
INSERT INTO sys_user_role (id, user_id, role_id, create_by, create_time, update_by, update_time, deleted) VALUES
('2016200002000000001', '2016200001000000001', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000002', '2016200001000000002', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000003', '2016200001000000003', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000004', '2016200001000000004', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000005', '2016200001000000005', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000006', '2016200001000000006', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000007', '2016200001000000007', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000008', '2016200001000000008', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000009', '2016200001000000009', '2016141604301180928', '', NOW(), '', NOW(), 0),
('2016200002000000010', '2016200001000000010', '2016141604301180928', '', NOW(), '', NOW(), 0);


-- 插入教师用户
INSERT INTO sys_user (id, username, password, real_name, email, phone, avatar, gender, birthday, introduction, status, create_by, create_time, update_by, update_time, deleted) VALUES
('2016200003000000001', '2200960001', '$2b$12$MkpbJY5I8ZhHogj7vXx6tOqcMrXnKJspHFYesR9gEibLnhFmfc9MC', '张建国', '2200960001@example.edu.cn', '13912345601', NULL, 1, '1980-05-15', '我是教师张建国', 1, '', NOW(), '', NOW(), 0),
('2016200003000000002', '2200960002', '$2b$12$MkpbJY5I8ZhHogj7vXx6tOqcMrXnKJspHFYesR9gEibLnhFmfc9MC', '李秀英', '2200960002@example.edu.cn', '13912345602', NULL, 2, '1985-08-22', '我是教师李秀英', 1, '', NOW(), '', NOW(), 0),
('2016200003000000003', '2200960003', '$2b$12$MkpbJY5I8ZhHogj7vXx6tOqcMrXnKJspHFYesR9gEibLnhFmfc9MC', '王志强', '2200960003@example.edu.cn', '13912345603', NULL, 1, '1978-03-10', '我是教师王志强', 1, '', NOW(), '', NOW(), 0),
('2016200003000000004', '2200960004', '$2b$12$MkpbJY5I8ZhHogj7vXx6tOqcMrXnKJspHFYesR9gEibLnhFmfc9MC', '陈美玲', '2200960004@example.edu.cn', '13912345604', NULL, 2, '1982-11-08', '我是教师陈美玲', 1, '', NOW(), '', NOW(), 0),
('2016200003000000005', '2200960005', '$2b$12$MkpbJY5I8ZhHogj7vXx6tOqcMrXnKJspHFYesR9gEibLnhFmfc9MC', '刘德明', '2200960005@example.edu.cn', '13912345605', NULL, 1, '1975-07-30', '我是教师刘德明', 1, '', NOW(), '', NOW(), 0);

-- 插入用户角色关联（TEACHER角色ID为2016141792088559616）
INSERT INTO sys_user_role (id, user_id, role_id, create_by, create_time, update_by, update_time, deleted) VALUES
('2016200004000000001', '2016200003000000001', '2016141792088559616', '', NOW(), '', NOW(), 0),
('2016200004000000002', '2016200003000000002', '2016141792088559616', '', NOW(), '', NOW(), 0),
('2016200004000000003', '2016200003000000003', '2016141792088559616', '', NOW(), '', NOW(), 0),
('2016200004000000004', '2016200003000000004', '2016141792088559616', '', NOW(), '', NOW(), 0),
('2016200004000000005', '2016200003000000005', '2016141792088559616', '', NOW(), '', NOW(), 0);