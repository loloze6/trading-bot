import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    def feats(df):
        c = df["close"].astype(float).reset_index(drop=True)
        h = df["high"].astype(float).reset_index(drop=True); l = df["low"].astype(float).reset_index(drop=True)
        r1 = c.pct_change()
        f = pd.DataFrame({"close": c})
        f["fc"] = df["forecast"].astype(float).values
        f["ret1"] = r1
        f["ret5"] = c / c.shift(5) - 1
        f["ret20"] = c / c.shift(20) - 1
        f["ret60"] = c / c.shift(60) - 1
        f["vol20"] = r1.rolling(20).std()
        f["z1"] = r1 / r1.rolling(20).std().shift(1)
        hi = h.rolling(60).max().shift(1); lo = l.rolling(60).min().shift(1)
        rng = (hi - lo)
        # break distance past range edge in range widths (+ above high, - below low)
        f["brk"] = np.where(c > hi, (c - hi) / rng, np.where(c < lo, (c - lo) / rng, 0.0))
        f["trendiness"] = (f["ret60"].abs()) / (r1.rolling(60).std() * np.sqrt(60))
        f["ret3"] = c / c.shift(3) - 1
        f["dow"] = pd.to_datetime(df["timestamp"]).dt.dayofweek.values
        f["alloc"] = df["postRebalance_current_allocation"].astype(float).values
        return f
    def grid(H, cols):
        rows = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                f = feats(df)
                f["fwd"] = f["close"].shift(-H) / f["close"] - 1
                g = f.iloc[::H].copy(); g["coin"] = coin; g["win"] = w
                rows.append(g[["coin", "win", "fwd"] + cols])
        d = pd.concat(rows)
        d["fwd_ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        return d
    def slope(d, x, y="fwd_ex"):
        d = d[[x, y]].dropna()
        if len(d) < 30: return pd.Series({"n": len(d)})
        s = stats.linregress(d[x], d[y])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})
    res = {}
    for H in (1, 3, 5, 10, 20):
        d = grid(H, ["fc", "ret1", "ret3", "ret5", "ret20", "ret60", "z1", "vol20", "brk", "trendiness"])
        for x in ["fc", "z1", "ret5", "ret20", "ret60", "vol20", "brk"]:
            res[f"H{H}_{x}"] = slope(d, x)
        if H in (5, 10, 20):
            dd = d[d["brk"] != 0].dropna(subset=["brk", "fwd_ex", "trendiness"])
            low = dd[dd["trendiness"] <= dd["trendiness"].median()]
            res[f"H{H}_brk_lowtrend"] = slope(low, "brk")
            res[f"H{H}_brk_hightrend"] = slope(dd[dd["trendiness"] > dd["trendiness"].median()], "brk")
    out["slopes"] = pd.DataFrame(res).T
    # forecast quintiles at H20
    d = grid(20, ["fc", "vol20", "ret5"]).dropna()
    d["q"] = pd.qcut(d["fc"], 5, labels=False)
    out["fc_quint_H20"] = d.groupby("q")["fwd_ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    d5 = grid(5, ["vol20", "z1", "ret5"]).dropna()
    d5["vq"] = pd.qcut(d5["vol20"], 3, labels=False)
    out["vol_tercile_H5"] = d5.groupby("vq")["fwd_ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    d5["zq"] = pd.qcut(d5["z1"], 5, labels=False)
    out["z1_quint_H5"] = d5.groupby("zq")["fwd_ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # weekday
    d1 = grid(1, ["dow"]).dropna()
    out["dow_H1"] = d1.groupby("dow")["fwd_ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # book by window and by position sign
    bk = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            b = bars[coin][w]
            a = b["postRebalance_current_allocation"].astype(float)
            r = b["close"].astype(float).pct_change().shift(-1)
            g = (a * r)
            bk.append(pd.DataFrame({"coin": coin, "win": w, "side": np.sign(a), "g": g}))
    bk = pd.concat(bk).dropna()
    out["gain_by_side"] = bk.groupby("side")["g"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["gain_by_window"] = bk.groupby("win")["g"].agg(["count", "mean"])
    out["gain_by_coin"] = bk.groupby("coin")["g"].agg(["count", "mean"])
    return out
