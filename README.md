<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Node.js-20+-green?style=for-the-badge&logo=node.js" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/版本-v2.0-orange?style=for-the-badge" />
  <br/>
  <img src="https://img.shields.io/github/stars/sevenliuhu/homo-stock-advisor?style=social" />
  <img src="https://img.shields.io/github/forks/sevenliuhu/homo-stock-advisor?style=social" />
</div>

<h1 align="center">📈 HOMO A股智能投研助手</h1>

<p align="center">
  <b>散户输的不是技术，是情绪</b><br/>
  三专家智囊团 · 零情绪 · 纯算法 · 给你明确买卖建议
</p>

<p align="center">
  <a href="#-散户之痛">散户之痛</a> ·
  <a href="#-智囊团三专家">智囊团</a> ·
  <a href="#-大师心法内置">大师心法</a> ·
  <a href="#-功能对比">功能对比</a> ·
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-购买方式">购买方式</a>
</p>

---

## 🎯 散户之痛

```text
❌ 看见涨了追进去，第二天就跌
❌ 跌了舍不得割，越拿越深
❌ 利好新闻一出，进去就是接盘
❌ 看了一堆K线图，还是不知道买还是卖

—— 你不是技术不行，你是被情绪控制了
```

**HOMO 智囊团没有恐慌和贪婪，只有算法。**

三个不同风格的AI专家，各自独立分析，然后投票。少数服从多数。就这么简单。

---

## 🏛️ 智囊团三专家

### 👤 技术面专家 — 趋势大师
> "趋势是你唯一的朋友" — 利弗莫尔

- MA/MACD/RSI/KDJ/BOLL五大指标全量计算
- 金叉死叉、超买超卖、布林带触顶触底
- 不看消息，只看数字

### 👤 基本面专家 — 价值猎手
> "用四毛钱买一块钱的东西" — 巴菲特

- PE/PB/PEG估值体系
- 市值/换手率/涨跌幅异常检测
- 你不是买股票，你是买公司

### 👤 资金面专家 — 量价侦探
> "价格永远是对的" — 利弗莫尔

- 量比分析（放量/缩量背后的主力意图）
- 5天量价配合模型
- 量是水的深浅，价是船的浮沉

### 🏆 最终决策
```
三专家独立投票 → 加权综合 → 买入/卖出/观望
每个决策都告诉你：为什么这么判
```

---

## 🧠 大师心法·内置

我们研究了**五位中国顶级游资**和**四位国际交易大师**的心法，把他们的核心策略变成了算法：

### 🇨🇳 中国游资篇

| 大师 | 绝活 | 如何内置 |
|:----|:-----|:---------|
| **章盟主** | "重势不重价" | 右侧确认信号 + 龙头强度评分 |
| **方新侠** | "龙头的尽头是天空" | 反包概率模型 + 趋势连板持有 |
| **赵老哥** | "二板定龙头" | 涨停梯队识别 + 溢价预期 |
| **炒股养家** | **情绪周期四阶段** | 冰点→启动→高潮→退潮自动判断 |
| **交易猿** | "用算法思维做短线" | 竞价选股 + 盘口量化 |

### 🌍 国际大师篇

| 大师 | 精华 | 内置方式 |
|:----|:-----|:---------|
| **利弗莫尔** | "截断亏损，让利润奔跑" | 动态止盈止损 + 金字塔仓位 |
| **索罗斯** | "市场的偏见就是你的机会" | 反身性预警 + 泡沫识别 |
| **彼得·林奇** | "在恐慌中买入" | PEG估值 + 消费类扫描 |
| **达利欧** | "用系统交易" | 风险平价仓位管理 |

---

## 🔥 你看到的不是预测，是信号

```
不是"明天必涨"
而是"三个专家里有2个认为应该买入，
因为MACD金叉+RSI超卖+量价企稳"
```

**散户看预测，高手读信号。**

---

## 🚀 核心功能

### 📊 全自动分析流
```
输入股票代码 → 拉取行情+K线 → 五维技术分析 → 三专家投票 → 输出决策
```

### 🏛️ 智囊团决策（核心）
| 场景 | 输入 | 输出 |
|:----|:-----|:-----|
| 查茅台 | `600519` 或 `茅台` | 完整分析 + 三专家投票 |
| 看市场 | `热点` | 上证/深证/创业板指数 |
| 模拟交易 | `买入茅台 10股` | 模拟买入 + 记录持仓 |
| 账户 | `持仓` | 持仓盈亏一览 |

