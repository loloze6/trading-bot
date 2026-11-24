def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        g3 = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = h - l
            mult = rng / rng.rolling(20).mean()
            ret20 = c / c.shift(20) - 1
            ret1 = c / c.shift(1) - 1
            ret5 = c / c.shift(5) - 1
            clv = (c - l) / rng.replace(0, np.nan)
            body = (c - o) / rng.replace(0, np.nan)
            volr = (rng.rolling(20).mean() / c)
            n = len(b)
            for H in (1, 3, 7):
                idx = np.arange(0, n - H, H)
                fwd = c.shift(-H) / c - 1
                d = pd.DataFrame({"coin": coin, "H": H, "ts": b["timestamp"].values[idx],
                                  "fwd": fwd.values[idx], "mult": mult.values[idx], "ret20": ret20.values[idx],
                                  "ret1": ret1.values[idx], "ret5": ret5.values[idx], "clv": clv.values[idx],
                                  "body": body.values[idx], "volr": volr.values[idx], "fc": b["forecast"].values[idx]})
                rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["wd"] = pd.to_datetime(D["ts"]).dt.weekday
    D["drift"] = D.groupby(["coin", "H"])["fwd"].transform("mean")
    D["un"] = D["fwd"] - D["drift"]
    D["z"] = D["un"] / D.groupby(["coin", "H"])["fwd"].transform("std")

    def ct(s):
        s = s.dropna()
        if len(s) < 10: return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan, "days": 0})
        dd = D.loc[s.index, "day"]
        m = s.mean()
        ds = (s - m).groupby(dd).sum()
        se = np.sqrt((ds ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "mean": m, "t": m / se if se > 0 else np.nan, "days": dd.nunique(), "zmean": D.loc[s.index, "z"].mean()})

    out = {}
    D3 = D[(D.H == 3)].dropna(subset=["mult", "ret20"])
    D3 = D3.assign(trend=np.where(D3.ret20 > 0, "up", "down"),
                   mb=pd.cut(D3.mult, [0, 0.7, 1.0, 1.3, 1.6, 2.0, 99]),
                   cl=pd.cut(D3.clv, [-0.01, 0.33, 0.67, 1.01], labels=["lowclose", "mid", "highclose"]))
    out["H3 trend x rangemult"] = D3.groupby(["trend", "mb"], observed=True)["un"].apply(ct).unstack()
    W = D3[D3.mult >= 1.5]
    out["H3 wide days trend x closeloc"] = W.groupby(["trend", "cl"], observed=True)["un"].apply(ct).unstack()
    N = D3[D3.mult < 1.0]
    out["H3 narrow days trend x closeloc"] = N.groupby(["trend", "cl"], observed=True)["un"].apply(ct).unstack()
    D3 = D3.assign(r1q=D3.groupby("coin")["ret1"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop")),
                   vq=D3.groupby("coin")["volr"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop")),
                   r20q=D3.groupby("coin")["ret20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop")))
    out["H3 by ret1 quintile"] = D3.groupby("r1q")["un"].apply(ct).unstack()
    out["H3 by ret20 quintile"] = D3.groupby("r20q")["un"].apply(ct).unstack()
    out["H3 by vol quintile x trend"] = D3.groupby(["vq", "trend"])["un"].apply(ct).unstack()
    D1 = D[D.H == 1].dropna(subset=["fwd"])
    out["H1 by weekday of signal bar"] = D1.groupby("wd")["un"].apply(ct).unstack()
    D7 = D[D.H == 7].dropna(subset=["mult", "ret20"])
    D7 = D7.assign(trend=np.where(D7.ret20 > 0, "up", "down"), wide=D7.mult >= 1.5)
    out["H7 trend x wide"] = D7.groupby(["trend", "wide"])["un"].apply(ct).unstack()
    # book weekday
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin))
    B = pd.concat(bk)
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    bd = B.groupby("day")["book_return"].mean().dropna()
    out["book by weekday"] = bd.groupby(pd.to_datetime(bd.index).weekday).agg(["count", "mean", "std"])
    return out
