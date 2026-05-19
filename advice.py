#!/usr/bin/env python3
"""HOMO股票投顾 — 买不买一句话"""
import sys, json, urllib.request, time
from datetime import datetime

def get_quote(code):
    prefix = ("sh" if code.startswith(('6','9','68')) else "sz" if code.startswith(('0','3')) else "bj") + code
    try:
        with urllib.request.urlopen("http://qt.gtimg.cn/q="+prefix, timeout=5) as r:
            p = r.read().decode('gbk').split('~')
            price = float(p[3] or 0); prev = float(p[4] or 0)
            return {'name':p[1],'price':price,'pct':(price-prev)/prev*100 if prev else 0,'pe':float(p[39] or 0)}
    except: return None

def get_block_trades(code):
    """大宗交易"""
    url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_DATA_BLOCKTRADE&columns=SECURITY_NAME_ABBR,DEAL_AMT,DEAL_PRICE,PREMIUM_RATIO&pageSize=5&pageNumber=1&sortTypes=-1&sortColumns=TRADE_DATE&filter=(SECURITY_CODE=%22{code[:6]}%22)"
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://data.eastmoney.com/"})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read())
        if d.get('result') and d.get('result').get('data'):
            return d['result']['data']
    except: return None

def get_news_sentiment(code):
    """新闻情绪"""
    url = "https://search-api-web.eastmoney.com/search/jsonp?cb=&param=" + urllib.parse.quote(f'{{"uid":"","keyword":"{code}","type":["cmsArticleWebOld"],"pageIndex":1,"pageSize":5}}')
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}), timeout=5) as r:
            raw = r.read().decode()
            if raw.startswith('('): raw = raw[1:-1]
            d = json.loads(raw)
        items = d.get('data',{}).get('list',[])
        pos = sum(1 for a in items if any(k in str(a) for k in ['利好','大涨','突破']))
        neg = sum(1 for a in items if any(k in str(a) for k in ['利空','大跌','减持','风险']))
        return {'total':len(items),'positive':pos,'negative':neg}
    except: return None

def advice(code):
    q = get_quote(code)
    if not q: return None
    score = 0; buy = []; sell = []
    
    # 估值面
    if q['pe'] < 15: score += 1; buy.append("PE<15估值偏低")
    elif q['pe'] > 60: score -= 1; sell.append("PE>60估值偏高")
    
    # 大宗交易
    blocks = get_block_trades(code)
    if blocks:
        total = sum(b.get('DEAL_AMT',0) or 0 for b in blocks)
        premium = sum(1 for b in blocks if (b.get('PREMIUM_RATIO',0) or 0) > 0)
        if total > 10000000:
            score += 2; buy.append(f"大宗交易¥{total/10000:.0f}万")
            if premium > len(blocks)/2: buy.append("大宗溢价成交，资金看好")
    
    # 新闻情绪
    news = get_news_sentiment(code)
    if news and news['total'] > 0:
        if news['positive'] > news['negative']: score += 1; buy.append("利好新闻偏多")
        elif news['negative'] > news['positive']: score -= 1; sell.append("利空新闻偏多")
    
    # 涨跌面
    if q['pct'] > 3: score += 1; buy.append("今日强势")
    elif q['pct'] < -3: score -= 1; sell.append("今日弱势")
    
    # 结论
    if score >= 3: verdict = "🟢 推荐买入"
    elif score >= 1: verdict = "🟡 可以关注"
    elif score >= -1: verdict = "⚪ 观望"
    elif score >= -3: verdict = "🟠 注意风险"
    else: verdict = "🔴 回避"
    
    out = f"\n{'='*50}\n {q['name']}({code}) → {verdict}  评分:{score:+.0f}\n{'='*50}"
    for b in buy: out += f"\n ✅ {b}"
    for s in sell: out += f"\n ⚠️ {s}"
    if score >= 3: out += f"\n 💡 建议：可逢低建仓"
    elif score <= -3: out += f"\n 💡 建议：注意风险"
    else: out += f"\n 💡 建议：继续观望"
    return out

if __name__ == "__main__":
    codes = sys.argv[1:] or ["600519"]
    for c in codes:
        r = advice(c)
        if r: print(r)
        time.sleep(0.3)
