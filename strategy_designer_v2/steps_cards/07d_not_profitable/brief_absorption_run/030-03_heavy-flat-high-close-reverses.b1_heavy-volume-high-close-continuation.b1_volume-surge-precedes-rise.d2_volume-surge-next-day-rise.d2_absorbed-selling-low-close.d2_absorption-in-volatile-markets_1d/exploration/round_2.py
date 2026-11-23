def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    P = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r = b.close.pct_change()
            b["nxt"] = b.close.shift(-1) / b.close - 1
            b["r60"] = b.close / b.close.shift(60) - 1
            b["ma100"] = b.close / b.close.rolling(100, min_periods=60).mean() - 1
            b["dayret"] = r
            vol = r.rolling(20).std()
            b["dsd"] = r / vol
            b["vr"] = vol / vol.rolling(60).mean()
            b["alloc"] = b.postRebalance_current_allocation
            b["dalloc"] = (b.alloc - b.previous_allocation).abs()
            b["gain"] = b.alloc * b.nxt
            b["coin"] = c; b["win"] = w
            b["day"] = pd.to_datetime(b.timestamp).dt.floor("D")
            b["pos"] = np.arange(len(b))
            P.append(b[["coin","win","day","pos","nxt","r60","ma100","dayret","dsd","vr","alloc","dalloc","gain","forecast","regime"]])
    P = pd.concat(P, ignore_index=True)
    P["sig"] = P.forecast > 0
    P["down"] = P.dayret < 0
    # condition alone vs with signal, next-day
    g = P.dropna(subset=["nxt","dayret"])
    out["nxt_by_down_sig"] = g.groupby(["down","sig"]).nxt.agg(["size","mean","std"])
    g2 = g.copy(); g2["dsdq"] = pd.qcut(g2.dsd, 5, labels=False)
    out["nxt_by_dsdq_sig"] = g2.groupby(["dsdq","sig"]).nxt.agg(["size","mean"]).unstack()
    # among signal & down bars, graded by forecast?
    s = g[g.sig & g.down].copy()
    s["fq"] = pd.qcut(s.forecast, 4, labels=False, duplicates="drop")
    out["sigdown_by_forecastq"] = s.groupby("fq").agg(n=("nxt","size"), f=("forecast","mean"), nxt=("nxt","mean"), gain=("gain","mean"))
    # trend state
    g3 = g.dropna(subset=["ma100"]).copy()
    g3["bear"] = g3.ma100 < 0
    out["nxt_by_bear_down_sig"] = g3.groupby(["bear","down","sig"]).agg(n=("nxt","size"), nxt=("nxt","mean"), gain=("gain","mean"), sd=("gain","std"))
    # simulated books with masks; costs 0.095% per unit traded
    def book(mask, name):
        Q = P.copy()
        a = np.where(mask, Q.alloc, 0.0)
        Q["a"] = a
        Q["pa"] = Q.groupby(["coin","win"]).a.shift(1).fillna(0)
        Q["g"] = Q.a * Q.nxt.fillna(0) - 0.00095 * (Q.a - Q.pa).abs()
        D = Q.groupby(["win","day"]).g.mean().reset_index()
        D["wn"] = D.win.str[1:].astype(int)
        D = D.sort_values(["wn","day"])
        v = (1 + D.g).cumprod()
        mdd = float((v / v.cummax() - 1).min())
        yr = float(v.iloc[-1] ** (365 / len(D)) - 1)
        sh = float(D.g.mean() / D.g.std() * np.sqrt(365))
        return {"name": name, "yearly": yr, "maxdd": mdd, "calmar": yr / -mdd, "sharpe": sh, "inpos": float((Q.a.abs() > 1e-6).mean())}
    rows = [book(np.ones(len(P), bool), "as_is_approx"),
            book((P.dayret < 0).values, "down_day_only"),
            book((P.dsd < -0.5).values, "dsd_below_-0.5"),
            book((P.ma100.fillna(0) >= 0).values, "above_ma100"),
            book(((P.dayret < 0) & (P.ma100.fillna(0) >= 0)).values, "down_and_above_ma100")]
    out["books"] = pd.DataFrame(rows)
    return out
