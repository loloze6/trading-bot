def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(30).std().values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(n):
                rows.append(dict(coin=coin, w=w, i=i, f=b["forecast"].iloc[i],
                    pos=b["postRebalance_current_allocation"].iloc[i],
                    fwd1=c[i+1]/c[i]-1 if i+1<n else np.nan,
                    fwd14=c[i+14]/c[i]-1 if i+14<n else np.nan,
                    p14=c[i]/c[i-14]-1 if i>=14 else np.nan,
                    p30=c[i]/c[i-30]-1 if i>=30 else np.nan,
                    p60=c[i]/c[i-60]-1 if i>=60 else np.nan,
                    vol=vol[i], wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year))
    d = pd.DataFrame(rows)
    d["fwd14x"] = d["fwd14"] - d.groupby("coin")["fwd14"].transform("mean")
    d["fwd1x"] = d["fwd1"] - d.groupby("coin")["fwd1"].transform("mean")
    s = d[d.i % 14 == 0].copy()
    def slope(x, col, y="fwd14x"):
        x = x.dropna(subset=[col, y])
        if len(x) < 10: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        r = stats.linregress(x[col], x[y])
        return pd.Series({"n": len(x), "slope": r.slope, "t": r.slope / r.stderr})
    res = {}
    res["f all"] = slope(s, "f")
    res["f>0 only"] = slope(s[s.f > 0], "f")
    res["f<0 only"] = slope(s[s.f < 0], "f")
    for col in ("p14", "p30", "p60"):
        res[col + " all"] = slope(s, col)
        res[col + " up only"] = slope(s[s[col] > 0], col)
        res[col + " down only"] = slope(s[s[col] < 0], col)
    out["slopes on fwd14x (non-overlap 14)"] = pd.DataFrame(res).T
    pc = {}
    for coin in s.coin.unique():
        for col in ("f", "p30", "p60"):
            pc[f"{coin} {col}"] = slope(s[s.coin == coin], col)
    out["slopes per coin"] = pd.DataFrame(pc).T
    # vol regime: slope of fwd14x on p30 in high vs low vol (per-coin median)
    s["hv"] = s["vol"] > s.groupby("coin")["vol"].transform("median")
    out["p30 slope by vol half"] = pd.DataFrame({str(k): slope(g, "p30") for k, g in s.groupby("hv")}).T
    out["f slope by vol half"] = pd.DataFrame({str(k): slope(g, "f") for k, g in s.groupby("hv")}).T
    # wednesday by coin and year
    w = d.dropna(subset=["fwd1x"]).copy()
    w["wed"] = w.wd == 2
    g = w.groupby(["coin", "wed"])["fwd1x"].agg(["count", "mean"])
    out["wed vs other by coin"] = g
    g2 = w[w.wed].groupby("yr")["fwd1x"].agg(["count", "mean", "std"])
    g2["t"] = g2["mean"] / (g2["std"] / np.sqrt(g2["count"]))
    out["wed by year"] = g2
    # book: market rise vs timing
    mu = d.groupby("coin")["fwd1"].mean()
    d["mkt"] = d["pos"] * d["coin"].map(mu)
    d["gain"] = d["pos"] * d["fwd1"]
    x = d.dropna(subset=["gain"])
    out["book gain split per bar"] = pd.Series({"mean gain": x.gain.mean(), "market part": x.mkt.mean(), "timing part": x.gain.mean() - x.mkt.mean(), "mean pos": x.pos.mean()})
    # gain by side and vol half
    x = x.copy(); x["hv"] = x["vol"] > x.groupby("coin")["vol"].transform("median")
    x["side"] = np.sign(x.pos)
    gg = x.groupby(["hv", "side"])["gain"].agg(["count", "mean", "std"])
    gg["t"] = gg["mean"] / (gg["std"] / np.sqrt(gg["count"]))
    out["bar gain by vol half x side"] = gg
    # trades skew
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trade pnl quantiles by side"] = tr.groupby("side")["net_profit_loss_percent"].quantile([0.1, 0.5, 0.9]).unstack()
    out["trade share winners"] = tr.groupby("side")["net_profit_loss_percent"].apply(lambda v: (v > 0).mean())
    return out
