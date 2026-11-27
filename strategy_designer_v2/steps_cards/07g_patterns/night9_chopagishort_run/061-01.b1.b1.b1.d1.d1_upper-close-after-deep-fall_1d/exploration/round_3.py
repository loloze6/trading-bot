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
            r5 = pd.Series(c).pct_change(5).values
            r60 = pd.Series(c).pct_change(60).values
            ts = pd.to_datetime(b["timestamp"])
            for H in (2, 3, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, fwd=c[i + H] / c[i] - 1,
                                     inprof=b["regime"].iloc[i] != "chop", cl=cl[i], r5=r5[i], r60=r60[i],
                                     year=ts.iloc[i].year, day=ts.iloc[i].normalize()))
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
        se = np.sqrt(((s - s.mean() * 0) ** 2).sum() * D / (D - 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean_unus": m, "t_day": m / se, "strength": x["str"].mean()})
    out = {}
    df["clb"] = pd.cut(df["cl"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["0-.25", ".25-.5", ".5-.75", ".75-1"])
    df["r5neg"] = df["r5"] < 0
    ip = df[df.inprof]
    out["inprof cl bins by H"] = ip.groupby(["H", "clb"]).apply(summ)
    out["inprof H5 cl bins x r5neg"] = ip[ip.H == 5].groupby(["r5neg", "clb"]).apply(summ)
    out["inprof H5 upper close by year"] = ip[(ip.H == 5) & (ip.cl > 0.5)].groupby("year").apply(summ)
    # short-direction move graded by cl: regress unus on cl inside profile, day-clustered
    for H in (2, 5):
        x = ip[ip.H == H].dropna(subset=["cl", "unus"])
        xc = x["cl"] - x["cl"].mean()
        beta = (xc * x["unus"]).sum() / (xc ** 2).sum()
        res = x["unus"] - x["unus"].mean() - beta * xc
        sc = (xc * res).groupby(x["day"]).sum()
        D = len(sc)
        se = np.sqrt((sc ** 2).sum() * D / (D - 1)) / (xc ** 2).sum()
        out[f"inprof H{H} slope of unus on cl"] = pd.Series({"n": len(x), "days": D, "beta": beta, "t_day": beta / se})
    # choppy calm comparison: choppy trend (r60 in window) but not in profile
    cc = df[(~df.inprof) & (df.r60.abs() <= 0.10)]
    out["choppy not agitated H5 cl bins"] = cc[cc.H == 5].groupby("clb").apply(summ)
    out["outside profile, all, H5 cl bins"] = df[(~df.inprof) & (df.H == 5)].groupby("clb").apply(summ)
    return out
