# Copyright (c) 2026 HOMO AI. Proprietary. License required. Contact: 16208204@qq.com
#!/usr/bin/env python3
"""
HOMO 股票Pro版 — 批量分析 + 热点 + 龙虎榜 + 解禁预警
"""
import sys, json, urllib.request, time, re
from datetime import datetime, timedelta

RED = "\033[91m"; GREEN = "\033[92m"; RESET = "\033[0m"

def get_quote(code):
    prefix = ("sh" if code.startswith(('6','9','68')) else "sz" if code.startswith(('0','3')) else "bj") + code
    try:
        with urllib.request.urlopen("http://qt.gtimg.cn/q="+prefix, timeout=5) as r:
            p = r.read().decode('gbk').split('~')
            price = float(p[3] or 0); prev = float(p[4] or 0)
            return {'name':p[1],'price':price,'change':price-prev,'pct':(price-prev)/prev*100 if prev else 0,
                    'pe':float(p[39] or 0),'high':float(p[33] or 0),'low':float(p[34] or 0),'open':float(p[5] or 0),
                    'volume':int(p[6] or 0),'turnover':p[38] or '0'}
    except: return None

def get_hot_themes():
    """同花顺热点题材"""
    url = "https://push2.eastmoney.com/api/qt/clist/get?cb=&fid=f3&po=1&pz=10&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:2&fields=f12,f14,f3,f4,f8,f20"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        items = data.get('data',{}).get('diff',[])
        return [{'name':i.get('f14',''),'pct':i.get('f3',0),'rise':i.get('f4',0),'stock_count':i.get('f8',0),'amount':i.get('f20',0)} for i in items]
    except: return []

def get_dragon_tiger():
    """龙虎榜"""
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_DAILYBILLBOARD_ALL&columns=SECUCODE,SECURITY_NAME,TRADE_DATE,CHANGE_RATE,NETBUY_AMT,BILLBOARD_NETBUY_AMT&pageSize=10&pageNumber=1&sortTypes=-1&sortColumns=TRADE_DATE"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        items = data.get('result',{}).get('data',[])
        return [{'name':i.get('SECURITY_NAME',''),'code':i.get('SECUCODE',''),'pct':i.get('CHANGE_RATE',0),'net_buy':i.get('NETBUY_AMT',0)} for i in items]
    except: return []

def batch_analysis(codes):
    print(f"\n{'='*55}")
    print(f"📊 批量分析 ({len(codes)}只)")
    print(f"{'='*55}")
    print(f"{'代码':<8} {'名称':<10} {'现价':<10} {'涨跌%':<10} {'PE':<8} {'换手':<8}")
    for code in codes:
        q = get_quote(code.strip())
        if q:
            up = q['pct'] >= 0; c = RED if up else GREEN
            print(f"{code:<8} {q['name']:<10} {q['price']:<10.2f} {c}{'↑'if up else'↓'}{abs(q['pct']):.2f}%{RESET:<6} {q['pe']:<8.2f} {q['turnover']:<8}")
        time.sleep(0.3)

def show_hot():
    print(f"\n🔥 今日热点题材")
    print(f"{'='*55}")
    themes = get_hot_themes()
    if themes:
        print(f"{'题材':<20} {'涨跌幅':<10} {'上涨家数':<10}")
        for t in themes[:10]:
            up = t['pct'] >= 0; c = RED if up else GREEN
            print(f"{t['name']:<20} {c}{t['pct']:+.2f}%{RESET:<8} {t['rise']:<10}")
    else:
        print("暂无法获取热点数据")

def show_dragon():
    print(f"\n🐯 今日龙虎榜")
    print(f"{'='*55}")
    dragons = get_dragon_tiger()
    if dragons:
        print(f"{'名称':<15} {'涨跌幅':<10} {'净买入':<15}")
        for d in dragons[:10]:
            c = RED if d['pct'] >= 0 else GREEN
            net = d['net_buy'] / 10000 if d['net_buy'] else 0
            print(f"{d['name']:<15} {c}{d['pct']:+.2f}%{RESET:<8} {net:+.0f}万")
    else:
        print("暂无法获取龙虎榜数据")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("HOMO股票Pro版")
        print("  python3 pro_tools.py 600519,000001  批量分析")
        print("  python3 pro_tools.py --hot          热点题材")
        print("  python3 pro_tools.py --dragon       龙虎榜")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == '--hot': show_hot()
    elif cmd == '--dragon': show_dragon()
    else: batch_analysis(cmd.split(','))
