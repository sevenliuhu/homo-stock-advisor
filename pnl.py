#!/usr/bin/env python3
"""HOMO盈亏计算器 — 实时算盈亏"""
import sys, urllib.request

def calc(code, buy_price, shares):
    pfx = ("sh" if code.startswith(('6','9','68')) else "sz" if code.startswith(('0','3')) else "bj") + code
    try:
        with urllib.request.urlopen("http://qt.gtimg.cn/q="+pfx, timeout=5) as r:
            p = r.read().decode('gbk').split('~')
            price = float(p[3] or 0); prev = float(p[4] or 0)
            name = p[1]; pct = (price-prev)/prev*100 if prev else 0
    except: return None
    
    cost = buy_price * shares
    market = price * shares
    pnl = market - cost
    pnl_pct = pnl / cost * 100 if cost else 0
    
    print(f"\n{'='*50}")
    print(f"  {'🟢' if pnl>=0 else '🔴'} {name}({code}) 盈亏计算")
    print(f"{'='*50}")
    print(f"  买入价: ¥{buy_price:.2f}  ×  {shares:,}股")
    print(f"  当前价: ¥{price:.2f}  ({pct:+.2f}%)")
    print(f"{'='*50}")
    print(f"  持仓成本: ¥{cost:,.2f}")
    print(f"  当前市值: ¥{market:,.2f}")
    print(f"  {'='*50}")
    print(f"  盈亏: {'+' if pnl>=0 else ''}¥{pnl:,.2f}")
    print(f"  收益率: {'+' if pnl>=0 else ''}{pnl_pct:.2f}%")
    print(f"{'='*50}")
    
    if pnl > 0: print(f"  🎉 赚了¥{pnl:,.2f}，可以考虑止盈")
    elif pnl < 0: print(f"  😅 亏了¥{abs(pnl):,.2f}，耐心持有")
    else: print(f"  🤝 持平")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python3 pnl.py <代码> <买入价> <持股数>")
        print("示例: python3 pnl.py 600519 1200 100")
    else:
        calc(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]))
