import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "f3": c.shift(-3) / c - 1, "z1": r1 / sd30, "sd30": sd30,
                               "sdr": sd30 / r1.rolling(90, min_periods=60).std(),
                               "rising": (b["regime"] == "unknown").values,
                               "fc": b["forecast"].astype(float),
                               "day": ts.dt.floor("D"), "yr": ts.dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 3 == 0].dropna(subset=["f3"]).copy()
    drift = g.groupby("coin")["f3"].mean()
    usual = g.groupby("coin")["f3"].std()
    g["ex3"] = g["f3"] - g["coin"].map(drift)
    g["str"] = g["ex3"] / g["coin"].map(usual)
    g["volr"] = g.groupby("coin")["sd30"].rank(pct=True)
    g["volt"] = pd.cut(g["volr"], [0, 1/3, 2/3, 1], labels=["lo", "mid", "hi"], include_lowest=True)

    def dmean(x, col="ex3"):
        s = x.groupby("day")[col].apply(lambda v: (v - x[col].mean()).sum())
        se = np.sqrt((s ** 2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": x["day"].nunique(), "mean": x[col].mean(),
                          "t_day": x[col].mean() / se, "strength": x["str"].mean()})
    out["ex3 by rising x vol tercile, day-clustered"] = g.groupby(["rising", "volt"], observed=True).apply(dmean)
    out["rising lo-vol by year"] = g[g.rising & (g.volt == "lo")].groupby("yr")["ex3"].agg(["count", "mean"])
    out["rising lo-vol by coin"] = g[g.rising & (g.volt == "lo")].groupby("coin")["ex3"].agg(["count", "mean"])
    # vol vs its own 90d (relative calm)
    r = g[g.rising].dropna(subset=["sdr"]).copy()
    r["sdrq"] = pd.qcut(r["sdr"], 4)
    out["rising: ex3 by 30d/90d vol ratio quartile"] = r.groupby("sdrq", observed=True).apply(dmean)
    # tested forecast within vol tercile, rising
    rr = g[g.rising].copy()
    rr["dn"] = rr["fc"] > 0
    out["rising: forecast>0 vs 0 by vol tercile"] = rr.groupby(["volt", "dn"], observed=True)["ex3"].agg(["count", "mean"]).unstack()
    # graded slope of ex3 on volr within rising, dayclustered
    x = rr.dropna(subset=["volr"])
    X = x["volr"] - x["volr"].mean()
    b = (X * x["ex3"]).sum() / (X ** 2).sum()
    e = x["ex3"] - x["ex3"].mean() - b * X
    sc = (X * e).groupby(x["day"]).sum()
    out["rising slope on vol rank"] = pd.Series({"slope": b, "t": b / (np.sqrt((sc ** 2).sum()) / (X ** 2).sum())})
    return out
