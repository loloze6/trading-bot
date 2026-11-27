def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r = c.pct_change()
            rng = h - l
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "nxt": c.shift(-1) / c - 1,
                "nxt2": c.shift(-2) / c - 1,
                "ret": r,
                "loc": (c - l) / rng.replace(0, np.nan),
                "wid": rng / rng.rolling(30, min_periods=30).mean(),
                "rstd": (rng / c) / r.rolling(30, min_periods=30).std(),
                "z": r / r.rolling(30, min_periods=30).std(),
                "tr60": c / c.shift(60) - 1,
                "inprof": b["regime"].astype(str) != "chop",
                "regime": b["regime"].astype(str),
                "pos": b["postRebalance_current_allocation"],
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].transform("mean")
    d["unx"] = d["nxt"] - drift
    d["day"] = d["ts"].dt.floor("D")
    d["wd"] = d["ts"].dt.weekday
    d["year"] = d["ts"].dt.year

    def ct(x, days):
        x = pd.Series(x).dropna(); days = days.loc[x.index]
        n = len(x)
        if n < 5: return pd.Series({"n": n, "days": days.nunique(), "mean%": np.nan, "t": np.nan})
        m = x.mean(); rd = (x - m).groupby(days).sum(); D = len(rd)
        se = np.sqrt((rd ** 2).sum() * D / max(D - 1, 1)) / n
        return pd.Series({"n": n, "days": D, "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    out = {}
    v = d.dropna(subset=["unx", "loc", "wid"])
    # in profile: by loc bucket and wide
    v = v.assign(locb=pd.cut(v["loc"], [-0.01, .25, .5, .75, 1.01], labels=["low", "ml", "mh", "high"]),
                 wide=v["wid"] >= 1)
    for prof in [True, False]:
        s = v[v["inprof"] == prof]
        res = s.groupby(["wide", "locb"], observed=True).apply(lambda g: ct(g["unx"], g["day"]))
        out[f"unx by wide x loc, inprof={prof}"] = res
    # in profile, wide low close: graded by width
    s = v[(v["inprof"]) & (v["locb"] == "low")]
    s = s.assign(wq=pd.qcut(s["rstd"], 3, labels=False, duplicates="drop"))
    out["inprof low close by rstd tercile"] = s.groupby("wq").apply(lambda g: ct(g["unx"], g["day"]))
    # out of profile with trend sign
    s = v[(~v["inprof"]) & v["tr60"].notna()]
    s = s.assign(trend=pd.cut(s["tr60"], [-10, -.1, .1, 100], labels=["fall", "chop", "rise"]))
    out["outprof wide: trend x loc"] = s[s["wide"]].groupby(["trend", "locb"], observed=True).apply(lambda g: ct(g["unx"], g["day"]))
    # big moves scaled z
    s = d.dropna(subset=["unx", "z"])
    s = s.assign(zq=pd.qcut(s["z"], 5, labels=False))
    out["all: next unx by z quintile"] = s.groupby("zq").apply(lambda g: ct(g["unx"], g["day"]))
    out["inprof: next unx by z quintile"] = s[s["inprof"]].groupby("zq").apply(lambda g: ct(g["unx"], g["day"]))
    out["all: unx by weekday"] = d.dropna(subset=["unx"]).groupby("wd").apply(lambda g: ct(g["unx"], g["day"]))
    out["share inprof"] = float(d["inprof"].mean())
    out["regime counts"] = d["regime"].value_counts()
    return out
