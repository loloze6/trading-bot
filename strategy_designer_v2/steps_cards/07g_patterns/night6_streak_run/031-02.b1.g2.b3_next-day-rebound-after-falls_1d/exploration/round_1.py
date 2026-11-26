import pandas as pd, numpy as np
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std() / np.sqrt(len(x)))

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
                               "z3": (c / c.shift(3) - 1) / (vol * np.sqrt(3)),
                               "z10": (c / c.shift(10) - 1) / (vol * np.sqrt(10)),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            s = np.sign(r1.fillna(0)).values; st = np.zeros(len(s))
            for i in range(1, len(s)):
                st[i] = (st[i-1] + s[i]) if (s[i] != 0 and np.sign(st[i-1]) == s[i]) else s[i]
            df["streak"] = st
            for h in (1, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["rng"] = (b["high"] - b["low"]).astype(float) / c / vol
            df["clv"] = ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)).astype(float)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5):
        g = d[d["pos"] % h == 0]
        mu = g.groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(mu)
        d.loc[d["pos"] % h != 0, f"x{h}"] = np.nan
    d["wd"] = d["ts"].dt.dayofweek
    d["year"] = d["ts"].dt.year
    out = {}
    def tab(col, ycols, q=None, bins=None):
        x = d.copy()
        x["grp"] = pd.qcut(x[col], q, duplicates="drop") if q else pd.cut(x[col], bins)
        res = {}
        for y in ycols:
            gg = x.groupby("grp", observed=True)[y]
            res[y + "_mean%"] = gg.mean() * 100
            res[y + "_t"] = gg.apply(_t)
            res[y + "_n"] = gg.count()
        return pd.DataFrame(res).round(3)
    out["z1 deciles -> x1,x3,x5"] = tab("z1", ["x1", "x3", "x5"], q=10)
    out["z3 deciles -> x1,x3,x5"] = tab("z3", ["x1", "x3", "x5"], q=10)
    out["z10 deciles -> x1,x3,x5"] = tab("z10", ["x1", "x3", "x5"], q=10)
    out["streak -> x1,x3"] = tab("streak", ["x1", "x3"], bins=[-20, -5.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 5.5, 20])
    out["range/vol quintile -> x1,x3"] = tab("rng", ["x1", "x3"], q=5)
    out["close location quintile -> x1,x3"] = tab("clv", ["x1", "x3"], q=5)
    # fall effect by vol regime
    d["volq"] = d.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=["lowvol", "midvol", "hivol"]))
    d["zq"] = pd.cut(d["z1"], [-99, -1.5, -0.5, 0.5, 1.5, 99], labels=["<-1.5", "-1.5..-0.5", "mid", "0.5..1.5", ">1.5"])
    out["x1 by volq x zbucket mean%"] = (d.pivot_table(index="volq", columns="zq", values="x1", aggfunc="mean", observed=True) * 100).round(3)
    out["x1 by volq x zbucket t"] = d.pivot_table(index="volq", columns="zq", values="x1", aggfunc=_t, observed=True).round(2)
    out["x1 by weekday (signal day)"] = d.groupby("wd")["x1"].agg(["mean", _t, "count"]).assign(mean=lambda z: z["mean"] * 100).round(3)
    out["x1 by year x zbucket mean%"] = (d.pivot_table(index="year", columns="zq", values="x1", aggfunc="mean", observed=True) * 100).round(3)
    out["x1 by coin x zbucket mean%"] = (d.pivot_table(index="coin", columns="zq", values="x1", aggfunc="mean", observed=True) * 100).round(3)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; bd.append(t)
    bd = pd.concat(bd)
    book = bd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    book.index = book.index.set_names(["win", "day"])
    bk = book.reset_index()
    bk["wd"] = pd.to_datetime(bk["day"]).dt.dayofweek
    out["book by weekday"] = bk.groupby("wd")["book_return"].agg(["mean", _t, "count"]).assign(mean=lambda z: z["mean"] * 100).round(3)
    bk = bk.sort_values(["win", "day"])
    bk["prev_coin"] = bk.groupby("win")["coin_return"].shift(1)
    bk["bq"] = pd.qcut(bk["book_return"], 20, labels=False)
    out["book extremes: prev-day coin ret % by book ventile"] = bk.groupby("bq")[["prev_coin", "coin_return", "book_return"]].mean().mul(100).round(3).iloc[[0, 1, 2, 17, 18, 19]]
    return out
