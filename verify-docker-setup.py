#!/usr/bin/env python3
"""
Docker容器化设置验证脚本
验证所有Docker相关文件和配置是否正确
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (不存在)")
        return False

def check_docker_files():
    """检查Docker相关文件"""
    print("🐳 检查Docker配置文件")
    print("=" * 50)
    
    docker_files = [
        ("Dockerfile", "主Dockerfile"),
        ("docker-compose.yml", "生产环境配置"),
        ("docker-compose.dev.yml", "开发环境配置"),
        ("docker-compose.test.yml", "测试环境配置"),
        (".dockerignore", "Docker忽略文件"),
        (".env.example", "环境变量模板"),
        ("docker-manager.sh", "Docker管理脚本"),
        ("DOCKER_README.md", "Docker文档")
    ]
    
    all_exist = True
    for file_path, description in docker_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_docker_config_dirs():
    """检查Docker配置目录"""
    print("\n📁 检查Docker配置目录")
    print("=" * 50)
    
    config_dirs = [
        ("docker", "Docker配置根目录"),
        ("docker/nginx", "Nginx配置目录"),
        ("docker/postgres", "PostgreSQL配置目录"),
        ("docker/prometheus", "Prometheus配置目录"),
        ("docker/grafana", "Grafana配置目录"),
        ("docker/grafana/datasources", "Grafana数据源配置"),
        ("scripts", "管理脚本目录")
    ]
    
    all_exist = True
    for dir_path, description in config_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✅ {description}: {dir_path}")
        else:
            print(f"❌ {description}: {dir_path} (不存在)")
            all_exist = False
    
    return all_exist

def check_docker_config_files():
    """检查Docker配置文件"""
    print("\n⚙️ 检查Docker配置文件")
    print("=" * 50)
    
    config_files = [
        ("docker/nginx/nginx.conf", "Nginx配置文件"),
        ("docker/postgres/init.sql", "PostgreSQL初始化脚本"),
        ("docker/prometheus/prometheus.yml", "Prometheus配置"),
        ("docker/grafana/datasources/prometheus.yml", "Grafana数据源配置")
    ]
    
    all_exist = True
    for file_path, description in config_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_management_scripts():
    """检查管理脚本"""
    print("\n🛠️ 检查管理脚本")
    print("=" * 50)
    
    scripts = [
        ("scripts/docker-build.sh", "Docker构建脚本"),
        ("scripts/docker-deploy.sh", "Docker部署脚本"),
        ("scripts/docker-test.sh", "Docker测试脚本"),
        ("scripts/docker-cleanup.sh", "Docker清理脚本")
    ]
    
    all_exist = True
    for script_path, description in scripts:
        if check_file_exists(script_path, description):
            # 检查脚本是否可执行
            if os.access(script_path, os.X_OK):
                print(f"  ✅ {script_path} 具有执行权限")
            else:
                print(f"  ⚠️ {script_path} 缺少执行权限")
        else:
            all_exist = False
    
    return all_exist

def check_docker_installation():
    """检查Docker是否安装"""
    print("\n🔧 检查Docker安装")
    print("=" * 50)
    
    try:
        # 检查Docker
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker已安装: {result.stdout.strip()}")
            docker_installed = True
        else:
            print("❌ Docker未安装或无法访问")
            docker_installed = False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Docker未安装或无法访问")
        docker_installed = False
    
    try:
        # 检查Docker Compose (新版本)
        result = subprocess.run(['docker', 'compose', 'version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker Compose已安装: {result.stdout.strip()}")
            compose_installed = True
        else:
            # 尝试旧版本命令
            result = subprocess.run(['docker-compose', '--version'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Docker Compose已安装 (旧版本): {result.stdout.strip()}")
                compose_installed = True
            else:
                print("❌ Docker Compose未安装或无法访问")
                compose_installed = False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Docker Compose未安装或无法访问")
        compose_installed = False
    
    # 检查Docker守护进程
    try:
        result = subprocess.run(['docker', 'info'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker守护进程正在运行")
            daemon_running = True
        else:
            print("❌ Docker守护进程未运行")
            daemon_running = False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ 无法检查Docker守护进程状态")
        daemon_running = False
    
    return docker_installed and compose_installed and daemon_running

def check_env_configuration():
    """检查环境配置"""
    print("\n🔐 检查环境配置")
    print("=" * 50)
    
    if os.path.exists(".env"):
        print("✅ .env文件存在")
        
        # 检查关键配置项
        with open(".env", "r") as f:
            env_content = f.read()
            
        if "GOOGLE_API_KEY=" in env_content:
            if "your_google_api_key_here" in env_content:
                print("⚠️ Google API密钥未设置 (仍为默认值)")
            else:
                print("✅ Google API密钥已配置")
        else:
            print("❌ 缺少Google API密钥配置")
            
        return True
    else:
        print("⚠️ .env文件不存在，将使用.env.example")
        return False

def validate_dockerfile():
    """验证Dockerfile语法"""
    print("\n📋 验证Dockerfile")
    print("=" * 50)
    
    if not os.path.exists("Dockerfile"):
        print("❌ Dockerfile不存在")
        return False
    
    try:
        # 简单的语法检查
        with open("Dockerfile", "r") as f:
            content = f.read()
            
        # 检查必要的指令
        required_instructions = ["FROM", "WORKDIR", "COPY", "RUN"]
        missing_instructions = []
        
        for instruction in required_instructions:
            if instruction not in content:
                missing_instructions.append(instruction)
        
        if missing_instructions:
            print(f"❌ Dockerfile缺少必要指令: {', '.join(missing_instructions)}")
            return False
        else:
            print("✅ Dockerfile包含必要指令")
            
        # 检查多阶段构建
        if "as base" in content and "as production" in content:
            print("✅ Dockerfile使用多阶段构建")
        else:
            print("⚠️ Dockerfile未使用多阶段构建")
            
        return True
        
    except Exception as e:
        print(f"❌ 验证Dockerfile时出错: {e}")
        return False

def main():
    """主验证函数"""
    print("🔍 AutoGen Workflow Docker容器化验证")
    print("=" * 60)
    
    # 执行所有检查
    checks = [
        ("Docker配置文件", check_docker_files),
        ("Docker配置目录", check_docker_config_dirs),
        ("Docker配置文件内容", check_docker_config_files),
        ("管理脚本", check_management_scripts),
        ("Docker安装", check_docker_installation),
        ("环境配置", check_env_configuration),
        ("Dockerfile验证", validate_dockerfile)
    ]
    
    results = []
    for check_name, check_func in checks:
        result = check_func()
        results.append((check_name, result))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 验证结果总结")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {check_name:<20} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有检查通过！Docker容器化设置完成！")
        print("\n💡 下一步操作：")
        print("  1. 编辑.env文件，设置API密钥")
        print("  2. 运行: ./docker-manager.sh build")
        print("  3. 运行: ./docker-manager.sh prod")
        print("  4. 访问: http://localhost:8000")
    else:
        print("⚠️ 部分检查未通过，请检查上述问题")
        print("\n🔧 修复建议：")
        print("  1. 确保所有必需文件存在")
        print("  2. 安装Docker和Docker Compose")
        print("  3. 启动Docker守护进程")
        print("  4. 配置环境变量")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
