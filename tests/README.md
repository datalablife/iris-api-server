# 测试脚本归档

本目录包含了项目开发过程中的各种测试脚本和验证工具。

## 📁 目录结构

```
tests/
├── README.md                    # 本文件
├── autogen/                     # AutoGen相关测试
│   ├── test_installation.py    # AutoGen安装测试
│   ├── test_imports.py          # 导入测试
│   └── demo.py                  # 工作流演示
├── gemini/                      # Gemini API测试
│   ├── api/                     # API连接测试
│   ├── models/                  # 模型测试
│   └── clients/                 # 客户端测试
├── scripts/                     # Shell脚本
│   └── curl/                    # curl测试脚本
├── logs/                        # 测试日志
└── reports/                     # 测试报告
```

## 🧪 测试分类

### AutoGen测试
- **test_installation.py**: 验证AutoGen框架安装
- **test_imports.py**: 验证Python模块导入
- **demo.py**: 完整工作流演示

### Gemini API测试
- **API连接测试**: 验证与Google Gemini API的连接
- **模型测试**: 测试不同Gemini模型的可用性
- **客户端测试**: 验证自定义Gemini客户端

### Shell脚本
- **curl测试**: 使用curl直接测试API
- **环境脚本**: 环境配置和激活脚本

## 📝 使用说明

1. **运行AutoGen测试**:
   ```bash
   cd tests/autogen
   python test_installation.py
   ```

2. **运行Gemini测试**:
   ```bash
   cd tests/gemini
   python test_gemini_client.py
   ```

3. **运行Shell脚本**:
   ```bash
   cd tests/scripts
   ./test_curl.sh
   ```

## 🗂️ 归档日期

- 归档时间: 2025-06-17
- 归档原因: 项目重构，整理代码结构
- 归档内容: 开发阶段的测试脚本和验证工具
