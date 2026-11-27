def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            n = len(b)
            if n < 20: continue
            c = b["close"].values
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            loc = ((b["close"] - b["low"]) / rng).values
            s = pd.Series(c)
            ret5 = s.pct_change(5).values
            ret60 = s.pct_change(60).values
            vol30 = s.pct_change().rolling(30, min_periods=20).std().values
            ts = pd.to_datetime(b["timestamp"])
            inprof = (b["regime"] != "chop").values
            for h in (1, 2, 3, 5):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=ts[i].normalize(), year=ts[i].year,
                                     loc=loc[i], ret5=ret5[i], ret60=ret60[i], vol=vol30[i],
                                     inprof=inprof[i], fwd=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["unus"] = d["fwd"] - d["drift"]
    d["usual"] = d.groupby(["coin", "h"])["fwd"].transform("std")
    d["volrel"] = d["vol"] / d.groupby("coin")["vol"].transform("median")
    d["agit"] = np.where(d["volrel"] > 1, "agitated", "calm")
    d["trend"] = np.select([d.ret60 > 0.10, d.ret60 < -0.10, d.ret60.notna()], ["rising", "falling", "choppy"], "na")
    def tst(g):
        s = g.groupby("day")["unus"].sum()
        m = g["unus"].mean(); se = np.sqrt((s ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=len(s), mean=round(m, 4), t=round(m / se, 2) if se else np.nan,
                              strength=round((g["unus"] / g["usual"]).mean(), 3)))
    out = {}
    x = d.dropna(subset=["loc", "ret5", "vol"])
    x = x[(x["loc"] > 0.5) & (x["ret5"] < 0)].copy()
    x["dq"] = x.groupby("h")["ret5"].transform(lambda s: pd.qcut(s, 3, labels=False))
    for h in (1, 2, 3, 5):
        out[f"all upper r5neg h{h} agit x depth"] = x[x.h == h].groupby(["agit", "dq"]).apply(tst)
    y = x[x.h == 2]
    out["h2 agitated by trend"] = y[y.agit == "agitated"].groupby("trend").apply(tst)
    out["h2 agitated deep by year"] = y[(y.agit == "agitated") & (y.dq == 0)].groupby("year").apply(tst)
    ya = y[y.agit == "agitated"]
    r = stats.linregress(ya["ret5"] / ya["vol"], ya["unus"] / ya["usual"])
    out["h2 agitated slope of strength on ret5/vol"] = pd.Series(dict(slope=r.slope, t=r.slope / r.stderr, n=len(ya)))
    yc = y[y.agit == "calm"]
    r = stats.linregress(yc["ret5"] / yc["vol"], yc["unus"] / yc["usual"])
    out["h2 calm slope"] = pd.Series(dict(slope=r.slope, t=r.slope / r.stderr, n=len(yc)))
    # lower-half close control
    z = d.dropna(subset=["loc", "ret5", "vol"])
    z = z[(z["loc"] <= 0.5) & (z["ret5"] < 0) & (z.h == 2)].copy()
    z["dq"] = pd.qcut(z["ret5"], 3, labels=False)
    out["control lower-half r5neg h2 agit x depth"] = z.groupby(["agit", "dq"]).apply(tst)
    return out
