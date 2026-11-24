def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; H = 14
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            cs = df["close"].astype(float); v = df["volume"].astype(float)
            n = len(cs)
            if n < H + 2: continue
            r14 = cs / cs.shift(14) - 1
            r1 = cs.pct_change()
            r3 = cs / cs.shift(3) - 1
            vr = v.rolling(14).mean() / v.rolling(30).mean() - 1
            vr7 = v.rolling(7).mean() / v.rolling(30).mean() - 1
            vz1 = v / v.rolling(30).mean() - 1
            fwd = cs.shift(-H) / cs - 1
            fwd7 = cs.shift(-7) / cs - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                 r14=r14[i], r1=r1[i], r3=r3[i], vr=vr[i], vr7=vr7[i], vz1=vz1[i],
                                 fwd=fwd[i], fwd7=fwd7[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["ex7"] = g["fwd7"] - g.groupby("coin")["fwd7"].transform("mean")
    g["usd"] = g.groupby("coin")["fwd"].transform("std")
    def ct(s, col="ex"):
        s = s.dropna(subset=[col])
        d = s.groupby("day")[col].sum()
        m = s[col].mean(); nd = len(d)
        se = np.sqrt((d - d.mean() * 0).pow(2).sum() - 0) / len(s) if len(s) else np.nan
        dev = s.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return pd.Series(dict(mean=m, t=m / se, n=len(s), days=nd))
    out = {}
    s = g.dropna(subset=["vr", "r14"]).copy()
    s["q"] = s.groupby("coin")["vr"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["vr quintile, clustered"] = s.groupby("q").apply(ct)
    s["rs"] = np.where(s.r14 > 0, "r14up", "r14dn")
    out["vr quintile x r14 sign"] = s.groupby(["rs", "q"]).apply(ct)
    # signed volume bet: sign(vr) direction, graded by vr z
    s["vrz"] = s.groupby("coin")["vr"].transform(lambda x: (x - x.mean()) / x.std())
    s["bet"] = s["ex"] * np.sign(s["vr"])
    out["bet sign(vr) all, clustered"] = ct(s, "bet")
    s["big"] = s["vrz"].abs() >= s["vrz"].abs().median()
    out["bet sign(vr) by |vrz| half"] = s.groupby("big").apply(lambda x: ct(x, "bet"))
    out["bet sign(vr) by year"] = s.groupby("year").apply(lambda x: ct(x, "bet"))
    s["bet7"] = s["ex7"] * np.sign(s["vr"])
    out["bet sign(vr) 7d"] = ct(s, "bet7")
    s["strength"] = s["bet"] / s["usd"]
    out["strength sign(vr)"] = s["strength"].mean()
    s2 = g.dropna(subset=["vr7"]).copy(); s2["bet"] = s2["ex"] * np.sign(s2["vr7"])
    out["bet sign(vr7)"] = ct(s2, "bet")
    s3 = g.dropna(subset=["vz1"]).copy(); s3["bet"] = s3["ex"] * np.sign(s3["vz1"])
    out["bet sign(1d vol surge)"] = ct(s3, "bet")
    # large down day follow
    s4 = g.dropna(subset=["r1"]).copy()
    s4["q"] = s4.groupby("coin")["r1"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["r1 quintile clustered"] = s4.groupby("q").apply(ct)
    # weekday, clustered by day: daily coin returns
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            dd.append(pd.DataFrame(dict(r=df["coin_return"], day=pd.to_datetime(df["day"]))))
    d = pd.concat(dd).dropna()
    daym = d.groupby("day")["r"].mean()
    wd = pd.DataFrame(dict(r=daym, dow=daym.index.dayofweek, yr=daym.index.year))
    out["dow, cross-coin day mean"] = wd.groupby("dow")["r"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    wd["half"] = np.where(wd.yr <= 2021, "<=2021", ">=2022")
    out["dow by half"] = wd.groupby(["half", "dow"])["r"].mean().unstack()
    return out
