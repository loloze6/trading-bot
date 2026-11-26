def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["ret"] = b["close"] / b["close"].shift(1) - 1
            rng = (b["high"] - b["low"])
            b["cl"] = (b["close"] - b["low"]) / rng.replace(0, np.nan)
            b["rm"] = rng / rng.rolling(20).mean()
            b["vol20"] = b["ret"].rolling(20).std()
            b["zret"] = b["ret"] / b["vol20"].shift(1)
            b["tr60"] = b["close"] / b["close"].shift(60) - 1
            b["tr20"] = b["close"] / b["close"].shift(20) - 1
            b["vol30"] = b["ret"].rolling(30).std()
            b["volrank"] = b["vol30"].expanding(30).rank(pct=True)
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["nxt"]
            b["wd"] = b["ts"].dt.dayofweek
            b["year"] = b["ts"].dt.year
            b["coin"] = coin; b["win"] = w
            b["active"] = (b["regime"] == "mean_reversion")
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    d = d[d["nxt"].notna()]
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["usual"] = d["coin"].map(d.groupby("coin")["nxt"].std())
    d["exs"] = d["ex"] / d["usual"]
    def summ(g, col="exs"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    d["trend"] = pd.cut(d["tr60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
    d["agit"] = np.where(d["volrank"] > 0.5, "agit", "calm")
    d["clq"] = pd.cut(d["cl"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    d["rmq"] = pd.qcut(d["rm"], 4, labels=["rm1", "rm2", "rm3", "rm4"])
    out["all: exs by close location"] = d.groupby("clq").apply(summ)
    out["by trend x close location (upper half & rm>=1)"] = d[(d.cl > .5) & (d.rm >= 1)].groupby("trend").apply(summ)
    out["by trend x close loc lower half & rm>=1"] = d[(d.cl <= .5) & (d.rm >= 1)].groupby("trend").apply(summ)
    out["falling: exs by clq"] = d[d.trend == "falling"].groupby("clq").apply(summ)
    out["falling: exs by rm quartile"] = d[d.trend == "falling"].groupby("rmq").apply(summ)
    d["zq"] = pd.qcut(d["zret"], 5, labels=["z1", "z2", "z3", "z4", "z5"])
    out["all: exs by z return quintile"] = d.groupby("zq").apply(summ)
    out["falling: exs by z quintile"] = d[d.trend == "falling"].groupby("zq").apply(summ)
    out["rising: exs by z quintile"] = d[d.trend == "rising"].groupby("zq").apply(summ)
    out["all: exs by weekday"] = d.groupby("wd").apply(summ)
    out["active: exs (short side = -exs) by weekday"] = d[d.active].groupby("wd").apply(summ)
    out["active: by year"] = d[d.active].groupby("year").apply(summ)
    out["active: by coin"] = d[d.active].groupby("coin").apply(summ)
    out["active: by z quintile"] = d[d.active].groupby("zq").apply(summ)
    out["active: by clq"] = d[d.active].groupby("clq").apply(summ)
    out["vol rank half x trend: exs"] = d.groupby(["trend", "agit"]).apply(summ)
    # book's largest gains / losses
    a = d[d.pos.abs() > 0]
    out["pos bars gain quantiles"] = a["gain"].describe()
    q = a["gain"].quantile([0.1, 0.9])
    big = a[(a.gain <= q.iloc[0]) | (a.gain >= q.iloc[1])].copy()
    big["side"] = np.where(big.gain > 0, "top", "bottom")
    out["extreme pos bars: features"] = big.groupby("side")[["zret", "cl", "rm", "tr20", "tr60"]].mean()
    return out
