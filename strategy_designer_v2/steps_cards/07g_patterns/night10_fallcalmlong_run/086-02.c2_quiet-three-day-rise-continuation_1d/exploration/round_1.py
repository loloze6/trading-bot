import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        grid_all = []
        frames = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; v = b["volume"]
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["r1"] = c.pct_change()
            b["r3"] = c / c.shift(3) - 1
            b["r10"] = c / c.shift(10) - 1
            b["r20"] = c / c.shift(20) - 1
            b["vr1"] = np.log(v / v.shift(1).rolling(20).mean())
            b["vr3"] = np.log(v.rolling(3).mean() / v.shift(3).rolling(20).mean())
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["clv"] = (c - b["low"]) / rng
            b["rngrel"] = np.log(rng / rng.shift(1).rolling(20).mean())
            b["dd20"] = c / c.rolling(20).max() - 1
            b["up20"] = c / c.rolling(20).min() - 1
            b["vol10"] = b["r1"].rolling(10).std() / b["r1"].rolling(40).std()
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["grid"] = (np.arange(len(b)) % H) == 0
            b["fc"] = b["regime"].isin(["trending", "unknown"])
            b["coin"] = coin; b["win"] = w
            frames.append(b)
        cb = pd.concat(frames)
        g = cb[cb["grid"] & cb["fwd"].notna()]
        mu = g["fwd"].mean()
        cb["ex"] = cb["fwd"] - mu
        rows.append(cb)
    D = pd.concat(rows)
    G = D[D["grid"] & D["fc"] & D["ex"].notna()]
    out = {}
    out["counts"] = pd.Series({"falling calm grid cases": len(G),
                               "all grid cases": int((D["grid"] & D["ex"].notna()).sum()),
                               "mean ex fc": G["ex"].mean(),
                               "t ex fc": stats.ttest_1samp(G["ex"], 0).statistic,
                               "share fc bars": D["fc"].mean()})
    feats = ["r1", "r3", "r10", "r20", "vr1", "vr3", "clv", "rngrel", "dd20", "up20", "vol10"]
    res = []
    for f in feats:
        s = G[[f, "ex"]].dropna()
        lr = stats.linregress(s[f], s["ex"])
        rho = stats.spearmanr(s[f], s["ex"])[0]
        q = pd.qcut(s[f], 5, labels=False, duplicates="drop")
        qm = s.groupby(q)["ex"].mean()
        res.append({"feat": f, "n": len(s), "slope_t": lr.slope / lr.stderr, "spearman": rho,
                    **{f"q{int(k)}": qm[k] for k in qm.index}})
    out["features_fc"] = pd.DataFrame(res).set_index("feat").round(4)
    # up days only (brief's own situation): volume ratio
    U = G[G["r1"] > 0]
    res = []
    for f in ["vr1", "vr3", "r1", "clv", "dd20", "rngrel"]:
        s = U[[f, "ex"]].dropna()
        lr = stats.linregress(s[f], s["ex"])
        q = pd.qcut(s[f], 4, labels=False, duplicates="drop")
        qm = s.groupby(q)["ex"].mean()
        res.append({"feat": f, "n": len(s), "slope_t": lr.slope / lr.stderr,
                    **{f"q{int(k)}": qm[k] for k in qm.index}})
    out["updays_fc"] = pd.DataFrame(res).set_index("feat").round(4)
    out["weekday_fc"] = G.groupby("wd")["ex"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))]).round(4)
    out["coin_fc"] = G.groupby("coin")["ex"].agg(["count", "mean"]).round(4)
    W = G.copy(); W["yr"] = pd.to_datetime(W["timestamp"]).dt.year
    out["year_fc"] = W.groupby("yr")["ex"].agg(["count", "mean"]).round(4)
    # book: daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    br = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book"] = pd.Series({"days": len(br), "mean": br.mean(), "t": br.mean()/br.std()*np.sqrt(len(br)),
                             "top10 sum": br.nlargest(10).sum(), "bottom10 sum": br.nsmallest(10).sum()})
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    out["trades"] = pd.Series({"n": len(T), "mean net %": T["net_profit_loss_percent"].mean(),
                               "win share": (T["net_profit_loss_percent"] > 0).mean(),
                               "mean dur days": T["duration_minutes"].mean()/1440})
    return out
