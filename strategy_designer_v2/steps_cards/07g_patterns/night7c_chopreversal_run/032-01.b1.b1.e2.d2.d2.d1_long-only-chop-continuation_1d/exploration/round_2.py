def explore(data):
    import numpy as np, pandas as pd
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ret7 = c / c.shift(7) - 1
            ret30 = c / c.shift(30) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            vol30 = r1.rolling(30).std()
            vol10 = r1.rolling(10).std()
            vol60 = r1.rolling(60).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "day": ts.dt.floor("D"),
                               "ret7": ret7, "ret30": ret30, "er": er, "vol30": vol30,
                               "vr10_60": vol10 / vol60, "vr30_60": vol30 / vol60,
                               "s7": ret7 / (vol30 * np.sqrt(7)),
                               "r1s": r1 / vol30.shift(1),
                               "fwd": c.shift(-H) / c - 1,
                               "fwd1": (c.shift(-1) / c - 1) / vol30,
                               "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "wn": int(w[1:])})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def ct(d, col):
        d = d.dropna(subset=[col])
        if len(d) < 5:
            return pd.Series({"n": len(d), "days": np.nan, "mean": np.nan, "t_day": np.nan})
        m = d[col].mean()
        s = (d[col] - m).groupby(d["day"]).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series({"n": len(d), "days": D, "mean": m, "t_day": m / se})

    out = {}
    g = A[(A["pos"] % H == 0)].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean()
    g["un"] = g["fwd"] - g["coin"].map(drift)
    g["fold"] = np.where(g["wn"] <= 12, "B", "C")
    gg = g.dropna(subset=["er", "s7", "ret30"]).copy()
    gg["chop"] = np.where(gg["er"] <= 0.3, "chop", "trend")
    # chop, down month, graded by scaled down-week
    cd = gg[(gg["chop"] == "chop") & (gg["ret30"] < 0) & (gg["s7"] < 0)].copy()
    cd["q"] = pd.qcut(cd["s7"], 3, labels=False)
    out["chop dn30 s7<0 by s7 tercile (0=largest fall)"] = cd.groupby("q").apply(lambda d: ct(d, "un"))
    out["chop dn30 s7<0 by fold"] = cd.groupby("fold").apply(lambda d: ct(d, "un"))
    out["chop dn30 s7<0 total move (raw fwd)"] = ct(cd, "fwd").to_frame().T
    cu = gg[(gg["chop"] == "chop") & (gg["ret30"] > 0) & (gg["s7"] > 0)]
    out["chop up30 s7>0 by fold"] = cu.groupby("fold").apply(lambda d: ct(d, "un"))
    # chop overall: signed continuation, s7 sign
    ch = gg[gg["chop"] == "chop"].copy()
    ch["sun"] = ch["un"] * np.sign(ch["s7"])
    ch["q"] = pd.qcut(ch["s7"].abs(), 3, labels=False)
    out["chop signed continuation by |s7| tercile"] = ch.groupby("q").apply(lambda d: ct(d, "sun"))
    # trend regime reversal
    tr = gg[gg["chop"] == "trend"].copy()
    tr["sun"] = -tr["un"] * np.sign(tr["s7"])
    tr["q"] = pd.qcut(tr["s7"].abs(), 3, labels=False)
    out["trend signed reversal by |s7| tercile"] = tr.groupby("q").apply(lambda d: ct(d, "sun"))
    # vol compression
    v = g.dropna(subset=["vr10_60"]).copy()
    v["q"] = pd.qcut(v["vr10_60"], 4, labels=False)
    out["un by vol10/vol60 quartile"] = v.groupby("q").apply(lambda d: ct(d, "un"))
    v2 = g.dropna(subset=["vr30_60"]).copy()
    v2["q"] = pd.qcut(v2["vr30_60"], 4, labels=False)
    out["un by vol30/vol60 quartile"] = v2.groupby("q").apply(lambda d: ct(d, "un"))
    out["low vol30/60 quartile by fold"] = v2[v2["q"] == 0].groupby("fold").apply(lambda d: ct(d, "un"))
    # daily reversal after large scaled down days, clustered
    d1 = A.dropna(subset=["r1s", "fwd1"]).copy()
    d1["q"] = pd.qcut(d1["r1s"], 5, labels=False)
    out["next-day scaled ret by today quintile (day-clustered)"] = d1.groupby("q").apply(lambda d: ct(d, "fwd1"))
    d1["fold"] = np.where(d1["wn"] <= 12, "B", "C")
    out["next-day after bottom quintile, by fold"] = d1[d1["q"] == 0].groupby("fold").apply(lambda d: ct(d, "fwd1"))
    out["next-day scaled ret by weekday of t (day-clustered)"] = d1.groupby("wd").apply(lambda d: ct(d, "fwd1"))
    out["Thu return (wd t=2) by fold"] = d1[d1["wd"] == 2].groupby("fold").apply(lambda d: ct(d, "fwd1"))
    return out
