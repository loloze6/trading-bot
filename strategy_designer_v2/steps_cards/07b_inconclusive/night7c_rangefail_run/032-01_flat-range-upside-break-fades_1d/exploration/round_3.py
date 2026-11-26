import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 10, 10):
                g.append(c[i+10]/c[i]-1)
        drift[coin] = np.mean(g)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            s = df["close"]; c = s.values; n = len(c)
            ph = df["high"].shift(1).rolling(60).max().values
            ch = s.diff().abs().rolling(60).sum()
            er = ((s - s.shift(60)).abs() / ch).rolling(5).mean().values
            rng = (df["high"].shift(1).rolling(60).max() / df["low"].shift(1).rolling(60).min() - 1).values
            last = -999
            for i in range(1, n):
                if np.isnan(ph[i]) or np.isnan(er[i]) or np.isnan(ph[i-1]): continue
                if c[i] > ph[i] and c[i-1] <= ph[i-1]:
                    if i - last < 20: continue
                    last = i
                    r = {}
                    for h in (10, 20):
                        r[f"r{h}"] = (c[i+h]/c[i]-1 - drift[coin]*h/10) if i+h < n else np.nan
                    rows.append(dict(coin=coin, w=w, ts=str(df["timestamp"].iloc[i])[:10], er=er[i],
                                     os=c[i]/ph[i]-1, rng=rng[i], **r))
    ab = pd.DataFrame(rows)
    def tday(x, col):
        x = x.dropna(subset=[col])
        d = x.groupby("ts")[col].sum()
        return pd.Series(dict(n=len(x), days=len(d), mean=x[col].mean(), med=x[col].median(),
                              pos=(x[col] > 0).mean(),
                              t=d.mean()/(d.std(ddof=1)/np.sqrt(len(d))) if len(d) > 2 else np.nan))
    out = {}
    lo = ab[ab["er"] <= 0.3]
    out["ER<=0.3, 20d-spaced breakouts"] = pd.DataFrame({h: tday(lo, h) for h in ["r10","r20"]}).T
    out["ER<=0.3 excluding XRP"] = pd.DataFrame({h: tday(lo[lo.coin != "XRPUSD"], h) for h in ["r10","r20"]}).T
    ab["erh"] = pd.qcut(ab["er"].rank(method="first"), 3, labels=["flat","mid","trendy"])
    out["all breakouts by ER tercile r20"] = ab.groupby("erh").apply(lambda g: pd.concat([tday(g, "r20"), pd.Series({"er": g["er"].mean()})]))
    x = ab.dropna(subset=["r20"])
    res = {}
    for v in ["er", "os", "rng"]:
        sl = stats.linregress(x[v], x["r20"]); res[v] = (sl.slope, sl.slope/sl.stderr, len(x))
    out["slopes of r20 on er, overshoot, prior range width (all)"] = pd.DataFrame(res, index=["slope","t","n"]).T
    xl = lo.dropna(subset=["r20"])
    res = {}
    for v in ["er", "os", "rng"]:
        sl = stats.linregress(xl[v], xl["r20"]); res[v] = (sl.slope, sl.slope/sl.stderr, len(xl))
    out["slopes of r20 in ER<=0.3"] = pd.DataFrame(res, index=["slope","t","n"]).T
    out["ER<=0.3 r20 by coin"] = lo.groupby("coin").apply(lambda g: tday(g, "r20"))
    out["ER<=0.3 r20 by window"] = lo.groupby("w").apply(lambda g: tday(g, "r20"))
    return out
