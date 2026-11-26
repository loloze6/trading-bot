def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            if len(b) < 40: continue
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"])})
            d["coin"] = coin; d["win"] = w
            d["ret"] = c / c.shift(1) - 1
            d["f1"] = c.shift(-1) / c - 1
            d["f2"] = c.shift(-2) / c.shift(-1) - 1
            d["f3"] = c.shift(-3) / c - 1
            rng = (h - l) / c
            d["rm"] = (h - l) / (h - l).rolling(30, min_periods=10).mean()
            sd = d["ret"].rolling(30, min_periods=10).std()
            d["z"] = d["ret"] / sd
            d["cl"] = (c - l) / (h - l).replace(0, np.nan)
            d["ret5"] = c / c.shift(5) - 1
            d["ag"] = (b["regime"] != "chop").astype(int)
            d["alloc"] = b["postRebalance_current_allocation"]
            d["wd"] = d["ts"].dt.weekday
            d["yr"] = d["ts"].dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(drift)
    D["x2"] = D["f2"] - D["coin"].map(drift)
    def tcl(s, ts):
        m = s.mean(); dev = (s - m).groupby(ts).sum()
        n = len(s); se = np.sqrt((dev**2).sum()) / n
        return m / se if se > 0 else np.nan
    def summ(g):
        g = g.dropna(subset=["x1"])
        return pd.Series({"n": len(g), "x1%": g["x1"].mean()*100, "t": tcl(g["x1"], g["ts"]),
                          "x2%": g["x2"].mean()*100, "t2": tcl(g["x2"].dropna(), g.dropna(subset=["x2"])["ts"])})
    out = {}
    dn = D[(D["ret"] < 0)].dropna(subset=["z", "rm"]).copy()
    dn["zq"] = dn.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 3, labels=["bigfall", "mid", "small"]))
    dn["rq"] = dn.groupby("coin")["rm"].transform(lambda s: pd.qcut(s, 3, labels=["narrow", "mid", "wide"]))
    out["down: ag x fallsize x range"] = dn.groupby(["ag", "zq", "rq"]).apply(summ).round(3)
    up = D[D["ret"] > 0].dropna(subset=["z", "rm"]).copy()
    up["zq"] = up.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 3, labels=["small", "mid", "bigrise"]))
    up["rq"] = up.groupby("coin")["rm"].transform(lambda s: pd.qcut(s, 3, labels=["narrow", "mid", "wide"]))
    out["up: ag x risesize x range"] = up.groupby(["ag", "zq", "rq"]).apply(summ).round(3)
    al = D.dropna(subset=["cl", "rm"]).copy()
    al["clq"] = al.groupby("coin")["cl"].transform(lambda s: pd.qcut(s, 4, labels=["low", "q2", "q3", "high"]))
    al["rq"] = al.groupby("coin")["rm"].transform(lambda s: pd.qcut(s, 3, labels=["narrow", "mid", "wide"]))
    out["all: ag x closeloc x range"] = al.groupby(["ag", "clq", "rq"]).apply(summ).round(3)
    out["weekday ag-down"] = dn[dn["ag"] == 1].groupby("wd").apply(summ).round(3)
    out["weekday all"] = D.groupby("wd").apply(summ).round(3)
    out["year ag-down wide"] = dn[(dn["ag"] == 1) & (dn["rq"] == "wide")].groupby("yr").apply(summ).round(3)
    out["coin ag-down wide"] = dn[(dn["ag"] == 1) & (dn["rq"] == "wide")].groupby("coin").apply(summ).round(3)
    r5 = D.dropna(subset=["ret5", "x1"]).copy()
    r5["q"] = r5.groupby("coin")["ret5"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["5d ret quintile x ag"] = r5.groupby(["ag", "q"]).apply(summ).round(3)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd)
    br = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    q = br.quantile([0.01, 0.05, 0.5, 0.95, 0.99])
    out["book daily quantiles %"] = (q*100).round(3)
    srt = br.sort_values()
    tot = br.sum()
    out["share of book sum from top 5% days"] = float(srt[srt >= srt.quantile(0.95)].sum() / tot)
    out["share of book sum from bottom 5% days"] = float(srt[srt <= srt.quantile(0.05)].sum() / tot)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades by duration"] = T.groupby(pd.cut(T["dur_d"], [0, 1.5, 2.5, 4.5, 100]))["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return out
