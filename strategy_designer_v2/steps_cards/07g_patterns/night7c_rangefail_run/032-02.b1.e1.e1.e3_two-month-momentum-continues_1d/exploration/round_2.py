import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    def feats(df):
        c = df["close"].astype(float).reset_index(drop=True)
        h = df["high"].astype(float).reset_index(drop=True); l = df["low"].astype(float).reset_index(drop=True)
        r1 = c.pct_change()
        f = pd.DataFrame({"close": c})
        f["ret1"] = r1
        f["vol20"] = r1.rolling(20).std()
        f["z1"] = r1 / r1.rolling(20).std().shift(1)
        hi = h.rolling(60).max().shift(1); lo = l.rolling(60).min().shift(1)
        rng = hi - lo
        f["brk"] = np.where(c > hi, (c - hi) / rng, np.where(c < lo, (c - lo) / rng, 0.0))
        f["brkv"] = np.where(c > hi, (c - hi) / c / f["vol20"], np.where(c < lo, (c - lo) / c / f["vol20"], 0.0))
        f["side"] = np.sign(f["brk"])
        f["trendiness"] = (c / c.shift(60) - 1).abs() / (r1.rolling(60).std() * np.sqrt(60))
        f["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D").values
        f["year"] = pd.to_datetime(df["timestamp"]).dt.year.values
        return f
    def grid(H):
        rows = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                f = feats(df)
                f["fwd"] = f["close"].shift(-H) / f["close"] - 1
                g = f.iloc[::H].copy(); g["coin"] = coin; g["win"] = w
                rows.append(g)
        d = pd.concat(rows)
        d["fwd_ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        return d
    def tstat(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan})
    def slope(d, x, y="fwd_ex"):
        d = d[[x, y]].dropna()
        if len(d) < 10: return pd.Series({"n": len(d)})
        s = stats.linregress(d[x], d[y])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})
    res = {}
    for H in (3, 5, 10, 20):
        d = grid(H)
        b = d[d["brk"] != 0].dropna(subset=["fwd_ex"])
        b = b.assign(dirmove=b["fwd_ex"] * b["side"])
        res[f"H{H}_breaks_dirmove"] = tstat(b["dirmove"])
        res[f"H{H}_up_breaks"] = tstat(b.loc[b.side > 0, "fwd_ex"])
        res[f"H{H}_down_breaks"] = tstat(b.loc[b.side < 0, "fwd_ex"])
        res[f"H{H}_slope_brkv_all"] = slope(d, "brkv")
        res[f"H{H}_slope_brk_breaksonly"] = slope(b, "brk")
        res[f"H{H}_slope_z1_all"] = slope(d, "z1")
        if H == 10:
            out["H10_breaks_by_window"] = b.groupby("win")["dirmove"].agg(["count", "mean"])
            out["H10_breaks_by_coin"] = b.groupby("coin")["dirmove"].agg(["count", "mean"])
            out["H10_z1_by_year"] = d.dropna(subset=["z1", "fwd_ex"]).groupby("year").apply(lambda g: slope(g, "z1"))
            bb = b.dropna(subset=["trendiness"])
            bb["tq"] = pd.qcut(bb["trendiness"], 2, labels=False)
            out["H10_breaks_by_trendiness_half"] = bb.groupby("tq")["dirmove"].agg(["count", "mean"])
    out["tests"] = pd.DataFrame(res).T
    # one-day reversal and 5-day continuation of z1, by coin, signed by move direction
    d1 = grid(1).dropna(subset=["z1", "fwd_ex"])
    out["H1_z1_by_coin"] = d1.groupby("coin").apply(lambda g: slope(g, "z1"))
    d5 = grid(5).dropna(subset=["z1", "fwd_ex"])
    out["H5_z1_by_coin"] = d5.groupby("coin").apply(lambda g: slope(g, "z1"))
    big = d5[d5["z1"].abs() > 1.5]
    out["H5_bigmove_dirmove"] = tstat(big["fwd_ex"] * np.sign(big["z1"])).to_frame("v")
    # weekday by year, H1
    d1["dow"] = pd.to_datetime(d1["day"]).dt.dayofweek
    d1["thfr"] = d1["dow"].isin([3, 4]).astype(int)
    out["thfr_minus_rest_by_year"] = d1.groupby("year").apply(lambda g: g.loc[g.thfr == 1, "fwd_ex"].mean() - g.loc[g.thfr == 0, "fwd_ex"].mean())
    return out
