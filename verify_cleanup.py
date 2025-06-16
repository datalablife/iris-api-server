#!/usr/bin/env python3
"""
验证项目结构整理后的功能完整性
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (不存在)")
        return False

def check_directory_structure():
    """检查目录结构"""
    print("🏗️ 检查项目目录结构")
    print("=" * 50)
    
    # 核心目录
    directories = [
        ("tests", "测试根目录"),
        ("tests/autogen", "AutoGen测试目录"),
        ("tests/gemini", "Gemini测试目录"),
        ("tests/gemini/api", "Gemini API测试"),
        ("tests/gemini/models", "Gemini模型测试"),
        ("tests/gemini/clients", "Gemini客户端测试"),
        ("tests/scripts", "脚本目录"),
        ("tests/scripts/curl", "curl脚本目录"),
        ("tests/logs", "日志目录"),
        ("tests/reports", "报告目录"),
        ("autogen_workflow", "核心业务代码"),
        ("autogen_workflow/agents", "Agent实现")
    ]
    
    all_exist = True
    for dir_path, description in directories:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✅ {description}: {dir_path}")
        else:
            print(f"❌ {description}: {dir_path} (不存在)")
            all_exist = False
    
    return all_exist

def check_test_files():
    """检查测试文件"""
    print("\n🧪 检查测试文件")
    print("=" * 50)
    
    test_files = [
        # AutoGen测试
        ("tests/autogen/test_installation.py", "AutoGen安装测试"),
        ("tests/autogen/test_imports.py", "模块导入测试"),
        ("tests/autogen/demo.py", "工作流演示"),
        
        # Gemini API测试
        ("tests/gemini/api/simple_gemini_test.py", "简单API测试"),
        ("tests/gemini/api/test_gemini_rest.py", "REST API测试"),
        ("tests/gemini/api/debug_gemini.py", "API调试工具"),
        
        # Gemini模型测试
        ("tests/gemini/models/test_gemini_models.py", "模型测试"),
        
        # Gemini客户端测试
        ("tests/gemini/clients/test_gemini_client.py", "客户端测试"),
        ("tests/gemini/clients/test_updated_gemini.py", "更新客户端测试"),
        ("tests/gemini/clients/test_model_info.py", "模型信息测试"),
        
        # Shell脚本
        ("tests/scripts/curl/test_curl.sh", "基础curl测试"),
        ("tests/scripts/curl/simple_model_test.sh", "简单模型测试"),
        ("tests/scripts/curl/test_preview_models.sh", "预览模型测试"),
        
        # 日志和报告
        ("tests/logs/demo.log", "演示日志"),
        ("tests/reports/gemini_model_test_report.md", "模型测试报告")
    ]
    
    all_exist = True
    for file_path, description in test_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_core_files():
    """检查核心文件"""
    print("\n💼 检查核心业务文件")
    print("=" * 50)
    
    core_files = [
        ("autogen_workflow/__init__.py", "包初始化"),
        ("autogen_workflow/config.py", "配置管理"),
        ("autogen_workflow/workflow.py", "主工作流"),
        ("autogen_workflow/main.py", "程序入口"),
        ("autogen_workflow/gemini_client.py", "Gemini客户端"),
        ("autogen_workflow/mock_gemini_client.py", "Mock客户端"),
        ("autogen_workflow/agents/architect.py", "架构师Agent"),
        ("autogen_workflow/agents/project_manager.py", "项目经理Agent"),
        ("autogen_workflow/agents/programmer.py", "程序员Agent"),
        ("autogen_workflow/agents/code_reviewer.py", "代码审查员Agent"),
        ("autogen_workflow/agents/code_optimizer.py", "代码优化员Agent"),
        ("README.md", "项目文档"),
        ("requirements.txt", "依赖配置"),
        (".env", "环境配置")
    ]
    
    all_exist = True
    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_documentation():
    """检查文档文件"""
    print("\n📚 检查文档文件")
    print("=" * 50)
    
    doc_files = [
        ("tests/README.md", "测试说明文档"),
        ("tests/autogen/README.md", "AutoGen测试说明"),
        ("tests/gemini/README.md", "Gemini测试说明"),
        ("tests/scripts/README.md", "脚本说明"),
        ("ARCHITECTURE_CLEANUP.md", "架构整理报告"),
        ("QUICK_START.md", "快速开始指南"),
        ("Workflow_README.md", "工作流说明"),
        ("data_analysis_api_readme.md", "数据分析API说明")
    ]
    
    all_exist = True
    for file_path, description in doc_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_root_directory_clean():
    """检查根目录是否整洁"""
    print("\n🧹 检查根目录整洁度")
    print("=" * 50)
    
    # 应该不存在的测试文件（已移动）
    old_test_files = [
        "test_installation.py",
        "test_imports.py", 
        "demo.py",
        "test_gemini_client.py",
        "test_gemini_models.py",
        "simple_gemini_test.py",
        "debug_gemini.py",
        "demo.log",
        "gemini_model_test_report.md"
    ]
    
    clean = True
    for file_name in old_test_files:
        if os.path.exists(file_name):
            print(f"⚠️ 根目录仍有测试文件: {file_name}")
            clean = False
    
    if clean:
        print("✅ 根目录已整洁，所有测试文件已正确归档")
    
    return clean

def main():
    """主验证函数"""
    print("🔍 项目结构整理验证")
    print("=" * 60)
    
    # 执行所有检查
    checks = [
        ("目录结构", check_directory_structure),
        ("测试文件", check_test_files),
        ("核心文件", check_core_files),
        ("文档文件", check_documentation),
        ("根目录整洁度", check_root_directory_clean)
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
        print(f"  {check_name:<15} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有检查通过！项目结构整理成功！")
        print("\n💡 现在可以开始新功能开发了：")
        print("  - 根目录整洁，便于新功能开发")
        print("  - 测试脚本已归档，便于维护")
        print("  - 文档结构清晰，便于查阅")
        print("  - 核心代码结构稳定，便于扩展")
    else:
        print("⚠️ 部分检查未通过，请检查上述问题")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
