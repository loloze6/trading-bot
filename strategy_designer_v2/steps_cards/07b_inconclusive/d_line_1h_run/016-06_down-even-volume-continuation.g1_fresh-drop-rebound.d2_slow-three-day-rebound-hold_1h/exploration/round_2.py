import numpy as np, pandas as pd
from scipy import stats

def _ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    x, y = x[m], y[m]
    if len(x) < 10 or np.std(x) == 0:
        return np.nan, np.nan, len(x)
    r = stats.linregress(x, y)
    return r.slope, (r.slope / r.stderr if r.stderr > 0 else np.nan), len(x)

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values; reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"]); n = len(df)
            for p in range(0, n - 24, 24):
                d = dict(coin=coin, year=ts.iloc[p].year, reg=reg[p], fc=f[p],
                         r24=c[p+24]/c[p]-1,
                         r12=c[p+12]/c[p]-1 if p+12 < n else np.nan,
                         past24=(c[p]/c[p-24]-1) if p >= 24 else np.nan,
                         past72=(c[p]/c[p-72]-1) if p >= 72 else np.nan)
                rows.append(d)
    g = pd.DataFrame(rows)
    for h in ["r24", "r12"]:
        g["x_"+h] = g[h] - g.groupby("coin")[h].transform("mean")
    mr = g[g.reg == "mean_reversion"].copy()
    out = {}
    pc = []
    for coin, d in mr.groupby("coin"):
        s, t, n = _ols(d["fc"], d["x_r24"]); pc.append(dict(coin=coin, n=n, slope=s, t=t))
    out["g24_by_coin"] = pd.DataFrame(pc)
    py = []
    for y, d in mr.groupby("year"):
        s, t, n = _ols(d["fc"], d["x_r24"]); py.append(dict(year=y, n=n, slope=s, t=t))
    out["g24_by_year"] = pd.DataFrame(py)
    mr["fb"] = pd.cut(mr["fc"], [-0.01, 0.01, 5, 10, 15, 19.99, 20.01],
                      labels=["0", "0-5", "5-10", "10-15", "15-20", "20cap"])
    out["g24_buckets"] = mr.groupby("fb", observed=True).agg(n=("fc", "size"), x_r24=("x_r24", "mean"),
                                                             sd=("x_r24", "std"))
    # raw past 24h fall (negated), within 3-day fall, and outside
    g["fall24"] = (-g["past24"]).clip(lower=0)
    a = g[(g.past72 < 0)]
    s, t, n = _ols(a["fall24"], a["x_r24"])
    b = g[(g.past72 >= 0)]
    s2, t2, n2 = _ols(b["fall24"], b["x_r24"])
    s3, t3, n3 = _ols(g["fall24"], g["x_r24"])
    out["raw_fall24_slope"] = pd.DataFrame([dict(sub="3d fall", slope=s, t=t, n=n),
                                            dict(sub="3d rise", slope=s2, t=t2, n=n2),
                                            dict(sub="all", slope=s3, t=t3, n=n3)])
    a2 = a.copy()
    a2["q"] = pd.qcut(a2["past24"], 5, labels=False, duplicates="drop")
    out["3dfall_past24_quintile"] = a2.groupby("q").agg(n=("x_r24", "size"), past24=("past24", "mean"),
                                                        x_r24=("x_r24", "mean"), x_r12=("x_r12", "mean"))
    return out
