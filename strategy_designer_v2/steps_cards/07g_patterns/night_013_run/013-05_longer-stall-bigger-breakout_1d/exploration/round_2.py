import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    frames = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "ts": pd.to_datetime(b["timestamp"])})
            for H in [5, 10, 20, 30]:
                df["fwd%d" % H] = c.shift(-H)/c - 1
            for L in [14, 30, 60, 90, 180]:
                df["dist%d" % L] = c/c.rolling(L).max() - 1
            df["volu"] = v/v.rolling(20).mean()
            frames.append(df)
    a = pd.concat(frames, ignore_index=True)
    a["year"] = a["ts"].dt.year

    # grid per horizon, excess vs coin mean; quintile top-bottom t and per-bar slope t on rank
    res = []
    for H in [5, 10, 20, 30]:
        g = a[a.pos % H == 0].dropna(subset=["fwd%d" % H]).copy()
        g["ex"] = g["fwd%d" % H] - g.groupby("coin")["fwd%d" % H].transform("mean")
        for L in [14, 30, 60, 90, 180]:
            s = g.dropna(subset=["dist%d" % L]).copy()
            s["rk"] = s.groupby("coin")["dist%d" % L].rank(pct=True)
            sl = stats.linregress(s["rk"], s["ex"])
            top = s[s.rk > 0.8]["ex"]; bot = s[s.rk <= 0.2]["ex"]
            res.append({"H": H, "L": L, "n": len(s), "slope": sl.slope, "slope_t": sl.slope/sl.stderr,
                        "top_mean": top.mean(), "bot_mean": bot.mean(),
                        "tb_t": stats.ttest_ind(top, bot, equal_var=False).statistic})
    out["dist_grid"] = pd.DataFrame(res)

    # robustness for H=10, L=30: by coin and by year
    g = a[a.pos % 10 == 0].dropna(subset=["fwd10", "dist30"]).copy()
    g["ex"] = g["fwd10"] - g.groupby("coin")["fwd10"].transform("mean")
    g["rk"] = g.groupby("coin")["dist30"].rank(pct=True)
    def sl(x):
        r = stats.linregress(x["rk"], x["ex"])
        return pd.Series({"n": len(x), "slope": r.slope, "t": r.slope/r.stderr})
    out["d30_by_coin"] = g.groupby("coin").apply(sl)
    out["d30_by_year"] = g.groupby("year").apply(sl)
    # at the high exactly (dist30==0) vs others
    g["athigh"] = (g["dist30"] >= -1e-12).astype(int)
    out["d30_athigh"] = g.groupby("athigh")["ex"].agg(["mean", "count", "std"])

    # weekday: coin-demeaned daily return, by coin and year for Saturday
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; dd.append(d)
    d = pd.concat(dd, ignore_index=True).dropna(subset=["coin_return"])
    d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek
    d["year"] = pd.to_datetime(d["day"]).dt.year
    d["ex"] = d["coin_return"] - d.groupby("coin")["coin_return"].transform("mean")
    d["sat"] = (d.wd == 5)
    def satt(x):
        s1, s0 = x[x.sat]["ex"], x[~x.sat]["ex"]
        return pd.Series({"sat_mean": s1.mean(), "other_mean": s0.mean(),
                          "t": stats.ttest_ind(s1, s0, equal_var=False).statistic, "n_sat": len(s1)})
    out["sat_by_coin"] = d.groupby("coin").apply(satt)
    out["sat_by_year"] = d.groupby("year").apply(satt)
    # Saturday return vs Friday return sign (dependence)
    return out
