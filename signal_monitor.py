#!/usr/bin/env python3
"""
HOMO 庄家信号监测 — 检测主力进场/撤离/对倒
"""
import sys, json, urllib.request, time
from datetime import datetime, timedelta

RED = "\033[91m"; GREEN = "\033[92m"; YELLOW = "\033[93m"; RESET = "\033[0m"

def capital_flow(code):
    """主力资金流向（东财push2）"""
    prefix = ("1." if code.startswith(('6','9')) else "0." if code.startswith(('0','3')) else "3.") + code
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={prefix}&fields=f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            d = json.loads(r.read()).get('data',{})
        return {
            'main_in': d.get('f47',0), 'main_out': d.get('f48',0),
            'main_net': d.get('f49',0), 'main_net_pct': d.get('f170',0),
            'big_in': d.get('f50',0), 'big_out': d.get('f51',0),
            'big_net': d.get('f52',0),
            'mid_in': d.get('f53',0), 'mid_out': d.get('f54',0),
            'mid_net': d.get('f55',0),
            'small_in': d.get('f56',0), 'small_out': d.get('f57',0),
            'small_net': d.get('f58',0),
        }
    except: return None

def get_quote_simple(code):
    """简略行情"""
    prefix = ("sh" if code.startswith(('6','9','68')) else "sz" if code.startswith(('0','3')) else "bj") + code
    try:
        with urllib.request.urlopen("http://qt.gtimg.cn/q="+prefix, timeout=5) as r:
            p = r.read().decode('gbk').split('~')
            price = float(p[3] or 0); prev = float(p[4] or 0)
            return {'name':p[1],'price':price,'pct':(price-prev)/prev*100 if prev else 0}
    except: return None

def analyze_signal(code):
    """综合分析庄家信号"""
    q = get_quote_simple(code)
    if not q: return None
    
    flow = capital_flow(code)
    signals = []
    score = 0
    
    if flow:
        for k in flow: flow[k] = float(flow[k] or 0)
        main_net = flow['main_net'] / 10000  # 万元
        big_net = flow['big_net'] / 10000
        
        # 主力净流入
        if main_net > 500: signals.append(("🟢 主力大幅净买入", f"¥{main_net:.0f}万", True)); score += 3
        elif main_net > 100: signals.append(("🟢 主力净买入", f"¥{main_net:.0f}万", True)); score += 1
        elif main_net < -500: signals.append(("🔴 主力大幅净卖出", f"¥{main_net:.0f}万", False)); score -= 3
        elif main_net < -100: signals.append(("🔴 主力净卖出", f"¥{main_net:.0f}万", False)); score -= 1
        else: signals.append(("🟡 主力资金持平", f"¥{main_net:.0f}万", None))
        
        # 大单动向
        if big_net > 300: signals.append(("🟢 大单持续买入", f"¥{big_net:.0f}万", True)); score += 2
        elif big_net < -300: signals.append(("🔴 大单持续卖出", f"¥{big_net:.0f}万", False)); score -= 2
        
        # 小单反向（主力吸筹时小单卖出）
        small_net = flow['small_net'] / 10000
        if main_net > 200 and small_net < -100:
            signals.append(("🟢 主力吸筹明显", "大单进小单出", True)); score += 2
        if main_net < -200 and small_net > 100:
            signals.append(("🔴 主力派发明显", "大单出小单接", False)); score -= 2
    
    # 综合判断
    if score >= 4: verdict = "🟢 庄家进场"
    elif score >= 1: verdict = "🟡 庄家试探性买入"
    elif score >= -1: verdict = "⚪ 庄家观望"
    elif score >= -3: verdict = "🟠 庄家试探性卖出"
    else: verdict = "🔴 庄家撤离"
    
    return {'name': q['name'], 'price': q['price'], 'pct': q['pct'], 'verdict': verdict, 'score': score, 'signals': signals}

def print_report(code):
    result = analyze_signal(code)
    if not result: print(f"无法获取 {code} 数据"); return
    
    up = result['pct'] >= 0; c = RED if up else GREEN
    print(f"\n{'='*55}")
    print(f"  {result['name']} ({code}) — {result['verdict']}")
    print(f"  现价: {c}{result['price']:.2f} ({result['pct']:+.2f}%){RESET}  信心分: {result['score']:+.0f}")
    print(f"{'='*55}")
    for label, detail, direction in result['signals']:
        print(f"  {label}: {detail}")
    if result['score'] >= 4:
        print(f"\n  💡 建议: 主力进场明显，可关注")
    elif result['score'] <= -3:
        print(f"\n  ⚠️ 建议: 主力撤离明显，注意风险")
    else:
        print(f"\n  💡 建议: 主力动向不明确，观望为主")

def batch_monitor(codes):
    print(f"\n{'='*55}")
    print(f"  🕵️ 庄家信号批量监测 ({len(codes)}只)")
    print(f"{'='*55}")
    print(f"{'代码':<8} {'名称':<10} {'信号':<20} {'分数':<6}")
    for code in codes:
        r = analyze_signal(code.strip())
        if r:
            c = GREEN if r['score'] > 0 else RED if r['score'] < 0 else YELLOW
            print(f"{code:<8} {r['name']:<10} {c}{r['verdict']:<20}{RESET} {r['score']:+.0f}")
        time.sleep(0.5)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("HOMO庄家信号监测")
        print("  python3 signal_monitor.py 600519    单只分析")
        print("  python3 signal_monitor.py --batch 600519,000858,300750  批量")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == '--batch': batch_monitor(sys.argv[2].split(','))
    else: print_report(cmd)
