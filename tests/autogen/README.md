# AutoGen测试脚本

本目录包含AutoGen框架相关的测试脚本。

## 📁 文件说明

### test_installation.py
- **功能**: 验证AutoGen框架安装是否正确
- **测试内容**:
  - 检查Python环境
  - 验证AutoGen模块导入
  - 测试基本功能
- **使用方法**:
  ```bash
  python test_installation.py
  ```

### test_imports.py
- **功能**: 测试Python模块导入
- **测试内容**:
  - 验证所有必需的依赖包
  - 检查版本兼容性
  - 测试导入路径
- **使用方法**:
  ```bash
  python test_imports.py
  ```

### demo.py
- **功能**: AutoGen多代理编程工作流演示
- **测试内容**:
  - 完整的5代理工作流
  - Gemini API集成测试
  - 实际编程任务演示
- **使用方法**:
  ```bash
  source ../../.env
  python demo.py
  ```

## 🔧 环境要求

- Python 3.11+
- AutoGen框架
- Google Gemini API密钥
- 虚拟环境激活

## 📝 注意事项

1. 运行前确保虚拟环境已激活
2. 确保.env文件配置正确
3. 网络连接正常（用于API调用）
