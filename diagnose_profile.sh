#!/bin/bash

echo "========================================"
echo "  Profile页面问题诊断工具"
echo "========================================"
echo ""

# 1. 检查前端服务
echo "1. 检查前端服务状态..."
if curl -s http://localhost:5173/ | grep -q "企业AI需求对接平台"; then
    echo "   ✅ 前端服务运行正常 (http://localhost:5173)"
else
    echo "   ❌ 前端服务未运行或无法访问"
fi
echo ""

# 2. 检查后端服务
echo "2. 检查后端服务状态..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "   ✅ 后端服务运行正常 (http://localhost:8000)"
else
    echo "   ❌ 后端服务未运行或无法访问"
fi
echo ""

# 3. 测试登录并获取用户信息
echo "3. 测试用户登录..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "changan@demo.com", "password": "demo123"}')

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo "   ✅ 登录成功"
    
    TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
    USER_DATA=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; user=json.load(sys.stdin)['user']; print(f\"ID: {user['id']}, Email: {user['email']}, Role: {user['role']}, Enterprise ID: {user.get('enterprise_id', 'None')}\")" 2>/dev/null)
    
    echo "   用户信息: $USER_DATA"
else
    echo "   ❌ 登录失败"
    echo "   响应: $LOGIN_RESPONSE"
fi
echo ""

# 4. 检查Profile页面文件
echo "4. 检查Profile页面文件..."
if [ -f "frontend/src/pages/Profile.jsx" ]; then
    echo "   ✅ Profile.jsx 文件存在"
    LINE_COUNT=$(wc -l < "frontend/src/pages/Profile.jsx")
    echo "   文件行数: $LINE_COUNT"
else
    echo "   ❌ Profile.jsx 文件不存在"
fi
echo ""

# 5. 检查EnterpriseRoleSelection组件
echo "5. 检查EnterpriseRoleSelection组件..."
if [ -f "frontend/src/components/EnterpriseRoleSelection.jsx" ]; then
    echo "   ✅ EnterpriseRoleSelection.jsx 文件存在"
else
    echo "   ❌ EnterpriseRoleSelection.jsx 文件不存在"
fi
echo ""

# 6. 检查路由配置
echo "6. 检查路由配置..."
if grep -q "path=\"profile\"" "frontend/src/App.jsx"; then
    echo "   ✅ Profile路由已配置"
else
    echo "   ❌ Profile路由未配置"
fi
echo ""

echo "========================================"
echo "  诊断完成"
echo "========================================"
echo ""
echo "访问地址:"
echo "  前端: http://localhost:5173/#/profile"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "测试账号:"
echo "  需求方: changan@demo.com / demo123"
echo "  供应方: xiaoyi@demo.com / demo123"
echo ""
echo "如果页面仍然空白，请："
echo "  1. 打开浏览器开发者工具（F12）"
echo "  2. 查看Console标签的错误信息"
echo "  3. 检查localStorage中是否有token和user数据"
echo "  4. 尝试清除浏览器缓存后重新登录"
echo ""
