/**
 * HOMO 股票分析 — 后端API（权限保护版）
 * 
 * 用户通过Token调用，不接触源码
 * 
 * 用法:
 *   curl -H "X-Token: user_pro_001" http://localhost:9528/api/stock/600519
 *   curl -H "X-Token: user_pro_001" http://localhost:9528/api/hot
 */

const http = require('http');
const url = require('url');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// ===== 用户权限配置 =====
// 用户Token通过环境变量配置
// 格式: USERS='{"token1":{"plan":"pro","name":"用户","dailyLimit":999}}'
const USERS = process.env.USERS ? JSON.parse(process.env.USERS) : {
  'demo': { plan: 'free', name: '演示用户', dailyLimit: 3 },
};

// 调用次数记录
const usageFile = path.join(__dirname, '.usage.json');
let usage = {};
try { usage = JSON.parse(fs.readFileSync(usageFile, 'utf-8')); } catch(e) {}
function saveUsage() { fs.writeFileSync(usageFile, JSON.stringify(usage)); }
function getToday() { return new Date().toISOString().slice(0, 10); }

// ===== 鉴权中间件 =====
function checkAuth(req) {
  const token = req.headers['x-token'];
  if (!token) return { ok: false, error: '缺少X-Token头' };
  const user = USERS[token];
  if (!user) return { ok: false, error: 'Token无效' };
  
  const today = getToday();
  if (!usage[token]) usage[token] = {};
  if (!usage[token][today]) usage[token][today] = 0;
  
  if (usage[token][today] >= user.dailyLimit) {
    return { ok: false, error: `已达每日${user.dailyLimit}次上限` };
  }
  
  usage[token][today]++;
  saveUsage();
  return { ok: true, user };
}

// ===== 调用Python分析脚本 =====
function callPython(code) {
  try {
    const result = execSync(`python3 /data/homo-stock-advisor/stock_cli.py ${code} 2>&1`, {
      timeout: 15000, encoding: 'utf-8'
    });
    return { ok: true, data: result };
  } catch(e) {
    return { ok: false, error: e.message };
  }
}

// ===== HTTP服务 =====
const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  const parsed = url.parse(req.url, true);
  const pathParts = parsed.pathname.split('/');
  
  // API路由
  if (pathParts[1] === 'api' && pathParts[2] === 'stock' && pathParts[3]) {
    const auth = checkAuth(req);
    if (!auth.ok) { res.end(JSON.stringify(auth)); return; }
    
    const code = pathParts[3];
    const result = callPython(code);
    res.end(JSON.stringify({ code, ...result, user: auth.user.name }));
    return;
  }
  
  // 热点
  if (parsed.pathname === '/api/hot') {
    const auth = checkAuth(req);
    if (!auth.ok) { res.end(JSON.stringify(auth)); return; }
    res.end(JSON.stringify({ hot: '今日热点功能（即将上线）', user: auth.user.name }));
    return;
  }
  
  // 用量查询
  if (parsed.pathname === '/api/usage') {
    const auth = checkAuth(req);
    if (!auth.ok) { res.end(JSON.stringify(auth)); return; }
    const today = getToday();
    res.end(JSON.stringify({
      user: auth.user.name,
      plan: auth.user.plan,
      used: usage[auth.user]?.[today] || 0,
      limit: auth.user.dailyLimit,
    }));
    return;
  }
  
  // 首页（纯前端页面，无业务逻辑）
  if (parsed.pathname === '/' || parsed.pathname === '/index.html') {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.end(fs.readFileSync(path.join(__dirname, 'web', 'index.html'), 'utf-8'));
    return;
  }
  
  res.end(JSON.stringify({ error: '未知路由' }));
});

const PORT = 9528;
server.listen(PORT, () => {
  console.log(`📈 HOMO股票分析API运行中: http://localhost:${PORT}`);
  console.log(`   示例: curl -H "X-Token: user_pro_001" http://localhost:${PORT}/api/stock/600519`);
});

// 清理过期使用记录
setInterval(() => {
  const today = getToday();
  for (const token of Object.keys(usage)) {
    for (const day of Object.keys(usage[token])) {
      if (day < today) delete usage[token][day];
    }
  }
  saveUsage();
}, 3600000);
