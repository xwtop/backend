#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证函数测试脚本
用于测试所有提取到 app.utils.validation 模块的验证函数是否正常工作
"""

from app.utils import (
    validate_username,
    validate_password,
    validate_phone,
    validate_real_name,
    validate_code,
    validate_name,
    validate_email
)


def test_validate_username():
    """测试用户名验证函数"""
    print("测试用户名验证...")
    try:
        validate_username("test123")  # 正确格式
        print("✓ 正确的用户名通过验证")
    except Exception as e:
        print(f"✗ 正确的用户名验证失败: {e}")
    
    try:
        validate_username("ab")  # 太短
        print("✗ 太短的用户名应该验证失败但没有")
    except ValueError:
        print("✓ 太短的用户名正确地验证失败")


def test_validate_password():
    """测试密码验证函数"""
    print("\n测试密码验证...")
    try:
        validate_password("Test1234!")  # 正确格式
        print("✓ 正确的密码通过验证")
    except Exception as e:
        print(f"✗ 正确的密码验证失败: {e}")
    
    try:
        validate_password("weakpass")  # 缺少大写字母和特殊字符
        print("✗ 弱密码应该验证失败但没有")
    except ValueError:
        print("✓ 弱密码正确地验证失败")


def test_validate_phone():
    """测试手机号验证函数"""
    print("\n测试手机号验证...")
    try:
        validate_phone("13812345678")  # 正确格式
        print("✓ 正确的手机号通过验证")
    except Exception as e:
        print(f"✗ 正确的手机号验证失败: {e}")
    
    try:
        validate_phone("12345678901")  # 不符合规则
        print("✗ 错误的手机号应该验证失败但没有")
    except ValueError:
        print("✓ 错误的手机号正确地验证失败")


def test_validate_real_name():
    """测试真实姓名验证函数"""
    print("\n测试真实姓名验证...")
    try:
        validate_real_name("张三")  # 正确格式
        print("✓ 正确的真实姓名通过验证")
    except Exception as e:
        print(f"✗ 正确的真实姓名验证失败: {e}")
    
    try:
        validate_real_name("")  # 空字符串
        print("✗ 空姓名应该验证失败但没有")
    except ValueError:
        print("✓ 空姓名正确地验证失败")


def test_validate_code():
    """测试编码验证函数"""
    print("\n测试编码验证...")
    try:
        validate_code("user:add")  # 正确格式
        print("✓ 正确的编码通过验证")
    except Exception as e:
        print(f"✗ 正确的编码验证失败: {e}")
    
    try:
        validate_code("user@add")  # 包含非法字符
        print("✗ 包含非法字符的编码应该验证失败但没有")
    except ValueError:
        print("✓ 包含非法字符的编码正确地验证失败")


def test_validate_name():
    """测试名称验证函数"""
    print("\n测试名称验证...")
    try:
        validate_name("管理员")  # 正确格式
        print("✓ 正确的名称通过验证")
    except Exception as e:
        print(f"✗ 正确的名称验证失败: {e}")
    
    try:
        validate_name("")  # 空字符串
        print("✗ 空名称应该验证失败但没有")
    except ValueError:
        print("✓ 空名称正确地验证失败")


def test_validate_email():
    """测试邮箱验证函数"""
    print("\n测试邮箱验证...")
    try:
        validate_email("test@example.com")  # 正确格式
        print("✓ 正确的邮箱通过验证")
    except Exception as e:
        print(f"✗ 正确的邮箱验证失败: {e}")
    
    try:
        validate_email("invalid-email")  # 错误格式
        print("✗ 错误的邮箱应该验证失败但没有")
    except ValueError:
        print("✓ 错误的邮箱正确地验证失败")


if __name__ == "__main__":
    print("开始测试所有验证函数...\n")
    
    test_validate_username()
    test_validate_password()
    test_validate_phone()
    test_validate_real_name()
    test_validate_code()
    test_validate_name()
    test_validate_email()
    
    print("\n所有测试完成！")