def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            n = len(b)
            rng = np.where(h - l > 0, h - l, np.nan)
            cl = (c - l) / rng
            r1 = pd.Series(c).pct_change().values
            r20 = pd.Series(c).pct_change(20).values
            r60 = pd.Series(c).pct_change(60).values
            rngrel = rng / c
            rngz = rngrel / pd.Series(rngrel).rolling(20).mean().values
            v = b["volume"].values.astype(float)
            volz = v / pd.Series(v).rolling(20).mean().values
            ts = pd.to_datetime(b["timestamp"])
            for H in (2, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, fwd=c[i + H] / c[i] - 1,
                                     inprof=b["regime"].iloc[i] != "chop",
                                     cl=cl[i], r1=r1[i], r20=r20[i], r60=r60[i],
                                     rngz=rngz[i], volz=volz[i], year=ts.iloc[i].year,
                                     day=ts.iloc[i].normalize()))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "H"])["fwd"].transform("mean")
    df["usual"] = df.groupby(["coin", "H"])["fwd"].transform("std")
    df["unus"] = df["fwd"] - df["drift"]
    df["str"] = df["unus"] / df["usual"]
    def summ(g):
        x = g.dropna(subset=["unus"])
        if len(x) < 5:
            return pd.Series({"n": len(x), "days": np.nan, "mean_unus": x["unus"].mean(), "t_day": np.nan, "strength": np.nan})
        s = x.groupby("day")["unus"].sum()
        D = len(s); m = x["unus"].mean()
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean_unus": m, "t_day": m / se, "strength": x["str"].mean()})
    out = {}
    d2 = df[df.H == 2].dropna(subset=["volz", "r1", "rngz"]).copy()
    d2["volq"] = pd.qcut(d2["volz"], 5, labels=False)
    d2["updn"] = np.where(d2["r1"] > 0, "up", "down")
    out["H2 volq x day direction"] = d2.groupby(["updn", "volq"]).apply(summ)
    out["H2 volq x year"] = d2.assign(vh=np.where(d2.volq == 4, "top", np.where(d2.volq == 0, "bottom", "mid"))).groupby(["year", "vh"]).apply(summ)
    d2["trend"] = pd.cut(d2["r60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
    d2["rngq"] = pd.qcut(d2["rngz"], 5, labels=False)
    d2["clh"] = d2["cl"] > 0.5
    out["H2 wide(rngq>=3) by trend x clh"] = d2[d2.rngq >= 3].groupby(["trend", "clh"]).apply(summ)
    out["H2 volq by trend"] = d2.groupby(["trend", "volq"]).apply(summ)
    d5 = df[df.H == 5].dropna(subset=["r20"]).copy()
    d5["r20q"] = pd.qcut(d5["r20"], 5, labels=False)
    d5["trend"] = pd.cut(d5["r60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
    out["H5 r20q x year"] = d5.groupby(["year", "r20q"]).apply(summ)
    out["H5 r20q x trend"] = d5.groupby(["trend", "r20q"]).apply(summ)
    out["H5 r20q pooled"] = d5.groupby("r20q").apply(summ)
    return out
