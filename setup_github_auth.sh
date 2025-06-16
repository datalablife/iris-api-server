#!/bin/bash

# GitHub认证配置脚本
echo "🔐 GitHub认证配置"
echo "==================="
echo ""

# 收集GitHub邮箱
echo "请输入您的GitHub邮箱地址:"
read -p "邮箱: " github_email

# 收集GitHub用户名
echo ""
echo "请输入您的GitHub用户名:"
read -p "用户名: " github_username

# 收集Personal Access Token
echo ""
echo "⚠️ 重要提示: GitHub不再支持密码认证"
echo "您需要使用Personal Access Token作为密码"
echo "如果您还没有Token，请访问: https://github.com/settings/tokens"
echo ""
echo "请输入您的Personal Access Token:"
read -s -p "Token (输入时不会显示): " github_token
echo ""

# 配置Git
echo ""
echo "正在配置Git..."
git config user.email "$github_email"
git config user.name "$github_username"

echo "✅ Git配置完成"
echo "邮箱: $github_email"
echo "用户名: $github_username"
echo "Token: ${github_token:0:10}..."

# 设置远程仓库URL
echo ""
echo "设置远程仓库..."
git remote set-url origin https://github.com/datalablife/iris-api-server.git

# 尝试推送
echo ""
echo "现在尝试推送到GitHub..."
echo "🚀 推送中..."

# 使用token进行推送
git push https://$github_username:$github_token@github.com/datalablife/iris-api-server.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 推送成功！"
    echo "您的代码已经成功推送到GitHub仓库"
else
    echo ""
    echo "❌ 推送失败"
    echo "请检查您的认证信息是否正确"
fi
