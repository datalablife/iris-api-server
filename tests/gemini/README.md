# Gemini API测试脚本

本目录包含Google Gemini API相关的测试脚本。

## 📁 目录结构

### api/ - API连接测试
- **test_gemini_rest.py**: REST API连接测试
- **simple_gemini_test.py**: 简单API调用测试
- **debug_gemini.py**: API调试工具

### models/ - 模型测试
- **test_gemini_models.py**: 多模型可用性测试

### clients/ - 客户端测试
- **test_gemini_client.py**: 自定义Gemini客户端测试
- **test_updated_gemini.py**: 更新后的客户端测试
- **test_model_info.py**: 模型信息属性测试

## 🧪 测试说明

### API连接测试
验证与Google Gemini API的基本连接：
```bash
cd api
python simple_gemini_test.py
```

### 模型可用性测试
测试不同Gemini模型的可用性：
```bash
cd models
python test_gemini_models.py
```

### 客户端功能测试
测试自定义Gemini客户端：
```bash
cd clients
python test_gemini_client.py
```

## 🔑 API密钥配置

确保在根目录的.env文件中配置了正确的API密钥：
```bash
GOOGLE_API_KEY=your_api_key_here
```

## 📊 测试结果

- ✅ gemini-2.5-pro-preview-05-06: 可用（需要systemInstruction）
- ❌ gemini-2.5-pro-preview-06-05: 响应异常
- ✅ gemini-2.0-flash: 稳定可用
- ✅ gemini-1.5-pro: 标准可用
