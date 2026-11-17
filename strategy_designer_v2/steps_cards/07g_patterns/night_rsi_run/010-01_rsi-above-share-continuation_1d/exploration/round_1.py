def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            f = b["forecast"].values
            pos = b["postRebalance_current_allocation"].values
            r1 = pd.Series(c).pct_change().values
            for h in (7, 14):
                pass
            for i in range(n):
                rows.append(dict(coin=coin, w=w, i=i, f=f[i], pos=pos[i],
                    fwd1=c[i+1]/c[i]-1 if i+1<n else np.nan,
                    fwd7=c[i+7]/c[i]-1 if i+7<n else np.nan,
                    fwd14=c[i+14]/c[i]-1 if i+14<n else np.nan,
                    past7=c[i]/c[i-7]-1 if i>=7 else np.nan,
                    past30=c[i]/c[i-30]-1 if i>=30 else np.nan,
                    vol30=pd.Series(r1).rolling(30).std().values[i],
                    wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                    rng=(b["high"].iloc[i]-b["low"].iloc[i])/c[i]))
    d = pd.DataFrame(rows)
    # demean per coin
    for col in ("fwd1","fwd7","fwd14"):
        d[col+"x"] = d[col] - d.groupby("coin")[col].transform("mean")
    s14 = d[d.i % 14 == 0].dropna(subset=["fwd14x","f"])
    s14["fq"] = pd.qcut(s14["f"], 5, labels=False, duplicates="drop")
    out["fwd14 by forecast quintile"] = s14.groupby("fq")["fwd14x"].agg(["count","mean","std"])
    s7 = d[d.i % 7 == 0].copy()
    def tab(col, q=5):
        x = s7.dropna(subset=[col,"fwd7x"]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda v: pd.qcut(v, q, labels=False, duplicates="drop"))
        g = x.groupby("q")["fwd7x"].agg(["count","mean","std"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        return g
    out["fwd7 by past7 quintile"] = tab("past7")
    out["fwd7 by past30 quintile"] = tab("past30")
    out["fwd7 by vol30 quintile"] = tab("vol30")
    out["fwd7 by range quintile"] = tab("rng")
    # weekday daily return (all bars, 1-day non-overlapping anyway)
    g = d.dropna(subset=["fwd1x"]).groupby("wd")["fwd1x"].agg(["count","mean","std"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next-day excess by weekday"] = g
    # past30 x forecast sign interaction
    x = s14.dropna(subset=["past30"]).copy()
    x["p30pos"] = x["past30"] > 0
    x["fpos"] = x["f"] > 0
    out["fwd14x by fsign x past30sign"] = x.groupby(["fpos","p30pos"])["fwd14x"].agg(["count","mean"])
    # book: daily, by coin
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"]=coin; t["w"]=w; dd.append(t)
    dd = pd.concat(dd)
    out["book daily by coin"] = dd.groupby("coin")[["book_return","coin_return"]].agg(["mean","std"])
    # long vs short contribution
    d["gain"] = d["pos"]*d["fwd1"]
    d["side"] = np.sign(d["pos"])
    g = d.dropna(subset=["gain"]).groupby(["coin","side"])["gain"].agg(["count","mean","sum"])
    out["bar gain by side"] = g
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"]=coin; tr.append(t)
    tr = pd.concat(tr)
    out["trades by side"] = tr.groupby(["coin","side"])["net_profit_loss_percent"].agg(["count","mean","median"])
    # largest book losses: what preceded
    bb = d.dropna(subset=["gain"]).copy()
    lo = bb.nsmallest(30, "gain"); hi = bb.nlargest(30, "gain")
    out["worst30 bars"] = pd.Series({"mean pos": lo.pos.mean(), "share short": (lo.pos<0).mean(), "mean past7": lo.past7.mean(), "mean vol30": lo.vol30.mean(), "mean f": lo.f.mean()})
    out["best30 bars"] = pd.Series({"mean pos": hi.pos.mean(), "share short": (hi.pos<0).mean(), "mean past7": hi.past7.mean(), "mean vol30": hi.vol30.mean(), "mean f": hi.f.mean()})
    out["all bars"] = pd.Series({"mean pos": bb.pos.mean(), "share short": (bb.pos<0).mean(), "mean past7": bb.past7.mean(), "mean vol30": bb.vol30.mean()})
    return out
