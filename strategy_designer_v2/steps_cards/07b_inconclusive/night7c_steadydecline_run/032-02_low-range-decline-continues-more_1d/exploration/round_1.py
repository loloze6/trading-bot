import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            rng = ((b["high"] - b["low"]) / b["close"]).values
            r28 = pd.Series(c).pct_change(28).values
            rng28 = pd.Series(rng).rolling(28).mean().values
            rng365 = pd.Series(rng).rolling(365, min_periods=91).mean().values
            calm = b.get("debug_info.components.calm.last_history_value")
            fc = b["forecast"].values
            for h in (5, 10, 20):
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, ret=c[t+h]/c[t]-1,
                                     regime=b["regime"].iat[t], r28=r28[t],
                                     calm=(calm.iat[t] if calm is not None else np.nan),
                                     ratio=(rng365[t]/rng28[t] if rng28[t] > 0 else np.nan),
                                     fc=fc[t]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["ret"].transform("mean")
    df["adj"] = df["ret"] - df["drift"]
    tr = df[(df.regime == "trending") & df.r28.notna()].copy()
    out = {}
    res = []
    for h in (5, 10, 20):
        s = tr[tr.h == h].dropna(subset=["ratio"])
        for var in ["ratio", "r28"]:
            sl = stats.linregress(s[var], s["adj"])
            res.append(dict(h=h, var=var, n=len(s), slope=sl.slope, t=sl.slope/sl.stderr))
        s2 = s.copy()
        s2["q"] = pd.qcut(s2["ratio"], 5, labels=False)
        out[f"by calm quintile h{h}"] = s2.groupby("q")["adj"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
        s2["qr"] = pd.qcut(s2["r28"], 5, labels=False)
        out[f"by r28 quintile h{h}"] = s2.groupby("qr")["adj"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["slopes"] = pd.DataFrame(res)
    s5 = tr[tr.h == 5].dropna(subset=["ratio"])
    g = []
    for k, s in s5.groupby("coin"):
        sl = stats.linregress(s["ratio"], s["adj"]); g.append(dict(coin=k, n=len(s), mean=s.adj.mean(), slope=sl.slope, t=sl.slope/sl.stderr))
    out["by coin h5"] = pd.DataFrame(g)
    g = []
    for k, s in s5.groupby("win"):
        if len(s) > 10:
            sl = stats.linregress(s["ratio"], s["adj"]); g.append(dict(win=k, n=len(s), mean=s.adj.mean(), slope=sl.slope, t=sl.slope/sl.stderr))
    out["by window h5"] = pd.DataFrame(g)
    # interaction: deep falls only
    deep = s5[s5.r28 < s5.r28.median()]
    sl = stats.linregress(deep["ratio"], deep["adj"])
    out["deep half: ratio slope t"] = float(sl.slope/sl.stderr)
    s5 = s5.copy(); s5["calmdeep"] = -s5["r28"] * s5["ratio"]
    sl = stats.linregress(s5["calmdeep"], s5["adj"])
    out["h5 slope on -r28*ratio t"] = float(sl.slope/sl.stderr)
    out["corr ratio vs calm debug"] = float(s5[["ratio", "calm"]].corr().iloc[0, 1])
    return out
