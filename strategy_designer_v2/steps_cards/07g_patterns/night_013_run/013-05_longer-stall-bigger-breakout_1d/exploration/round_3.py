import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    frames = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "ts": pd.to_datetime(b["timestamp"])})
            df["fwd10"] = c.shift(-10)/c - 1
            df["fwd1"] = c.shift(-1)/c - 1
            hi30 = c.rolling(30).max()
            df["dist30"] = c/hi30 - 1
            newhi = (c >= hi30 - 1e-12).astype(float)
            df["nhigh10"] = newhi.rolling(10).sum()
            df["volu"] = v/v.rolling(20).mean()
            df["r1"] = c.pct_change()
            df["r7"] = c/c.shift(7) - 1
            frames.append(df)
    a = pd.concat(frames, ignore_index=True)
    a["year"] = a["ts"].dt.year
    a["wd"] = a["ts"].dt.dayofweek

    g = a[a.pos % 10 == 0].dropna(subset=["fwd10", "dist30", "nhigh10"]).copy()
    g["ex"] = g["fwd10"] - g.groupby("coin")["fwd10"].transform("mean")
    t = g.groupby("nhigh10")["ex"].agg(["mean", "count"])
    out["ex10_by_newhighs_last10"] = t
    r = stats.linregress(g["nhigh10"], g["ex"])
    out["nhigh_slope_t"] = pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(g)})
    ah = g[g.dist30 >= -1e-12]; nah = g[g.dist30 < -1e-12]
    def ab(x):
        h = x[x.dist30 >= -1e-12]["ex"]; o = x[x.dist30 < -1e-12]["ex"]
        return pd.Series({"high_mean": h.mean(), "n_high": len(h), "other_mean": o.mean(),
                          "t": stats.ttest_ind(h, o, equal_var=False).statistic if len(h) > 2 else np.nan})
    out["athigh_by_coin"] = g.groupby("coin").apply(ab)
    out["athigh_by_year"] = g.groupby("year").apply(ab)
    # at high, graded by volume ratio
    h = ah.dropna(subset=["volu"])
    rr = stats.linregress(h["volu"].rank(pct=True), h["ex"])
    out["athigh_volu_slope"] = pd.Series({"slope": rr.slope, "t": rr.slope/rr.stderr, "n": len(h)})

    # Saturday: next-day return from Friday close, graded by past 7-day return
    f = a[(a.wd == 4)].dropna(subset=["fwd1", "r7"]).copy()
    f["ex"] = f["fwd1"] - f.groupby("coin")["fwd1"].transform("mean")
    f["q"] = f.groupby("coin")["r7"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["sat_ret_by_fri_r7_q"] = f.groupby("q")["fwd1"].agg(["mean", "count", "std"])
    r2 = stats.linregress(f.groupby("coin")["r7"].rank(pct=True), f["fwd1"])
    out["sat_r7_slope"] = pd.Series({"slope": r2.slope, "t": r2.slope/r2.stderr, "n": len(f)})
    f["vq"] = f.groupby("coin")["volu"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["sat_ret_by_fri_volu_q"] = f.groupby("vq")["fwd1"].agg(["mean", "count"])
    s = a[a.wd == 5].dropna(subset=["r1"])
    o = a[a.wd != 5].dropna(subset=["r1"])
    out["sat_vs_other_bar"] = pd.Series({"sat": s.r1.mean(), "other": o.r1.mean(),
        "t": stats.ttest_ind(s.r1, o.r1, equal_var=False).statistic, "n_sat": len(s),
        "sat_pos_share": (s.r1 > 0).mean(), "other_pos_share": (o.r1 > 0).mean()})
    return out
