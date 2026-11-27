def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            loc = (c - b["low"]) / rng
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            r1 = c / c.shift(1) - 1
            vol = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            inprof = b["regime"].isin(["unknown", "mean_reversion"])
            for h in (2, 5, 10):
                f = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({"coin": coin, "w": w, "h": h, "loc": loc.iloc[idx].values,
                                  "r1": r1.iloc[idx].values, "r5": r5.iloc[idx].values,
                                  "r20": r20.iloc[idx].values, "r60": r60.iloc[idx].values,
                                  "vol": vol.iloc[idx].values, "fwd": f.iloc[idx].values,
                                  "inprof": inprof.iloc[idx].values,
                                  "yr": ts.iloc[idx].dt.year.values,
                                  "day": ts.iloc[idx].dt.floor("D").values})
                rows.append(d)
    df = pd.concat(rows).dropna(subset=["fwd"])
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["unus"] = df["fwd"] - df["drift"]

    def summ(g):
        n = len(g)
        dd = g.groupby("day")["unus"].sum()
        nd = len(dd)
        m = g["unus"].mean()
        se = np.sqrt((dd - dd.mean() * 0).pow(2).sum() * 0 + ((g.groupby("day")["unus"].apply(lambda x: (x - m).sum())) ** 2).sum()) / n if n > 2 else np.nan
        return pd.Series({"n": n, "days": nd, "mean_unus": m, "t_day": m / se if se and se > 0 else np.nan})

    def trend(r):
        return np.where(r > .1, "rising", np.where(r < -.1, "falling", "choppy"))
    df["trend"] = trend(df["r60"])
    df.loc[df["r60"].isna(), "trend"] = "na"
    df["locb"] = pd.cut(df["loc"], [0, .5, .8, 1.0001], include_lowest=True)

    for h in (2, 5, 10):
        d = df[df.h == h]
        out[f"h{h} in profile by loc"] = d[d.inprof].groupby("locb").apply(summ)
    d5 = df[df.h == 5]
    ip = d5[d5.inprof]
    out["h5 in profile all"] = summ(ip)
    out["h5 in profile loc>0.5 by year"] = ip[ip["loc"] > .5].groupby("yr").apply(summ)
    out["h5 in profile loc>0.5 by r5 sign"] = ip[ip["loc"] > .5].groupby(ip["r5"] < 0).apply(summ)
    # graded slope of unusual on loc in profile
    x = ip.dropna(subset=["loc"])
    out["h5 in profile corr loc vs unus"] = float(np.corrcoef(x["loc"], x["unus"])[0, 1])
    # out of profile: choppy trend (not agitated -> mostly calm) loc effect (brief's falsifier)
    op = d5[~d5.inprof]
    out["h5 out profile choppy trend by loc"] = op[op.trend == "choppy"].groupby("locb").apply(summ)
    out["h5 out profile by trend"] = op.groupby("trend").apply(summ)
    # r20 moderate fall out of profile
    op = op.copy()
    op["r20b"] = pd.cut(op["r20"], [-1, -.2, -.1, 0, .1, .2, 10])
    out["h5 out r20 -20..-10 by trend"] = op[op.r20b.astype(str) == "(-0.2, -0.1]"].groupby("trend").apply(summ)
    out["h5 out r20 -20..-10 by year"] = op[op.r20b.astype(str) == "(-0.2, -0.1]"].groupby("yr").apply(summ)
    out["h5 out by r20 bin (day t)"] = op.groupby("r20b").apply(summ)
    d10 = df[(df.h == 10) & (~df.inprof)].copy()
    d10["r20b"] = pd.cut(d10["r20"], [-1, -.2, -.1, 0, .1, .2, 10])
    out["h10 out by r20 bin"] = d10.groupby("r20b").apply(summ)
    return out
