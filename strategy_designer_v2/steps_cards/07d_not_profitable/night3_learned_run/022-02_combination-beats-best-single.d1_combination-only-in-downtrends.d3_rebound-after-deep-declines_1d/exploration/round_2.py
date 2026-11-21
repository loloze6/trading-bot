import numpy as np, pandas as pd

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            hi = c.rolling(90, min_periods=20).max()
            depth = c / hi - 1
            r20 = c / c.shift(20) - 1
            fwd = c.shift(-H) / c - 1
            fwd10 = c.shift(-10) / c - 1
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, regime=b.loc[i, "regime"], depth=depth[i], r20=r20[i],
                                 alloc=b.loc[i, "postRebalance_current_allocation"], fwd=fwd[i],
                                 fwd10=fwd10[i] if i + 10 < n else np.nan,
                                 year=pd.to_datetime(b.loc[i, "timestamp"]).year))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    sd = g.groupby("coin")["fwd"].std()
    g["str"] = g["ex"] / g["coin"].map(sd)
    out = {}
    def tt(x):
        x = x.dropna(); return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    mr = g[g.regime == "mean_reversion"].copy()
    bins = [-1, -0.6, -0.46, -0.35, -0.2, -0.1, 0.01]
    mr["db"] = pd.cut(mr["depth"], bins)
    out["MR by depth bin"] = mr.groupby("db").agg(n=("ex", "size"), ex=("ex", "mean"), fwd=("fwd", "mean"),
                                                 strength=("str", "mean"), alloc=("alloc", "mean"),
                                                 t=("ex", tt), fwd10=("fwd10", "mean"))
    deep = mr[mr.depth < -0.46]
    out["MR deep: by year"] = deep.groupby("year").agg(n=("ex", "size"), ex=("ex", "mean"))
    out["MR deep: by coin"] = deep.groupby("coin").agg(n=("ex", "size"), ex=("ex", "mean"))
    out["MR deep: windows with positive mean"] = float((deep.groupby(["coin","win"])["ex"].mean() > 0).mean())
    deep = deep.copy(); deep["r20q"] = pd.qcut(deep["r20"], 3, labels=False)
    out["MR deep by 20d return tercile"] = deep.groupby("r20q").agg(n=("ex", "size"), r20=("r20", "mean"),
                                                                  ex=("ex", "mean"), t=("ex", tt))
    nm = g[g.regime != "mean_reversion"].copy()
    nm["db"] = pd.cut(nm["depth"], bins)
    out["notMR by depth bin"] = nm.groupby("db").agg(n=("ex", "size"), ex=("ex", "mean"), fwd=("fwd", "mean"),
                                                    strength=("str", "mean"), t=("ex", tt))
    # book daily: gain when long vs flat, and depth contribution
    dd = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy(); c = b["close"].astype(float)
            b["dep"] = c / c.rolling(90, min_periods=20).max() - 1
            b["g"] = b["postRebalance_current_allocation"] * (c.shift(-1) / c - 1)
            b["coin"] = coin; dd.append(b[["coin", "dep", "g", "postRebalance_current_allocation", "regime"]])
    B = pd.concat(dd).dropna(subset=["g"])
    B["db"] = pd.cut(B["dep"], bins)
    out["book bar gain by depth bin (sum share)"] = B.groupby("db").agg(n=("g", "size"), meang=("g", "mean"),
                                                                       sumg=("g", "sum"))
    return out
