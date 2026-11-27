def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 10: continue
            c = b["close"].values; h = b["high"].values; l = b["low"].values; o = b["open"].values
            rng = np.where(h - l > 0, h - l, np.nan)
            cl = (c - l) / rng
            r1 = pd.Series(c).pct_change().values
            mabs = pd.Series(np.abs(r1)).rolling(20, min_periods=10).mean().values
            r3p = pd.Series(c).shift(1) / pd.Series(c).shift(4) - 1
            n = len(b)
            for H in (2, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, i=i, cl=cl[i], r1=r1[i],
                                     z=r1[i] / mabs[i] if mabs[i] and not np.isnan(mabs[i]) else np.nan,
                                     prior3=r3p.iloc[i], inprof=b["regime"].iloc[i] != "chop",
                                     regime=b["regime"].iloc[i],
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                     year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     fwd=c[i + H] / c[i] - 1))
    d = pd.DataFrame(rows)
    for H in (2, 5):
        dh = d[d.H == H].copy()
        drift = dh.groupby("coin")["fwd"].transform("mean")
        dh["ex"] = dh["fwd"] - drift
        dh["clq"] = pd.cut(dh["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
        g = dh.groupby(["inprof", "clq"])["ex"].agg(["mean", "count", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
        g.columns = ["mean", "n", "t"]
        out[f"H{H} excess by inprofile x closeloc"] = g.round(4)
        dh["zq"] = pd.cut(dh["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
        g = dh.groupby(["inprof", "zq"])["ex"].agg(["mean", "count", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
        g.columns = ["mean", "n", "t"]
        out[f"H{H} excess by inprofile x z(day move)"] = g.round(4)
        if H == 5:
            g = dh.groupby("wd")["ex"].agg(["mean", "count"]); out["H5 by weekday"] = g.round(4)
            g = dh.groupby("year")["ex"].agg(["mean", "count"]); out["H5 by year"] = g.round(4)
            g = dh.groupby("regime")["ex"].agg(["mean", "count"]); out["H5 by regime"] = g.round(4)
            # high close after prior fall vs prior rise, in profile
            s = dh[dh.inprof & (dh.cl >= 0.75) & (dh.r1 > 0)].copy()
            s["pf"] = np.where(s.prior3 < 0, "prior fall", "prior rise")
            g = s.groupby("pf")["ex"].agg(["mean", "count", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
            g.columns = ["mean", "n", "t"]; out["H5 inprof highclose up day by prior3"] = g.round(4)
    # book: largest gain/loss days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    dd = pd.concat(dd)
    out["share profile days per coin"] = d[d.H == 5].groupby("coin")["inprof"].mean().round(3)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    if tr:
        tr = pd.concat(tr)
        out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count", "sum"]).round(3)
    return out
