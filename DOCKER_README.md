# 🐳 AutoGen Workflow Docker容器化指南

本文档详细介绍了AutoGen Programming Workflow项目的Docker容器化实现。

## 📋 目录

- [概述](#概述)
- [架构设计](#架构设计)
- [快速开始](#快速开始)
- [环境配置](#环境配置)
- [部署选项](#部署选项)
- [管理命令](#管理命令)
- [监控和日志](#监控和日志)
- [故障排除](#故障排除)

## 🎯 概述

AutoGen Workflow项目已完全容器化，支持：

- **多环境部署**: 开发、测试、生产环境
- **微服务架构**: 应用、数据库、缓存、代理分离
- **自动化测试**: 容器化测试套件
- **监控集成**: Prometheus + Grafana
- **负载均衡**: Nginx反向代理
- **数据持久化**: PostgreSQL + Redis

## 🏗️ 架构设计

### 容器组件

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx (反向代理)                      │
│                   Port: 80, 443                        │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                AutoGen App                              │
│              (主应用容器)                                │
│                Port: 8000                               │
└─────────────┬───────────────────────┬───────────────────┘
              │                       │
┌─────────────▼─────────────┐ ┌───────▼─────────────────────┐
│        Redis              │ │      PostgreSQL             │
│      (缓存/会话)           │ │      (数据存储)              │
│      Port: 6379           │ │      Port: 5432             │
└───────────────────────────┘ └─────────────────────────────┘
```

### 多阶段构建

- **base**: 基础Python环境
- **development**: 开发环境 (包含开发工具)
- **testing**: 测试环境 (包含测试工具)
- **production**: 生产环境 (精简版)
- **api-server**: API服务器 (包含Gunicorn)

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd DataApiServer

# 确保Docker已安装并运行
docker --version
docker-compose --version
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量 (必须设置API密钥)
nano .env
```

### 3. 一键启动

```bash
# 使用Docker管理器 (推荐)
chmod +x docker-manager.sh
./docker-manager.sh build    # 构建镜像
./docker-manager.sh prod     # 启动生产环境

# 或直接使用Docker Compose
docker-compose up -d
```

### 4. 验证部署

```bash
# 检查服务状态
./docker-manager.sh status

# 检查健康状态
./docker-manager.sh health

# 访问应用
curl http://localhost:8000/health
```

## ⚙️ 环境配置

### 必需的环境变量

```bash
# API密钥 (必须)
GOOGLE_API_KEY=your_google_api_key_here

# 模型配置
GEMINI_MODEL=gemini-2.5-pro-preview-05-06
TEMPERATURE=0.7
MAX_TOKENS=4000

# 数据库配置
POSTGRES_DB=autogen_db
POSTGRES_USER=autogen_user
POSTGRES_PASSWORD=autogen_password
```

### 可选配置

```bash
# 调试模式
DEBUG=false
LOG_LEVEL=INFO

# 安全配置
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here

# 监控配置
ENABLE_METRICS=true
```

## 🎛️ 部署选项

### 开发环境

```bash
# 启动开发环境
./docker-manager.sh dev

# 特点:
# - 代码热重载
# - 调试工具
# - Jupyter Notebook
# - 详细日志
```

### 生产环境

```bash
# 启动生产环境
./docker-manager.sh prod

# 特点:
# - Nginx负载均衡
# - 数据持久化
# - 监控集成
# - 自动重启
```

### 测试环境

```bash
# 运行测试套件
./docker-manager.sh test

# 运行特定测试
./docker-manager.sh test unit      # 单元测试
./docker-manager.sh test gemini    # Gemini API测试
./docker-manager.sh test shell     # Shell脚本测试
```

## 🛠️ 管理命令

### Docker管理器

```bash
# 主要命令
./docker-manager.sh build         # 构建镜像
./docker-manager.sh dev           # 开发环境
./docker-manager.sh prod          # 生产环境
./docker-manager.sh test          # 测试套件
./docker-manager.sh stop          # 停止服务
./docker-manager.sh restart       # 重启服务
./docker-manager.sh status        # 服务状态
./docker-manager.sh health        # 健康检查
./docker-manager.sh logs          # 查看日志
./docker-manager.sh shell         # 进入容器
./docker-manager.sh cleanup       # 清理资源
./docker-manager.sh monitor       # 资源监控
```

### 直接使用Docker Compose

```bash
# 生产环境
docker-compose up -d                    # 启动
docker-compose down                     # 停止
docker-compose logs -f                  # 查看日志
docker-compose ps                       # 服务状态

# 开发环境
docker-compose -f docker-compose.dev.yml up -d

# 测试环境
docker-compose -f docker-compose.test.yml up
```

## 📊 监控和日志

### 访问监控界面

```bash
# Grafana (数据可视化)
http://localhost:3000
# 用户名: admin
# 密码: admin123

# Prometheus (指标收集)
http://localhost:9090

# 应用健康检查
http://localhost:8000/health
```

### 日志管理

```bash
# 查看所有服务日志
./docker-manager.sh logs

# 查看特定服务日志
./docker-manager.sh logs autogen-app
./docker-manager.sh logs nginx
./docker-manager.sh logs redis

# 实时日志
docker-compose logs -f --tail=100
```

### 性能监控

```bash
# 资源使用情况
./docker-manager.sh monitor

# 容器统计
docker stats

# 系统使用情况
docker system df
```

## 🔧 故障排除

### 常见问题

#### 1. 容器启动失败

```bash
# 检查日志
./docker-manager.sh logs

# 检查配置
cat .env

# 重新构建
./docker-manager.sh build
```

#### 2. API密钥问题

```bash
# 验证环境变量
docker-compose exec autogen-app env | grep GOOGLE_API_KEY

# 测试API连接
./docker-manager.sh test gemini
```

#### 3. 端口冲突

```bash
# 检查端口使用
netstat -tulpn | grep :8000

# 修改端口配置
# 编辑 docker-compose.yml 中的端口映射
```

#### 4. 磁盘空间不足

```bash
# 清理Docker资源
./docker-manager.sh cleanup full

# 系统清理
docker system prune -a --volumes
```

### 调试技巧

```bash
# 进入容器调试
./docker-manager.sh shell autogen-app

# 查看容器详细信息
docker inspect autogen-app

# 检查网络连接
docker network ls
docker network inspect autogen-network
```

## 📁 文件结构

```
├── Dockerfile                    # 多阶段构建文件
├── docker-compose.yml           # 生产环境配置
├── docker-compose.dev.yml       # 开发环境配置
├── docker-compose.test.yml      # 测试环境配置
├── .dockerignore                # Docker忽略文件
├── .env.example                 # 环境变量模板
├── docker-manager.sh            # Docker管理脚本
├── docker/                      # Docker配置文件
│   ├── nginx/                   # Nginx配置
│   ├── postgres/                # PostgreSQL配置
│   ├── prometheus/              # Prometheus配置
│   └── grafana/                 # Grafana配置
└── scripts/                     # 管理脚本
    ├── docker-build.sh          # 构建脚本
    ├── docker-deploy.sh         # 部署脚本
    ├── docker-test.sh           # 测试脚本
    └── docker-cleanup.sh        # 清理脚本
```

## 🎯 最佳实践

1. **安全性**
   - 使用非root用户运行容器
   - 定期更新基础镜像
   - 妥善管理API密钥

2. **性能优化**
   - 使用多阶段构建减小镜像大小
   - 合理配置资源限制
   - 启用缓存机制

3. **监控运维**
   - 定期检查日志
   - 监控资源使用情况
   - 设置健康检查

4. **数据管理**
   - 定期备份数据卷
   - 使用持久化存储
   - 实施数据保护策略

## 🆘 获取帮助

```bash
# 查看帮助信息
./docker-manager.sh help

# 检查系统状态
./docker-manager.sh status

# 运行健康检查
./docker-manager.sh health
```

---

**注意**: 首次部署前请确保正确配置.env文件中的API密钥，否则应用将无法正常工作。
