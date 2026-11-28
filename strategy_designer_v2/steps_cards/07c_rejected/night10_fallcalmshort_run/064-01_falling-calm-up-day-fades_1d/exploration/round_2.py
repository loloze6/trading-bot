def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.shift(1).rolling(30, min_periods=20).std()
            z1 = r / sd
            z2 = (c / c.shift(2) - 1) / (sd * np.sqrt(2))
            z3 = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            inprof = (b["regime"] == "unknown").values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            n = len(b)
            for h in [3, 5, 7, 10, 14]:
                fwd = (c.shift(-h) / c - 1).values
                # drift: non-overlapping grid of all bars
                for start in range(0, n, h):
                    recs.append(dict(kind="grid", coin=coin, w=w, h=h, fwd=fwd[start],
                                     z1=np.nan, z2=np.nan, z3=np.nan, yr=yr[start], day=day[start]))
                    # case: first in-profile bar with z1>0 in this cell
                    for i in range(start, min(start + h, n)):
                        if inprof[i] and z1.iloc[i] > 0:
                            recs.append(dict(kind="case", coin=coin, w=w, h=h, fwd=fwd[i],
                                             z1=z1.iloc[i], z2=z2.iloc[i], z3=z3.iloc[i],
                                             yr=yr[i], day=day[i]))
                            break
    d = pd.DataFrame(recs).dropna(subset=["fwd"])
    drift = d[d.kind == "grid"].groupby(["coin", "h"])["fwd"].mean().rename("drift")
    usual = d[d.kind == "grid"].groupby(["coin", "h"])["fwd"].std().rename("usual")
    cs = d[d.kind == "case"].join(drift, on=["coin", "h"]).join(usual, on=["coin", "h"])
    cs["unu_short"] = -(cs["fwd"] - cs["drift"])
    cs["str"] = cs["unu_short"] / cs["usual"]
    res = []
    for h, g in cs.groupby("h"):
        dd = g.groupby("day")["unu_short"].sum()
        tday = g["unu_short"].mean() / (dd.std() * np.sqrt(len(dd)) / len(g))
        med = g["z1"].median()
        hi = g[g.z1 > med]["unu_short"]; lo = g[g.z1 <= med]["unu_short"]
        s = stats.linregress(g.z1, g.unu_short)
        res.append(dict(h=h, n=len(g), days=len(dd), mean_short=g.unu_short.mean(), t_day=tday,
                        strength=g["str"].mean(), hi_minus_lo=hi.mean() - lo.mean(),
                        t_hilo=stats.ttest_ind(hi, lo, equal_var=False).statistic,
                        slope_z1=s.slope, t_slope=s.slope / s.stderr, total_short=-g.fwd.mean()))
    out["cases z1>0 in profile, short unusual move by horizon"] = pd.DataFrame(res)
    for zc in ["z2", "z3"]:
        rr = []
        for h, g in cs.dropna(subset=[zc]).groupby("h"):
            gg = g[g[zc] > 0]
            if len(gg) > 5:
                s = stats.linregress(gg[zc], gg.unu_short)
                rr.append(dict(h=h, n=len(gg), mean=gg.unu_short.mean(), slope=s.slope, t=s.slope / s.stderr))
        out[f"multi-day rise {zc}>0: short unusual move slope"] = pd.DataFrame(rr)
    g = cs[cs.h == 10]
    g = g.assign(zb=pd.cut(g.z1, [0, 0.5, 1, 1.5, 99]))
    out["h10 by z1 bucket"] = g.groupby("zb")["unu_short"].agg(["mean", "count"]).reset_index()
    out["h10 by coin"] = g.groupby("coin")["unu_short"].agg(["mean", "count"]).reset_index()
    out["h10 by year"] = g.groupby("yr")["unu_short"].agg(["mean", "count"]).reset_index()
    g7 = cs[cs.h == 7]
    out["h7 by coin"] = g7.groupby("coin")["unu_short"].agg(["mean", "count"]).reset_index()
    return out
