# 🔧 Git & GitHub 配置指南

本文档详细说明了AutoGen Workflow项目的Git和GitHub配置过程。

## 📋 配置概述

### ✅ 已完成的配置

1. **Git仓库初始化** ✅
   - 初始化Git仓库
   - 配置用户信息 (Jack Chan, 163439565+datalablife@users.noreply.github.com)
   - 设置默认分支为 `main`
   - 添加远程仓库: `git@github.com:datalablife/iris-api-server.git`

2. **初始提交** ✅
   - 创建了包含所有项目文件的初始提交
   - 提交信息包含完整的功能描述
   - 65个文件，13,564行代码

3. **SSH密钥生成** ✅
   - 生成了ED25519 SSH密钥对
   - 公钥已准备好添加到GitHub

4. **GitHub工作流配置** ✅
   - CI/CD管道 (`.github/workflows/ci.yml`)
   - Docker构建流程 (`.github/workflows/docker.yml`)
   - Issue模板 (Bug报告、功能请求)
   - PR模板

## 🔑 SSH密钥配置

### 生成的SSH公钥
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIRscqAABFnQQj7A9+l6hAwYHqVaL1jzPa8Bg481UY46 163439565+datalablife@users.noreply.github.com
```

### 添加SSH密钥到GitHub

1. **复制上面的SSH公钥**

2. **登录GitHub并添加SSH密钥**:
   - 访问: https://github.com/settings/ssh/new
   - 标题: `AutoGen Workflow - WSL`
   - 密钥类型: `Authentication Key`
   - 粘贴上面的公钥内容

3. **验证SSH连接**:
   ```bash
   ssh -T git@github.com
   ```

## 🚀 推送到GitHub

### 首次推送
```bash
# 推送到远程仓库
git push -u origin main
```

### 验证推送
```bash
# 检查远程状态
git remote -v
git status
```

## 📁 项目结构

### Git配置文件
```
.git/                           # Git仓库数据
.gitignore                      # Git忽略规则
.github/                        # GitHub配置
├── workflows/                  # GitHub Actions
│   ├── ci.yml                 # CI/CD管道
│   └── docker.yml             # Docker构建
├── ISSUE_TEMPLATE/            # Issue模板
│   ├── bug_report.md          # Bug报告模板
│   └── feature_request.md     # 功能请求模板
└── pull_request_template.md   # PR模板
```

### 管理脚本
```
scripts/
├── git-setup.sh               # Git设置脚本
└── github-manager.sh          # GitHub管理脚本
```

## 🛠️ 管理命令

### Git操作
```bash
# 检查状态
git status

# 查看提交历史
git log --oneline

# 创建新分支
git checkout -b feature/new-feature

# 提交更改
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

### GitHub管理
```bash
# 使用GitHub管理脚本
./scripts/github-manager.sh setup    # 完整设置
./scripts/github-manager.sh check    # 检查仓库状态
./scripts/github-manager.sh info     # 显示仓库信息
```

## 🔐 GitHub Personal Access Token

### 配置的Token
- **Token**: `ghp_****************************` (已配置)
- **用途**: Augment GitHub MCP配置
- **权限**: 需要repo、workflow、admin:org权限

### 使用Token
```bash
# 设置环境变量
export GITHUB_TOKEN=your_github_token_here

# 或在.env文件中添加
echo "GITHUB_TOKEN=your_github_token_here" >> .env
```

## 🎯 GitHub Actions配置

### CI/CD管道特性
- **自动测试**: 单元测试、集成测试、类型检查
- **代码质量**: Linting、格式检查
- **Docker构建**: 多阶段构建和推送
- **安全扫描**: Trivy漏洞扫描
- **自动部署**: 基于分支的部署策略

### 需要设置的Secrets
在GitHub仓库设置中添加以下Secrets:
```
GOOGLE_API_KEY          # Google Gemini API密钥
DOCKER_USERNAME         # Docker Hub用户名
DOCKER_PASSWORD         # Docker Hub密码
```

## 📊 仓库配置

### 分支保护规则
建议为`main`分支设置保护规则:
- 要求PR审查
- 要求状态检查通过
- 要求分支为最新
- 限制推送到分支

### Issue标签
自动创建的标签包括:
- `bug`, `enhancement`, `documentation`
- `priority:high/medium/low`
- `type:feature/bugfix/refactor`
- `status:in-progress/review/blocked`
- `docker`, `autogen`, `gemini-api`

## 🔄 工作流程

### 开发流程
1. **创建功能分支**:
   ```bash
   git checkout -b feature/your-feature
   ```

2. **开发和测试**:
   ```bash
   # 本地开发
   ./docker-manager.sh dev
   
   # 运行测试
   ./docker-manager.sh test
   ```

3. **提交更改**:
   ```bash
   git add .
   git commit -m "feat: implement new feature"
   git push origin feature/your-feature
   ```

4. **创建Pull Request**:
   - 在GitHub上创建PR
   - 填写PR模板
   - 等待CI检查通过
   - 请求代码审查

5. **合并到主分支**:
   - 审查通过后合并
   - 自动触发部署流程

### 发布流程
1. **创建发布分支**:
   ```bash
   git checkout -b release/v1.0.0
   ```

2. **更新版本信息**:
   - 更新版本号
   - 更新CHANGELOG
   - 更新文档

3. **创建标签**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

## 🚨 故障排除

### SSH连接问题
```bash
# 测试SSH连接
ssh -T git@github.com

# 如果失败，检查SSH代理
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 推送权限问题
```bash
# 检查远程URL
git remote -v

# 确保使用SSH URL
git remote set-url origin git@github.com:datalablife/iris-api-server.git
```

### GitHub Actions失败
1. 检查Secrets是否正确设置
2. 查看Actions日志
3. 验证工作流文件语法

## 📞 下一步操作

1. **立即执行**:
   ```bash
   # 添加SSH密钥到GitHub (手动)
   # 然后推送代码
   git push -u origin main
   ```

2. **设置GitHub仓库**:
   ```bash
   # 使用GitHub管理脚本
   ./scripts/github-manager.sh setup
   ```

3. **配置Secrets**:
   - 在GitHub仓库设置中添加必要的Secrets
   - 测试GitHub Actions工作流

4. **开始开发**:
   ```bash
   # 创建开发分支
   git checkout -b develop
   git push -u origin develop
   ```

## 🎉 总结

✅ **Git配置完成**:
- 仓库初始化和配置
- 用户信息设置
- 远程仓库连接
- 初始提交创建

✅ **GitHub配置准备就绪**:
- SSH密钥生成
- GitHub Actions工作流
- Issue和PR模板
- 管理脚本

🔄 **待完成**:
- 添加SSH密钥到GitHub
- 首次推送到远程仓库
- 设置GitHub仓库Secrets
- 配置分支保护规则

现在您可以开始使用Git和GitHub进行版本控制和协作开发了！🚀
