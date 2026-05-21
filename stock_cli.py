# Copyright (c) 2026 HOMO AI. Proprietary. License required. Contact: 16208204@qq.com
#!/usr/bin/env python3
"""
HOMO 股票分析助手 — CLI版
用法: python3 stock_cli.py <股票代码>
"""
import sys, json, urllib.request
from datetime import datetime

def get_prefix(code):
    if code.startswith(('6','9','68')): return "sh"+code
    if code.startswith(('0','3')): return "sz"+code
    if code.startswith(('4','8')): return "bj"+code
    return code

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def up(text, up_flag=True):
    return (RED if up_flag else GREEN) + str(text) + RESET

def get_quote(code):
    prefix = get_prefix(code)
    try:
        with urllib.request.urlopen("http://qt.gtimg.cn/q="+prefix, timeout=5) as r:
            raw = r.read().decode('gbk')
        parts = raw.split('~')
        if len(parts) > 45:
            price = float(parts[3] or 0)
            prev_close = float(parts[4] or 0)
            return {
                'name': parts[1], 'price': price,
                'change': price - prev_close,
                'pct': (price - prev_close) / prev_close * 100 if prev_close else 0,
                'high': float(parts[33] or 0), 'low': float(parts[34] or 0),
                'open': float(parts[5] or 0),
                'volume': int(parts[6] or 0),
                'pe': float(parts[39] or 0) if parts[39] else 0,
                'turnover': parts[38] or '0',
                'cap': float(parts[45] or 0),
            }
    except: return None

def get_reports(code):
    try:
        url = "https://reportapi.eastmoney.com/report/list?cb=&pageSize=5&page=1&stockCode="+code+"&industryCode=*"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        return [{'title':i.get('title','')[:45],'rating':i.get('ratingName',''),'org':i.get('orgName',''),'date':(i.get('publishDate','') or '')[:10]} for i in data.get('data',[])]
    except: return []

def get_news(code):
    try:
        url = "https://search-api-web.eastmoney.com/search/jsonp?cb=&param=" + urllib.parse.quote('{"uid":"","keyword":"'+code+'","type":["cmsArticleWebOld"],"pageIndex":1,"pageSize":5}')
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        return [{'title':a.get('title','')[:40],'date':(a.get('date','') or '')[:10]} for a in data.get('data',{}).get('list',[])]
    except: return []

def print_report(code):
    q = get_quote(code)
    if not q:
        print("无法获取数据:", code)
        return
    is_up = q['pct'] >= 0
    print("\n"+ "="*50)
    print(" %s (%s)" % (q['name'], code))
    print("="*50)
    print(" 现价: " + up("%.2f" % q['price'], is_up))
    print(" 涨跌: " + up("%+.2f (%+.2f%%)" % (q['change'], q['pct']), is_up))
    print(" 最高: %.2f  最低: %.2f  开盘: %.2f" % (q['high'], q['low'], q['open']))
    print(" PE: %.2f  换手率: %s" % (q['pe'], q['turnover']))
    if q['cap']: print(" 市值: %.2f亿" % (q['cap']/100000000))
    
    reps = get_reports(code)
    if reps:
        print("\n研报:")
        for r in reps[:3]:
            print("  [%s] %s - %s" % (r['rating'], r['title'][:40], r['org']))
    
    news = get_news(code)
    if news:
        print("\n新闻:")
        for n in news[:3]:
            print("  %s %s" % (n['date'], n['title']))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 stock_cli.py <股票代码>")
        sys.exit(1)
    print_report(sys.argv[1])
