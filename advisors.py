# Copyright (c) 2026 HOMO AI. Proprietary. License required. Contact: 16208204@qq.com
#!/usr/bin/env python3
"""HOMO智囊团 — 三专家综合建议"""
import sys, json, urllib.request, time

def get_quote(code):
    pfx = ("sh" if code.startswith(('6','9','68')) else "sz" if code.startswith(('0','3')) else "bj") + code
    try:
        with urllib.request.urlopen("http://qt.gtimg.cn/q="+pfx, timeout=5) as r:
            p = r.read().decode('gbk').split('~')
            price = float(p[3] or 0); prev = float(p[4] or 0)
            return {'name':p[1],'price':price,'pct':(price-prev)/prev*100 if prev else 0,'pe':float(p[39] or 0)}
    except: return None

def get_blocks(code):
    url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_DATA_BLOCKTRADE&columns=DEAL_AMT,DEAL_PRICE,PREMIUM_RATIO&pageSize=5&pageNumber=1&sortTypes=-1&sortColumns=TRADE_DATE&filter=(SECURITY_CODE=%22{code[:6]}%22)"
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://data.eastmoney.com/"})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read())
        if d.get('result') and d.get('result').get('data'): return d['result']['data']
    except: return None

def full(code):
    q = get_quote(code)
    if not q: return None
    blocks = get_blocks(code)
    
    # 三个专家
    experts = []
    
    # 技术派
    ts, tr = 0, []
    if abs(q['pct']) < 0.5: tr.append("今日窄幅震荡")
    elif q['pct'] > 2: ts=2; tr.append("今日强势上涨")
    elif q['pct'] > 0: ts=1; tr.append("今日小幅上涨")
    elif q['pct'] < -2: ts=-2; tr.append("今日明显下跌")
    elif q['pct'] < 0: ts=-1; tr.append("今日小幅下跌")
    experts.append({'name':'技术派','score':ts,'reason':tr[0] if tr else '方向不明','vote':'买入' if ts>0 else '卖出' if ts<0 else '观望'})
    
    # 价值派
    vs, vr = 0, []
    if q['pe'] <= 0: vr.append("PE为负")
    elif q['pe'] < 15: vs=2; vr.append(f"PE{q['pe']:.1f}低估")
    elif q['pe'] < 25: vs=1; vr.append(f"PE{q['pe']:.1f}合理")
    elif q['pe'] < 40: vs=-1; vr.append(f"PE{q['pe']:.1f}偏高")
    else: vs=-2; vr.append(f"PE{q['pe']:.1f}过高")
    experts.append({'name':'价值派','score':vs,'reason':vr[0],'vote':'买入' if vs>0 else '卖出' if vs<0 else '观望'})
    
    # 资金派
    cs, cr = 0, []
    if blocks:
        total = sum(b.get('DEAL_AMT',0) or 0 for b in blocks)
        if total > 50000000: cs=3; cr.append(f"巨额大宗¥{total/10000:.0f}万")
        elif total > 10000000: cs=2; cr.append(f"大额大宗¥{total/10000:.0f}万")
        elif total > 1000000: cs=1; cr.append(f"大宗¥{total/10000:.0f}万")
        else: cr.append("大宗交易量小")
    else: cr.append("近期无大宗交易")
    experts.append({'name':'资金派','score':cs,'reason':cr[0] if cr else '暂无数据','vote':'买入' if cs>=2 else '卖出' if cs<=-2 else '观望'})
    
    # 投票
    buy = sum(1 for e in experts if e['vote']=='买入')
    sell = sum(1 for e in experts if e['vote']=='卖出')
    total = ts*0.3 + vs*0.35 + cs*0.35
    
    if total >= 1.5 or buy >= 2: final = "🟢 推荐买入"
    elif total <= -1.5 or sell >= 2: final = "🔴 建议卖出"
    else: final = "⚪ 观望为主"
    
    return {'name':q['name'],'price':q['price'],'pct':q['pct'],'pe':q['pe'],
            'final':final,'score':total,'experts':experts,'buy':buy,'sell':sell}

if __name__ == "__main__":
    for code in sys.argv[1:] or ["600519"]:
        r = full(code)
        if not r: continue
        print(f"\n{'='*55}")
        print(f"  🏛️  HOMO智囊团 · {r['name']}({code})")
        print(f"  综合: {r['final']} (评分:{r['score']:+.1f})")
        print(f"  {'='*55}")
        for e in r['experts']:
            em = '🟢' if e['score']>0 else '🔴' if e['score']<0 else '⚪'
            print(f"  {em} {e['name']}: {e['vote']}({e['score']:+d}) {e['reason']}")
        print(f"  🗳️  买入{r['buy']}票 卖出{r['sell']}票")
        time.sleep(0.5)
