def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r1 = c / c.shift(1) - 1
            vol = r1.rolling(20, min_periods=20).std()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]), "pos_i": np.arange(len(b))})
            d["z"] = r1 / vol
            d["vol"] = vol
            d["volrank"] = vol / vol.rolling(60, min_periods=20).mean()
            rng = (h - l) / c
            d["rngz"] = rng / vol
            d["clv"] = ((c - l) / (h - l)).where(h > l)
            d["body"] = ((c - o).abs() / (h - l)).where(h > l)
            d["run5"] = (c / c.shift(5) - 1) / (vol * np.sqrt(5))
            d["run20"] = (c / c.shift(20) - 1) / (vol * np.sqrt(20))
            for k in (1, 3, 5):
                d[f"f{k}"] = c.shift(-k) / c - 1
            d["fc"] = b["forecast"].values
            d["alloc"] = b["postRebalance_current_allocation"].values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    # coin drift per horizon, non-overlapping grid
    for k in (1, 3, 5):
        g = D[D["pos_i"] % k == 0]
        m = g.groupby("coin")[f"f{k}"].mean()
        D[f"e{k}"] = D[f"f{k}"] - D["coin"].map(m)
        D[f"g{k}"] = (D["pos_i"] % k == 0)

    def dt(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 20: return (len(s), np.nan, np.nan, np.nan)
        pd_ = s.groupby("day")[col].sum()
        cnt = s.groupby("day")[col].size()
        mean = s[col].mean()
        # day-clustered t: sum per day / n
        n = len(s); nd = len(pd_)
        dev = (s[col] - mean).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n * np.sqrt(nd / (nd - 1))
        return (n, nd, mean * 100, mean / se)

    def table(groupcol, k, sub=None):
        S = D if sub is None else sub
        S = S[S[f"g{k}"]]
        out = {}
        for gv, s in S.groupby(groupcol, observed=True):
            n, nd, m, t = dt(s, f"e{k}")
            out[str(gv)] = {"n": n, "days": nd, "mean%": m, "t": t}
        return pd.DataFrame(out).T

    D["zb"] = pd.cut(D["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    res = {}
    res["z bucket fwd1"] = table("zb", 1)
    res["z bucket fwd3"] = table("zb", 3)
    res["z bucket fwd5"] = table("zb", 5)
    # brief's original: wide flat day after run
    D["rb"] = pd.qcut(D["rngz"], 4, labels=["r1", "r2", "r3", "r4"])
    D["bb"] = pd.cut(D["body"], [-0.01, 0.25, 0.6, 1.01], labels=["flat", "mid", "full"])
    D["runb"] = pd.cut(D["run5"], [-99, -1, 1, 99], labels=["down", "none", "up"])
    D["sgnrun"] = np.sign(D["run5"])
    for k in (1, 3):
        D[f"ag{k}"] = -D["sgnrun"] * D[f"e{k}"]  # move against run
    fl = D[(D["bb"] == "flat") & (D["runb"] != "none")]
    out = {}
    for k in (1, 3):
        S = fl[fl[f"g{k}"]]
        for gv, s in S.groupby("rb", observed=True):
            n, nd, m, t = dt(s, f"ag{k}")
            out[f"h{k}_{gv}"] = {"n": n, "days": nd, "against%": m, "t": t}
    res["flat day after run, against-run move by range quartile"] = pd.DataFrame(out).T
    # falls by vol regime
    dn = D[D["z"] < -1].copy()
    dn["vb"] = pd.qcut(dn["volrank"], 3, labels=["lowvol", "midvol", "highvol"])
    res["fall z<-1 by vol regime fwd1"] = table("vb", 1, dn)
    dn["r20b"] = pd.cut(dn["run20"], [-99, -1, 1, 99], labels=["down20", "flat20", "up20"])
    res["fall z<-1 by 20d trend fwd1"] = table("r20b", 1, dn)
    res["fall z<-1 by 20d trend fwd5"] = table("r20b", 5, dn)
    dn["clvb"] = pd.cut(dn["clv"], [-0.01, 0.33, 0.66, 1.01], labels=["closelow", "closemid", "closehigh"])
    res["fall z<-1 by close location fwd1"] = table("clvb", 1, dn)
    res["weekday all fwd1"] = table("wd", 1)
    D["clvall"] = pd.cut(D["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    res["close location all fwd1"] = table("clvall", 1)
    # book
    bk = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
            bk.append(x)
    B = pd.concat(bk).dropna()
    bd = B.groupby(["win", "day"])["book_return"].mean().reset_index()
    bd["wd"] = pd.to_datetime(bd["day"]).dt.dayofweek
    res["book by weekday"] = bd.groupby("wd")["book_return"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"] / x["std"] * np.sqrt(x["count"]))
    res["book by year"] = bd.groupby(pd.to_datetime(bd["day"]).dt.year)["book_return"].agg(["count", "mean", "std"])
    return res
