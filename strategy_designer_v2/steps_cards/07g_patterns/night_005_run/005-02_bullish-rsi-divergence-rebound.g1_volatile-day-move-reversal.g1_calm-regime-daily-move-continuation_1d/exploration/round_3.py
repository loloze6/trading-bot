def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            r1 = b["close"].pct_change()
            absm = r1.abs().rolling(60, min_periods=30).mean()
            vol20 = r1.rolling(20, min_periods=15).std()
            vrank = vol20.rolling(100, min_periods=50).rank(pct=True)
            for i in range(0, n - 5, 5):
                rows.append(dict(coin=c, w=w, y=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 f=b["forecast"].iloc[i], pos=b["postRebalance_current_allocation"].iloc[i],
                                 sm=r1.iloc[i] / absm.iloc[i] if absm.iloc[i] else np.nan, vr=vrank.iloc[i],
                                 fwd=cl[i + 5] / cl[i] - 1,
                                 pnl=(np.prod(1 + np.diff(cl[i:i+6]) / cl[i:i+5]) - 1)))
    g = pd.DataFrame(rows).dropna(subset=["sm"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    up = g[g.sm > 0].copy(); dn = g[g.sm < 0].copy()
    up["q"] = pd.qcut(up.sm.rank(method="first"), 4, labels=False)
    dn["q"] = pd.qcut(dn.sm.rank(method="first"), 4, labels=False)
    out["up days: excess by scaled-move quartile (3=largest)"] = up.groupby("q")["ex"].apply(tt).unstack()
    out["down days: excess by scaled-move quartile (0=largest drop)"] = dn.groupby("q")["ex"].apply(tt).unstack()
    res = {}
    for nm, s in [("up", up), ("down", dn)]:
        lr = stats.linregress(s.sm, s.ex); res[nm] = dict(n=len(s), slope=lr.slope, t=lr.slope / lr.stderr)
        s2 = s.dropna(subset=["vr"]); s2 = s2[s2.vr < 0.5]
        lr = stats.linregress(s2.sm, s2.ex); res[nm + "_vr<0.5"] = dict(n=len(s2), slope=lr.slope, t=lr.slope / lr.stderr)
    out["slope excess on scaled move, up vs down"] = pd.DataFrame(res).T
    out["largest-quartile up days excess by year"] = up[up.q == 3].groupby("y")["ex"].apply(tt).unstack()
    out["largest-quartile up days excess by coin"] = up[up.q == 3].groupby("coin")["ex"].apply(tt).unstack()
    g["fs"] = np.sign(g.f)
    g["sig"] = g.fs * g.ex
    g["fq"] = g.groupby("coin")["f"].transform(lambda x: x.abs().rank(pct=True))
    top = g[g.fq > 0.8]
    out["top |f| quintile signed excess by forecast side"] = top.groupby("fs")["sig"].apply(tt).unstack()
    return out
