# AutoGen 编程工作流 - 快速开始指南

## 🚀 5分钟快速上手

### 第1步: 环境准备

```bash
# 确保Python版本
python --version  # 需要 3.9+

# 安装依赖
pip install -r requirements.txt
```

### 第2步: 配置API密钥

选择以下方式之一：

**方式A: 环境变量 (推荐)**
```bash
# 使用Google Gemini (推荐)
export GOOGLE_API_KEY="your_gemini_api_key"

# 或使用OpenAI
export OPENAI_API_KEY="your_openai_api_key"
```

**方式B: 配置文件**
```bash
# 复制配置模板
cp .env.example .env

# 编辑.env文件，添加你的API密钥
```

### 第3步: 验证安装

```bash
# 运行安装测试
python test_installation.py
```

如果看到 "🎉 All tests passed!" 说明安装成功。

### 第4步: 运行演示

```bash
# 运行简单演示
python demo.py
```

## 📝 基本使用示例

### 示例1: 创建简单API

```python
from autogen_workflow import ProgrammingWorkflow, WorkflowConfig

# 创建工作流
workflow = ProgrammingWorkflow()

# 定义任务
task = """
创建一个简单的FastAPI应用，包含：
1. 健康检查端点 /health
2. 计算器端点 /calculate (加法)
3. 基本错误处理
"""

# 运行工作流
result = await workflow.run_workflow(task)

# 查看结果
if result["status"] == "success":
    print("✅ 任务完成!")
    # 查看生成的代码
    artifacts = result["artifacts"]
```

### 示例2: 数据分析API

```python
task = """
创建数据分析API服务器：
- CSV文件上传
- 基础统计分析
- 数据可视化
- JWT认证
- PostgreSQL存储
"""

context = {
    "project_type": "data_api",
    "complexity": "medium",
    "timeline": "4 weeks"
}

result = await workflow.run_workflow(task, context)
```

## 🎯 常用任务模板

### Web API开发
```python
task = """
创建RESTful API服务：
- 用户认证和授权
- CRUD操作接口
- 数据验证和错误处理
- API文档生成
- 单元测试
"""
```

### 数据处理系统
```python
task = """
开发数据处理系统：
- 多格式文件解析
- 数据清洗和转换
- 批量处理能力
- 结果导出功能
- 进度监控
"""
```

### 微服务架构
```python
task = """
设计微服务架构：
- 服务拆分策略
- API网关设计
- 服务间通信
- 配置管理
- 监控和日志
"""
```

## ⚙️ 配置选项

### 基础配置
```python
from autogen_workflow.config import ModelConfig, WorkflowConfig

# 模型配置
model_config = ModelConfig(
    gemini_model="gemini-2.0-flash",  # 推荐模型
    temperature=0.7,                  # 创造性平衡
    max_tokens=4000                   # 响应长度
)

# 工作流配置
workflow_config = WorkflowConfig(
    model_config=model_config,
    max_messages=50,                  # 最大消息数
    max_rounds=20,                    # 最大轮次
    timeout_seconds=300               # 超时时间
)
```

### 高级配置
```python
# 自定义Agent行为
config = WorkflowConfig.create_default()

# 修改架构师Agent
architect_config = config.get_agent_config("architect")
architect_config.system_message += "\n专注于云原生架构设计。"

# 修改程序员Agent
programmer_config = config.get_agent_config("programmer")
programmer_config.system_message += "\n优先使用异步编程模式。"
```

## 📊 结果处理

### 查看生成的产物
```python
result = await workflow.run_workflow(task)

if result["status"] == "success":
    artifacts = result["artifacts"]
    
    # 架构设计
    if artifacts.get("architecture_design"):
        print("📐 架构设计已生成")
    
    # 源代码
    source_code = artifacts.get("source_code", [])
    print(f"💻 生成了 {len(source_code)} 个代码文件")
    
    # 审查报告
    reviews = artifacts.get("review_reports", [])
    print(f"🔍 生成了 {len(reviews)} 个审查报告")
```

### 保存结果到文件
```python
import json
from datetime import datetime

# 保存完整结果
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"workflow_result_{timestamp}.json", "w") as f:
    json.dump(result, f, indent=2, default=str)

# 保存源代码
if artifacts.get("source_code"):
    for i, code in enumerate(artifacts["source_code"]):
        with open(f"generated_code_{i+1}.py", "w") as f:
            f.write(code["content"])
```

## 🔧 故障排除

### 常见错误及解决方案

**错误1: API密钥无效**
```
ValueError: No valid API key found
```
解决：检查环境变量或配置文件中的API密钥

**错误2: 模型不可用**
```
Model 'gemini-2.5-pro' not available
```
解决：使用可用模型如 `gemini-2.0-flash`

**错误3: 超时错误**
```
TimeoutError: Workflow execution timeout
```
解决：增加 `timeout_seconds` 配置或简化任务

**错误4: 内存不足**
```
OutOfMemoryError
```
解决：减少 `max_tokens` 或分阶段执行任务

### 调试技巧

```bash
# 启用详细日志
python autogen_workflow/main.py --log-level DEBUG

# 检查配置
python -c "
from autogen_workflow.config import WorkflowConfig
config = WorkflowConfig.create_default()
print('配置验证:', config.validate())
"

# 测试API连接
python -c "
import os
print('Gemini Key:', bool(os.getenv('GOOGLE_API_KEY')))
print('OpenAI Key:', bool(os.getenv('OPENAI_API_KEY')))
"
```

## 💡 使用技巧

### 1. 任务描述优化
- **具体化**: 明确功能需求和技术要求
- **结构化**: 使用列表和分层描述
- **上下文**: 提供项目背景和约束条件

### 2. 分阶段执行
```python
# 第一阶段：架构设计
arch_task = "设计数据分析API的系统架构"
arch_result = await workflow.run_workflow(arch_task)

# 第二阶段：基于架构实现
impl_task = f"""
基于以下架构实现代码：
{arch_result['artifacts']['architecture_design']}
"""
impl_result = await workflow.run_workflow(impl_task)
```

### 3. 质量控制
```python
# 设置严格的质量要求
task = """
创建高质量的API服务，要求：
- 代码覆盖率 > 90%
- 无安全漏洞
- 性能测试通过
- 完整的API文档
"""
```

## 🎓 学习资源

### 官方文档
- [AutoGen官方文档](https://github.com/microsoft/autogen)
- [Google Gemini API](https://ai.google.dev/)
- [OpenAI API文档](https://platform.openai.com/docs)

### 示例项目
- `demo.py` - 基础演示
- `autogen_workflow/main.py` - 完整示例
- `Workflow_README.md` - 详细说明

### 社区支持
- GitHub Issues: 报告问题和建议
- 讨论区: 技术交流和经验分享

## 🚀 下一步

1. **熟悉基础**: 运行几个简单示例
2. **尝试定制**: 修改Agent配置和行为
3. **实际项目**: 在真实项目中使用工作流
4. **贡献代码**: 参与项目改进和扩展

---

**提示**: 建议从简单任务开始，逐步尝试复杂的项目。记住保存重要的工作流结果！
