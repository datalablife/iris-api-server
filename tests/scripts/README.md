# 测试脚本

本目录包含各种Shell脚本和自动化测试工具。

## 📁 目录结构

### curl/ - curl测试脚本
包含使用curl直接测试API的脚本，绕过Python网络配置问题。

## 🔧 curl测试脚本说明

### test_curl.sh
- **功能**: 基本的Gemini API curl测试
- **使用方法**:
  ```bash
  cd curl
  ./test_curl.sh
  ```

### simple_model_test.sh
- **功能**: 简化的模型测试
- **测试模型**:
  - gemini-2.5-pro-preview-05-06
  - gemini-2.5-pro-preview-06-05
  - gemini-2.0-flash

### test_models_curl.sh
- **功能**: 完整的模型测试套件
- **包含**: 模型列表API测试

### test_preview_models.sh
- **功能**: 预览模型专项测试
- **特点**: 包含systemInstruction测试

### test_preview_simple.sh
- **功能**: 简化的预览模型测试

### test_with_system_instruction.sh
- **功能**: 系统指令测试
- **用途**: 验证预览模型的特殊要求

## 🚀 使用说明

1. **确保脚本可执行**:
   ```bash
   chmod +x *.sh
   ```

2. **运行测试**:
   ```bash
   ./script_name.sh
   ```

3. **查看结果**:
   - 成功: 返回JSON响应
   - 失败: 显示错误信息

## 📝 注意事项

- 所有脚本都包含API密钥，请确保安全
- 网络连接需要正常
- 某些脚本需要jq工具（JSON解析）
