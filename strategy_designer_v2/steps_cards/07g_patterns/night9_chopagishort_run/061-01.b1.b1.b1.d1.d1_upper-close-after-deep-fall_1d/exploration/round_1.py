def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values; o = b["open"].values
            n = len(b)
            rng = np.where(h - l > 0, h - l, np.nan)
            cl = (c - l) / rng
            r1 = pd.Series(c).pct_change().values
            r5 = pd.Series(c).pct_change(5).values
            r20 = pd.Series(c).pct_change(20).values
            vol20 = pd.Series(r1).rolling(20).std().values
            rngrel = rng / c
            rngz = rngrel / pd.Series(rngrel).rolling(20).mean().values
            v = b["volume"].values.astype(float)
            volz = v / pd.Series(v).rolling(20).mean().values
            ts = pd.to_datetime(b["timestamp"])
            for H in (1, 2, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, i=i, fwd=c[i + H] / c[i] - 1,
                                     inprof=b["regime"].iloc[i] != "chop", regime=b["regime"].iloc[i],
                                     cl=cl[i], r1=r1[i], r5=r5[i], r20=r20[i], vol20=vol20[i],
                                     rngz=rngz[i], volz=volz[i], wd=ts.iloc[i].dayofweek,
                                     year=ts.iloc[i].year, pos=b["postRebalance_current_allocation"].iloc[i]))
    df = pd.DataFrame(rows)
    # drift per coin and H over all windows
    df["drift"] = df.groupby(["coin", "H"])["fwd"].transform("mean")
    df["usual"] = df.groupby(["coin", "H"])["fwd"].transform("std")
    df["unus"] = df["fwd"] - df["drift"]
    df["str"] = df["unus"] / df["usual"]
    out = {}
    def summ(g):
        x = g["unus"].dropna()
        return pd.Series({"n": len(x), "mean_unus": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": g["str"].mean()})
    for H in (1, 2, 5):
        d = df[df.H == H].copy()
        d["clq"] = pd.qcut(d["cl"], 5, labels=False)
        d["r5q"] = pd.qcut(d["r5"], 5, labels=False)
        d["r1q"] = pd.qcut(d["r1"], 5, labels=False)
        d["rngq"] = pd.qcut(d["rngz"], 5, labels=False)
        d["volq"] = pd.qcut(d["volz"], 5, labels=False)
        d["r20q"] = pd.qcut(d["r20"], 5, labels=False)
        out[f"H{H} by inprof x clq"] = d.groupby(["inprof", "clq"]).apply(summ)
        if H in (2, 5):
            out[f"H{H} by r5q x inprof"] = d.groupby(["inprof", "r5q"]).apply(summ)
            out[f"H{H} by r1q all"] = d.groupby("r1q").apply(summ)
            out[f"H{H} by rngq x clq(all)"] = d.assign(clh=d.clq >= 3).groupby(["rngq", "clh"]).apply(summ)
            out[f"H{H} by volq"] = d.groupby("volq").apply(summ)
            out[f"H{H} by r20q"] = d.groupby("r20q").apply(summ)
        if H == 1:
            out["H1 by weekday"] = d.groupby("wd").apply(summ)
    # book daily
    bd = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bd.append(dd.assign(coin=coin, w=w))
    bd = pd.concat(bd)
    bd["dow"] = pd.to_datetime(bd["day"]).dt.dayofweek
    br = bd.dropna(subset=["book_return"])
    nz = br[br.book_return.abs() > 1e-9]
    out["book active days by coin"] = nz.groupby("coin")["book_return"].agg(["count", "mean", "sum"])
    out["book active by year"] = nz.assign(y=pd.to_datetime(nz["day"]).dt.year).groupby("y")["book_return"].agg(["count", "mean", "sum"])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    tr["absf"] = tr["entry_forecast"].abs()
    tr["fq"] = pd.qcut(tr["absf"], 3, labels=False, duplicates="drop")
    out["trades by forecast tercile"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