### 📈 技术指标
MA5/10/20/60 · MACD金叉死叉 · RSI超买超卖 · KDJ · 布林带上中下轨

### 🎯 智囊团仓位建议
```
总资金100,000 → 建议投入33,333 → 凯利公式优化 → 风报比1.88
```

---

## 📋 功能对比

| 功能 | 🆓 免费版 | 💎 Pro版 | 🏢 企业版 |
|:----|:--------:|:---------:|:---------:|
| 单股分析 | ✅ | ✅ | ✅ |
| 五大技术指标 | ✅ | ✅ | ✅ |
| 智囊团三专家投票 | ❌ | ✅ | ✅ |
| 模拟交易 | ✅ | ✅ | ✅ |
| 热点题材 | ❌ | ✅ | ✅ |
| 情绪周期判断 | ❌ | ✅ | ✅ |
| 龙虎榜游资识别 | ❌ | ✅ | ✅ |
| 大师心法策略引擎 | ❌ | ✅ | ✅ |
| 批量分析 | ❌ | ❌ | ✅ |
| 解禁预警 | ❌ | ❌ | ✅ |
| 自动推送提醒 | ❌ | ❌ | ✅ |
| 定制策略 | ❌ | ❌ | ✅ |

---

## ⚡ 快速开始

### 在线体验（无需安装）
```
浏览器打开：http://101.37.234.151:3000
或直接输入：http://101.37.234.151:3000/chat
输入 600519 试试！
```

### CLI 方式
```bash
git clone https://github.com/sevenliuhu/homo-stock-advisor.git
cd homo-stock-advisor
pip install -r requirements.txt

# 分析单只股票
python stock_cli.py 600519

# 查看市场热点
python stock_cli.py market
```

### API 方式
```bash
curl "http://101.37.234.151:3000/api/analyze?code=600519"
```

---

## 💰 购买方式

| 版本 | 价格 | 权益 |
|:-----|:----:|:------|
| **💎 Pro版** | **¥500/年** | 智囊团 + 情绪周期 + 龙虎榜 + 大师心法引擎 |
| **🏢 企业版** | **¥2,000/年** | 批量 + 解禁 + 策略 + 推送 + 定制 |
| **🔒 永久版** | **¥2,000** | 买断终身更新 |

**👉 联系购买**

| 方式 | 账号 |
|:-----|:------|
| 📧 邮箱 | （联系作者获取） |
| 💬 微信 | （联系作者获取） |

> 购买后提供独立 Token，在网页版或 CLI 中使用。
> 源码不公开，核心逻辑跑在服务端，保障代码安全。

---

## ⚖️ 免责声明

```
本工具提供的所有信息仅供参考，不构成投资建议。
股市有风险，投资需谨慎。过去的表现不代表未来的收益。
```

---

## 🏗️ 技术架构

```text
用户（网页 / CLI） →  🔑 Token 鉴权
                    ↓
HOMO 后端服务器
 ├── 📡 腾讯行情 API     →  实时行情 + K线
 ├── 🧠 智囊团分析引擎   →  三专家投票
 ├── 🧘 情绪周期判定     →  冰点/启动/高潮/退潮
 ├── 🐉 龙虎榜扫描器     →  游资席位识别
 ├── 💰 模拟交易引擎     →  买入/卖出/持仓/止盈止损
 └── 📊 大师心法策略库   →  5位大师+Kelly仓位
```

---

<p align="center">
  <b>Made with ❤️ by <a href="https://github.com/sevenliuhu">HOMO Team</a></b><br/>
  <sub>让每个股民都能享受专业级的投资分析 —— 不带情绪的那种</sub>
</p>


---

## Business Contact

**HOMO AI Agent OS** — Not just an AI assistant, your entire AI team.

| Channel | Contact |
|:--------|:--------|
| Email | **16208204@qq.com** |
| Phone/WeChat | **** |
| GitHub | [sevenliuhu](https://github.com/sevenliuhu) |
| Services | Web Scraping, AI Agent Workflows, Web Dev, Brand Design, Short Video, Tech Solutions |

> For custom development or commercial license, contact us above. Response within 24h.
> This repository is for reference only. Commercial use requires a license.

