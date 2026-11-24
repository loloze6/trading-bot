import pandas as pd, numpy as np

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "wd": ts.dt.weekday, "year": ts.dt.year, "sd20": sd20, "z1": r1 / sd20,
                               "z14": (c / c.shift(14) - 1) / (sd20 * np.sqrt(14)),
                               "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["u1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    d["vq"] = d.groupby("coin")["sd20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out = {}
    s = d.dropna(subset=["z1", "u1"]).copy()
    hv = s[s.vq == 2].copy()
    hv["side"] = np.where(hv.z1 < 0, "down day", "up day")
    hv["p"] = -hv["z1"].clip(-4, 4) * hv["u1"]
    out["high-vol reversal by side of the day's move"] = hv.groupby("side").apply(
        lambda x: pd.Series({"mean_p": x["p"].mean(), "mean_u1": x["u1"].mean(),
                             "t_day": _t(x.groupby("day")["p"].sum()), "days": x["day"].nunique()}))
    hd = hv[hv.z1 < 0].copy()
    hd["q"] = pd.qcut(hd["z1"], 4, labels=False)
    g = hd.groupby("q").agg(z=("z1", "mean"), u1=("u1", "mean"), n=("u1", "size"))
    g["t_day"] = [_t(hd[hd.q == k].groupby("day")["u1"].sum()) for k in g.index]
    out["high-vol down days: z1 quartile -> next-day unusual"] = g
    out["high-vol reversal by year"] = hv.groupby("year").apply(
        lambda x: pd.Series({"mean_p": x["p"].mean(), "t_day": _t(x.groupby("day")["p"].sum()), "n": len(x)}))
    out["high-vol reversal by coin"] = hv.groupby("coin").apply(
        lambda x: pd.Series({"mean_p": x["p"].mean(), "t_day": _t(x.groupby("day")["p"].sum()), "n": len(x)}))
    fr = d[d.wd == 4].dropna(subset=["z14", "u1"]).copy()
    fr["p"] = fr["z14"].clip(-3, 3) * fr["u1"]
    out["friday z14 x saturday unusual by year"] = fr.groupby("year").apply(
        lambda x: pd.Series({"mean_p": x["p"].mean(), "t_day": _t(x.groupby("day")["p"].sum()), "n": len(x)}))
    fr["q"] = pd.qcut(fr["z14"], 5, labels=False)
    out["friday z14 quintile -> saturday unusual"] = fr.groupby("q").agg(z=("z14", "mean"), u1=("u1", "mean"), n=("u1", "size"))
    return out
