def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        mu_all = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            mu_all.append(c.pct_change().dropna())
        mu = pd.concat(mu_all).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            nxt3 = c.shift(-3) / c - 1
            tr60 = c / c.shift(60) - 1
            sdrank = sd.rolling(60, min_periods=30).rank(pct=True)
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "z": z, "sd": sd,
                               "nxt": nxt, "nx_ex": nxt - mu, "nxt2": nxt2, "nxt3": nxt3,
                               "tr60": tr60, "sdrank": sdrank, "rng": rng, "clpos": clpos,
                               "fa": (b["regime"] == "unknown"), "alloc": b["postRebalance_current_allocation"],
                               "fc": b["forecast"], "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "r5": c / c.shift(5) - 1})
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["z", "nxt"])
    out = {}
    def tstat(x):
        x = x.dropna(); return (x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, len(x))
    # z buckets by profile approx
    d["prof"] = np.where(d.fa, "FA", np.where(d.tr60 < -0.10, "fall_other", np.where(d.tr60 > 0.10, "rise", "chop")))
    d["zb"] = pd.cut(d.z, [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    g = d.groupby(["prof", "zb"]).nx_ex.agg(["mean", "count", lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan])
    g.columns = ["mean", "n", "t"]; out["next-day excess by profile x z"] = g
    # slope of nx_ex on -z for falls by profile
    res = {}
    for p, s in d[d.z < 0].groupby("prof"):
        sl = stats.linregress(-s.z, s.nx_ex); res[p] = {"slope": sl.slope, "t": sl.slope/sl.stderr, "n": len(s)}
    for p, s in d[d.z > 0].groupby("prof"):
        sl = stats.linregress(s.z, s.nx_ex); res["up_"+p] = {"slope": sl.slope, "t": sl.slope/sl.stderr, "n": len(s)}
    out["slope falls (-z) / rises (z) by profile"] = pd.DataFrame(res).T
    # FA falls: horizon decay (non overlap not exact for 2,3 but quick)
    fa = d[d.fa & (d.z < -1)]
    out["FA z<-1 horizons"] = pd.Series({"n1": tstat(fa.nxt)[1], "m1": fa.nxt.mean(), "t1": tstat(fa.nxt)[0],
                                          "m2": fa.nxt2.mean(), "t2": tstat(fa.nxt2)[0], "m3": fa.nxt3.mean(), "t3": tstat(fa.nxt3)[0]})
    # close position within falls in FA
    fz = d[d.z < -1].copy()
    fz["cp"] = pd.cut(fz.clpos, [0, 0.25, 0.5, 0.75, 1.0], include_lowest=True)
    g = fz.groupby(["fa", "cp"]).nx_ex.agg(["mean", "count"]); out["z<-1 next by close pos in range, FA flag"] = g
    # weekday among all falls z<-1
    g = fz.groupby("wd").nx_ex.agg(["mean", "count"]); out["z<-1 next by weekday"] = g
    # all bars weekday
    g = d.groupby("wd").nx_ex.agg(["mean", "count", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))]); g.columns=["mean","n","t"]
    out["all bars next by weekday"] = g
    # vol level rank
    d["vb"] = pd.qcut(d.sdrank, 3, labels=["lowvol","mid","hivol"])
    g = d[d.z < -1].groupby("vb").nx_ex.agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))]); g.columns=["mean","n","t"]
    out["z<-1 next by in-window vol rank"] = g
    # 5-day fall
    d["r5b"] = pd.qcut(d.r5, 5)
    g = d.groupby("r5b").nx_ex.agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))]); g.columns=["mean","n","t"]
    out["next by 5d return quintile"] = g
    # by coin in FA
    g = d[d.fa & (d.z<0)].groupby("coin").apply(lambda s: pd.Series({"n": len(s), "slope_t": (lambda l: l.slope/l.stderr)(stats.linregress(-s.z, s.nx_ex)), "mean": s.nx_ex.mean()}))
    out["FA falls by coin"] = g
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin, w=w))
    bd = pd.concat(bd).dropna(subset=["book_return"])
    book = bd.groupby(["w","day"]).book_return.mean()
    out["book by window"] = book.groupby(level=0).agg(["mean","std","count"])
    return out
