def explore(data):
    import numpy as np, pandas as pd
    out = {}
    def tcl(df, col="ex", key="dkey"):
        s = df.dropna(subset=[col])
        if len(s) < 3: return (len(s), np.nan, np.nan, 0)
        m = s[col].mean()
        dev = (s[col] - m).groupby(s[key]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return (len(s), m, m / se if se > 0 else np.nan, s[key].nunique())
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 2, 3, 5, 7):
                fr = c.shift(-h) / c - 1
                grid = (np.arange(len(b)) % h) == 0
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "fr": fr, "grid": grid,
                    "r1z": r1 / vol30.shift(1), "ret60": c / c.shift(60) - 1,
                    "clv": (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                    "inprof": (b["regime"] == "unknown").values, "yr": ts.dt.year,
                    "dkey": ts.dt.floor("D").astype("int64")}))
    D = pd.concat(rows, ignore_index=True)
    G = D[D.grid & D.fr.notna()].copy()
    G = G.join(G.groupby(["coin", "h"]).fr.mean().rename("drift"), on=["coin", "h"])
    G["ex"] = G.fr - G.drift
    G["zb"] = pd.cut(G.r1z, [-99, -2, -1, 0, 1, 2, 3, 99])
    res = []
    for (h, ip, zb), s in G.groupby(["h", "inprof", "zb"], observed=True):
        n, m, t, nd = tcl(s)
        res.append({"h": h, "inprof": ip, "zbin": str(zb), "n": n, "mean_ex": m, "t_cl": t, "days": nd})
    out["daymove_bins_clustered"] = pd.DataFrame(res)
    # big up day in profile: by year, by coin, by close location
    g = G[(G.h == 1) & G.inprof & (G.r1z > 1.5)]
    out["inprof_up_by_year_h1"] = pd.DataFrame([dict(zip(["n", "mean", "t", "days"], tcl(s)), yr=y) for y, s in g.groupby("yr")])
    out["inprof_up_by_coin_h1"] = pd.DataFrame([dict(zip(["n", "mean", "t", "days"], tcl(s)), coin=k) for k, s in g.groupby("coin")])
    g3 = G[(G.h == 3) & G.inprof & (G.r1z > 1.5)]
    out["inprof_up_by_year_h3"] = pd.DataFrame([dict(zip(["n", "mean", "t", "days"], tcl(s)), yr=y) for y, s in g3.groupby("yr")])
    # graded slope: in profile, up days r1z>0, regress ex(h) on r1z, clustered
    res = []
    for h in (1, 2, 3, 5):
        s = G[(G.h == h) & G.inprof & (G.r1z > 0)].dropna(subset=["ex", "r1z"])
        x = s.r1z - s.r1z.mean(); y = s.ex
        b = (x * y).sum() / (x ** 2).sum()
        e = y - y.mean() - b * x
        dev = (x * e).groupby(s.dkey).sum()
        se = np.sqrt((dev ** 2).sum()) / (x ** 2).sum()
        res.append({"h": h, "n": len(s), "slope": b, "t_cl": b / se})
    out["inprof_updays_slope"] = pd.DataFrame(res)
    # same slope outside profile, by 60d trend band
    res = []
    for h in (1, 3):
        s0 = G[(G.h == h) & (G.r1z > 0)].dropna(subset=["ex", "r1z", "ret60"])
        s0 = s0.assign(tr=np.where(s0.ret60 > 0.1, "rising", np.where(s0.ret60 < -0.1, "falling", "choppy")))
        for (tr, ip), s in s0.groupby(["tr", "inprof"]):
            x = s.r1z - s.r1z.mean(); y = s.ex
            b = (x * y).sum() / (x ** 2).sum()
            e = y - y.mean() - b * x
            dev = (x * e).groupby(s.dkey).sum()
            se = np.sqrt((dev ** 2).sum()) / (x ** 2).sum()
            res.append({"h": h, "trend": tr, "inprof": ip, "n": len(s), "slope": b, "t_cl": b / se})
    out["updays_slope_by_trend"] = pd.DataFrame(res)
    # big down day rebound by trend (out of profile)
    s0 = G[(G.h == 1) & (G.r1z < -1.5)].dropna(subset=["ret60"])
    s0 = s0.assign(tr=np.where(s0.ret60 > 0.1, "rising", np.where(s0.ret60 < -0.1, "falling", "choppy")))
    out["downday_by_trend_h1"] = pd.DataFrame([dict(zip(["n", "mean", "t", "days"], tcl(s)), tr=k[0], inprof=k[1]) for k, s in s0.groupby(["tr", "inprof"])])
    return out
