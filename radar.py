# Copyright (c) 2026 HOMO AI. Proprietary. License required. Contact: 16208204@qq.com
#!/usr/bin/env python3
"""
HOMO 股票雷达 — 实时捕捉异动股
付费版核心功能：监控全市场放量上涨/放量下行
"""
import sys, json, urllib.request, time, re
from datetime import datetime

RED = "\033[91m"; GREEN = "\033[92m"; YELLOW = "\033[93m"; RESET = "\033[0m"

def fetch_eastmoney(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://quote.eastmoney.com/"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.loads(r.read().decode('utf-8', errors='ignore'))
    except: return None

def get_top_gainers(top=30):
    """涨幅榜（含成交量数据）"""
    url = f"https://push2.eastmoney.com/api/qt/clist/get?cb=&fid=f3&po=1&pz={top}&pn=1&np=1&fltt=2&invt=2&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18"
    data = fetch_eastmoney(url)
    if not data or not data.get('data'): return []
    return data['data'].get('diff',[])

def detect_volume_breakout(items):
    """检测放量异动"""
    results = []
    for item in items:
        name = item.get('f14','')
        code = item.get('f12','')
        price = item.get('f2',0)
        pct = item.get('f3',0)
        amount = item.get('f6',0)  # 成交额
        volume = item.get('f5',0)  # 成交量
        turnover = item.get('f8',0)  # 换手率
        
        if not price or not amount: continue
        
        # 放量判断（成交额/价格估算）
        vol_score = 0
        signals = []
        
        # 涨幅+放量=主力拉升
        if pct > 4 and amount > 100000000:
            vol_score = 3
            signals.append(("🔴 放量暴涨", f"+{pct:.2f}% 成交¥{amount/100000000:.1f}亿"))
        elif pct > 2 and amount > 50000000:
            vol_score = 2
            signals.append(("🟡 放量拉升", f"+{pct:.2f}% 成交¥{amount/100000000:.1f}亿"))
        elif pct > 1 and amount > 30000000:
            vol_score = 1
            signals.append(("🟢 温和放量", f"+{pct:.2f}% 成交¥{amount/100000000:.1f}亿"))
        
        # 跌幅+放量=主力出逃
        if pct < -4 and amount > 100000000:
            vol_score = -3
            signals.append(("🔴 放量暴跌", f"{pct:.2f}% 成交¥{amount/100000000:.1f}亿"))
        elif pct < -2 and amount > 50000000:
            vol_score = -2
            signals.append(("🔵 放量下跌", f"{pct:.2f}% 成交¥{amount/100000000:.1f}亿"))
        
        if signals:
            results.append({'name':name,'code':code,'price':price,'pct':pct,
                           'amount':amount,'turnover':turnover,'score':vol_score,'signals':signals})
    
    # 按异动强度排序
    results.sort(key=lambda x: -abs(x['score']))
    return results

if __name__ == "__main__":
    print(f"\n{'='*55}")
    print(f"  📡 HOMO 股票雷达 · {datetime.now().strftime('%m-%d %H:%M')}")
    print(f"  {'='*55}")
    print(f"  {'名称':<12} {'代码':<8} {'现价':<8} {'异动':<12} {'成交额':<12}")
    print(f"  {'—'*12} {'—'*8} {'—'*8} {'—'*12} {'—'*12}")
    
    data = get_top_gainers(50)
    alerts = detect_volume_breakout(data)
    
    up_alerts = [a for a in alerts if a['score'] > 0][:10]
    down_alerts = [a for a in alerts if a['score'] < 0][:10]
    
    if up_alerts:
        print(f"\n  🔥 放量上涨 TOP:")
        for a in up_alerts:
            s, desc = a['signals'][0]
            print(f"  {s} {a['name']:<8} {a['code']:<8} {a['price']:<8.2f} {desc}")
    
    if down_alerts:
        print(f"\n  💧 放量下跌 TOP:")
        for a in down_alerts:
            s, desc = a['signals'][0]
            print(f"  {s} {a['name']:<8} {a['code']:<8} {a['price']:<8.2f} {desc}")
    
    if not up_alerts and not down_alerts:
        print("\n  暂无明显异动")
    
    print(f"\n  {'='*55}")
    print(f"  📊 扫描50只, 发现{len(alerts)}只异动")
    print(f"  {'='*55}")
