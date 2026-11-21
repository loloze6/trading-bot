import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drift = {}
    for c, ws in data["bars"].items():
        r = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl)-5, 5)
            r += list(cl[idx+5]/cl[idx]-1)
        drift[c] = np.mean(r)
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = pd.Series(b["close"].values)
            n = len(cl)
            idx = np.arange(0, n-5, 5)
            fr = cl.values[idx+5]/cl.values[idx]-1 - drift[c]
            lr = np.log(cl).diff()
            d = {"coin": c, "win": w, "ex": fr,
                 "r28": cl.pct_change(28).values[idx],
                 "r1": cl.pct_change(1).values[idx],
                 "r7": cl.pct_change(7).values[idx],
                 "near": (cl/cl.rolling(90, min_periods=30).max()-1).values[idx],
                 "vol30": lr.rolling(30).std().values[idx]}
            for k in ["mom","rev","high","vol"]:
                d[k+"_raw"] = b[f"debug_info.components.{k}.last_history_value"].values[idx]
            rows.append(pd.DataFrame(d))
    df = pd.concat(rows, ignore_index=True)
    out = {}
    # carry-forward test: split by inferred sign of w_k (component raw sign vs signal sign)
    res = []
    for k, raw in [("mom","r28"),("rev","r1")]:
        s = df[[k+"_raw", raw, "ex"]].dropna()
        s = s[(s[raw]!=0)&(s[k+"_raw"]!=0)]
        wpos = np.sign(s[k+"_raw"])==np.sign(s[raw])
        sx = np.sign(s[raw])*s["ex"]
        for lab, m in [("past_w_pos", wpos), ("past_w_neg", ~wpos)]:
            x = sx[m]
            res.append({"sig": k, "group": lab, "n": len(x), "signed_ex_by_raw_sign": x.mean(),
                        "t": x.mean()/x.std()*np.sqrt(len(x))})
    out["future_power_by_past_sign"] = pd.DataFrame(res)
    # raw signals, graded: quintiles within coin
    q = []
    for raw in ["r28","r7","r1","near","vol30"]:
        s = df[["coin",raw,"ex"]].dropna().copy()
        s["q"] = s.groupby("coin")[raw].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
        g = s.groupby("q")["ex"].agg(["mean","count"])
        g.index = [f"{raw}_q{int(i)}" for i in g.index]
        q.append(g)
    out["raw_quintiles"] = pd.concat(q)
    # simple t of spread top minus bottom quintile
    sp = []
    for raw in ["r28","r7","r1","near","vol30"]:
        s = df[["coin",raw,"ex"]].dropna().copy()
        s["q"] = s.groupby("coin")[raw].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
        a = s[s.q==4].ex; b = s[s.q==0].ex
        t = stats.ttest_ind(a, b, equal_var=False).statistic
        sp.append({"sig": raw, "top_minus_bottom": a.mean()-b.mean(), "t": t, "n_top": len(a), "n_bot": len(b)})
    out["spread"] = pd.DataFrame(sp)
    return out
