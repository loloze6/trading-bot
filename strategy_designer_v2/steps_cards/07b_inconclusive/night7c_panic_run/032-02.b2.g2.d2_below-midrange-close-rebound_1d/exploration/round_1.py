import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allret = []
        for w, b in wins.items():
            allret.append((b["close"].shift(-1) / b["close"] - 1).dropna())
        cmean = pd.concat(allret).mean()
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            rng = (b["high"] - b["low"]) / c
            rr = rng.rolling(90, min_periods=60).mean() / rng.rolling(30, min_periods=20).mean()
            loc = (b["high"] - c) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 2, 3, 5):
                b[f"r{h}"] = c.shift(-h) / c - 1
            b["coin"] = coin; b["win"] = w; b["cmean"] = cmean
            b["rr"] = rr; b["loc"] = loc; b["day"] = ts.dt.floor("D"); b["year"] = ts.dt.year
            b["ret30"] = c / c.shift(30) - 1
            b["pos"] = np.arange(len(b))
            rows.append(b[["coin","win","year","day","pos","forecast","rr","loc","r1","r2","r3","r5","cmean","ret30"]])
    d = pd.concat(rows, ignore_index=True)
    d["ex1"] = d["r1"] - d["cmean"]
    act = d[(d["forecast"] > 0) & d["ex1"].notna()].copy()

    def wt(g):
        f = g["forecast"]; x = g["ex1"]
        m = (f * x).sum() / f.sum()
        dev = (f * (x - m)).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / f.sum()
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "wmean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    out["overall_BC"] = wt(act).to_frame().T
    out["by_coin"] = act.groupby("coin").apply(wt)
    out["by_window"] = act.groupby("win").apply(wt)
    act["fq"] = pd.qcut(act["forecast"], 4, labels=False, duplicates="drop")
    out["by_forecast_quartile"] = act.groupby("fq").apply(wt)
    act["down30"] = np.where(act["ret30"] < 0, "falling30", "rising30")
    out["by_30d_trend"] = act.groupby("down30").apply(wt)

    # outside regime: lower-half closes when ranges are not wide, and all loc deciles in wide regime
    v = d[d["ex1"].notna() & d["loc"].notna() & d["rr"].notna()].copy()
    v["wide"] = np.where(v["rr"] < 1, "wide", "narrow")
    v["locq"] = pd.cut(v["loc"], [0, .2, .4, .5, .6, .8, 1.0001], include_lowest=True)
    out["ex1_by_wide_loc"] = v.groupby(["wide", "locq"])["ex1"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))]).rename(columns={"<lambda_0>": "t"})
    # slope of ex1 on loc in wide regime, per wide/narrow
    sl = {}
    for k, g in v.groupby("wide"):
        r = stats.linregress(g["loc"], g["ex1"])
        sl[k] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(g)}
    out["slope_ex1_on_loc"] = pd.DataFrame(sl).T
    # horizons: non-overlapping grid within each window
    hz = {}
    for h in (1, 2, 3, 5):
        g = v[(v["pos"] % h == 0) & v[f"r{h}"].notna() & (v["wide"] == "wide") & (v["loc"] >= 0.5)]
        x = g[f"r{h}"] - g["cmean"] * h
        hz[h] = {"n": len(g), "mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)), "corr_loc": np.corrcoef(g["loc"], x)[0, 1]}
    out["horizons_wide_lowerhalf"] = pd.DataFrame(hz).T
    return out
