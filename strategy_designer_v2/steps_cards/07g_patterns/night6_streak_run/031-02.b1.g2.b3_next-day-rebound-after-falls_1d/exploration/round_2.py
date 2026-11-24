import pandas as pd, numpy as np

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std() / np.sqrt(len(x)))

def _ct(df, y):
    z = df[["day", y]].dropna()
    if len(z) < 5: return pd.Series({"mean%": np.nan, "t_day": np.nan, "n": len(z), "days": 0})
    s = z.groupby("day")[y].sum()
    cnt = z.groupby("day")[y].count()
    m = s.sum() / cnt.sum()
    dev = (z[y] - m).groupby(z["day"]).sum()
    se = np.sqrt((dev ** 2).sum()) / cnt.sum()
    return pd.Series({"mean%": m * 100, "t_day": m / se if se > 0 else np.nan, "n": len(z), "days": len(s)})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(60, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "ts": pd.to_datetime(b["timestamp"], utc=True),
                               "r1": r1, "vol": vol, "z1": r1 / vol,
                               "z10": (c / c.shift(10) - 1) / (vol * np.sqrt(10)),
                               "vol10": r1.rolling(10, min_periods=8).std()})
            df["vratio"] = df["vol10"] / vol
            for h in (1, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["rng"] = (b["high"] - b["low"]).astype(float) / c / vol
            df["clv"] = ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)).astype(float)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = d["ts"].dt.floor("D")
    d["year"] = d["ts"].dt.year
    for h in (1, 3, 5):
        g = d[d["pos"] % h == 0]
        mu = g.groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(mu)
        d.loc[d["pos"] % h != 0, f"x{h}"] = np.nan
    out = {}
    d["side"] = np.where(d["r1"] < 0, "down", "up")
    d["rq"] = d.groupby("coin")["rng"].transform(lambda v: pd.qcut(v, 5, labels=False))
    out["range quintile x side -> x1 (day-clustered)"] = d.groupby(["side", "rq"]).apply(lambda g: _ct(g, "x1")).round(3)
    d["cq"] = pd.qcut(d["clv"], 5, labels=False, duplicates="drop")
    out["close location quintile x side -> x1"] = d.groupby(["side", "cq"]).apply(lambda g: _ct(g, "x1")).round(3)
    # vol-of-vol: recent 10d vol vs 60d vol, falls
    dn = d[d["z1"] < -0.5].copy()
    dn["vrq"] = pd.qcut(dn["vratio"], 3, labels=["calmer", "same", "hotter"])
    out["falls (z1<-0.5) by recent/60d vol tercile -> x1"] = dn.groupby("vrq", observed=True).apply(lambda g: _ct(g, "x1")).round(3)
    # vol level relative to coin history
    d["volq"] = d.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    dn = d[d["z1"] < -0.5]
    out["falls by 60d vol tercile -> x1 clustered"] = dn.groupby("volq").apply(lambda g: _ct(g, "x1")).round(3)
    out["falls hivol by year -> x1"] = dn[dn["volq"] == 2].groupby("year").apply(lambda g: _ct(g, "x1")).round(3)
    out["falls hivol by coin -> x1"] = dn[dn["volq"] == 2].groupby("coin").apply(lambda g: _ct(g, "x1")).round(3)
    # graded: raw fall size in % (not vol scaled) deciles among down days
    dd = d[d["r1"] < 0].copy()
    dd["rawq"] = pd.qcut(dd["r1"], 5, labels=False)
    out["down days by raw % fall quintile -> x1"] = dd.groupby("rawq").apply(lambda g: _ct(g, "x1")).round(3)
    # z10 deep lows: horizon 5
    d["z10q"] = pd.qcut(d["z10"], 10, labels=False)
    out["z10 decile -> x5 clustered"] = d.groupby("z10q").apply(lambda g: _ct(g, "x5")).round(3)
    out["z10 bottom decile by year -> x5"] = d[d["z10q"] == 0].groupby("year").apply(lambda g: _ct(g, "x5")).round(3)
    out["z10 bottom decile by coin -> x5"] = d[d["z10q"] == 0].groupby("coin").apply(lambda g: _ct(g, "x5")).round(3)
    return out
